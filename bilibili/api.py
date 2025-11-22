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

    def get_user_series_list(self, uid: str) -> Optional[Dict]:
        """
        获取UP主的合集和视频列表

        Args:
            uid: UP主的UID

        Returns:
            包含seasons_list和series_list的字典
        """
        url = f"{self.api_base}/x/polymer/web-space/seasons_series_list"
        params = {
            "mid": uid,
            "page_num": 1,
            "page_size": 20
        }

        try:
            time.sleep(0.5)
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 0:
                logger.info(f"成功获取UP主 {uid} 的合集列表")
                return data.get("data", {}).get("items_lists", {})
            else:
                logger.error(f"获取合集列表失败: {data.get('message')}")
                return None

        except Exception as e:
            logger.error(f"请求合集列表时出错: {e}")
            return None

    def get_season_videos(self, season_id: int) -> List[Dict]:
        """
        获取合集中的所有视频

        Args:
            season_id: 合集ID

        Returns:
            视频列表
        """
        url = f"{self.api_base}/x/polymer/web-space/seasons_archives_list"
        all_videos = []
        page = 1

        while True:
            params = {
                "season_id": season_id,
                "page_num": page,
                "page_size": 30
            }

            try:
                time.sleep(0.5)
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                if data.get("code") == 0:
                    archives = data.get("data", {}).get("archives", [])
                    if not archives:
                        break

                    all_videos.extend(archives)
                    logger.info(f"获取合集 {season_id} 第 {page} 页，共 {len(archives)} 个视频")

                    # 检查是否还有更多
                    meta = data.get("data", {}).get("meta", {})
                    total = meta.get("total", 0)
                    if len(all_videos) >= total:
                        break

                    page += 1
                else:
                    logger.error(f"获取合集视频失败: {data.get('message')}")
                    break

            except Exception as e:
                logger.error(f"请求合集视频时出错: {e}")
                break

        logger.info(f"合集 {season_id} 共获取 {len(all_videos)} 个视频")
        return all_videos

    def get_series_videos(self, series_id: int, uid: str) -> List[Dict]:
        """
        获取视频列表中的所有视频

        Args:
            series_id: 视频列表ID
            uid: UP主UID

        Returns:
            视频列表
        """
        url = f"{self.api_base}/x/series/archives"
        all_videos = []
        page = 1

        while True:
            params = {
                "mid": uid,
                "series_id": series_id,
                "pn": page,
                "ps": 30
            }

            try:
                time.sleep(0.5)
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                if data.get("code") == 0:
                    archives = data.get("data", {}).get("archives", [])
                    if not archives:
                        break

                    all_videos.extend(archives)
                    logger.info(f"获取视频列表 {series_id} 第 {page} 页，共 {len(archives)} 个视频")

                    # 检查是否还有更多
                    meta = data.get("data", {}).get("meta", {})
                    total = meta.get("total", 0)
                    if len(all_videos) >= total:
                        break

                    page += 1
                else:
                    logger.error(f"获取视频列表失败: {data.get('message')}")
                    break

            except Exception as e:
                logger.error(f"请求视频列表时出错: {e}")
                break

        logger.info(f"视频列表 {series_id} 共获取 {len(all_videos)} 个视频")
        return all_videos
