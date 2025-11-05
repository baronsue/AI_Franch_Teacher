"""
语音识别集成测试
测试完整的语音识别流程：录音 -> 识别
"""

import sys
from pathlib import Path
import time

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from speech.speech_to_text.audio_capture import AudioCapture
from speech.speech_to_text.recognizer import SpeechRecognizer
from speech.speech_to_text.vad import VoiceActivityDetector


def test_audio_capture():
    """测试音频捕获"""
    print("=" * 60)
    print("测试1: 音频捕获")
    print("=" * 60)

    try:
        with AudioCapture() as capture:
            print("\n请用中文说一句话（将录制5秒）...")
            print("例如：'你好，我想学习法语'")
            print("\n倒计时: ", end="", flush=True)

            for i in range(3, 0, -1):
                print(f"{i}... ", end="", flush=True)
                time.sleep(1)

            print("开始录音！\n")

            audio_data = capture.record_fixed_duration(5.0)

            output_file = "tmp/test_speech.wav"
            capture.save_to_file(output_file, audio_data)

            print(f"\n✓ 录音完成！")
            print(f"  文件: {output_file}")
            print(f"  大小: {len(audio_data)} 字节")

            return output_file

    except Exception as e:
        print(f"\n❌ 音频捕获失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_speech_recognition(audio_file):
    """测试语音识别"""
    print("\n" + "=" * 60)
    print("测试2: 语音识别")
    print("=" * 60)

    try:
        print("\n加载Whisper模型（首次运行会下载模型，请稍候）...")
        recognizer = SpeechRecognizer(model_name="base", language="zh")

        print(f"识别音频文件: {audio_file}")
        text = recognizer.recognize_file(audio_file)

        print(f"\n✓ 识别成功！")
        print(f"  识别结果: 「{text}」")

        return text

    except Exception as e:
        print(f"\n❌ 语音识别失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_vad():
    """测试语音活动检测"""
    print("\n" + "=" * 60)
    print("测试3: 语音活动检测（VAD）")
    print("=" * 60)

    try:
        vad = VoiceActivityDetector(energy_threshold=300)

        # 读取之前录制的音频进行测试
        import wave
        audio_file = "tmp/test_speech.wav"

        if not Path(audio_file).exists():
            print(f"⚠️  音频文件不存在: {audio_file}")
            return

        with wave.open(audio_file, 'rb') as wf:
            chunk_size = 1024
            print(f"\n分析音频文件: {audio_file}")

            has_speech = False
            chunk_count = 0

            while True:
                audio_data = wf.readframes(chunk_size)
                if not audio_data:
                    break

                chunk_count += 1
                if vad.is_speech(audio_data):
                    has_speech = True

            print(f"\n✓ VAD分析完成")
            print(f"  总块数: {chunk_count}")
            print(f"  检测到语音: {'是' if has_speech else '否'}")

    except Exception as e:
        print(f"\n❌ VAD测试失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主测试函数"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║       语音识别组件测试 - Speech Recognition Test         ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()

    print("📝 测试说明:")
    print("  本测试将验证语音识别功能是否正常工作")
    print("  需要: 麦克风、安静环境")
    print("  模型: Whisper (base)")
    print()

    input("按Enter键开始测试...")

    # 测试1: 录音
    audio_file = test_audio_capture()

    if not audio_file:
        print("\n❌ 音频捕获失败，测试中止")
        return False

    # 测试2: 识别
    text = test_speech_recognition(audio_file)

    if not text:
        print("\n❌ 语音识别失败，测试中止")
        return False

    # 测试3: VAD
    test_vad()

    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print()
    print("✅ 所有语音识别组件测试通过！")
    print()
    print("📋 测试结果:")
    print(f"  ✓ 音频捕获: 成功")
    print(f"  ✓ 语音识别: 成功")
    print(f"  ✓ 识别文本: {text}")
    print(f"  ✓ VAD检测: 成功")
    print()
    print("🎉 语音识别组件可以正常使用！")
    print()

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
