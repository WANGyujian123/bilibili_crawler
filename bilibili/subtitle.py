"""B站字幕下载和解析"""
import requests
import json
from typing import Dict, List, Optional
from loguru import logger
import config


class SubtitleDownloader:
    """字幕下载器"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(config.BILIBILI_HEADERS)
        self.api_base = config.BILIBILI_API_BASE

    def get_subtitle_info(self, bvid: str, cid: int) -> Optional[Dict]:
        """
        获取视频字幕信息

        Args:
            bvid: 视频BV号
            cid: 视频CID

        Returns:
            字幕信息，失败返回None
        """
        url = f"{self.api_base}/x/player/v2"
        params = {
            "bvid": bvid,
            "cid": cid
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 0:
                subtitle_data = data.get("data", {}).get("subtitle")
                if subtitle_data:
                    logger.info(f"成功获取视频 {bvid} 的字幕信息")
                    return subtitle_data
                else:
                    logger.warning(f"视频 {bvid} 没有字幕")
                    return None
            else:
                logger.error(f"获取字幕信息失败: {data.get('message')}")
                return None

        except Exception as e:
            logger.error(f"请求字幕信息时出错: {e}")
            return None

    def download_subtitle(self, subtitle_url: str) -> Optional[List[Dict]]:
        """
        下载字幕内容

        Args:
            subtitle_url: 字幕URL

        Returns:
            字幕内容列表，每项包含时间和文本
        """
        # B站字幕URL可能需要补全协议
        if subtitle_url.startswith("//"):
            subtitle_url = "https:" + subtitle_url

        try:
            response = self.session.get(subtitle_url, timeout=10)
            response.raise_for_status()
            subtitle_data = response.json()

            if "body" in subtitle_data:
                logger.info(f"成功下载字幕，共 {len(subtitle_data['body'])} 条")
                return subtitle_data["body"]
            else:
                logger.error("字幕数据格式错误")
                return None

        except Exception as e:
            logger.error(f"下载字幕时出错: {e}")
            return None

    def get_video_subtitle(self, bvid: str, cid: int, lang: str = "zh-CN") -> Optional[str]:
        """
        获取视频的完整字幕文本

        Args:
            bvid: 视频BV号
            cid: 视频CID
            lang: 字幕语言，默认中文

        Returns:
            完整字幕文本，失败返回None
        """
        # 获取字幕信息
        subtitle_info = self.get_subtitle_info(bvid, cid)
        if not subtitle_info:
            return None

        # 查找指定语言的字幕
        subtitles = subtitle_info.get("subtitles", [])
        if not subtitles:
            logger.warning(f"视频 {bvid} 没有可用的字幕")
            return None

        # 优先使用指定语言，否则使用第一个可用字幕
        subtitle_url = None
        for sub in subtitles:
            if sub.get("lan") == lang:
                subtitle_url = sub.get("subtitle_url")
                break

        if not subtitle_url and subtitles:
            subtitle_url = subtitles[0].get("subtitle_url")
            logger.info(f"未找到 {lang} 字幕，使用 {subtitles[0].get('lan')} 字幕")

        if not subtitle_url:
            logger.error("无法获取字幕URL")
            return None

        # 下载字幕
        subtitle_body = self.download_subtitle(subtitle_url)
        if not subtitle_body:
            return None

        # 合并字幕文本
        full_text = " ".join([item.get("content", "") for item in subtitle_body])
        logger.info(f"字幕总长度: {len(full_text)} 字符")

        return full_text

    def get_subtitle_with_timeline(self, bvid: str, cid: int, lang: str = "zh-CN") -> Optional[List[Dict]]:
        """
        获取带时间轴的字幕

        Args:
            bvid: 视频BV号
            cid: 视频CID
            lang: 字幕语言，默认中文

        Returns:
            带时间轴的字幕列表，每项包含 {from, to, content}
        """
        # 获取字幕信息
        subtitle_info = self.get_subtitle_info(bvid, cid)
        if not subtitle_info:
            return None

        # 查找指定语言的字幕
        subtitles = subtitle_info.get("subtitles", [])
        if not subtitles:
            return None

        # 优先使用指定语言
        subtitle_url = None
        for sub in subtitles:
            if sub.get("lan") == lang:
                subtitle_url = sub.get("subtitle_url")
                break

        if not subtitle_url and subtitles:
            subtitle_url = subtitles[0].get("subtitle_url")

        if not subtitle_url:
            return None

        # 下载字幕
        subtitle_body = self.download_subtitle(subtitle_url)
        return subtitle_body
