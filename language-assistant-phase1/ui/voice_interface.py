"""
语音交互界面模块
提供语音输入输出界面
"""

import sys
import tempfile
from pathlib import Path
from typing import Optional
from utils.logger import logger
from mcp.intent_detector import IntentDetector
from mcp.conversation_manager import ConversationManager
from mcp.response_formatter import ResponseFormatter
from llm.api_client import LLMClient
from speech.speech_to_text.audio_capture import AudioCapture
from speech.speech_to_text.recognizer import SpeechRecognizer
from speech.speech_to_text.vad import VoiceActivityDetector
from speech.text_to_speech.synthesizer import SpeechSynthesizer
from speech.text_to_speech.audio_player import AudioPlayer
from utils.error_handler import APIError, SpeechRecognitionError, SpeechSynthesisError


class VoiceInterface:
    """语音交互界面类"""

    def __init__(self):
        """初始化语音界面"""
        logger.info("初始化语音界面...")

        # 核心组件
        self.intent_detector = IntentDetector()
        self.conversation_manager = ConversationManager(max_history=10)
        self.response_formatter = ResponseFormatter()

        # LLM客户端
        self.llm_client = None
        try:
            self.llm_client = LLMClient()
        except Exception as e:
            logger.error(f"LLM客户端初始化失败: {e}")

        # 语音组件
        self.audio_capture = None
        self.speech_recognizer = None
        self.vad = None
        self.speech_synthesizer = None
        self.audio_player = None

        self._init_speech_components()

        logger.info("语音界面初始化完成")

    def _init_speech_components(self):
        """初始化语音组件"""
        try:
            # 语音识别
            self.audio_capture = AudioCapture()
            self.speech_recognizer = SpeechRecognizer(model_name="base", language="zh")
            self.vad = VoiceActivityDetector(energy_threshold=300, silence_threshold=1.0)

            # 语音合成
            self.speech_synthesizer = SpeechSynthesizer()
            self.audio_player = AudioPlayer()

            logger.info("语音组件初始化成功")

        except Exception as e:
            logger.error(f"语音组件初始化失败: {e}")
            print(f"\n⚠️  警告: 语音组件初始化失败: {e}")
            print("将回退到命令行模式\n")

    def print_welcome(self):
        """打印欢迎信息"""
        welcome = """
╔═══════════════════════════════════════════════════════════╗
║   AI French Language Assistant - Voice Mode              ║
║   AI 法语学习助手 - 语音模式                             ║
╚═══════════════════════════════════════════════════════════╝

欢迎使用AI法语学习助手（语音模式）！🎤

语音交互说明：
✓ 按 Enter 键开始录音
✓ 说话时系统会自动检测
✓ 停止说话后会自动识别并回复
✓ AI的回复会自动播放语音

文本命令：
• 输入 'quit' 或 'exit' 退出
• 输入 'help' 查看帮助
• 输入 'text' 切换到文本输入模式

让我们开始吧！ Commençons!
"""
        print(welcome)

    def record_with_vad(self, max_duration: float = 10.0) -> Optional[bytes]:
        """
        使用VAD录制语音

        Args:
            max_duration: 最大录制时长（秒）

        Returns:
            Optional[bytes]: 音频数据
        """
        try:
            self.audio_capture.start_recording()
            self.vad.reset()

            chunk_duration = self.audio_capture.chunk_size / self.audio_capture.sample_rate
            max_chunks = int(max_duration / chunk_duration)

            print("🎤 正在录音... (停止说话后会自动结束)")

            for _ in range(max_chunks):
                chunk = self.audio_capture.record_chunk()

                # 检测是否应该停止
                if self.vad.detect_silence_end(chunk, chunk_duration):
                    break

            audio_data = self.audio_capture.stop_recording()
            print("✓ 录音完成")

            return audio_data

        except Exception as e:
            logger.error(f"录音失败: {e}")
            print(f"❌ 录音失败: {e}")
            return None

    def recognize_speech(self, audio_data: bytes) -> Optional[str]:
        """
        识别语音

        Args:
            audio_data: 音频数据

        Returns:
            Optional[str]: 识别的文本
        """
        try:
            print("🔍 正在识别...")
            text = self.speech_recognizer.recognize_audio_data(audio_data)

            if text:
                print(f"您说: {text}")
                return text
            else:
                print("⚠️  未识别到内容")
                return None

        except SpeechRecognitionError as e:
            logger.error(f"语音识别失败: {e}")
            print(f"❌ 识别失败: {e}")
            return None

    def process_input(self, user_input: str) -> Optional[str]:
        """
        处理用户输入

        Args:
            user_input: 用户输入文本

        Returns:
            Optional[str]: 助手响应
        """
        if not self.llm_client:
            return "❌ LLM客户端未初始化，请检查配置"

        try:
            # 检测意图
            intent_result = self.intent_detector.analyze(user_input)
            intent_type = intent_result['intent'].value

            # 添加到历史
            self.conversation_manager.add_user_message(user_input)

            # 获取历史
            history = self.conversation_manager.get_formatted_history(limit=5)

            # 调用LLM
            response = self.llm_client.chat(
                user_input,
                intent_type=intent_type,
                history=history[:-1]
            )

            # 添加到历史
            self.conversation_manager.add_assistant_message(response)

            return response

        except APIError as e:
            logger.error(f"API调用失败: {e}")
            return f"API调用失败: {e}"
        except Exception as e:
            logger.error(f"处理失败: {e}", exc_info=True)
            return f"处理失败: {e}"

    def speak_response(self, text: str) -> bool:
        """
        播放语音响应

        Args:
            text: 要播放的文本

        Returns:
            bool: 是否成功
        """
        try:
            # 生成临时文件
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                output_file = tmp_file.name

            # 合成语音
            print("🔊 正在合成语音...")
            success = self.speech_synthesizer.synthesize(text, output_file)

            if not success:
                return False

            # 播放语音
            print("📢 正在播放...")
            self.audio_player.play(output_file)

            # 清理临时文件
            Path(output_file).unlink(missing_ok=True)

            return True

        except SpeechSynthesisError as e:
            logger.error(f"语音合成失败: {e}")
            print(f"❌ 语音合成失败: {e}")
            return False
        except Exception as e:
            logger.error(f"播放失败: {e}")
            print(f"❌ 播放失败: {e}")
            return False

    def handle_voice_interaction(self):
        """处理一轮语音交互"""
        # 录音
        audio_data = self.record_with_vad()
        if not audio_data:
            return

        # 识别
        text = self.recognize_speech(audio_data)
        if not text:
            return

        # 处理
        print("\n💭 正在思考...")
        response = self.process_input(text)

        if response:
            print(f"\n助手: {response}\n")

            # 播放语音
            self.speak_response(response)

    def run(self):
        """运行语音界面"""
        # 检查语音组件
        if not all([self.audio_capture, self.speech_recognizer,
                   self.speech_synthesizer, self.audio_player]):
            print("\n⚠️  语音组件未完全初始化")
            print("回退到CLI模式...\n")
            from ui.cli_interface import CLIInterface
            cli = CLIInterface()
            cli.run()
            return

        self.print_welcome()

        text_mode = False

        while True:
            try:
                if text_mode:
                    # 文本输入模式
                    user_input = input("\n您 (文本): ").strip()

                    if not user_input:
                        continue

                    if user_input.lower() == 'voice':
                        text_mode = False
                        print("\n✓ 已切换到语音模式\n")
                        continue

                    if user_input.lower() in ['quit', 'exit']:
                        break

                    if user_input.lower() == 'help':
                        print("\n输入 'voice' 切换回语音模式")
                        print("输入 'quit' 退出\n")
                        continue

                    # 处理文本输入
                    print("\n💭 正在思考...")
                    response = self.process_input(user_input)

                    if response:
                        print(f"\n助手: {response}\n")

                else:
                    # 语音输入模式
                    command = input("\n按 Enter 开始录音 (或输入命令): ").strip().lower()

                    if command == 'quit' or command == 'exit':
                        break
                    elif command == 'help':
                        print("\n帮助:")
                        print("  Enter - 开始录音")
                        print("  text  - 切换到文本模式")
                        print("  quit  - 退出\n")
                        continue
                    elif command == 'text':
                        text_mode = True
                        print("\n✓ 已切换到文本模式\n")
                        continue
                    elif command:
                        # 作为文本命令处理
                        response = self.process_input(command)
                        if response:
                            print(f"\n助手: {response}\n")
                        continue

                    # 语音交互
                    self.handle_voice_interaction()

            except KeyboardInterrupt:
                print("\n\n再见！Au revoir! 👋\n")
                break
            except Exception as e:
                logger.error(f"运行时错误: {e}", exc_info=True)
                print(f"\n❌ 错误: {e}\n")

        # 清理
        if self.audio_capture:
            self.audio_capture.cleanup()


# 独立运行测试
if __name__ == "__main__":
    interface = VoiceInterface()
    interface.run()
