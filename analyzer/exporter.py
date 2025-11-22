"""分析结果导出器"""
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from loguru import logger


class AnalysisExporter:
    """分析结果导出器，支持多种格式"""

    def __init__(self, database):
        """
        初始化导出器

        Args:
            database: 数据库实例
        """
        self.db = database

    def export_to_markdown(self, uid: str, output_path: str = None) -> str:
        """
        导出为Markdown格式

        Args:
            uid: UP主UID
            output_path: 输出文件路径，None则返回字符串

        Returns:
            Markdown格式的内容
        """
        # 获取UP主信息
        user_info = self.db.get_user(uid)
        if not user_info:
            raise ValueError(f"未找到UID {uid} 的信息")

        # 获取视频统计
        videos = self.db.get_user_videos(uid)

        # 获取分析结果
        analyses = self.db.get_user_analysis(uid)

        # 生成Markdown内容
        md_content = []

        # 标题和UP主信息
        md_content.append(f"# {user_info['name']} - 内容分析报告\n")
        md_content.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md_content.append(f"**UP主UID**: {uid}\n")
        md_content.append(f"**签名**: {user_info.get('sign', 'N/A')}\n")
        md_content.append(f"**粉丝数**: {user_info.get('follower', 0):,}\n")
        md_content.append(f"**已爬取视频数**: {len(videos)}\n")
        md_content.append("\n---\n\n")

        # 添加分析结果
        if analyses:
            md_content.append("## 分析结果\n\n")
            for analysis in analyses:
                analysis_type = analysis['analysis_type']
                analysis_result = analysis['analysis_result']
                created_at = analysis['created_at']

                md_content.append(f"### {analysis_type}\n\n")
                md_content.append(f"*分析时间: {created_at}*\n\n")
                md_content.append(f"{analysis_result}\n\n")
                md_content.append("---\n\n")
        else:
            md_content.append("## 暂无分析结果\n\n")
            md_content.append("请先运行分析命令生成分析报告。\n\n")

        # 视频列表
        if videos:
            md_content.append("## 视频列表\n\n")
            md_content.append("| # | 标题 | 发布时间 | 播放量 | 时长 |\n")
            md_content.append("|---|------|---------|--------|------|\n")

            for i, video in enumerate(videos[:50], 1):  # 只显示前50个
                title = video.get('title', 'N/A')
                pubdate = datetime.fromtimestamp(video.get('pubdate', 0)).strftime('%Y-%m-%d')
                play = video.get('play', 0)
                duration = self._format_duration(video.get('duration', 0))
                md_content.append(f"| {i} | {title} | {pubdate} | {play:,} | {duration} |\n")

            if len(videos) > 50:
                md_content.append(f"\n*...还有 {len(videos)-50} 个视频未显示*\n\n")

        full_md = "".join(md_content)

        # 保存到文件或返回内容
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(full_md, encoding='utf-8')
            logger.info(f"Markdown报告已导出到: {output_path}")
            return output_path
        else:
            return full_md

    def export_to_json(self, uid: str, output_path: str = None) -> str:
        """
        导出为JSON格式

        Args:
            uid: UP主UID
            output_path: 输出文件路径，None则返回JSON字符串

        Returns:
            JSON格式的内容
        """
        # 获取数据
        user_info = self.db.get_user(uid)
        if not user_info:
            raise ValueError(f"未找到UID {uid} 的信息")

        videos = self.db.get_user_videos(uid)
        analyses = self.db.get_user_analysis(uid)

        # 构建JSON结构
        data = {
            "export_time": datetime.now().isoformat(),
            "uploader": {
                "uid": uid,
                "name": user_info.get('name'),
                "sign": user_info.get('sign'),
                "follower": user_info.get('follower'),
                "face": user_info.get('face'),
            },
            "statistics": {
                "total_videos": len(videos),
                "total_analyses": len(analyses),
            },
            "analyses": [
                {
                    "type": a['analysis_type'],
                    "result": a['analysis_result'],
                    "created_at": a['created_at'],
                    "video_bvid": a.get('video_bvid'),
                }
                for a in analyses
            ],
            "videos": [
                {
                    "bvid": v.get('bvid'),
                    "title": v.get('title'),
                    "description": v.get('description'),
                    "pubdate": v.get('pubdate'),
                    "play": v.get('play'),
                    "like": v.get('like'),
                    "coin": v.get('coin'),
                    "favorite": v.get('favorite'),
                    "duration": v.get('duration'),
                }
                for v in videos
            ]
        }

        json_str = json.dumps(data, ensure_ascii=False, indent=2)

        # 保存到文件或返回内容
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(json_str, encoding='utf-8')
            logger.info(f"JSON报告已导出到: {output_path}")
            return output_path
        else:
            return json_str

    def _format_duration(self, seconds: int) -> str:
        """格式化时长"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds//60}m{seconds%60}s"
        else:
            h = seconds // 3600
            m = (seconds % 3600) // 60
            return f"{h}h{m}m"
