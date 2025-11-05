"""
语音识别模块
使用Whisper进行语音识别
"""

import whisper
from pathlib import Path
from typing import Optional, Union
from utils.logger import logger
from utils.error_handler import SpeechRecognitionError, handle_errors


class SpeechRecognizer:
    """语音识别器"""

    def __init__(self, model_name: str = "base", language: str = "zh"):
        """
        初始化语音识别器

        Args:
            model_name: Whisper模型名称 (tiny, base, small, medium, large)
            language: 识别语言代码
        """
        self.model_name = model_name
        self.language = language
        self.model = None

        logger.info(f"初始化语音识别器 (模型: {model_name}, 语言: {language})")

    def load_model(self):
        """加载Whisper模型"""
        if self.model is None:
            logger.info(f"加载Whisper模型: {self.model_name}")
            try:
                self.model = whisper.load_model(self.model_name)
                logger.info("模型加载完成")
            except Exception as e:
                raise SpeechRecognitionError(f"模型加载失败: {e}")

    @handle_errors(default_return=None, raise_error=True)
    def recognize_file(self, audio_file: Union[str, Path]) -> str:
        """
        识别音频文件

        Args:
            audio_file: 音频文件路径

        Returns:
            str: 识别的文本

        Raises:
            SpeechRecognitionError: 识别失败
        """
        self.load_model()

        audio_path = Path(audio_file)
        if not audio_path.exists():
            raise SpeechRecognitionError(f"音频文件不存在: {audio_file}")

        logger.info(f"识别音频文件: {audio_file}")

        try:
            # 使用Whisper进行转录
            result = self.model.transcribe(
                str(audio_path),
                language=self.language,
                verbose=False
            )

            text = result["text"].strip()
            logger.info(f"识别结果: {text}")

            return text

        except Exception as e:
            raise SpeechRecognitionError(f"语音识别失败: {e}")

    @handle_errors(default_return=None, raise_error=True)
    def recognize_audio_data(self, audio_data: bytes, sample_rate: int = 16000) -> str:
        """
        识别音频数据

        Args:
            audio_data: 音频数据（字节）
            sample_rate: 采样率

        Returns:
            str: 识别的文本

        Raises:
            SpeechRecognitionError: 识别失败
        """
        # 将音频数据保存到临时文件
        import tempfile
        import wave

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_path = tmp_file.name

            # 写入WAV文件
            with wave.open(tmp_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(sample_rate)
                wf.writeframes(audio_data)

        try:
            # 识别临时文件
            text = self.recognize_file(tmp_path)
            return text
        finally:
            # 删除临时文件
            Path(tmp_path).unlink(missing_ok=True)

    def get_model_info(self) -> dict:
        """
        获取模型信息

        Returns:
            dict: 模型信息
        """
        return {
            "model_name": self.model_name,
            "language": self.language,
            "loaded": self.model is not None
        }


# 使用示例
if __name__ == "__main__":
    import sys
    from pathlib import Path

    # 添加项目路径
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    print("🎤 Whisper语音识别测试\n")

    try:
        # 初始化识别器
        recognizer = SpeechRecognizer(model_name="base", language="zh")

        # 如果有测试音频文件，进行识别
        test_file = Path("tmp/test_recording.wav")
        if test_file.exists():
            print(f"识别文件: {test_file}")
            text = recognizer.recognize_file(test_file)
            print(f"\n识别结果: {text}\n")
        else:
            print(f"⚠️  未找到测试音频文件: {test_file}")
            print("请先运行 audio_capture.py 生成测试音频")

    except SpeechRecognitionError as e:
        print(f"\n❌ 识别错误: {e}")
    except Exception as e:
        print(f"\n❌ 未知错误: {e}")
        import traceback
        traceback.print_exc()
