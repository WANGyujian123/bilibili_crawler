# B站内容爬虫与分析工具

一个用于爬取B站UP主视频内容、提取字幕并使用Claude AI分析UP主思想观点的工具。

## 功能特性

- 爬取B站UP主的基本信息和视频列表
- 自动下载视频字幕（支持中文和其他语言）
- 使用Claude AI分析UP主的思想、观点和表达风格
- 多维度分析：思想分析、主题分析、风格分析
- SQLite数据库存储，方便查询和管理
- 命令行界面，操作简单直观

## 快速开始

### 1. 创建虚拟环境并安装依赖

```bash
cd bilibili_crawler
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

### 2. 配置API密钥

```bash
cp .env.example .env
nano .env  # 编辑文件，填入你的Claude API密钥
```

**配置说明：**

```env
# Claude API配置
CLAUDE_API_KEY=your_api_key_here

# 如果使用代理站，填入代理地址
CLAUDE_API_BASE_URL=https://api.your-proxy.com/v1

# B站Cookie（可选，用于获取需要登录的字幕）
BILIBILI_COOKIE=你的B站Cookie
```

> - **Claude API**：
>   - **官方API**：访问 [Anthropic Console](https://console.anthropic.com/) 获取密钥
>   - **代理站**：填入代理站提供的API密钥和代理地址
>
> - **B站Cookie**（可选）：
>   - 某些视频的字幕需要登录才能访问
>   - 如何获取Cookie：查看 [GET_COOKIE.md](GET_COOKIE.md)
>   - 如果不配置，仍可爬取公开的字幕

### 3. 开始使用

```bash
# 方式1：激活虚拟环境后使用
source venv/bin/activate
python3 main.py --help
python3 main.py crawl 9458053 --max-videos 10 --with-subtitle
python3 main.py analyze 9458053

# 方式2：直接使用虚拟环境中的Python
./venv/bin/python3 main.py --help
```

## 使用方法

### 基本命令

```bash
# 激活虚拟环境（推荐）
source venv/bin/activate
python3 main.py --help
```

### 1. 爬取UP主内容

爬取UP主的视频信息：

```bash
python3 main.py crawl <UID>
```

同时下载字幕：

```bash
python3 main.py crawl <UID> --with-subtitle
```

限制爬取数量：

```bash
python3 main.py crawl <UID> --max-videos 20
```

**如何获取UP主的UID：**
1. 访问UP主的B站主页
2. 查看URL，例如：`https://space.bilibili.com/123456`
3. 其中的 `123456` 就是UID

### 2. 下载字幕

为已爬取的视频单独下载字幕：

```bash
python3 main.py download-subtitle <UID>
```

指定下载数量：

```bash
python3 main.py download-subtitle <UID> --max-videos 10
```

### 3. 分析内容

使用Claude AI分析UP主的内容：

```bash
# 综合分析（包括思想、主题、风格）
python3 main.py analyze <UID>

# 仅思想分析
python3 main.py analyze <UID> --analysis-type ideology

# 仅主题分析
python3 main.py analyze <UID> --analysis-type themes

# 仅风格分析
python3 main.py analyze <UID> --analysis-type style
```

指定分析的视频数量：

```bash
python3 main.py analyze <UID> --max-videos 20
```

### 4. 查看结果

查看已保存的分析结果：

```bash
python3 main.py show <UID>
```

## 完整使用流程示例

假设要分析UID为`123456`的UP主：

```bash
# 1. 爬取UP主的视频信息（最多20个视频）
python3 main.py crawl 123456 --max-videos 20 --with-subtitle

# 2. 如果第一步没有加--with-subtitle，可以单独下载字幕
python3 main.py download-subtitle 123456

# 3. 进行综合分析
python3 main.py analyze 123456 --max-videos 10

# 4. 查看分析结果
python3 main.py show 123456
```

## 项目结构

```
bilibili_crawler/
├── README.md                 # 项目说明文档
├── requirements.txt          # Python依赖
├── config.py                 # 配置文件
├── main.py                   # 主程序入口
├── .env.example              # 环境变量示例
├── .gitignore                # Git忽略文件
├── bilibili/                 # B站爬虫模块
│   ├── __init__.py
│   ├── api.py                # B站API封装
│   └── subtitle.py           # 字幕下载器
├── analyzer/                 # 分析模块
│   ├── __init__.py
│   └── claude_analyzer.py    # Claude AI分析器
├── database/                 # 数据库模块
│   ├── __init__.py
│   └── db.py                 # SQLite数据库操作
├── data/                     # 数据存储目录
│   └── bilibili.db           # SQLite数据库文件
└── logs/                     # 日志目录
    └── bilibili_crawler.log  # 日志文件
```

## 数据库结构

项目使用SQLite数据库存储数据，包含以下表：

- `users`: UP主信息
- `videos`: 视频信息
- `subtitles`: 字幕内容
- `analysis`: 分析结果

## 注意事项

1. **API调用频率**：爬取时会自动控制请求频率，避免被B站限制
2. **Claude API费用**：使用Claude API会产生费用，请注意控制分析的视频数量
3. **字幕可用性**：不是所有视频都有字幕，如果视频没有字幕，字幕下载会跳过
4. **数据存储**：所有数据存储在`data/bilibili.db`数据库中，可以直接使用SQLite工具查看

## 常见问题

### Q: 如何获取UP主的UID？
A: 访问UP主的B站主页，URL中的数字就是UID，例如 `space.bilibili.com/123456` 中的 `123456`

### Q: 为什么有些视频下载不了字幕？
A: 不是所有视频都有字幕。UP主需要上传字幕文件，或者B站自动生成字幕，视频才会有字幕。

### Q: 分析需要多长时间？
A: 取决于视频数量和字幕长度。一般10个视频的综合分析需要2-5分钟。

### Q: 可以分析多个UP主吗？
A: 可以。每个UP主的数据独立存储，可以对多个UP主分别进行爬取和分析。

### Q: 如何导出分析结果？
A: 可以使用 `python3 main.py show <UID>` 查看结果，也可以直接查询SQLite数据库的 `analysis` 表。

## 开发者信息

使用的主要技术：
- Python 3.8+
- Requests: HTTP请求
- Anthropic Claude API: AI分析
- SQLite: 数据存储
- Click: 命令行界面
- Loguru: 日志记录

## 许可证

MIT License

## 免责声明

本工具仅供学习和研究使用。请遵守B站的使用条款和机器人协议，不要过度爬取造成服务器负担。使用本工具产生的任何后果由使用者自行承担。
