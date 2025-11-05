"""语音处理模块"""

from speech.speech_to_text.recognizer import SpeechRecognizer
from speech.speech_to_text.audio_capture import AudioCapture
from speech.speech_to_text.vad import VoiceActivityDetector
from speech.text_to_speech.synthesizer import SpeechSynthesizer
from speech.text_to_speech.audio_player import AudioPlayer
from speech.text_to_speech.voice_config import VoiceConfig

__all__ = [
    'SpeechRecognizer',
    'AudioCapture',
    'VoiceActivityDetector',
    'SpeechSynthesizer',
    'AudioPlayer',
    'VoiceConfig'
]
