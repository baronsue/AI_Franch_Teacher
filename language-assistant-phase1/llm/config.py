"""
LLM配置模块
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from utils.logger import logger
from utils.error_handler import ConfigurationError

# 加载环境变量
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class LLMConfig:
    """LLM配置类"""

    def __init__(self):
        """初始化配置"""
        # API配置
        self.api_key = os.getenv("QWEN_API_KEY")
        self.api_url = os.getenv(
            "QWEN_API_URL",
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        )

        # 模型配置
        self.model = os.getenv("LLM_MODEL", "qwen-turbo")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "2000"))

        # 验证配置
        self._validate()

        logger.info("LLM配置加载完成")

    def _validate(self):
        """验证配置"""
        if not self.api_key:
            raise ConfigurationError(
                "未找到QWEN_API_KEY，请在.env文件中配置"
            )

        if not self.api_url:
            raise ConfigurationError(
                "未找到QWEN_API_URL，请在.env文件中配置"
            )

    def to_dict(self):
        """转换为字典"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "api_url": self.api_url
        }


# 创建全局配置实例
try:
    llm_config = LLMConfig()
except ConfigurationError as e:
    logger.error(f"配置加载失败: {e}")
    llm_config = None
