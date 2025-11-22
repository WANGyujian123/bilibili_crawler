# 如何获取B站Cookie

某些B站视频的字幕需要登录才能访问。为了让爬虫能够获取这些字幕，需要提供你的B站登录凭证（Cookie）。

## 获取Cookie的步骤

### 方法1：使用浏览器开发者工具（推荐）

1. **打开B站并登录**
   - 访问 https://www.bilibili.com
   - 使用你的账号登录

2. **打开浏览器开发者工具**
   - Chrome/Edge：按 `F12` 或 `Ctrl+Shift+I`（Mac: `Cmd+Option+I`）
   - Firefox：按 `F12`

3. **切换到 Network（网络）标签**
   - 点击开发者工具顶部的 "Network" 或 "网络" 标签

4. **刷新页面**
   - 按 `F5` 或点击浏览器刷新按钮

5. **找到请求**
   - 在网络请求列表中，找到第一个请求（通常是 `www.bilibili.com`）
   - 点击这个请求

6. **复制Cookie**
   - 在右侧面板找到 "Request Headers"（请求头）
   - 找到 `Cookie:` 这一行
   - 复制整个Cookie值（注意：可能很长）

### 方法2：使用浏览器扩展

1. 安装 "EditThisCookie" 或类似的Cookie管理扩展
2. 访问 https://www.bilibili.com 并登录
3. 点击扩展图标
4. 导出Cookie

## 配置Cookie

将获取到的Cookie添加到 `.env` 文件中：

```env
# B站Cookie（可选，用于访问需要登录的字幕）
BILIBILI_COOKIE=你的完整Cookie字符串
```

**重要提示：**
- Cookie包含你的登录凭证，**不要分享给他人**
- 不要将包含真实Cookie的 `.env` 文件提交到GitHub
- Cookie可能会过期，过期后需要重新获取

## Cookie示例格式

Cookie通常是这样的格式：
```
SESSDATA=cb06xxx...; bili_jct=xxx...; DedeUserID=xxx; ...
```

只需要完整复制这一长串字符串即可。

## 安全建议

1. 定期更换密码会导致Cookie失效
2. 不要在公共电脑上使用此功能
3. 项目的 `.gitignore` 已配置忽略 `.env` 文件，确保不会意外提交
