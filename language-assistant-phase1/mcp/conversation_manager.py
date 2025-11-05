"""
对话管理模块
管理对话历史和上下文
"""

from typing import List, Dict, Optional
from datetime import datetime
from collections import deque
from utils.logger import logger


class Message:
    """消息类"""

    def __init__(self, role: str, content: str, timestamp: Optional[datetime] = None):
        """
        初始化消息

        Args:
            role: 角色 ('user' 或 'assistant')
            content: 消息内容
            timestamp: 时间戳
        """
        self.role = role
        self.content = content
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }

    def __repr__(self):
        return f"Message(role={self.role}, content={self.content[:30]}...)"


class ConversationManager:
    """对话管理器"""

    def __init__(self, max_history: int = 10):
        """
        初始化对话管理器

        Args:
            max_history: 最大保留的历史消息数
        """
        self.max_history = max_history
        self.messages = deque(maxlen=max_history)
        self.session_start = datetime.now()
        logger.info(f"对话管理器初始化完成 (最大历史: {max_history})")

    def add_message(self, role: str, content: str) -> Message:
        """
        添加消息到历史记录

        Args:
            role: 角色 ('user' 或 'assistant')
            content: 消息内容

        Returns:
            Message: 创建的消息对象
        """
        message = Message(role, content)
        self.messages.append(message)
        logger.debug(f"添加消息: {role} - {content[:50]}...")
        return message

    def add_user_message(self, content: str) -> Message:
        """添加用户消息"""
        return self.add_message("user", content)

    def add_assistant_message(self, content: str) -> Message:
        """添加助手消息"""
        return self.add_message("assistant", content)

    def get_history(self, limit: Optional[int] = None) -> List[Message]:
        """
        获取对话历史

        Args:
            limit: 限制返回的消息数量

        Returns:
            List[Message]: 消息列表
        """
        if limit:
            return list(self.messages)[-limit:]
        return list(self.messages)

    def get_formatted_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        获取格式化的对话历史（用于LLM API）

        Args:
            limit: 限制返回的消息数量

        Returns:
            List[Dict]: 格式化的消息列表
        """
        messages = self.get_history(limit)
        return [{"role": msg.role, "content": msg.content} for msg in messages]

    def get_context_window(self, window_size: int = 5) -> List[Message]:
        """
        获取最近的上下文窗口

        Args:
            window_size: 窗口大小

        Returns:
            List[Message]: 最近的消息列表
        """
        return list(self.messages)[-window_size:]

    def clear_history(self):
        """清空对话历史"""
        self.messages.clear()
        self.session_start = datetime.now()
        logger.info("对话历史已清空")

    def get_stats(self) -> Dict:
        """
        获取对话统计信息

        Returns:
            Dict: 统计信息
        """
        user_messages = sum(1 for msg in self.messages if msg.role == "user")
        assistant_messages = sum(1 for msg in self.messages if msg.role == "assistant")
        duration = (datetime.now() - self.session_start).total_seconds()

        return {
            "total_messages": len(self.messages),
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "session_duration_seconds": duration,
            "session_start": self.session_start.isoformat()
        }

    def __len__(self):
        """返回消息数量"""
        return len(self.messages)

    def __repr__(self):
        return f"ConversationManager(messages={len(self.messages)}, max_history={self.max_history})"


# 使用示例
if __name__ == "__main__":
    manager = ConversationManager(max_history=5)

    # 模拟对话
    manager.add_user_message("你好，请把'bonjour'翻译成中文")
    manager.add_assistant_message("'Bonjour'在中文中是'你好'的意思。")
    manager.add_user_message("它怎么发音？")
    manager.add_assistant_message("'Bonjour'的发音是[bɔ̃ʒuʁ]，让我为你播放...")

    print("对话历史:")
    for msg in manager.get_history():
        print(f"{msg.role}: {msg.content}")

    print("\n统计信息:")
    print(manager.get_stats())
