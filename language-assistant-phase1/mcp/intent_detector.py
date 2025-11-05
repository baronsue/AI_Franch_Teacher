"""
意图检测模块
识别用户输入的意图类型
"""

from enum import Enum
from typing import Dict, Optional
from utils.logger import logger


class IntentType(Enum):
    """意图类型枚举"""
    TRANSLATION = "translation"  # 翻译请求
    EXPLANATION = "explanation"  # 解释请求
    VOCABULARY = "vocabulary"    # 词汇查询
    PRONUNCIATION = "pronunciation"  # 发音请求
    CONVERSATION = "conversation"  # 一般对话


class IntentDetector:
    """意图检测器"""

    def __init__(self):
        """初始化意图检测器"""
        self.keywords = {
            IntentType.TRANSLATION: [
                "翻译", "translate", "怎么说", "法语是", "用法语",
                "français", "french"
            ],
            IntentType.EXPLANATION: [
                "解释", "explain", "为什么", "什么意思", "区别",
                "différence", "signification"
            ],
            IntentType.VOCABULARY: [
                "词汇", "单词", "vocabulary", "mot", "vocabulaire",
                "这个词", "那个词"
            ],
            IntentType.PRONUNCIATION: [
                "发音", "怎么读", "pronunciation", "prononciation",
                "读法", "音标"
            ]
        }
        logger.info("意图检测器初始化完成")

    def detect(self, text: str) -> IntentType:
        """
        检测文本的意图类型

        Args:
            text: 输入文本

        Returns:
            IntentType: 检测到的意图类型
        """
        text_lower = text.lower()

        # 检查每种意图的关键词
        for intent_type, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    logger.debug(f"检测到意图: {intent_type.value} (关键词: {keyword})")
                    return intent_type

        # 默认为一般对话
        logger.debug("未检测到特定意图，归类为一般对话")
        return IntentType.CONVERSATION

    def get_confidence(self, text: str, intent: IntentType) -> float:
        """
        计算意图置信度

        Args:
            text: 输入文本
            intent: 意图类型

        Returns:
            float: 置信度 (0-1)
        """
        if intent not in self.keywords:
            return 0.5

        text_lower = text.lower()
        keywords = self.keywords[intent]
        matches = sum(1 for keyword in keywords if keyword in text_lower)

        confidence = min(matches * 0.3, 1.0)
        return confidence

    def analyze(self, text: str) -> Dict:
        """
        分析文本并返回详细信息

        Args:
            text: 输入文本

        Returns:
            Dict: 包含意图类型和置信度的字典
        """
        intent = self.detect(text)
        confidence = self.get_confidence(text, intent)

        return {
            "intent": intent,
            "confidence": confidence,
            "text": text
        }


# 使用示例
if __name__ == "__main__":
    detector = IntentDetector()

    test_cases = [
        "请把'你好'翻译成法语",
        "bonjour怎么发音？",
        "tu和vous有什么区别？",
        "法语里的être是什么意思？",
        "今天天气真好"
    ]

    for text in test_cases:
        result = detector.analyze(text)
        print(f"输入: {text}")
        print(f"意图: {result['intent'].value}, 置信度: {result['confidence']:.2f}")
        print()
