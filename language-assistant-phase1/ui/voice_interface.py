"""
语音交互界面模块
提供语音输入输出界面（待实现）
"""

from utils.logger import logger


class VoiceInterface:
    """语音交互界面类"""

    def __init__(self):
        """初始化语音界面"""
        logger.info("语音界面初始化")
        print("\n⚠️  语音功能尚未实现")
        print("请先完成语音识别和语音合成组件的测试")
        print("当前将使用命令行界面代替\n")

    def run(self):
        """运行语音界面"""
        # TODO: 实现语音输入输出
        # 暂时使用CLI界面
        from ui.cli_interface import CLIInterface
        cli = CLIInterface()
        cli.run()


if __name__ == "__main__":
    interface = VoiceInterface()
    interface.run()
