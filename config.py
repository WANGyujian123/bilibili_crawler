"""配置文件"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目根目录
BASE_DIR = Path(__file__).parent

# Claude API配置
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
CLAUDE_API_BASE_URL = os.getenv("CLAUDE_API_BASE_URL", "")  # 代理站API地址（可选）
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"  # 使用最新的Claude模型

# B站API配置
BILIBILI_API_BASE = "https://api.bilibili.com"
BILIBILI_COOKIE = os.getenv("BILIBILI_COOKIE", "")  # B站Cookie（可选）
BILIBILI_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Origin": "https://www.bilibili.com"
}

# 如果有Cookie，添加到headers中
if BILIBILI_COOKIE:
    BILIBILI_HEADERS["Cookie"] = BILIBILI_COOKIE

# 数据库配置
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "data" / "bilibili.db"))

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# 数据存储目录
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# 邮件通知配置
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
EMAIL_SMTP_HOST = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "")
