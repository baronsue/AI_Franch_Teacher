"""
语音配置模块
定义不同语言的语音选项
"""

from typing import Dict


class VoiceConfig:
    """语音配置类"""

    # Edge-TTS支持的中文语音
    CHINESE_VOICES = {
        "xiaoxiao": "zh-CN-XiaoxiaoNeural",  # 女声，温柔
        "yunyang": "zh-CN-YunyangNeural",    # 男声，稳重
        "xiaoyi": "zh-CN-XiaoyiNeural",      # 女声，甜美
        "yunjian": "zh-CN-YunjianNeural",    # 男声，活力
    }

    # Edge-TTS支持的法语语音
    FRENCH_VOICES = {
        "denise": "fr-FR-DeniseNeural",      # 女声
        "henri": "fr-FR-HenriNeural",        # 男声
        "alain": "fr-FR-AlainNeural",        # 男声
        "brigitte": "fr-FR-BrigitteNeural",  # 女声
    }

    @classmethod
    def get_chinese_voice(cls, name: str = "xiaoxiao") -> str:
        """
        获取中文语音

        Args:
            name: 语音名称

        Returns:
            str: 语音ID
        """
        return cls.CHINESE_VOICES.get(name, cls.CHINESE_VOICES["xiaoxiao"])

    @classmethod
    def get_french_voice(cls, name: str = "denise") -> str:
        """
        获取法语语音

        Args:
            name: 语音名称

        Returns:
            str: 语音ID
        """
        return cls.FRENCH_VOICES.get(name, cls.FRENCH_VOICES["denise"])

    @classmethod
    def list_voices(cls, language: str = "all") -> Dict:
        """
        列出可用语音

        Args:
            language: 语言类型 ('chinese', 'french', 'all')

        Returns:
            Dict: 语音列表
        """
        if language == "chinese":
            return cls.CHINESE_VOICES
        elif language == "french":
            return cls.FRENCH_VOICES
        else:
            return {
                "chinese": cls.CHINESE_VOICES,
                "french": cls.FRENCH_VOICES
            }


# 使用示例
if __name__ == "__main__":
    print("可用的语音选项:\n")

    print("中文语音:")
    for name, voice_id in VoiceConfig.CHINESE_VOICES.items():
        print(f"  {name}: {voice_id}")

    print("\n法语语音:")
    for name, voice_id in VoiceConfig.FRENCH_VOICES.items():
        print(f"  {name}: {voice_id}")
