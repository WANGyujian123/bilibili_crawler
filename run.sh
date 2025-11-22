#!/bin/bash
# B站爬虫快捷运行脚本

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 使用虚拟环境中的Python运行主程序
./venv/bin/python3 main.py "$@"
