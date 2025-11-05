"""
错误处理工具
"""

import functools
from typing import Callable, Any
from utils.logger import logger


class APIError(Exception):
    """API调用错误"""
    pass


class SpeechRecognitionError(Exception):
    """语音识别错误"""
    pass


class SpeechSynthesisError(Exception):
    """语音合成错误"""
    pass


class ConfigurationError(Exception):
    """配置错误"""
    pass


def handle_errors(default_return=None, raise_error=False):
    """
    错误处理装饰器

    Args:
        default_return: 出错时的默认返回值
        raise_error: 是否重新抛出异常

    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{func.__name__} 执行失败: {e}", exc_info=True)
                if raise_error:
                    raise
                return default_return
        return wrapper
    return decorator


def retry(max_attempts=3, delay=1.0):
    """
    重试装饰器

    Args:
        max_attempts: 最大重试次数
        delay: 重试延迟（秒）

    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            import time

            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"{func.__name__} 第 {attempt + 1}/{max_attempts} 次尝试失败: {e}"
                    )
                    if attempt < max_attempts - 1:
                        time.sleep(delay)

            logger.error(f"{func.__name__} 重试 {max_attempts} 次后仍然失败")
            raise last_exception

        return wrapper
    return decorator
