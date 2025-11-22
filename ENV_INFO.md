# 环境配置信息

## 项目环境

- **Python版本**: Python 3.12
- **虚拟环境**: venv (已配置)
- **包管理**: pip (已配置清华镜像源)
- **镜像源配置**: ~/.pip/pip.conf (全局生效)

## pip镜像源配置

已永久配置清华大学PyPI镜像源，所有pip安装都会自动使用镜像加速：

**配置文件**: `~/.pip/pip.conf`

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple

[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
```

**效果**:
- ✅ 无需每次使用 `-i` 参数
- ✅ 全局生效（所有Python项目）
- ✅ 虚拟环境也会自动使用

**验证配置**:
```bash
pip config list
```

**常用命令**:
```bash
# 现在可以直接安装，会自动使用镜像源
pip install package-name

# 无需再加 -i 参数
pip install -r requirements.txt
```

## 其他可用镜像源

如需更换镜像源，编辑 `~/.pip/pip.conf` 文件，替换 `index-url` 值：

| 镜像源 | URL |
|--------|-----|
| 清华大学 (推荐) | https://pypi.tuna.tsinghua.edu.cn/simple |
| 阿里云 | https://mirrors.aliyun.com/pypi/simple/ |
| 中国科技大学 | https://pypi.mirrors.ustc.edu.cn/simple/ |
| 豆瓣 | http://pypi.douban.com/simple/ |

或运行项目提供的配置脚本：
```bash
./pip-config.sh
```

## 已安装的依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| anthropic | 0.74.1 | Claude AI API客户端 |
| requests | 2.32.5 | HTTP请求库（B站API） |
| httpx | 0.28.1 | 现代HTTP客户端 |
| pandas | 2.3.3 | 数据处理 |
| numpy | 2.3.5 | 数值计算（pandas依赖） |
| click | 8.3.1 | 命令行界面 |
| loguru | 0.7.3 | 日志记录 |
| python-dotenv | 1.2.1 | 环境变量管理 |

## 便捷脚本

| 脚本 | 说明 |
|------|------|
| `setup.sh` | 一键环境设置脚本 |
| `run.sh` | 快捷运行主程序 |
| `activate.sh` | 激活虚拟环境 |
| `pip-config.sh` | 配置pip镜像源 |

## 配置文件

| 文件 | 说明 |
|------|------|
| `.env` | 环境变量（API密钥等） |
| `config.py` | Python配置模块 |
| `requirements.txt` | 依赖列表 |
| `~/.pip/pip.conf` | pip全局配置（镜像源） |

## 虚拟环境使用

### 激活虚拟环境
```bash
source activate.sh
# 或
source venv/bin/activate
```

### 退出虚拟环境
```bash
deactivate
```

### 在虚拟环境中安装新包
```bash
# 现在无需指定镜像源，会自动使用配置的镜像
pip install <package-name>

# 或使用完整路径
./venv/bin/pip install <package-name>
```

## 故障排除

### 依赖安装失败
```bash
# 重新运行设置脚本
./setup.sh

# 或手动重装
pip install -r requirements.txt
```

### 镜像源配置失效
```bash
# 重新配置镜像源
./pip-config.sh

# 或手动检查配置
cat ~/.pip/pip.conf
```

### 环境变量未生效
确保项目根目录有 `.env` 文件，且包含必要的配置：
```bash
cat .env
```

### Python版本问题
项目需要Python 3.8+，检查版本：
```bash
python3 --version
```

## 性能优化

使用清华镜像源后，pip安装速度提升明显：

- **官方源**: 通常 100-500 KB/s
- **清华镜像**: 通常 5-10 MB/s

大型包（如numpy, pandas）下载时间可从几分钟缩短到几秒钟。
