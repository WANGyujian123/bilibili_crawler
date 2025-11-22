# 邮箱配置指南

monitor功能需要配置邮箱才能发送通知。以下是常见邮箱服务商的配置方法。

## Gmail 配置

### 1. 启用两步验证

1. 访问 [Google账户安全页面](https://myaccount.google.com/security)
2. 找到"登录Google"部分
3. 点击"两步验证"并按照提示启用

### 2. 生成应用专用密码

1. 在"两步验证"页面，滚动到底部找到"应用专用密码"
2. 点击"生成"
3. 选择应用类型：邮件
4. 选择设备类型：其他（自定义名称），输入"B站爬虫"
5. 点击"生成"
6. **复制生成的16位密码**（类似：`abcd efgh ijkl mnop`）

### 3. 配置.env文件

```env
EMAIL_ENABLED=true
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop  # 粘贴应用专用密码（去掉空格）
EMAIL_RECEIVER=your_email@gmail.com
```

## QQ邮箱配置

### 1. 开启SMTP服务

1. 登录QQ邮箱网页版
2. 点击"设置" -> "账户"
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 开启"SMTP服务"
5. 按照提示发送短信验证
6. **保存生成的授权码**

### 2. 配置.env文件

```env
EMAIL_ENABLED=true
EMAIL_SMTP_HOST=smtp.qq.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER=your_qq@qq.com
EMAIL_PASSWORD=your_authorization_code  # 填入授权码
EMAIL_RECEIVER=your_qq@qq.com
```

## 163网易邮箱配置

### 1. 开启SMTP服务

1. 登录163邮箱网页版
2. 点击"设置" -> "POP3/SMTP/IMAP"
3. 开启"SMTP服务"
4. 设置授权密码（或使用账户密码）

### 2. 配置.env文件

```env
EMAIL_ENABLED=true
EMAIL_SMTP_HOST=smtp.163.com
EMAIL_SMTP_PORT=25
EMAIL_SENDER=your_email@163.com
EMAIL_PASSWORD=your_password  # 授权密码或账户密码
EMAIL_RECEIVER=your_email@163.com
```

## Outlook/Hotmail 配置

```env
EMAIL_ENABLED=true
EMAIL_SMTP_HOST=smtp.office365.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER=your_email@outlook.com
EMAIL_PASSWORD=your_password
EMAIL_RECEIVER=your_email@outlook.com
```

## 测试邮件功能

配置完成后，可以使用 `--once` 参数测试：

```bash
python3 main.py monitor <UID> --once
```

如果配置正确，会在发现新视频时发送邮件。

## 常见问题

### Q: 提示"Authentication failed"

**A**: 检查以下几点：
1. 确认使用的是"应用专用密码"或"授权码"，而不是账户密码
2. 密码中不要有空格
3. 确认SMTP服务已开启

### Q: 提示"Connection refused"

**A**: 检查SMTP服务器地址和端口是否正确

### Q: Gmail提示"Less secure app access"

**A**: Gmail已停用"允许不够安全的应用"功能，必须使用"应用专用密码"

### Q: 如何发送到多个邮箱？

**A**: 目前只支持单个接收邮箱。如需发送到多个邮箱，可以：
- 使用邮箱的自动转发功能
- 或修改 `monitor/email_notifier.py` 中的代码

## 安全建议

1. **不要**将.env文件提交到Git仓库
2. 使用应用专用密码而非账户密码
3. 定期更换应用专用密码
4. 不要在公共场所展示.env文件内容
