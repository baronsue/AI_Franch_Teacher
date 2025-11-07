"""
语音合成模块
使用Edge-TTS进行文本转语音
"""

import asyncio
import edge_tts
from pathlib import Path
from typing import Optional
from utils.logger import logger
from utils.error_handler import SpeechSynthesisError, handle_errors
from speech.text_to_speech.voice_config import VoiceConfig


class SpeechSynthesizer:
    """语音合成器"""

    def __init__(
        self,
        chinese_voice: str = "xiaoxiao",
        french_voice: str = "denise",
        rate: str = "+0%",
        volume: str = "+0%"
    ):
        """
        初始化语音合成器

        Args:
            chinese_voice: 中文语音名称
            french_voice: 法语语音名称
            rate: 语速调整 (如: "+10%" 或 "-10%")
            volume: 音量调整 (如: "+10%" 或 "-10%")
        """
        self.chinese_voice = VoiceConfig.get_chinese_voice(chinese_voice)
        self.french_voice = VoiceConfig.get_french_voice(french_voice)
        self.rate = rate
        self.volume = volume

        logger.info(f"语音合成器初始化完成 (中文: {self.chinese_voice}, 法语: {self.french_voice})")

    def _detect_language(self, text: str) -> str:
        """
        检测文本语言

        Args:
            text: 文本内容

        Returns:
            str: 'chinese' 或 'french'
        """
        # 简单检测：如果包含中文字符，判断为中文
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return 'chinese'

        # 否则判断为法语
        return 'french'

    def _get_voice_for_language(self, language: str) -> str:
        """
        根据语言获取对应的语音

        Args:
            language: 语言类型

        Returns:
            str: 语音ID
        """
        if language == 'chinese':
            return self.chinese_voice
        else:
            return self.french_voice

    @handle_errors(default_return=False, raise_error=True)
    async def synthesize_async(
        self,
        text: str,
        output_file: str,
        language: Optional[str] = None
    ) -> bool:
        """
        异步合成语音

        Args:
            text: 要合成的文本
            output_file: 输出文件路径
            language: 语言类型（如果为None，自动检测）

        Returns:
            bool: 是否成功

        Raises:
            SpeechSynthesisError: 合成失败
        """
        if not text or not text.strip():
            raise SpeechSynthesisError("文本不能为空")

        # 检测语言
        if language is None:
            language = self._detect_language(text)

        # 获取对应语音
        voice = self._get_voice_for_language(language)

        logger.info(f"合成语音 (语言: {language}, 语音: {voice})")
        logger.debug(f"文本: {text[:50]}...")

        try:
            # 创建输出目录
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # 使用Edge-TTS合成
            communicate = edge_tts.Communicate(
                text,
                voice,
                rate=self.rate,
                volume=self.volume
            )

            await communicate.save(str(output_path))

            logger.info(f"语音已保存到: {output_file}")
            return True

        except Exception as e:
            raise SpeechSynthesisError(f"语音合成失败: {e}")

    def synthesize(
        self,
        text: str,
        output_file: str,
        language: Optional[str] = None
    ) -> bool:
        """
        同步合成语音（内部调用异步方法）

        Args:
            text: 要合成的文本
            output_file: 输出文件路径
            language: 语言类型（如果为None，自动检测）

        Returns:
            bool: 是否成功
        """
        # 修复事件循环问题：检查是否已有运行中的事件循环
        try:
            loop = asyncio.get_running_loop()
            # 如果已有事件循环，在新线程中运行
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    asyncio.run,
                    self.synthesize_async(text, output_file, language)
                )
                return future.result()
        except RuntimeError:
            # 没有运行中的事件循环，直接运行
            return asyncio.run(
                self.synthesize_async(text, output_file, language)
            )

    def synthesize_chinese(self, text: str, output_file: str) -> bool:
        """
        合成中文语音

        Args:
            text: 中文文本
            output_file: 输出文件路径

        Returns:
            bool: 是否成功
        """
        return self.synthesize(text, output_file, language='chinese')

    def synthesize_french(self, text: str, output_file: str) -> bool:
        """
        合成法语语音

        Args:
            text: 法语文本
            output_file: 输出文件路径

        Returns:
            bool: 是否成功
        """
        return self.synthesize(text, output_file, language='french')


# 使用示例
if __name__ == "__main__":
    import sys
    from pathlib import Path

    # 添加项目路径
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    print("🔊 Edge-TTS语音合成测试\n")

    try:
        synthesizer = SpeechSynthesizer()

        # 测试中文合成
        print("1. 合成中文语音...")
        chinese_text = "你好，我是AI法语学习助手。"
        chinese_file = "tmp/test_chinese.mp3"
        synthesizer.synthesize_chinese(chinese_text, chinese_file)
        print(f"   ✓ 已保存到: {chinese_file}\n")

        # 测试法语合成
        print("2. 合成法语语音...")
        french_text = "Bonjour, je suis votre assistant d'apprentissage du français."
        french_file = "tmp/test_french.mp3"
        synthesizer.synthesize_french(french_text, french_file)
        print(f"   ✓ 已保存到: {french_file}\n")

        # 测试自动检测
        print("3. 测试自动语言检测...")
        auto_text = "这是中文测试"
        auto_file = "tmp/test_auto.mp3"
        synthesizer.synthesize(auto_text, auto_file)
        print(f"   ✓ 已保存到: {auto_file}\n")

        print("✅ 所有测试完成！")

    except SpeechSynthesisError as e:
        print(f"\n❌ 合成错误: {e}")
    except Exception as e:
        print(f"\n❌ 未知错误: {e}")
        import traceback
        traceback.print_exc()
