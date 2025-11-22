#!/bin/bash
# 在GitHub上创建仓库后，运行此脚本推送代码

echo "===================================="
echo "   推送代码到GitHub"
echo "===================================="
echo ""
echo "执行以下命令："
echo ""

# 添加远程仓库
echo "# 1. 添加远程仓库"
echo "git remote add origin https://github.com/WANGyujian123/bilibili_crawler.git"
git remote add origin https://github.com/WANGyujian123/bilibili_crawler.git 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ 远程仓库已添加"
else
    echo "⚠️  远程仓库可能已存在，继续推送..."
fi

echo ""
echo "# 2. 推送到GitHub"
echo "git push -u origin main"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "===================================="
    echo "  ✅ 推送成功！"
    echo "===================================="
    echo ""
    echo "🎉 你的仓库地址："
    echo "   https://github.com/WANGyujian123/bilibili_crawler"
    echo ""
else
    echo ""
    echo "===================================="
    echo "  ❌ 推送失败"
    echo "===================================="
    echo ""
    echo "可能的原因："
    echo "1. 需要GitHub身份验证"
    echo "   - 用户名: WANGyujian123"
    echo "   - 密码: 使用个人访问令牌（不是GitHub密码）"
    echo ""
    echo "2. 创建个人访问令牌："
    echo "   访问: https://github.com/settings/tokens/new"
    echo "   - 勾选 'repo' 权限"
    echo "   - 生成并复制token"
    echo "   - 推送时使用token作为密码"
    echo ""
fi
