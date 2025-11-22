#!/bin/bash
# GitHub推送脚本

echo "===================================="
echo "   推送到GitHub"
echo "===================================="
echo ""

# 检查是否已经添加远程仓库
if git remote get-url origin &> /dev/null; then
    echo "✓ 远程仓库已配置"
    echo "  地址: $(git remote get-url origin)"
    echo ""
    read -p "是否要重新设置远程仓库？(y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "请输入新的仓库URL: " repo_url
        git remote set-url origin "$repo_url"
        echo "✓ 远程仓库地址已更新"
    fi
else
    echo "⚠️  远程仓库未配置"
    echo ""
    echo "请先在GitHub上创建仓库，然后输入仓库URL"
    echo "格式: https://github.com/用户名/bilibili_crawler.git"
    echo ""
    read -p "仓库URL: " repo_url

    if [ -z "$repo_url" ]; then
        echo "❌ 错误：仓库URL不能为空"
        exit 1
    fi

    git remote add origin "$repo_url"
    echo "✓ 远程仓库已添加"
fi

echo ""
echo "准备推送代码..."
echo ""

# 显示当前状态
git status

echo ""
read -p "确认推送到GitHub？(Y/n) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo ""
    echo "推送中..."
    git push -u origin main

    if [ $? -eq 0 ]; then
        echo ""
        echo "===================================="
        echo "  ✓ 推送成功！"
        echo "===================================="
        echo ""
        echo "访问你的仓库："
        echo "$(git remote get-url origin | sed 's/\.git$//')"
        echo ""
    else
        echo ""
        echo "===================================="
        echo "  ❌ 推送失败"
        echo "===================================="
        echo ""
        echo "可能的原因："
        echo "1. 需要身份验证 - 请使用GitHub个人访问令牌"
        echo "2. 远程仓库已有内容 - 需要先拉取"
        echo "3. 网络问题"
        echo ""
        echo "详细帮助请查看: GITHUB_SETUP.md"
        echo ""
    fi
else
    echo "取消推送"
fi
