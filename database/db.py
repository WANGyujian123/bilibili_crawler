"""SQLite数据库操作"""
import sqlite3
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
from loguru import logger
import config


class Database:
    """数据库操作类"""

    def __init__(self, db_path: str = None):
        """
        初始化数据库连接

        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path or config.DATABASE_PATH
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()

    def _connect(self):
        """连接数据库"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # 使结果可以按列名访问
            self.cursor = self.conn.cursor()
            logger.info(f"成功连接到数据库: {self.db_path}")
        except Exception as e:
            logger.error(f"连接数据库失败: {e}")
            raise

    def _create_tables(self):
        """创建数据表"""
        # UP主信息表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                face TEXT,
                sign TEXT,
                level INTEGER,
                follower INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 视频信息表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                bvid TEXT PRIMARY KEY,
                uid TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                cid INTEGER,
                duration INTEGER,
                pubdate INTEGER,
                view_count INTEGER,
                like_count INTEGER,
                coin_count INTEGER,
                share_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (uid) REFERENCES users(uid)
            )
        """)

        # 字幕表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS subtitles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bvid TEXT NOT NULL,
                subtitle_text TEXT NOT NULL,
                subtitle_lang TEXT DEFAULT 'zh-CN',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bvid) REFERENCES videos(bvid)
            )
        """)

        # 分析结果表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT NOT NULL,
                bvid TEXT,
                analysis_type TEXT NOT NULL,
                analysis_result TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (uid) REFERENCES users(uid),
                FOREIGN KEY (bvid) REFERENCES videos(bvid)
            )
        """)

        self.conn.commit()
        logger.info("数据表创建完成")

    def save_user(self, user_data: Dict) -> bool:
        """
        保存或更新UP主信息

        Args:
            user_data: UP主信息字典

        Returns:
            是否成功
        """
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO users (uid, name, face, sign, level, follower, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(user_data.get("mid")),
                user_data.get("name"),
                user_data.get("face"),
                user_data.get("sign"),
                user_data.get("level"),
                user_data.get("follower", 0),
                datetime.now()
            ))
            self.conn.commit()
            logger.info(f"成功保存UP主信息: {user_data.get('name')}")
            return True
        except Exception as e:
            logger.error(f"保存UP主信息失败: {e}")
            return False

    def save_video(self, uid: str, video_data: Dict) -> bool:
        """
        保存或更新视频信息

        Args:
            uid: UP主UID
            video_data: 视频信息字典

        Returns:
            是否成功
        """
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO videos
                (bvid, uid, title, description, cid, duration, pubdate,
                 view_count, like_count, coin_count, share_count, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                video_data.get("bvid"),
                uid,
                video_data.get("title"),
                video_data.get("description"),
                video_data.get("cid"),
                video_data.get("length", 0),
                video_data.get("created", 0),
                video_data.get("play", 0),
                video_data.get("like", 0),
                video_data.get("coin", 0),
                video_data.get("share", 0),
                datetime.now()
            ))
            self.conn.commit()
            logger.info(f"成功保存视频: {video_data.get('title')}")
            return True
        except Exception as e:
            logger.error(f"保存视频信息失败: {e}")
            return False

    def save_subtitle(self, bvid: str, subtitle_text: str, lang: str = "zh-CN") -> bool:
        """
        保存字幕

        Args:
            bvid: 视频BV号
            subtitle_text: 字幕文本
            lang: 字幕语言

        Returns:
            是否成功
        """
        try:
            # 检查是否已存在
            self.cursor.execute("""
                SELECT id FROM subtitles WHERE bvid = ? AND subtitle_lang = ?
            """, (bvid, lang))

            if self.cursor.fetchone():
                # 更新现有字幕
                self.cursor.execute("""
                    UPDATE subtitles SET subtitle_text = ? WHERE bvid = ? AND subtitle_lang = ?
                """, (subtitle_text, bvid, lang))
            else:
                # 插入新字幕
                self.cursor.execute("""
                    INSERT INTO subtitles (bvid, subtitle_text, subtitle_lang)
                    VALUES (?, ?, ?)
                """, (bvid, subtitle_text, lang))

            self.conn.commit()
            logger.info(f"成功保存字幕: {bvid}")
            return True
        except Exception as e:
            logger.error(f"保存字幕失败: {e}")
            return False

    def save_analysis(self, uid: str, analysis_type: str, result: str, bvid: str = None) -> bool:
        """
        保存分析结果

        Args:
            uid: UP主UID
            analysis_type: 分析类型（如：思想分析、主题总结等）
            result: 分析结果
            bvid: 视频BV号（可选）

        Returns:
            是否成功
        """
        try:
            self.cursor.execute("""
                INSERT INTO analysis (uid, bvid, analysis_type, analysis_result)
                VALUES (?, ?, ?, ?)
            """, (uid, bvid, analysis_type, result))
            self.conn.commit()
            logger.info(f"成功保存分析结果: {analysis_type}")
            return True
        except Exception as e:
            logger.error(f"保存分析结果失败: {e}")
            return False

    def get_user(self, uid: str) -> Optional[Dict]:
        """获取UP主信息"""
        self.cursor.execute("SELECT * FROM users WHERE uid = ?", (uid,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_user_videos(self, uid: str) -> List[Dict]:
        """获取UP主的所有视频"""
        self.cursor.execute("""
            SELECT * FROM videos WHERE uid = ? ORDER BY pubdate DESC
        """, (uid,))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_video_subtitle(self, bvid: str) -> Optional[str]:
        """获取视频字幕"""
        self.cursor.execute("""
            SELECT subtitle_text FROM subtitles WHERE bvid = ? LIMIT 1
        """, (bvid,))
        row = self.cursor.fetchone()
        return row["subtitle_text"] if row else None

    def get_user_analysis(self, uid: str, analysis_type: str = None) -> List[Dict]:
        """获取UP主的分析结果"""
        if analysis_type:
            self.cursor.execute("""
                SELECT * FROM analysis WHERE uid = ? AND analysis_type = ?
                ORDER BY created_at DESC
            """, (uid, analysis_type))
        else:
            self.cursor.execute("""
                SELECT * FROM analysis WHERE uid = ? ORDER BY created_at DESC
            """, (uid,))
        return [dict(row) for row in self.cursor.fetchall()]

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            logger.info("数据库连接已关闭")

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时关闭连接"""
        self.close()
