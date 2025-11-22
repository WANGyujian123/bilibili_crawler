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

**Claude API配置：**

```env
# Claude API配置
CLAUDE_API_KEY=your_api_key_here

# 如果使用代理站，填入代理地址
CLAUDE_API_BASE_URL=https://api.your-proxy.com/v1
```

> - **官方API**：访问 [Anthropic Console](https://console.anthropic.com/) 获取密钥
> - **代理站**：填入代理站提供的API密钥和代理地址

### 2.5. B站登录（可选，推荐）

某些视频的字幕需要登录才能访问。**推荐使用扫码登录（最方便）：**

```bash
source venv/bin/activate
python3 bilibili_login.py
```

程序会显示二维码，使用B站APP扫码即可自动完成配置。

**或者手动配置Cookie**（查看 [GET_COOKIE.md](GET_COOKIE.md)）：
```env
BILIBILI_COOKIE=你的B站Cookie
```

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

### 1. 查看UP主的合集列表

查看UP主所有的合集和视频列表：

```bash
python3 main.py list-series <UID>
```

这会显示所有合集的ID和视频数量，方便你选择感兴趣的合集进行爬取。

**如何获取UP主的UID：**
1. 访问UP主的B站主页
2. 查看URL，例如：`https://space.bilibili.com/123456`
3. 其中的 `123456` 就是UID

### 2. 爬取UP主内容

**爬取所有视频：**

```bash
python3 main.py crawl <UID> --with-subtitle
```

**爬取指定合集的视频：**

```bash
# 先查看合集列表
python3 main.py list-series <UID>

# 然后爬取指定合集
python3 main.py crawl <UID> --season-id <合集ID> --with-subtitle
```

**爬取指定视频列表：**

```bash
python3 main.py crawl <UID> --series-id <列表ID> --with-subtitle
```

**限制爬取数量：**

```bash
python3 main.py crawl <UID> --max-videos 20 --with-subtitle
```

### 3. 下载字幕

为已爬取的视频单独下载字幕：

```bash
python3 main.py download-subtitle <UID>
```

指定下载数量：

```bash
python3 main.py download-subtitle <UID> --max-videos 10
```

### 4. 分析内容

**分析整个UP主的内容：**

```bash
# 综合分析（包括思想、主题、风格）
python3 main.py analyze <UID>

# 仅思想分析
python3 main.py analyze <UID> --analysis-type ideology

# 仅主题分析
python3 main.py analyze <UID> --analysis-type themes

# 仅风格分析
python3 main.py analyze <UID> --analysis-type style

# 指定分析的视频数量
python3 main.py analyze <UID> --max-videos 20
```

**分析单个视频：**

```bash
# 综合分析单个视频
python3 main.py analyze-video <BVID>

# 仅分析主题
python3 main.py analyze-video <BVID> --analysis-type themes

# 仅分析风格
python3 main.py analyze-video <BVID> --analysis-type style
```

**示例**：
```bash
# 分析BV1WxnYzTEi2这个视频
python3 main.py analyze-video BV1WxnYzTEi2

# 只分析这个视频的主题
python3 main.py analyze-video BV1WxnYzTEi2 -t themes
```

### 5. 查看和导出结果

**在终端查看**（默认）：
```bash
python3 main.py show <UID>
```

**导出为Markdown文件**（推荐用于学习）：
```bash
python3 main.py show <UID> --format markdown --output reports/分析报告.md
```

**导出为JSON文件**（用于数据分析）：
```bash
python3 main.py show <UID> --format json --output reports/数据.json
```

**在终端预览Markdown格式**：
```bash
python3 main.py show <UID> --format markdown
```

### 6. 查询单个视频

查看单个视频的详细信息和完整字幕：

```bash
# 在终端查看
python3 main.py query <BVID>

# 导出到文件
python3 main.py query <BVID> --output reports/视频字幕.txt
```

**示例**：
```bash
# 查看BV1WxnYzTEi2的字幕
python3 main.py query BV1WxnYzTEi2

# 导出到文件
python3 main.py query BV1WxnYzTEi2 -o reports/比特币分析.txt
```

## 完整使用流程示例

### 示例1：分析UP主的某个合集

```bash
# 1. 查看UP主的所有合集
python3 main.py list-series 9458053

# 2. 爬取指定合集的视频和字幕（例如：高中物理必修一）
python3 main.py crawl 9458053 --season-id 2352600 --with-subtitle

# 3. 分析这个合集的内容
python3 main.py analyze 9458053

# 4. 查看分析结果
python3 main.py show 9458053
```

### 示例2：分析UP主的所有视频

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

## 学习资源

本项目提供了完整的商业财经分析学习资源：

- [UP主商业财经分析方法论](docs/UP主商业财经分析方法论.md) - 提取UP主的核心分析框架和知识体系
- [学习实践指南](docs/学习实践指南.md) - 12个月系统学习路径
- [获取Cookie指南](docs/GET_COOKIE.md) - 手动获取B站Cookie的方法

## 许可证

MIT License

## 免责声明

本工具仅供学习和研究使用。请遵守B站的使用条款和机器人协议，不要过度爬取造成服务器负担。使用本工具产生的任何后果由使用者自行承担。
