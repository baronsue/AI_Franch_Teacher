"""
命令行界面模块
提供文本交互界面
"""

import sys
from typing import Optional
from utils.logger import logger
from mcp.intent_detector import IntentDetector
from mcp.conversation_manager import ConversationManager
from mcp.response_formatter import ResponseFormatter
from llm.api_client import LLMClient
from utils.error_handler import APIError


class CLIInterface:
    """命令行界面类"""

    def __init__(self):
        """初始化CLI界面"""
        self.intent_detector = IntentDetector()
        self.conversation_manager = ConversationManager(max_history=10)
        self.response_formatter = ResponseFormatter()
        self.llm_client = None

        try:
            self.llm_client = LLMClient()
        except Exception as e:
            logger.error(f"LLM客户端初始化失败: {e}")

        logger.info("CLI界面初始化完成")

    def print_welcome(self):
        """打印欢迎信息"""
        welcome = """
╔═══════════════════════════════════════════════════════════╗
║      AI French Language Assistant - Phase 1              ║
║      AI 法语学习助手 - 第一阶段                           ║
╚═══════════════════════════════════════════════════════════╝

欢迎使用AI法语学习助手！👋

我可以帮你：
✓ 中法互译
✓ 解释法语语法和词汇
✓ 提供发音指导
✓ 回答法语学习问题

输入 'quit' 或 'exit' 退出
输入 'clear' 清空对话历史
输入 'help' 查看帮助信息

让我们开始吧！ Commençons!
"""
        print(welcome)

    def print_help(self):
        """打印帮助信息"""
        help_text = """
📖 帮助信息:

基本命令:
  quit/exit  - 退出程序
  clear      - 清空对话历史
  help       - 显示此帮助信息
  stats      - 显示会话统计

使用示例:
  请把'你好'翻译成法语
  bonjour怎么发音？
  tu和vous有什么区别？
  法语的être动词怎么变位？

只需用中文自然地提问即可！
"""
        print(help_text)

    def print_stats(self):
        """打印统计信息"""
        stats = self.conversation_manager.get_stats()
        print(f"\n📊 会话统计:")
        print(f"  总消息数: {stats['total_messages']}")
        print(f"  用户消息: {stats['user_messages']}")
        print(f"  助手消息: {stats['assistant_messages']}")
        print(f"  会话时长: {stats['session_duration_seconds']:.1f}秒")
        print()

    def process_command(self, user_input: str) -> bool:
        """
        处理特殊命令

        Args:
            user_input: 用户输入

        Returns:
            bool: 如果是命令返回True，否则返回False
        """
        command = user_input.strip().lower()

        if command in ['quit', 'exit']:
            print("\n再见！Au revoir! 👋\n")
            return True

        if command == 'clear':
            self.conversation_manager.clear_history()
            print("\n✓ 对话历史已清空\n")
            return True

        if command == 'help':
            self.print_help()
            return True

        if command == 'stats':
            self.print_stats()
            return True

        return False

    def process_user_input(self, user_input: str) -> Optional[str]:
        """
        处理用户输入

        Args:
            user_input: 用户输入

        Returns:
            Optional[str]: 助手响应
        """
        if not self.llm_client:
            return "❌ LLM客户端未初始化，请检查配置"

        try:
            # 检测意图
            intent_result = self.intent_detector.analyze(user_input)
            intent_type = intent_result['intent'].value

            logger.debug(f"检测到意图: {intent_type}")

            # 添加用户消息到历史
            self.conversation_manager.add_user_message(user_input)

            # 获取对话历史
            history = self.conversation_manager.get_formatted_history(limit=5)

            # 调用LLM
            response = self.llm_client.chat(
                user_input,
                intent_type=intent_type,
                history=history[:-1]  # 排除刚添加的用户消息
            )

            # 添加助手消息到历史
            self.conversation_manager.add_assistant_message(response)

            # 格式化响应
            formatted_response = self.response_formatter.format_with_intent(
                response,
                intent_type
            )

            return formatted_response

        except APIError as e:
            error_msg = f"API调用失败: {e}"
            logger.error(error_msg)
            return self.response_formatter.format_error(error_msg)

        except Exception as e:
            error_msg = f"处理请求时出错: {e}"
            logger.error(error_msg, exc_info=True)
            return self.response_formatter.format_error(error_msg)

    def run(self):
        """运行CLI界面"""
        self.print_welcome()

        while True:
            try:
                # 获取用户输入
                user_input = input("\n您: ").strip()

                # 跳过空输入
                if not user_input:
                    continue

                # 处理命令
                if self.process_command(user_input):
                    if user_input.lower() in ['quit', 'exit']:
                        break
                    continue

                # 处理正常输入
                response = self.process_user_input(user_input)

                if response:
                    print(f"\n助手: {response}")

            except KeyboardInterrupt:
                print("\n\n再见！Au revoir! 👋\n")
                break

            except EOFError:
                break

            except Exception as e:
                logger.error(f"运行时错误: {e}", exc_info=True)
                print(f"\n❌ 发生错误: {e}\n")


# 独立运行测试
if __name__ == "__main__":
    interface = CLIInterface()
    interface.run()
