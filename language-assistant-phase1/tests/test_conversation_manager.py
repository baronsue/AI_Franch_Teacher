"""
测试对话管理器
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.conversation_manager import ConversationManager


def test_conversation_manager():
    """测试对话管理功能"""
    print("🧪 测试对话管理器\n")

    manager = ConversationManager(max_history=5)

    # 测试添加消息
    print("1. 测试添加消息")
    manager.add_user_message("你好")
    manager.add_assistant_message("您好！我是AI法语学习助手。")
    manager.add_user_message("请翻译'bonjour'")
    manager.add_assistant_message("'Bonjour'的中文意思是'你好'。")

    assert len(manager) == 4, "消息数量应该是4"
    print("  ✓ 添加消息功能正常\n")

    # 测试获取历史
    print("2. 测试获取历史")
    history = manager.get_history()
    assert len(history) == 4, "历史记录应该有4条消息"
    print("  ✓ 获取历史功能正常\n")

    # 测试格式化历史
    print("3. 测试格式化历史")
    formatted = manager.get_formatted_history()
    assert all('role' in msg and 'content' in msg for msg in formatted), \
        "格式化消息应该包含role和content"
    print("  ✓ 格式化历史功能正常\n")

    # 测试上下文窗口
    print("4. 测试上下文窗口")
    context = manager.get_context_window(window_size=2)
    assert len(context) == 2, "上下文窗口应该返回最近2条消息"
    print("  ✓ 上下文窗口功能正常\n")

    # 测试统计信息
    print("5. 测试统计信息")
    stats = manager.get_stats()
    assert stats['total_messages'] == 4, "总消息数应该是4"
    assert stats['user_messages'] == 2, "用户消息数应该是2"
    assert stats['assistant_messages'] == 2, "助手消息数应该是2"
    print("  ✓ 统计信息功能正常\n")

    # 测试清空历史
    print("6. 测试清空历史")
    manager.clear_history()
    assert len(manager) == 0, "清空后应该没有消息"
    print("  ✓ 清空历史功能正常\n")

    print("✅ 所有测试通过！")
    return True


if __name__ == "__main__":
    success = test_conversation_manager()
    sys.exit(0 if success else 1)
