# 快速启动指南

## 第一步：安装依赖

```bash
pip install -r requirements.txt
```

或者使用 pip3：

```bash
pip3 install -r requirements.txt
```

## 第二步：配置API密钥

1. 复制环境变量示例文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的Claude API密钥：
```bash
CLAUDE_API_KEY=sk-ant-xxxxx  # 替换成你的实际密钥
```

**获取Claude API密钥：**
- 访问 https://console.anthropic.com/
- 注册账号并创建API密钥

## 第三步：测试运行

查看帮助信息：
```bash
python3 main.py --help
```

## 完整使用示例

假设要分析UID为 `123456` 的UP主（以李永乐老师为例，UID: `9458053`）：

### 1. 爬取视频信息和字幕
```bash
python3 main.py crawl 9458053 --max-videos 10 --with-subtitle
```

这一步会：
- 获取UP主的基本信息
- 获取最多10个视频的信息
- 自动下载这些视频的字幕
- 保存到SQLite数据库

### 2. 分析内容
```bash
python3 main.py analyze 9458053 --max-videos 10
```

这一步会：
- 使用Claude AI分析UP主的思想、主题和风格
- 生成详细的分析报告
- 保存分析结果到数据库

### 3. 查看结果
```bash
python3 main.py show 9458053
```

这会显示：
- UP主基本信息
- 视频统计
- 所有历史分析结果

## 常用命令速查

```bash
# 爬取内容（含字幕）
python3 main.py crawl <UID> --max-videos 20 --with-subtitle

# 单独下载字幕
python3 main.py download-subtitle <UID> --max-videos 20

# 综合分析
python3 main.py analyze <UID> --max-videos 10

# 仅思想分析
python3 main.py analyze <UID> --analysis-type ideology

# 查看结果
python3 main.py show <UID>
```

## 如何找到UP主的UID

1. 打开UP主的B站主页
2. 查看浏览器地址栏的URL
3. URL格式为：`https://space.bilibili.com/UID`
4. 其中的数字就是UID

例如：
- 李永乐老师：https://space.bilibili.com/9458053 → UID是 `9458053`
- 罗翔老师：https://space.bilibili.com/517327498 → UID是 `517327498`

## 注意事项

1. 确保有稳定的网络连接
2. Claude API会产生费用，建议先用少量视频测试
3. 不是所有视频都有字幕，程序会自动跳过没有字幕的视频
4. 建议从 `--max-videos 5` 开始测试，确认正常后再增加数量

## 故障排除

**问题：ModuleNotFoundError**
- 解决：运行 `pip3 install -r requirements.txt` 安装依赖

**问题：CLAUDE_API_KEY错误**
- 解决：检查 `.env` 文件中的API密钥是否正确

**问题：无法获取视频信息**
- 解决：检查网络连接，确认UID是否正确

**问题：没有字幕**
- 解决：尝试其他UP主，或者查看原视频是否确实有字幕
