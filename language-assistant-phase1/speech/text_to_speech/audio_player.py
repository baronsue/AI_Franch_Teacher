"""
音频播放模块
播放合成的语音文件
"""

import os
import sys
from pathlib import Path
from typing import Optional
from utils.logger import logger


class AudioPlayer:
    """音频播放器"""

    def __init__(self):
        """初始化音频播放器"""
        self.player_command = self._detect_player()
        logger.info(f"音频播放器初始化完成 (播放器: {self.player_command})")

    def _detect_player(self) -> Optional[str]:
        """
        检测可用的音频播放器

        Returns:
            Optional[str]: 播放器命令
        """
        # Windows
        if sys.platform == "win32":
            return "start"

        # macOS
        elif sys.platform == "darwin":
            return "afplay"

        # Linux
        else:
            # 尝试常见的Linux播放器
            for player in ["mpg123", "ffplay", "mplayer", "vlc"]:
                if os.system(f"which {player} > /dev/null 2>&1") == 0:
                    return player

            return None

    def play(self, audio_file: str, blocking: bool = True) -> bool:
        """
        播放音频文件

        Args:
            audio_file: 音频文件路径
            blocking: 是否阻塞等待播放完成

        Returns:
            bool: 是否成功
        """
        audio_path = Path(audio_file)

        if not audio_path.exists():
            logger.error(f"音频文件不存在: {audio_file}")
            return False

        if not self.player_command:
            logger.error("未找到可用的音频播放器")
            return False

        try:
            logger.info(f"播放音频: {audio_file}")

            if sys.platform == "win32":
                # Windows
                os.system(f'start "" "{audio_path}"')
            elif sys.platform == "darwin":
                # macOS
                cmd = f'afplay "{audio_path}"'
                if blocking:
                    os.system(cmd)
                else:
                    os.system(f'{cmd} &')
            else:
                # Linux
                cmd = f'{self.player_command} "{audio_path}"'
                if not blocking:
                    cmd += " &"
                os.system(cmd)

            return True

        except Exception as e:
            logger.error(f"播放音频失败: {e}")
            return False

    def play_async(self, audio_file: str) -> bool:
        """
        异步播放音频（不阻塞）

        Args:
            audio_file: 音频文件路径

        Returns:
            bool: 是否成功
        """
        return self.play(audio_file, blocking=False)


# 使用示例
if __name__ == "__main__":
    import sys
    from pathlib import Path

    # 添加项目路径
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    print("🔊 音频播放器测试\n")

    player = AudioPlayer()

    # 检查测试文件
    test_files = [
        "tmp/test_chinese.mp3",
        "tmp/test_french.mp3"
    ]

    for test_file in test_files:
        if Path(test_file).exists():
            print(f"播放: {test_file}")
            success = player.play(test_file)
            if success:
                print(f"  ✓ 播放成功\n")
            else:
                print(f"  ✗ 播放失败\n")
        else:
            print(f"⚠️  文件不存在: {test_file}")
            print("  请先运行 synthesizer.py 生成测试音频\n")
