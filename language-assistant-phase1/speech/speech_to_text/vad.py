"""
语音活动检测（Voice Activity Detection）模块
检测音频中是否有人声
"""

import numpy as np
from typing import Optional
from utils.logger import logger


class VoiceActivityDetector:
    """语音活动检测器"""

    def __init__(
        self,
        energy_threshold: float = 300,
        silence_threshold: float = 0.5
    ):
        """
        初始化VAD

        Args:
            energy_threshold: 能量阈值
            silence_threshold: 静音时长阈值（秒）
        """
        self.energy_threshold = energy_threshold
        self.silence_threshold = silence_threshold
        self.silence_duration = 0.0

        logger.info("语音活动检测器初始化完成")

    def calculate_energy(self, audio_data: bytes) -> float:
        """
        计算音频能量

        Args:
            audio_data: 音频数据

        Returns:
            float: 能量值
        """
        # 将字节数据转换为numpy数组
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        # 计算RMS能量
        energy = np.sqrt(np.mean(audio_array ** 2))

        return energy

    def is_speech(self, audio_data: bytes) -> bool:
        """
        检测音频中是否有语音

        Args:
            audio_data: 音频数据

        Returns:
            bool: True表示有语音，False表示静音
        """
        energy = self.calculate_energy(audio_data)
        is_speech = energy > self.energy_threshold

        logger.debug(f"音频能量: {energy:.2f}, 是否为语音: {is_speech}")

        return is_speech

    def detect_silence_end(
        self,
        audio_data: bytes,
        chunk_duration: float
    ) -> bool:
        """
        检测是否达到静音结束条件

        Args:
            audio_data: 音频数据
            chunk_duration: 音频块时长（秒）

        Returns:
            bool: True表示应该停止录音
        """
        if self.is_speech(audio_data):
            # 检测到语音，重置静音计时
            self.silence_duration = 0.0
            return False
        else:
            # 累加静音时长
            self.silence_duration += chunk_duration

            if self.silence_duration >= self.silence_threshold:
                logger.info(f"检测到 {self.silence_duration:.2f}秒静音，停止录音")
                return True

            return False

    def reset(self):
        """重置检测器状态"""
        self.silence_duration = 0.0
        logger.debug("VAD状态已重置")


# 使用示例
if __name__ == "__main__":
    import sys
    from pathlib import Path

    # 添加项目路径
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    vad = VoiceActivityDetector(energy_threshold=300)

    # 模拟音频数据
    print("🎤 语音活动检测测试\n")

    # 测试1: 有语音的音频（模拟）
    speech_data = np.random.randint(-5000, 5000, 1024, dtype=np.int16).tobytes()
    print(f"测试1 - 有语音: {vad.is_speech(speech_data)}")

    # 测试2: 静音音频（模拟）
    silence_data = np.random.randint(-100, 100, 1024, dtype=np.int16).tobytes()
    print(f"测试2 - 静音: {vad.is_speech(silence_data)}")

    # 测试3: 静音结束检测
    vad.reset()
    print("\n测试3 - 静音结束检测:")
    for i in range(5):
        should_stop = vad.detect_silence_end(silence_data, 0.1)
        print(f"  第{i+1}次检测 (静音时长: {vad.silence_duration:.2f}s): {'应停止' if should_stop else '继续'}")
        if should_stop:
            break
