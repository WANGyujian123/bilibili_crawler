#!/bin/bash
# 激活虚拟环境的快捷脚本

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "激活虚拟环境..."
echo "退出虚拟环境请输入: deactivate"
echo ""

# 激活虚拟环境
source "$SCRIPT_DIR/venv/bin/activate"

# 进入项目目录
cd "$SCRIPT_DIR"
