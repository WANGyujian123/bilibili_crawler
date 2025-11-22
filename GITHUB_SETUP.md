# GitHub 仓库设置指南

本地Git仓库已初始化完成，现在需要在GitHub上创建远程仓库并推送代码。

## 方法一：通过GitHub网页创建（推荐）

### 1. 在GitHub上创建新仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `bilibili_crawler`
   - **Description**: B站内容爬虫与AI分析工具 - 爬取UP主视频字幕并使用Claude AI分析思想观点
   - **Visibility**:
     - ✅ Public（公开）- 推荐，可以分享给其他人
     - ⬜ Private（私有）- 仅自己可见
   - **重要**:
     - ❌ 不要勾选 "Add a README file"
     - ❌ 不要添加 .gitignore
     - ❌ 不要选择 license
     （因为我们本地已经有这些文件了）

3. 点击 **"Create repository"** 创建仓库

### 2. 连接远程仓库并推送

创建完成后，GitHub会显示一个页面。在 "…or push an existing repository from the command line" 部分，你会看到类似的命令。

**在你的项目目录执行以下命令：**

```bash
# 添加远程仓库（替换 WANGyujian123 为你的GitHub用户名）
git remote add origin https://github.com/WANGyujian123/bilibili_crawler.git

# 推送代码到GitHub
git push -u origin main
```

### 3. 验证推送成功

刷新GitHub仓库页面，你应该能看到所有文件已经上传成功。

---

## 方法二：使用GitHub CLI（需要先安装）

如果你安装了GitHub CLI，可以用一条命令完成：

### 1. 安装GitHub CLI

**在WSL/Ubuntu上：**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 2. 登录GitHub

```bash
gh auth login
# 选择 GitHub.com
# 选择 HTTPS
# 选择 Login with a web browser
# 按照提示在浏览器中完成登录
```

### 3. 创建仓库并推送

```bash
# 一键创建公开仓库并推送
gh repo create bilibili_crawler --public --source=. --remote=origin --push

# 或创建私有仓库
gh repo create bilibili_crawler --private --source=. --remote=origin --push
```

---

## 快捷脚本

为了方便，我已经准备好了推送脚本。只需修改其中的GitHub用户名即可使用。

### 创建推送脚本

```bash
# 查看当前Git状态
git status

# 推送到GitHub（首次推送）
git remote add origin https://github.com/你的用户名/bilibili_crawler.git
git push -u origin main
```

---

## 常见问题

### Q: 推送时提示需要身份验证？

A: GitHub现在要求使用个人访问令牌（Personal Access Token）而不是密码。

**创建Token：**
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 给token命名，如 "bilibili_crawler"
4. 勾选权限：至少选择 `repo` 完整权限
5. 点击 "Generate token"
6. **重要**：立即复制生成的token（离开页面后无法再查看）

**使用Token：**
当推送时提示输入密码时，输入Token而不是GitHub密码。

### Q: 如何修改远程仓库地址？

```bash
# 查看当前远程仓库
git remote -v

# 修改远程仓库地址
git remote set-url origin https://github.com/你的用户名/bilibili_crawler.git
```

### Q: 如何使用SSH而不是HTTPS？

```bash
# 首先生成SSH密钥（如果还没有）
ssh-keygen -t ed25519 -C "1165903555@qq.com"

# 添加SSH密钥到GitHub
# 复制公钥内容
cat ~/.ssh/id_ed25519.pub
# 访问 https://github.com/settings/keys 添加SSH key

# 使用SSH URL添加远程仓库
git remote add origin git@github.com:WANGyujian123/bilibili_crawler.git
git push -u origin main
```

### Q: 推送失败，提示已存在内容？

如果远程仓库不是空的（比如已经有README等文件），需要先拉取：

```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## 后续使用

### 日常提交流程

```bash
# 1. 查看修改
git status

# 2. 添加修改的文件
git add .

# 3. 提交修改
git commit -m "描述你的修改"

# 4. 推送到GitHub
git push
```

### 查看提交历史

```bash
git log --oneline
```

### 创建分支

```bash
# 创建并切换到新分支
git checkout -b feature-name

# 推送新分支到GitHub
git push -u origin feature-name
```

---

## 你的配置信息

- **GitHub用户名**: WANGyujian123
- **邮箱**: 1165903555@qq.com
- **仓库名**: bilibili_crawler
- **默认分支**: main

**推荐的远程仓库URL**:
```
https://github.com/WANGyujian123/bilibili_crawler.git
```

---

## 下一步

1. ✅ 本地Git仓库已初始化
2. ✅ 代码已提交到本地main分支
3. ⏳ 在GitHub上创建远程仓库
4. ⏳ 推送代码到GitHub
5. 🎉 完成！

现在请按照上述"方法一"的步骤，在GitHub上创建仓库并推送代码。
