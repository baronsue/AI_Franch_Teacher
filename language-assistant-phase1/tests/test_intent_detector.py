"""
测试意图检测器
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.intent_detector import IntentDetector, IntentType


def test_intent_detector():
    """测试意图检测功能"""
    detector = IntentDetector()

    test_cases = [
        ("请把'你好'翻译成法语", IntentType.TRANSLATION),
        ("bonjour怎么发音？", IntentType.PRONUNCIATION),
        ("tu和vous有什么区别？", IntentType.EXPLANATION),
        ("être是什么意思？", IntentType.VOCABULARY),
        ("今天天气真好", IntentType.CONVERSATION),
        ("如何学习法语？", IntentType.CONVERSATION),
    ]

    print("🧪 测试意图检测器\n")
    passed = 0
    total = len(test_cases)

    for text, expected_intent in test_cases:
        result = detector.analyze(text)
        detected_intent = result['intent']
        confidence = result['confidence']

        status = "✓" if detected_intent == expected_intent else "✗"
        print(f"{status} 输入: {text}")
        print(f"  预期: {expected_intent.value}")
        print(f"  检测: {detected_intent.value} (置信度: {confidence:.2f})")
        print()

        if detected_intent == expected_intent:
            passed += 1

    print(f"测试结果: {passed}/{total} 通过")
    return passed == total


if __name__ == "__main__":
    success = test_intent_detector()
    sys.exit(0 if success else 1)
