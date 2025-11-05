"""
音频捕获模块
从麦克风捕获音频输入
"""

import wave
import pyaudio
from pathlib import Path
from typing import Optional
from utils.logger import logger


class AudioCapture:
    """音频捕获类"""

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 1024,
        format: int = pyaudio.paInt16
    ):
        """
        初始化音频捕获器

        Args:
            sample_rate: 采样率（Hz）
            channels: 声道数
            chunk_size: 每次读取的帧数
            format: 音频格式
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.format = format

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []

        logger.info("音频捕获器初始化完成")

    def start_recording(self):
        """开始录音"""
        self.frames = []
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        logger.info("开始录音...")

    def record_chunk(self) -> bytes:
        """
        录制一个音频块

        Returns:
            bytes: 音频数据
        """
        if not self.stream:
            raise RuntimeError("录音流未启动")

        data = self.stream.read(self.chunk_size)
        self.frames.append(data)
        return data

    def stop_recording(self) -> bytes:
        """
        停止录音

        Returns:
            bytes: 完整的音频数据
        """
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        logger.info("停止录音")
        return b''.join(self.frames)

    def save_to_file(self, filename: str, audio_data: Optional[bytes] = None):
        """
        保存音频到文件

        Args:
            filename: 文件名
            audio_data: 音频数据（如果为None，使用当前frames）
        """
        if audio_data is None:
            audio_data = b''.join(self.frames)

        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with wave.open(str(filepath), 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data)

        logger.info(f"音频已保存到: {filename}")

    def record_fixed_duration(self, duration: float) -> bytes:
        """
        录制固定时长的音频

        Args:
            duration: 录制时长（秒）

        Returns:
            bytes: 音频数据
        """
        self.start_recording()

        num_chunks = int(self.sample_rate / self.chunk_size * duration)
        logger.info(f"录制 {duration} 秒音频...")

        for _ in range(num_chunks):
            self.record_chunk()

        return self.stop_recording()

    def cleanup(self):
        """清理资源"""
        if self.stream:
            self.stop_recording()
        self.audio.terminate()
        logger.info("音频捕获器已清理")

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.cleanup()


# 使用示例
if __name__ == "__main__":
    import time

    print("🎤 音频捕获测试\n")

    try:
        with AudioCapture() as capture:
            print("请说话（将录制5秒）...")
            audio_data = capture.record_fixed_duration(5.0)

            output_file = "tmp/test_recording.wav"
            capture.save_to_file(output_file, audio_data)

            print(f"\n✓ 录音完成！已保存到: {output_file}")
            print(f"  音频大小: {len(audio_data)} 字节")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
