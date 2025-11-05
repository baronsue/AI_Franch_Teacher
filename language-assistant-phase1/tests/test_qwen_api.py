"""
测试Qwen API连接
运行此测试前，请确保已配置.env文件中的API密钥
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm.api_client import LLMClient
from utils.error_handler import APIError


def test_qwen_api():
    """测试Qwen API基本功能"""
    print("🧪 测试Qwen API连接\n")

    try:
        # 初始化客户端
        print("1. 初始化LLM客户端...")
        client = LLMClient()
        print("  ✓ 客户端初始化成功\n")

        # 测试简单对话
        print("2. 测试简单对话...")
        response = client.chat(
            "你好，请用一句话介绍你自己。",
            intent_type="conversation"
        )
        print(f"  响应: {response[:100]}...")
        print("  ✓ 对话测试成功\n")

        # 测试翻译
        print("3. 测试翻译功能...")
        response = client.chat(
            "请把'你好'翻译成法语",
            intent_type="translation"
        )
        print(f"  响应: {response}")
        assert "bonjour" in response.lower(), "翻译响应应该包含'bonjour'"
        print("  ✓ 翻译测试成功\n")

        # 测试解释
        print("4. 测试解释功能...")
        response = client.chat(
            "tu和vous有什么区别？",
            intent_type="explanation"
        )
        print(f"  响应: {response[:100]}...")
        print("  ✓ 解释测试成功\n")

        print("✅ 所有API测试通过！")
        print("\n📝 注意: 如果上述测试都通过，说明Qwen API配置正确。")
        return True

    except APIError as e:
        print(f"\n❌ API测试失败: {e}")
        print("\n💡 请检查:")
        print("  1. .env文件是否存在")
        print("  2. QWEN_API_KEY是否正确配置")
        print("  3. 网络连接是否正常")
        print("  4. API配额是否充足")
        return False

    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_qwen_api()
    sys.exit(0 if success else 1)
