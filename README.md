# AI法语老师 - French Learning Assistant 🎓

一个基于AI的法语学习助手，面向中文母语者设计的交互式法语学习平台。

## 项目简介

这是一个智能法语教学系统，通过自然的对话方式帮助中文用户学习法语。系统支持：

- 📝 **中法翻译**：准确的双向翻译服务
- 🗣️ **发音指导**：法语单词和句子的发音教学
- 📖 **语法解释**：详细的语法规则说明
- 💬 **对话学习**：通过对话自然学习法语

## 项目特点

- ✨ 现代化的Web界面，简洁易用
- 🎯 中文为主的交互语言，降低学习门槛
- 🔄 实时对话，即时反馈
- 📱 响应式设计，支持移动端访问
- 🚀 模块化架构，易于扩展

## 技术栈

### 前端
- HTML5 + CSS3
- Vanilla JavaScript
- 响应式设计

### 后端
- Python 3.8+
- Flask Web框架
- RESTful API

### 未来集成（Phase 1完整版）
- 语音识别：Whisper / Paraformer
- 语音合成：MeloTTS / Edge-TTS
- 大语言模型：Qwen 2.5 / DeepSeek

## 快速开始

### 1. 环境要求

- Python 3.8 或更高版本
- pip 包管理器
- 现代浏览器（Chrome, Firefox, Safari, Edge）

### 2. 安装依赖

```bash
# 克隆项目（如果使用Git）
git clone <repository-url>
cd AI_Franch_Teacher

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\\Scripts\\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 运行应用

```bash
# 启动后端服务
cd backend
python app.py
```

### 4. 访问应用

打开浏览器访问：`http://localhost:5000`

## 项目结构

```
AI_Franch_Teacher/
│
├── frontend/                 # 前端代码
│   ├── templates/           # HTML模板
│   │   └── index.html      # 主页面
│   └── static/             # 静态资源
│       ├── css/
│       │   └── style.css   # 样式文件
│       └── js/
│           └── main.js     # JavaScript逻辑
│
├── backend/                 # 后端代码
│   ├── app.py              # Flask主应用
│   ├── api/                # API接口
│   ├── mcp/                # 意图检测和管理
│   ├── llm/                # LLM集成
│   └── utils/              # 工具函数
│
├── config/                  # 配置文件
│   └── settings.yaml       # 应用配置
│
├── requirements.txt         # Python依赖
├── README.md               # 项目说明
└── project_society.md      # 项目详细文档
```

## 使用指南

### 基本对话

1. **翻译功能**
   - 输入："请把'你好'翻译成法语"
   - AI会提供详细的翻译和用法说明

2. **发音学习**
   - 输入："bonjour怎么发音？"
   - AI会提供音标、发音技巧和常见错误

3. **语法解释**
   - 输入："tu和vous有什么区别？"
   - AI会详细解释两者的用法差异

### 快捷示例

界面底部提供了常用问题示例，点击即可快速输入：
- "bonjour怎么发音？"
- "翻译：我很高兴"
- "tu和vous的区别"

## 开发路线图

### Phase 1 (当前) - 基础文本交互 ✅
- [x] Web前端界面
- [x] Flask后端API
- [x] 基础对话功能
- [x] 意图识别
- [ ] 真实LLM集成
- [ ] 语音输入输出

### Phase 2 (未来) - RAG系统
- [ ] 向量数据库集成
- [ ] 课程材料索引
- [ ] 高级教学功能
- [ ] 学习进度跟踪

## 配置说明

### API配置

如果要集成真实的LLM API，需要配置API密钥：

1. 创建 `.env` 文件：
```bash
# LLM API配置
LLM_API_KEY=your_api_key_here
LLM_API_BASE=https://api.example.com
LLM_MODEL=qwen-plus

# TTS配置
TTS_API_KEY=your_tts_key_here
```

2. 在代码中使用：
```python
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('LLM_API_KEY')
```

## 常见问题

### Q: 如何切换到真实的AI模型？
A: 修改 `backend/app.py` 中的 `generate_response()` 函数，集成实际的LLM API调用。

### Q: 如何添加语音功能？
A: 需要集成语音识别和语音合成库，参考 `project_society.md` 中的详细说明。

### Q: 为什么有些功能还不能使用？
A: 这是Phase 1的基础版本，主要实现了文本交互。语音功能将在后续版本中添加。

## 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

[MIT License](LICENSE)

## 联系方式

项目维护者：Baptiste Dupuis

---

## 致谢

感谢所有为这个项目做出贡献的开发者和用户！

**开始你的法语学习之旅吧！Bonne chance！🇫🇷**
