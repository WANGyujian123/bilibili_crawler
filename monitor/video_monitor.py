"""视频监控模块"""
import time
from typing import List, Dict, Optional
from loguru import logger
from bilibili import BilibiliAPI, SubtitleDownloader
from analyzer import ClaudeAnalyzer
from database import Database


class VideoMonitor:
    """视频监控器"""

    def __init__(self, uid: str, season_id: Optional[int] = None, series_id: Optional[int] = None):
        """
        初始化监控器

        Args:
            uid: UP主UID
            season_id: 合集ID（可选）
            series_id: 视频列表ID（可选）
        """
        self.uid = uid
        self.season_id = season_id
        self.series_id = series_id
        self.api = BilibiliAPI()
        self.db = Database()

    def check_new_videos(self) -> List[Dict]:
        """
        检查是否有新视频

        Returns:
            List[Dict]: 新视频列表
        """
        logger.info(f"开始检查UP主 {self.uid} 的新视频...")

        # 获取数据库中已有的视频BV号
        existing_videos = self.db.get_user_videos(self.uid)
        existing_bvids = set(v['bvid'] for v in existing_videos)

        # 获取最新视频列表
        if self.season_id:
            logger.info(f"检查合集 {self.season_id}")
            latest_videos = self.api.get_season_videos(self.uid, self.season_id)
        elif self.series_id:
            logger.info(f"检查视频列表 {self.series_id}")
            latest_videos = self.api.get_series_videos(self.series_id)
        else:
            logger.info("检查所有视频")
            latest_videos = self.api.get_user_videos(self.uid, max_count=50)

        # 筛选出新视频
        new_videos = [v for v in latest_videos if v.get('bvid') not in existing_bvids]

        if new_videos:
            logger.info(f"发现 {len(new_videos)} 个新视频")
        else:
            logger.info("没有发现新视频")

        return new_videos

    def download_and_analyze_video(self, video: Dict) -> Optional[str]:
        """
        下载字幕并分析视频（精简版）

        Args:
            video: 视频信息

        Returns:
            Optional[str]: 分析摘要
        """
        bvid = video.get('bvid')
        title = video.get('title', '未知标题')

        logger.info(f"处理新视频: {title} ({bvid})")

        # 1. 保存视频信息到数据库
        self.db.save_video(video)

        # 2. 下载字幕
        try:
            downloader = SubtitleDownloader()
            subtitle_text = downloader.get_subtitle(bvid)

            if subtitle_text:
                self.db.save_subtitle(bvid, subtitle_text)
                logger.info(f"字幕下载成功: {bvid}")
            else:
                logger.warning(f"未找到字幕: {bvid}")
                return "该视频暂无字幕，无法进行分析。"

        except Exception as e:
            logger.error(f"字幕下载失败: {e}")
            return f"字幕下载失败: {str(e)}"

        # 3. 执行精简版分析
        try:
            analyzer = ClaudeAnalyzer()
            summary = self._quick_analyze(analyzer, subtitle_text, title)

            # 保存分析结果到数据库
            if summary:
                self.db.save_analysis(self.uid, "快速分析", summary, bvid)
                logger.info(f"视频分析完成: {bvid}")

            return summary

        except Exception as e:
            logger.error(f"视频分析失败: {e}")
            return f"分析失败: {str(e)}"

    def _quick_analyze(self, analyzer: ClaudeAnalyzer, subtitle: str, title: str) -> str:
        """
        快速分析（精简版）

        Args:
            analyzer: Claude分析器
            subtitle: 字幕文本
            title: 视频标题

        Returns:
            str: 分析摘要
        """
        prompt = f"""请用200字以内简要分析这个视频的核心内容：

视频标题：{title}

字幕内容：
{subtitle[:2000]}  # 只取前2000字符，加快分析速度

请用简洁的语言回答以下问题：
1. 这个视频主要讲什么？（1-2句话）
2. 核心观点是什么？（1-2句话）
3. 是否值得深入关注？（简要说明）

要求：总字数不超过200字，使用简洁的语言。"""

        try:
            response = analyzer.client.messages.create(
                model=analyzer.model,
                max_tokens=500,  # 限制输出长度
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            summary = response.content[0].text
            logger.info(f"快速分析完成，返回 {len(summary)} 字符")
            return summary

        except Exception as e:
            logger.error(f"Claude API调用失败: {e}")
            return "分析失败"

    def process_new_videos(self, new_videos: List[Dict]) -> Dict[str, str]:
        """
        处理所有新视频

        Args:
            new_videos: 新视频列表

        Returns:
            Dict[str, str]: {bvid: analysis_summary}
        """
        analyses = {}

        for video in new_videos:
            bvid = video.get('bvid')
            summary = self.download_and_analyze_video(video)
            analyses[bvid] = summary

            # 避免API调用过快
            time.sleep(2)

        return analyses

    def close(self):
        """关闭数据库连接"""
        self.db.close()
