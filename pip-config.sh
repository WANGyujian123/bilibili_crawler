#!/bin/bash
# pip镜像源配置脚本

echo "===================================="
echo "   配置pip镜像源"
echo "===================================="
echo ""

# 创建pip配置目录
mkdir -p ~/.pip

# 创建配置文件
cat > ~/.pip/pip.conf << 'EOF'
[global]
# 默认镜像源：清华大学
index-url = https://pypi.tuna.tsinghua.edu.cn/simple

[install]
# 信任的主机
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF

echo "✓ pip镜像源配置完成"
echo ""
echo "配置文件位置: ~/.pip/pip.conf"
echo "当前镜像源: 清华大学 PyPI 镜像"
echo ""
echo "查看配置:"
cat ~/.pip/pip.conf
echo ""
echo "===================================="
echo ""
echo "其他可用镜像源："
echo "  清华: https://pypi.tuna.tsinghua.edu.cn/simple"
echo "  阿里云: https://mirrors.aliyun.com/pypi/simple/"
echo "  中科大: https://pypi.mirrors.ustc.edu.cn/simple/"
echo "  豆瓣: http://pypi.douban.com/simple/"
echo ""
echo "如需更换镜像源，编辑: ~/.pip/pip.conf"
echo ""
