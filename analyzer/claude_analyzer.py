"""使用Claude API进行文本分析"""
from anthropic import Anthropic
from typing import List, Dict, Optional
from loguru import logger
import config


class ClaudeAnalyzer:
    """Claude文本分析器"""

    def __init__(self, api_key: str = None):
        """
        初始化Claude分析器

        Args:
            api_key: Claude API密钥
        """
        self.api_key = api_key or config.CLAUDE_API_KEY
        if not self.api_key:
            raise ValueError("未设置CLAUDE_API_KEY，请在.env文件中配置")

        self.client = Anthropic(api_key=self.api_key)
        self.model = config.CLAUDE_MODEL
        logger.info(f"Claude分析器初始化完成，使用模型: {self.model}")

    def analyze_text(self, text: str, prompt: str, max_tokens: int = 4096) -> Optional[str]:
        """
        使用Claude分析文本

        Args:
            text: 要分析的文本
            prompt: 分析提示词
            max_tokens: 最大返回token数

        Returns:
            分析结果
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}\n\n以下是需要分析的文本：\n\n{text}"
                    }
                ]
            )

            result = message.content[0].text
            logger.info(f"成功完成文本分析，返回 {len(result)} 字符")
            return result

        except Exception as e:
            logger.error(f"Claude分析失败: {e}")
            return None

    def analyze_ideology(self, texts: List[str], user_name: str = "该UP主") -> Optional[str]:
        """
        分析UP主的思想和观点

        Args:
            texts: 字幕文本列表
            user_name: UP主名称

        Returns:
            思想分析结果
        """
        combined_text = "\n\n===\n\n".join(texts)

        prompt = f"""请分析{user_name}在这些视频中表达的思想和观点。

分析维度：
1. 核心价值观和信念
2. 主要关注的话题和领域
3. 思维方式和逻辑特点
4. 对重要议题的立场和态度
5. 思想的发展和变化（如果有）

请提供深入、全面的分析，避免表面化的总结。"""

        logger.info(f"开始分析{user_name}的思想，文本总长度: {len(combined_text)} 字符")
        return self.analyze_text(combined_text, prompt, max_tokens=8192)

    def analyze_themes(self, texts: List[str]) -> Optional[str]:
        """
        分析主要主题

        Args:
            texts: 字幕文本列表

        Returns:
            主题分析结果
        """
        combined_text = "\n\n===\n\n".join(texts)

        prompt = """请分析这些视频内容的主要主题。

分析要求：
1. 识别出现频率最高的主题
2. 归纳主题之间的关联性
3. 分析主题的深度和广度
4. 总结内容创作的特点

请以清晰的结构呈现分析结果。"""

        logger.info(f"开始主题分析，文本总长度: {len(combined_text)} 字符")
        return self.analyze_text(combined_text, prompt, max_tokens=4096)

    def analyze_style(self, texts: List[str]) -> Optional[str]:
        """
        分析表达风格

        Args:
            texts: 字幕文本列表

        Returns:
            风格分析结果
        """
        combined_text = "\n\n===\n\n".join(texts[:5])  # 限制文本长度

        prompt = """请分析这位UP主的表达风格和语言特点。

分析维度：
1. 语言风格（正式/轻松、严肃/幽默等）
2. 表达习惯和常用词汇
3. 论证方式和逻辑结构
4. 与观众的互动方式
5. 独特的语言特色

请提供具体的例子支持你的分析。"""

        logger.info("开始风格分析")
        return self.analyze_text(combined_text, prompt, max_tokens=4096)

    def summarize_content(self, text: str, max_length: int = 500) -> Optional[str]:
        """
        总结单个视频内容

        Args:
            text: 字幕文本
            max_length: 摘要最大长度

        Returns:
            内容摘要
        """
        prompt = f"""请用不超过{max_length}字总结这个视频的主要内容。

要求：
1. 提取核心观点
2. 保留关键信息
3. 语言简洁明了"""

        logger.info("开始内容总结")
        return self.analyze_text(text, prompt, max_tokens=1024)

    def comprehensive_analysis(self, texts: List[str], user_name: str = "该UP主") -> Dict[str, str]:
        """
        综合分析UP主的内容

        Args:
            texts: 字幕文本列表
            user_name: UP主名称

        Returns:
            包含多个维度分析结果的字典
        """
        logger.info(f"开始对{user_name}进行综合分析")

        results = {}

        # 思想分析
        logger.info("1/3 正在进行思想分析...")
        ideology = self.analyze_ideology(texts, user_name)
        if ideology:
            results["思想分析"] = ideology

        # 主题分析
        logger.info("2/3 正在进行主题分析...")
        themes = self.analyze_themes(texts)
        if themes:
            results["主题分析"] = themes

        # 风格分析
        logger.info("3/3 正在进行风格分析...")
        style = self.analyze_style(texts)
        if style:
            results["风格分析"] = style

        logger.info(f"综合分析完成，共生成 {len(results)} 个分析维度")
        return results

    def custom_analysis(self, texts: List[str], custom_prompt: str, max_tokens: int = 4096) -> Optional[str]:
        """
        自定义分析

        Args:
            texts: 字幕文本列表
            custom_prompt: 自定义提示词
            max_tokens: 最大返回token数

        Returns:
            分析结果
        """
        combined_text = "\n\n===\n\n".join(texts)
        logger.info(f"开始自定义分析，文本总长度: {len(combined_text)} 字符")
        return self.analyze_text(combined_text, custom_prompt, max_tokens)
