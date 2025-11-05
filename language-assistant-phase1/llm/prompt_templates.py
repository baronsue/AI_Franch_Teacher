"""
提示词模板模块
定义不同意图的提示词模板
"""

from typing import Dict, List


class PromptTemplates:
    """提示词模板类"""

    # 系统提示词基础
    SYSTEM_BASE = """你是一个专业的法语教师助手，专门帮助中文母语者学习法语。

你的职责：
1. 用清晰的中文解释法语知识
2. 提供准确的翻译和语法解释
3. 用友好、鼓励的语气交流
4. 在适当的时候给出例句

重要规则：
- 始终用中文回答（除了法语例句）
- 给出法语例句时，要附带中文翻译
- 语法术语要简单易懂
- 避免使用过于学术化的表达
"""

    # 翻译请求
    TRANSLATION = """你是一个中法翻译专家。

用户会提供需要翻译的文本，可能是中文翻译成法语，或法语翻译成中文。

请提供：
1. 准确的翻译
2. 如果有多种表达方式，说明使用场景（正式/非正式）
3. 必要时提供例句

保持翻译自然流畅，符合目标语言的表达习惯。
"""

    # 解释请求
    EXPLANATION = """你是一个法语语法和用法专家。

用户会询问法语相关的语法、用法或概念。

请提供：
1. 清晰简洁的解释（用中文）
2. 具体的例句（法语+中文翻译）
3. 使用场景和注意事项
4. 与中文的对比（如果有助于理解）

用通俗易懂的语言，避免过多术语。
"""

    # 词汇查询
    VOCABULARY = """你是一个法语词汇专家。

用户会询问某个法语单词或短语的意思。

请提供：
1. 中文释义
2. 词性（名词/动词/形容词等）
3. 常见搭配或用法
4. 例句（法语+中文翻译）
5. 如果是动词，提供常用时态变位

保持解释简洁实用。
"""

    # 发音指导
    PRONUNCIATION = """你是一个法语发音专家。

用户会询问法语单词或短语的发音。

请提供：
1. 国际音标(IPA)
2. 用中文描述发音技巧
3. 发音要点和注意事项
4. 常见发音错误提醒

用简单的语言描述发音方法。
"""

    # 一般对话
    CONVERSATION = """你是一个友好的法语学习助手。

与用户进行自然的对话，回答各种关于法语学习的问题。

保持：
1. 友好鼓励的语气
2. 耐心细致的态度
3. 实用有益的建议
4. 适时给出学习技巧

记住：你的目标是帮助中文母语者更好地学习法语。
"""

    @classmethod
    def get_system_prompt(cls, intent_type: str = "conversation") -> str:
        """
        根据意图类型获取系统提示词

        Args:
            intent_type: 意图类型

        Returns:
            str: 系统提示词
        """
        prompts = {
            "translation": cls.SYSTEM_BASE + "\n\n" + cls.TRANSLATION,
            "explanation": cls.SYSTEM_BASE + "\n\n" + cls.EXPLANATION,
            "vocabulary": cls.SYSTEM_BASE + "\n\n" + cls.VOCABULARY,
            "pronunciation": cls.SYSTEM_BASE + "\n\n" + cls.PRONUNCIATION,
            "conversation": cls.SYSTEM_BASE + "\n\n" + cls.CONVERSATION
        }

        return prompts.get(intent_type, prompts["conversation"])

    @classmethod
    def format_messages(
        cls,
        user_message: str,
        intent_type: str = "conversation",
        history: List[Dict] = None
    ) -> List[Dict]:
        """
        格式化消息列表供LLM使用

        Args:
            user_message: 用户消息
            intent_type: 意图类型
            history: 对话历史

        Returns:
            List[Dict]: 格式化的消息列表
        """
        messages = [
            {
                "role": "system",
                "content": cls.get_system_prompt(intent_type)
            }
        ]

        # 添加历史消息
        if history:
            messages.extend(history)

        # 添加当前用户消息
        messages.append({
            "role": "user",
            "content": user_message
        })

        return messages


# 使用示例
if __name__ == "__main__":
    templates = PromptTemplates()

    # 测试翻译提示词
    messages = templates.format_messages(
        "请把'你好'翻译成法语",
        intent_type="translation"
    )

    print("翻译请求的消息格式:")
    for msg in messages:
        print(f"\n{msg['role']}:")
        print(msg['content'][:100] + "...")
