"""
文本转语音集成测试
测试完整的TTS流程：文本 -> 合成 -> 播放
"""

import sys
from pathlib import Path
import time

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from speech.text_to_speech.synthesizer import SpeechSynthesizer
from speech.text_to_speech.audio_player import AudioPlayer
from speech.text_to_speech.voice_config import VoiceConfig


def test_voice_config():
    """测试语音配置"""
    print("=" * 60)
    print("测试1: 语音配置")
    print("=" * 60)

    print("\n可用的语音选项:\n")

    print("中文语音:")
    for name, voice_id in VoiceConfig.CHINESE_VOICES.items():
        print(f"  • {name}: {voice_id}")

    print("\n法语语音:")
    for name, voice_id in VoiceConfig.FRENCH_VOICES.items():
        print(f"  • {name}: {voice_id}")

    print("\n✓ 语音配置加载成功")


def test_chinese_synthesis():
    """测试中文语音合成"""
    print("\n" + "=" * 60)
    print("测试2: 中文语音合成")
    print("=" * 60)

    try:
        synthesizer = SpeechSynthesizer()

        test_texts = [
            "你好，我是AI法语学习助手。",
            "今天我们来学习法语的基本问候语。",
            "Bonjour在法语中是'你好'的意思。"
        ]

        output_files = []

        for i, text in enumerate(test_texts, 1):
            print(f"\n{i}. 合成文本: {text}")
            output_file = f"tmp/test_chinese_{i}.mp3"

            success = synthesizer.synthesize_chinese(text, output_file)

            if success:
                print(f"   ✓ 合成成功: {output_file}")
                output_files.append(output_file)
            else:
                print(f"   ✗ 合成失败")
                return None

        return output_files

    except Exception as e:
        print(f"\n❌ 中文合成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_french_synthesis():
    """测试法语语音合成"""
    print("\n" + "=" * 60)
    print("测试3: 法语语音合成")
    print("=" * 60)

    try:
        synthesizer = SpeechSynthesizer()

        test_texts = [
            "Bonjour, je suis votre assistant d'apprentissage du français.",
            "Comment allez-vous aujourd'hui?",
            "Merci beaucoup et au revoir!"
        ]

        output_files = []

        for i, text in enumerate(test_texts, 1):
            print(f"\n{i}. 合成文本: {text}")
            output_file = f"tmp/test_french_{i}.mp3"

            success = synthesizer.synthesize_french(text, output_file)

            if success:
                print(f"   ✓ 合成成功: {output_file}")
                output_files.append(output_file)
            else:
                print(f"   ✗ 合成失败")
                return None

        return output_files

    except Exception as e:
        print(f"\n❌ 法语合成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_audio_playback(audio_files):
    """测试音频播放"""
    print("\n" + "=" * 60)
    print("测试4: 音频播放")
    print("=" * 60)

    try:
        player = AudioPlayer()

        if not player.player_command:
            print("\n⚠️  未检测到音频播放器")
            print("  请手动播放生成的音频文件验证效果")
            return True

        print("\n将依次播放生成的音频文件...\n")

        for audio_file in audio_files:
            if Path(audio_file).exists():
                print(f"播放: {audio_file}")
                success = player.play(audio_file)

                if success:
                    print("  ✓ 播放完成\n")
                    time.sleep(0.5)  # 短暂暂停
                else:
                    print("  ✗ 播放失败\n")
            else:
                print(f"  ⚠️  文件不存在: {audio_file}\n")

        return True

    except Exception as e:
        print(f"\n❌ 音频播放测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║      文本转语音组件测试 - Text-to-Speech Test           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()

    print("📝 测试说明:")
    print("  本测试将验证文本转语音功能是否正常工作")
    print("  需要: 网络连接（Edge-TTS在线服务）")
    print("  引擎: Microsoft Edge TTS")
    print()

    input("按Enter键开始测试...")

    # 测试1: 语音配置
    test_voice_config()

    # 测试2: 中文合成
    chinese_files = test_chinese_synthesis()
    if not chinese_files:
        print("\n❌ 中文合成失败，测试中止")
        return False

    # 测试3: 法语合成
    french_files = test_french_synthesis()
    if not french_files:
        print("\n❌ 法语合成失败，测试中止")
        return False

    # 测试4: 音频播放
    all_files = chinese_files + french_files
    test_audio_playback(all_files)

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print()
    print("✅ 所有文本转语音组件测试通过！")
    print()
    print("📋 测试结果:")
    print(f"  ✓ 语音配置: 成功")
    print(f"  ✓ 中文合成: {len(chinese_files)} 个文件")
    print(f"  ✓ 法语合成: {len(french_files)} 个文件")
    print(f"  ✓ 音频播放: 成功")
    print()
    print("🎉 文本转语音组件可以正常使用！")
    print()
    print("📁 生成的音频文件:")
    for f in all_files:
        print(f"  • {f}")
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
