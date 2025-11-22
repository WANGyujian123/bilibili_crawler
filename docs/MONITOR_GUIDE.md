# 视频监控功能使用指南

## 功能简介

monitor命令可以自动监控UP主的新视频更新，并通过邮件发送分析摘要。

## 快速开始

### 1. 配置邮箱

编辑 `.env` 文件：

```env
EMAIL_ENABLED=true
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=your_email@gmail.com
```

详细配置方法见 [docs/EMAIL_SETUP.md](docs/EMAIL_SETUP.md)

### 2. 测试监控（一次性检查）

```bash
# 先测试一次，确保功能正常
python3 main.py monitor 191640 --season-id 2910000 --once
```

### 3. 启动定时监控

```bash
# 每天早上9点自动检查
python3 main.py monitor 191640 --season-id 2910000 --check-time 09:00
```

## 工作流程

1. **定时检查**: 每天指定时间检查UP主是否有新视频
2. **发现新视频**: 对比数据库，找出未记录的视频
3. **下载字幕**: 自动下载新视频的字幕
4. **AI分析**: 使用Claude生成200字精简摘要
5. **邮件通知**: 发送HTML格式的邮件，包含所有新视频的分析

## 邮件内容示例

```
📺 B站新视频通知
UP主「egg淳雨」发布了 2 个新视频

━━━━━━━━━━━━━━━━━━━━━━

🎬 比特币突破10万美元！
BV号: BV1xxxxx

📊 AI分析摘要:
这个视频主要讨论比特币价格突破10万美元的历史性时刻...
核心观点是长期持有者应该保持冷静...
值得深入关注，因为涉及重要的市场转折点。

━━━━━━━━━━━━━━━━━━━━━━

🎬 新型网络诈骗警示
BV号: BV1yyyyy

📊 AI分析摘要:
这个视频主要讲述了最新的网络诈骗手段...
...
```

## 使用场景

### 场景1: 监控商业财经内容

```bash
# 监控egg淳雨的商业财经合集
python3 main.py monitor 191640 --season-id 2910000 --check-time 08:00
```

### 场景2: 监控UP主所有新视频

```bash
# 不指定合集，监控所有新视频
python3 main.py monitor 9458053 --check-time 10:00
```

### 场景3: 设置为系统服务（后台运行）

```bash
# 1. 创建systemd服务文件
sudo nano /etc/systemd/system/bilibili-monitor.service

# 2. 添加配置（修改路径）
[Unit]
Description=Bilibili Video Monitor
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/user/bilibili_crawler
ExecStart=/home/user/bilibili_crawler/venv/bin/python3 main.py monitor 191640 --season-id 2910000 --check-time 09:00
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# 3. 启动服务
sudo systemctl daemon-reload
sudo systemctl enable bilibili-monitor
sudo systemctl start bilibili-monitor

# 4. 查看状态
sudo systemctl status bilibili-monitor

# 5. 查看日志
sudo journalctl -u bilibili-monitor -f
```

## 注意事项

1. **API费用**: 精简版分析每个视频消耗约500 tokens，注意控制成本
2. **检查频率**: 建议每天1-2次，避免过于频繁
3. **邮箱限制**: 注意邮箱服务商的发送限制
4. **网络稳定**: 确保服务器网络稳定，否则可能漏掉新视频

## 故障排查

### 问题1: 没有收到邮件

检查：
- .env中EMAIL_ENABLED是否为true
- 邮箱密码是否正确（应该是应用专用密码）
- 查看日志中的错误信息

### 问题2: 分析失败

检查：
- CLAUDE_API_KEY是否配置正确
- 网络是否可以访问Claude API
- 查看日志了解具体错误

### 问题3: 检测不到新视频

检查：
- 数据库中是否已有该视频记录
- UP主是否真的发布了新视频
- 使用--once参数手动测试一次

## 高级用法

### 只在工作日检查

修改monitor命令，添加日期判断：

```python
# 在check_and_notify函数开头添加
import datetime
if datetime.datetime.now().weekday() >= 5:  # 周六日跳过
    logger.info("周末，跳过检查")
    return
```

### 多个UP主监控

创建多个systemd服务，或使用cron：

```cron
# 编辑crontab
crontab -e

# 添加
0 9 * * * cd /path/to/bilibili_crawler && ./venv/bin/python3 main.py monitor 191640 --once
0 10 * * * cd /path/to/bilibili_crawler && ./venv/bin/python3 main.py monitor 9458053 --once
```

