"""邮件通知模块"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from loguru import logger
import config


class EmailNotifier:
    """邮件通知器"""

    def __init__(self):
        """初始化邮件通知器"""
        self.enabled = config.EMAIL_ENABLED
        self.smtp_host = config.EMAIL_SMTP_HOST
        self.smtp_port = config.EMAIL_SMTP_PORT
        self.sender = config.EMAIL_SENDER
        self.password = config.EMAIL_PASSWORD
        self.receiver = config.EMAIL_RECEIVER

        if self.enabled and not all([self.sender, self.password, self.receiver]):
            logger.warning("邮件功能已启用但配置不完整，将无法发送邮件")
            self.enabled = False

    def send_email(self, subject: str, content: str, content_type: str = "plain") -> bool:
        """
        发送邮件

        Args:
            subject: 邮件主题
            content: 邮件内容
            content_type: 内容类型，'plain'或'html'

        Returns:
            bool: 是否发送成功
        """
        if not self.enabled:
            logger.info("邮件功能未启用，跳过发送")
            return False

        try:
            # 创建邮件
            message = MIMEMultipart()
            message['From'] = Header(f"B站监控 <{self.sender}>")
            message['To'] = Header(self.receiver)
            message['Subject'] = Header(subject, 'utf-8')

            # 添加邮件内容
            message.attach(MIMEText(content, content_type, 'utf-8'))

            # 连接SMTP服务器并发送
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()  # 启用TLS加密
                server.login(self.sender, self.password)
                server.send_message(message)

            logger.info(f"邮件发送成功: {subject}")
            return True

        except Exception as e:
            logger.error(f"邮件发送失败: {e}")
            return False

    def send_video_notification(self, uploader_name: str, videos: list, analyses: dict) -> bool:
        """
        发送新视频通知

        Args:
            uploader_name: UP主名称
            videos: 新视频列表
            analyses: 分析结果字典 {bvid: analysis_text}

        Returns:
            bool: 是否发送成功
        """
        if not videos:
            return False

        # 构建HTML邮件内容
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #00a1d6; color: white; padding: 20px; text-align: center; }}
                .video-card {{ border: 1px solid #ddd; margin: 20px 0; padding: 15px; border-radius: 5px; }}
                .video-title {{ font-size: 18px; font-weight: bold; color: #00a1d6; margin-bottom: 10px; }}
                .video-bvid {{ color: #666; font-size: 12px; margin-bottom: 15px; }}
                .analysis {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; white-space: pre-wrap; }}
                .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📺 B站新视频通知</h1>
                <p>UP主「{uploader_name}」发布了 {len(videos)} 个新视频</p>
            </div>
        """

        for video in videos:
            bvid = video.get('bvid')
            title = video.get('title', '未知标题')
            analysis = analyses.get(bvid, '暂无分析')

            html_content += f"""
            <div class="video-card">
                <div class="video-title">🎬 {title}</div>
                <div class="video-bvid">BV号: {bvid}</div>
                <div class="analysis">
                    <strong>📊 AI分析摘要:</strong><br><br>
                    {analysis}
                </div>
            </div>
            """

        html_content += """
            <div class="footer">
                <p>🤖 本邮件由B站内容爬虫工具自动生成</p>
                <p>Powered by Claude AI</p>
            </div>
        </body>
        </html>
        """

        subject = f"[B站监控] {uploader_name} 发布了 {len(videos)} 个新视频"
        return self.send_email(subject, html_content, content_type="html")
