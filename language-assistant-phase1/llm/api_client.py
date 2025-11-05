"""
LLM API客户端模块
处理与Qwen API的通信
"""

import requests
from typing import List, Dict, Optional
from utils.logger import logger
from utils.error_handler import APIError, retry, handle_errors
from llm.config import llm_config
from llm.prompt_templates import PromptTemplates


class LLMClient:
    """LLM API客户端"""

    def __init__(self):
        """初始化客户端"""
        if not llm_config:
            raise APIError("LLM配置未正确加载")

        self.api_key = llm_config.api_key
        self.api_url = llm_config.api_url
        self.model = llm_config.model
        self.temperature = llm_config.temperature
        self.max_tokens = llm_config.max_tokens

        logger.info(f"LLM客户端初始化完成 (模型: {self.model})")

    @retry(max_attempts=3, delay=1.0)
    def _make_request(self, messages: List[Dict]) -> Dict:
        """
        发送API请求

        Args:
            messages: 消息列表

        Returns:
            Dict: API响应

        Raises:
            APIError: API调用失败
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "input": {
                "messages": messages
            },
            "parameters": {
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
        }

        try:
            logger.debug(f"发送API请求: {len(messages)} 条消息")
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            logger.debug("API请求成功")
            return result

        except requests.exceptions.Timeout:
            raise APIError("API请求超时")
        except requests.exceptions.RequestException as e:
            raise APIError(f"API请求失败: {e}")
        except Exception as e:
            raise APIError(f"未知错误: {e}")

    def _extract_response(self, api_response: Dict) -> str:
        """
        从API响应中提取文本

        Args:
            api_response: API响应

        Returns:
            str: 提取的文本内容
        """
        try:
            # Qwen API响应格式
            output = api_response.get("output", {})
            text = output.get("text", "")

            if not text:
                raise APIError("API响应中未找到文本内容")

            return text.strip()

        except Exception as e:
            logger.error(f"解析API响应失败: {e}")
            raise APIError("解析API响应失败")

    @handle_errors(default_return=None, raise_error=True)
    def chat(
        self,
        user_message: str,
        intent_type: str = "conversation",
        history: Optional[List[Dict]] = None
    ) -> str:
        """
        与LLM对话

        Args:
            user_message: 用户消息
            intent_type: 意图类型
            history: 对话历史

        Returns:
            str: LLM的响应

        Raises:
            APIError: API调用失败
        """
        # 格式化消息
        messages = PromptTemplates.format_messages(
            user_message,
            intent_type,
            history
        )

        # 发送请求
        api_response = self._make_request(messages)

        # 提取响应
        response_text = self._extract_response(api_response)

        logger.info(f"LLM响应: {response_text[:100]}...")
        return response_text

    def chat_stream(self, user_message: str, intent_type: str = "conversation"):
        """
        流式对话（未来实现）

        Args:
            user_message: 用户消息
            intent_type: 意图类型

        Yields:
            str: 响应片段
        """
        # TODO: 实现流式响应
        raise NotImplementedError("流式响应功能尚未实现")


# 使用示例
if __name__ == "__main__":
    try:
        client = LLMClient()

        # 测试翻译
        response = client.chat(
            "请把'你好'翻译成法语",
            intent_type="translation"
        )
        print("翻译响应:")
        print(response)

    except APIError as e:
        print(f"错误: {e}")
