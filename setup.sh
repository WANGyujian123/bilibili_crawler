#!/bin/bash
# 环境设置和配置脚本

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "===================================="
echo "   B站爬虫项目环境设置"
echo "===================================="
echo ""

# 检查虚拟环境
if [ -d "venv" ]; then
    echo "✓ 虚拟环境已存在"
else
    echo "✗ 虚拟环境不存在，正在创建..."
    python3 -m venv venv
    echo "✓ 虚拟环境创建完成"
fi

# 检查依赖
echo ""
echo "检查依赖安装..."
if ./venv/bin/python3 -c "import anthropic, requests, pandas, click, loguru" 2>/dev/null; then
    echo "✓ 所有依赖已安装"
else
    echo "正在安装依赖（使用清华镜像源加速）..."
    ./venv/bin/pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo "✓ 依赖安装完成"
fi

# 检查.env文件
echo ""
if [ -f ".env" ]; then
    echo "✓ .env配置文件已存在"
else
    echo "✗ .env配置文件不存在"
    echo "正在创建.env文件..."
    cp .env.example .env
    echo "✓ 已创建.env文件"
    echo ""
    echo "⚠️  重要：请编辑 .env 文件，填入你的 Claude API 密钥"
    echo "   编辑命令：nano .env 或 vim .env"
fi

echo ""
echo "===================================="
echo "  环境设置完成！"
echo "===================================="
echo ""
echo "使用方法："
echo "  ./run.sh --help              # 查看帮助"
echo "  ./run.sh crawl <UID>         # 爬取UP主视频"
echo "  ./run.sh analyze <UID>       # 分析UP主内容"
echo ""
echo "配置文件："
echo "  .env - API密钥和配置"
echo ""
