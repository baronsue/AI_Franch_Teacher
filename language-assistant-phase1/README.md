# AI French Language Assistant - Phase 1

一个智能的法语学习助手，帮助中文母语者通过语音交互学习法语。

## 项目概述

这是Phase 1版本，提供基础的翻译和对话功能：
- 中法互译
- 法语语法和词汇解释（中文）
- 法语发音播放
- 语音交互
- 对话历史记录

## 技术栈

- **LLM**: 阿里云 Qwen 2.5 Instruct
- **语音识别**: OpenAI Whisper
- **语音合成**: Microsoft Edge TTS
- **编程语言**: Python 3.8+

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置API密钥

复制配置文件模板：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的API密钥：
```
QWEN_API_KEY=your_actual_api_key
```

### 3. 运行应用

```bash
# 运行主程序
python main.py

# 或使用命令行界面模式
python main.py --mode cli

# 或使用语音交互模式
python main.py --mode voice
```

## 项目结构

```
language-assistant-phase1/
├── main.py                    # 应用入口
├── requirements.txt           # Python依赖
├── .env.example              # 环境变量模板
├── README.md                 # 项目说明
│
├── mcp/                      # 意图检测和对话管理
│   ├── intent_detector.py    # 意图检测
│   ├── conversation_manager.py # 对话管理
│   └── response_formatter.py # 响应格式化
│
├── llm/                      # LLM集成
│   ├── api_client.py         # API客户端
│   ├── prompt_templates.py   # 提示词模板
│   └── config.py             # LLM配置
│
├── speech/                   # 语音处理
│   ├── speech_to_text/       # 语音识别
│   │   ├── recognizer.py
│   │   ├── vad.py
│   │   └── audio_capture.py
│   └── text_to_speech/       # 语音合成
│       ├── synthesizer.py
│       ├── voice_config.py
│       └── audio_player.py
│
├── prompts/                  # 提示词文件
│   ├── translation.txt
│   ├── explanation.txt
│   ├── vocabulary.txt
│   └── conversation.txt
│
├── ui/                       # 用户界面
│   ├── voice_interface.py
│   ├── cli_interface.py
│   └── web_interface.py
│
├── utils/                    # 工具函数
│   ├── logger.py
│   └── error_handler.py
│
├── config/                   # 配置文件
│   └── settings.yaml
│
└── tests/                    # 测试文件
    ├── test_llm.py
    ├── test_speech.py
    └── test_integration.py
```

## 使用示例

### 语音交互
```
您（中文）: "你好，bonjour在法语里怎么发音？"
AI（中文+法语）: "Bonjour的发音是[bɔ̃ʒuʁ]，让我为你读一遍..."
[播放法语发音]
```

### 文本交互
```
您: 请把这句话翻译成法语：我很高兴见到你
AI: 法语翻译：'Je suis très heureux de vous rencontrer'（正式）
    或者 'Je suis très content de te rencontrer'（非正式）
```

## 开发步骤

1. ✅ 学习基础知识（Python OOP、API、Git）
2. ⬜ 测试语音识别组件
3. ⬜ 测试语音合成组件
4. ⬜ 测试Qwen API
5. ⬜ 实现LLM + 意图检测（文本）
6. ⬜ 添加对话管理
7. ⬜ 集成语音识别
8. ⬜ 集成语音合成
9. ⬜ 完善系统
10. ⬜ 全面测试

## 常见问题

### Q: 如何获取Qwen API密钥？
A: 访问阿里云官网，注册账号后在控制台创建API密钥。

### Q: Whisper运行很慢怎么办？
A: 可以使用更小的模型（tiny或base），或者切换到Paraformer。

### Q: 语音合成没有声音？
A: 检查系统音频设置，确保Python有音频输出权限。

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

本项目采用MIT许可证。

## 联系方式

如有问题，请联系项目维护者。
