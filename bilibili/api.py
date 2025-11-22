"""B站API封装"""
import requests
import time
from typing import Dict, List, Optional
from loguru import logger
import config


class BilibiliAPI:
    """B站API封装类"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(config.BILIBILI_HEADERS)
        self.api_base = config.BILIBILI_API_BASE

    def get_user_info(self, uid: str) -> Optional[Dict]:
        """
        获取UP主基本信息

        Args:
            uid: UP主的UID

        Returns:
            UP主信息字典，失败返回None
        """
        url = f"{self.api_base}/x/space/acc/info"
        params = {"mid": uid}

        try:
            time.sleep(0.5)  # 添加延迟避免频率限制
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 0:
                logger.info(f"成功获取UP主 {uid} 的信息")
                return data.get("data")
            else:
                logger.error(f"获取UP主信息失败: {data.get('message')}")
                return None

        except Exception as e:
            logger.error(f"请求UP主信息时出错: {e}")
            return None

    def get_user_videos(self, uid: str, page: int = 1, page_size: int = 30) -> Optional[Dict]:
        """
        获取UP主的视频列表

        Args:
            uid: UP主的UID
            page: 页码，从1开始
            page_size: 每页视频数量

        Returns:
            视频列表数据，失败返回None
        """
        url = f"{self.api_base}/x/space/wbi/arc/search"
        params = {
            "mid": uid,
            "pn": page,
            "ps": page_size,
            "order": "pubdate",  # 按发布时间排序
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 0:
                logger.info(f"成功获取UP主 {uid} 第 {page} 页视频列表")
                return data.get("data")
            else:
                logger.error(f"获取视频列表失败: {data.get('message')}")
                return None

        except Exception as e:
            logger.error(f"请求视频列表时出错: {e}")
            return None

    def get_all_user_videos(self, uid: str, max_videos: Optional[int] = None) -> List[Dict]:
        """
        获取UP主的所有视频

        Args:
            uid: UP主的UID
            max_videos: 最多获取的视频数量，None表示获取全部

        Returns:
            视频列表
        """
        all_videos = []
        page = 1
        page_size = 30

        while True:
            data = self.get_user_videos(uid, page, page_size)

            if not data or "list" not in data:
                break

            vlist = data["list"].get("vlist", [])
            if not vlist:
                break

            all_videos.extend(vlist)
            logger.info(f"已获取 {len(all_videos)} 个视频")

            # 检查是否达到最大数量
            if max_videos and len(all_videos) >= max_videos:
                all_videos = all_videos[:max_videos]
                break

            # 检查是否还有更多视频
            page_info = data.get("page", {})
            total_count = page_info.get("count", 0)
            if len(all_videos) >= total_count:
                break

            page += 1
            time.sleep(1)  # 避免请求过快

        logger.info(f"共获取 {len(all_videos)} 个视频")
        return all_videos

    def get_video_info(self, bvid: str) -> Optional[Dict]:
        """
        获取视频详细信息

        Args:
            bvid: 视频的BV号

        Returns:
            视频详细信息，失败返回None
        """
        url = f"{self.api_base}/x/web-interface/view"
        params = {"bvid": bvid}

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 0:
                logger.info(f"成功获取视频 {bvid} 的信息")
                return data.get("data")
            else:
                logger.error(f"获取视频信息失败: {data.get('message')}")
                return None

        except Exception as e:
            logger.error(f"请求视频信息时出错: {e}")
            return None

    def get_video_cid(self, bvid: str) -> Optional[int]:
        """
        获取视频的CID（用于获取字幕）

        Args:
            bvid: 视频的BV号

        Returns:
            视频CID，失败返回None
        """
        video_info = self.get_video_info(bvid)
        if video_info and "cid" in video_info:
            return video_info["cid"]
        return None
