#!/usr/bin/env python3
"""B站扫码登录工具"""
import requests
import qrcode
import time
import os
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv, set_key

class BilibiliLogin:
    """B站登录工具"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com"
        })
        self.qrcode_url = None
        self.qrcode_key = None

    def get_qrcode(self):
        """获取登录二维码"""
        url = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate"

        try:
            response = self.session.get(url)
            data = response.json()

            if data.get("code") == 0:
                qrcode_data = data.get("data", {})
                self.qrcode_url = qrcode_data.get("url")
                self.qrcode_key = qrcode_data.get("qrcode_key")
                logger.info("成功获取登录二维码")
                return True
            else:
                logger.error(f"获取二维码失败: {data.get('message')}")
                return False

        except Exception as e:
            logger.error(f"获取二维码时出错: {e}")
            return False

    def show_qrcode(self):
        """在终端显示二维码"""
        if not self.qrcode_url:
            logger.error("二维码URL不存在")
            return

        # 生成二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=1,
        )
        qr.add_data(self.qrcode_url)
        qr.make(fit=True)

        # 在终端打印二维码
        print("\n" + "="*60)
        print("请使用B站APP扫描下方二维码登录")
        print("="*60 + "\n")
        qr.print_ascii(invert=True)
        print("\n" + "="*60)
        print("提示：打开B站APP → 首页右上角扫一扫")
        print("="*60 + "\n")

    def check_login_status(self):
        """检查登录状态"""
        if not self.qrcode_key:
            return None

        url = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"
        params = {"qrcode_key": self.qrcode_key}

        try:
            response = self.session.get(url, params=params)
            data = response.json()

            if data.get("code") == 0:
                poll_data = data.get("data", {})
                code = poll_data.get("code")
                message = poll_data.get("message")

                # 86101: 未扫码
                # 86090: 已扫码未确认
                # 86038: 二维码已失效
                # 0: 登录成功

                if code == 0:
                    # 登录成功，获取Cookie
                    logger.success("登录成功！")
                    return self._extract_cookies()
                elif code == 86101:
                    return "waiting"  # 等待扫码
                elif code == 86090:
                    logger.info("已扫码，等待确认...")
                    return "scanned"  # 已扫码，等待确认
                elif code == 86038:
                    logger.error("二维码已失效")
                    return "expired"
                else:
                    logger.warning(f"未知状态: {code} - {message}")
                    return None
            else:
                logger.error(f"检查登录状态失败: {data.get('message')}")
                return None

        except Exception as e:
            logger.error(f"检查登录状态时出错: {e}")
            return None

    def _extract_cookies(self):
        """提取Cookie"""
        cookies = self.session.cookies.get_dict()

        # 构建Cookie字符串
        cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])

        if cookie_str:
            logger.info(f"成功获取Cookie，长度: {len(cookie_str)} 字符")
            return cookie_str
        else:
            logger.error("未能获取到Cookie")
            return None

    def save_cookie_to_env(self, cookie_str):
        """保存Cookie到.env文件"""
        env_file = Path(__file__).parent / ".env"

        # 如果.env不存在，从.env.example复制
        if not env_file.exists():
            env_example = Path(__file__).parent / ".env.example"
            if env_example.exists():
                import shutil
                shutil.copy(env_example, env_file)
                logger.info("已从 .env.example 创建 .env 文件")

        try:
            # 使用set_key更新或添加BILIBILI_COOKIE
            set_key(str(env_file), "BILIBILI_COOKIE", cookie_str)
            logger.success(f"Cookie已保存到 {env_file}")
            return True
        except Exception as e:
            logger.error(f"保存Cookie失败: {e}")
            return False

    def login(self):
        """执行登录流程"""
        logger.info("开始B站扫码登录流程...")

        # 1. 获取二维码
        if not self.get_qrcode():
            return False

        # 2. 显示二维码
        self.show_qrcode()

        # 3. 轮询检查登录状态
        logger.info("等待扫码...")
        max_wait_time = 180  # 最多等待3分钟
        start_time = time.time()

        while True:
            if time.time() - start_time > max_wait_time:
                logger.error("登录超时，请重试")
                return False

            status = self.check_login_status()

            if status == "waiting":
                # 等待扫码
                time.sleep(2)
            elif status == "scanned":
                # 已扫码，等待确认
                time.sleep(1)
            elif status == "expired":
                # 二维码过期
                return False
            elif status and status.startswith("SESSDATA"):
                # 登录成功，获得Cookie
                logger.success("\n" + "="*60)
                logger.success("✅ 登录成功！")
                logger.success("="*60 + "\n")

                # 保存Cookie
                if self.save_cookie_to_env(status):
                    logger.info("现在可以使用爬虫功能了！")
                    return True
                else:
                    logger.warning("Cookie保存失败，请手动添加到.env文件")
                    logger.info(f"Cookie: {status[:50]}...")
                    return False
            else:
                # 其他错误
                time.sleep(2)

def main():
    """主函数"""
    print("\n" + "="*60)
    print("  B站扫码登录工具")
    print("="*60 + "\n")

    login_tool = BilibiliLogin()
    success = login_tool.login()

    if success:
        print("\n" + "="*60)
        print("✅ 配置完成！现在可以使用爬虫了")
        print("="*60)
        print("\n示例命令：")
        print("  python3 main.py crawl 9458053 --max-videos 5 --with-subtitle")
        print("  python3 main.py analyze 9458053")
        print()
    else:
        print("\n" + "="*60)
        print("❌ 登录失败")
        print("="*60)
        print("\n请重试或查看 GET_COOKIE.md 手动配置Cookie")
        print()

if __name__ == "__main__":
    main()
