# 测试指南

本指南帮助您测试项目的各个组件。

## 前置准备

### 1. 安装依赖

```bash
cd language-assistant-phase1

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

编辑 `.env` 文件，填入您的Qwen API密钥：
```
QWEN_API_KEY=your_actual_api_key_here
```

---

## 测试步骤

### ✅ 步骤1: 测试意图检测器

```bash
python tests/test_intent_detector.py
```

**预期结果**: 应该能正确识别不同类型的意图（翻译、解释、词汇等）

---

### ✅ 步骤2: 测试对话管理器

```bash
python tests/test_conversation_manager.py
```

**预期结果**: 对话历史记录功能正常

---

### ✅ 步骤3: 测试Qwen API连接

**重要**: 此测试需要有效的API密钥和网络连接

```bash
python tests/test_qwen_api.py
```

**预期结果**:
- API连接成功
- 能够完成简单对话
- 翻译功能正常
- 解释功能正常

**可能的问题**:
- ❌ API密钥未配置 → 检查 `.env` 文件
- ❌ 网络连接失败 → 检查网络或代理设置
- ❌ API配额不足 → 检查阿里云账户余额

---

### ✅ 步骤4: 测试语音识别（Speech-to-Text）

**需要**: 麦克风设备

```bash
python tests/test_speech_recognition.py
```

**测试流程**:
1. 程序会提示您说话
2. 录制5秒音频
3. 使用Whisper进行识别
4. 显示识别结果

**预期结果**: 能够正确识别中文语音

**注意**: 首次运行会下载Whisper模型（约140MB），请耐心等待

**可能的问题**:
- ❌ 麦克风权限被拒绝 → 在系统设置中允许麦克风访问
- ❌ 找不到音频设备 → 检查麦克风是否连接
- ❌ 识别不准确 → 确保环境安静，说话清晰

---

### ✅ 步骤5: 测试语音合成（Text-to-Speech）

**需要**: 网络连接（Edge-TTS在线服务）

```bash
python tests/test_text_to_speech.py
```

**测试流程**:
1. 合成中文语音
2. 合成法语语音
3. 自动播放音频（如果有播放器）

**预期结果**:
- 成功生成音频文件
- 中文和法语语音清晰自然

**可能的问题**:
- ❌ 网络连接失败 → 检查网络连接
- ❌ 无法播放音频 → 手动打开 `tmp/` 目录下的音频文件

---

### ✅ 步骤6: 运行完整系统（CLI模式）

完成上述所有测试后，运行完整系统：

```bash
python main.py --mode cli
```

**使用示例**:
```
您: 请把'你好'翻译成法语
助手: 📝 翻译结果:
'你好'在法语中是'Bonjour'...

您: bonjour怎么发音？
助手: 🔊 发音指导:
'Bonjour'的发音是[bɔ̃ʒuʁ]...

您: tu和vous有什么区别？
助手: 💡 解释:
'Tu'用于非正式场合...
```

**退出**: 输入 `quit` 或按 `Ctrl+C`

---

## 测试清单

完成测试后，确保以下功能正常：

- [ ] 意图检测能正确识别用户请求类型
- [ ] 对话历史记录正常工作
- [ ] Qwen API连接成功，能够获取回复
- [ ] 语音识别能够正确识别中文
- [ ] 语音合成能够生成中文和法语音频
- [ ] 完整系统的CLI界面运行正常

---

## 常见问题

### Q1: 虚拟环境激活失败

**Windows**: 运行 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
**Linux/Mac**: 确保有执行权限 `chmod +x venv/bin/activate`

### Q2: pip安装依赖失败

尝试使用国内镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: Whisper模型下载慢

首次运行会自动下载模型，如果太慢可以：
1. 使用更小的模型（在代码中改为 `model_name="tiny"`）
2. 手动下载模型文件
3. 使用代理

### Q4: 没有音频设备

如果没有麦克风或扬声器：
- 语音识别测试可以跳过（后续可以补测）
- 语音合成会生成音频文件，可以手动查看
- 系统可以在CLI模式下正常运行

---

## 下一步

所有测试通过后，您可以：

1. **体验系统**: 使用CLI模式体验完整功能
2. **集成语音**: 将语音识别和合成集成到主程序（步骤7-8）
3. **开发新功能**: 添加更多教学功能
4. **准备Phase 2**: 开始学习RAG和向量数据库

---

## 获取帮助

遇到问题？

1. 查看日志文件: `logs/app_YYYYMMDD.log`
2. 运行调试模式: `python main.py --debug`
3. 查看项目文档: `README.md`
4. 咨询AI助手（Qwen、DeepSeek等）

祝测试顺利！🎉
