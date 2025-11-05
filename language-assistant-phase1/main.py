#!/usr/bin/env python3
"""
AI French Language Assistant - Phase 1
主程序入口
"""

import argparse
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import setup_logger
from ui.cli_interface import CLIInterface
from ui.voice_interface import VoiceInterface


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="AI French Language Assistant")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["cli", "voice"],
        default="cli",
        help="交互模式: cli (命令行) 或 voice (语音)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="启用调试模式"
    )

    args = parser.parse_args()

    # 设置日志
    logger = setup_logger(debug=args.debug)
    logger.info(f"启动 AI French Language Assistant (模式: {args.mode})")

    try:
        if args.mode == "cli":
            # 命令行界面模式
            interface = CLIInterface()
            interface.run()
        elif args.mode == "voice":
            # 语音交互模式
            interface = VoiceInterface()
            interface.run()
    except KeyboardInterrupt:
        logger.info("用户中断程序")
        print("\n\n再见！Au revoir! 👋")
    except Exception as e:
        logger.error(f"程序运行出错: {e}", exc_info=True)
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
