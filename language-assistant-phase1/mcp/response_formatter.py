"""
响应格式化模块
格式化和美化AI响应
"""

from typing import Dict, Optional
from utils.logger import logger


class ResponseFormatter:
    """响应格式化器"""

    def __init__(self):
        """初始化响应格式化器"""
        logger.info("响应格式化器初始化完成")

    def format_translation(self, response: str) -> str:
        """
        格式化翻译响应

        Args:
            response: 原始响应

        Returns:
            str: 格式化后的响应
        """
        return f"📝 翻译结果:\n{response}"

    def format_explanation(self, response: str) -> str:
        """
        格式化解释响应

        Args:
            response: 原始响应

        Returns:
            str: 格式化后的响应
        """
        return f"💡 解释:\n{response}"

    def format_vocabulary(self, response: str) -> str:
        """
        格式化词汇响应

        Args:
            response: 原始响应

        Returns:
            str: 格式化后的响应
        """
        return f"📚 词汇信息:\n{response}"

    def format_pronunciation(self, response: str) -> str:
        """
        格式化发音响应

        Args:
            response: 原始响应

        Returns:
            str: 格式化后的响应
        """
        return f"🔊 发音指导:\n{response}"

    def format_conversation(self, response: str) -> str:
        """
        格式化一般对话响应

        Args:
            response: 原始响应

        Returns:
            str: 格式化后的响应
        """
        return f"💬 {response}"

    def format_error(self, error_message: str) -> str:
        """
        格式化错误消息

        Args:
            error_message: 错误消息

        Returns:
            str: 格式化后的错误消息
        """
        return f"❌ 错误: {error_message}"

    def format_with_intent(self, response: str, intent_type: str) -> str:
        """
        根据意图类型格式化响应

        Args:
            response: 原始响应
            intent_type: 意图类型

        Returns:
            str: 格式化后的响应
        """
        formatters = {
            "translation": self.format_translation,
            "explanation": self.format_explanation,
            "vocabulary": self.format_vocabulary,
            "pronunciation": self.format_pronunciation,
            "conversation": self.format_conversation
        }

        formatter = formatters.get(intent_type, self.format_conversation)
        return formatter(response)

    def add_metadata(self, response: str, metadata: Optional[Dict] = None) -> Dict:
        """
        为响应添加元数据

        Args:
            response: 响应内容
            metadata: 额外的元数据

        Returns:
            Dict: 包含响应和元数据的字典
        """
        result = {
            "content": response,
            "formatted": True
        }

        if metadata:
            result.update(metadata)

        return result


# 使用示例
if __name__ == "__main__":
    formatter = ResponseFormatter()

    # 测试各种格式化
    print(formatter.format_translation("'Bonjour'在中文中是'你好'的意思。"))
    print()
    print(formatter.format_explanation("'Tu'用于非正式场合，'vous'用于正式场合。"))
    print()
    print(formatter.format_error("API调用失败，请检查网络连接。"))
