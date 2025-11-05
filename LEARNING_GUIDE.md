# Phase 1 学习指南

本指南帮助您掌握项目所需的基础知识。

## 📚 1. Python OOP（面向对象编程）

### 核心概念
- **类（Class）**：定义对象的模板
- **对象（Object）**：类的实例
- **继承（Inheritance）**：子类继承父类的属性和方法
- **封装（Encapsulation）**：隐藏内部实现细节

### 实践示例

```python
# 基础类定义
class LanguageAssistant:
    def __init__(self, name, language):
        self.name = name
        self.language = language
        self.conversation_history = []

    def add_message(self, message):
        """添加消息到历史记录"""
        self.conversation_history.append(message)

    def get_history(self):
        """获取对话历史"""
        return self.conversation_history

# 继承示例
class FrenchAssistant(LanguageAssistant):
    def __init__(self, name):
        super().__init__(name, "French")

    def translate(self, chinese_text):
        """翻译中文到法语"""
        return f"Translating: {chinese_text}"

# 使用示例
assistant = FrenchAssistant("小法")
assistant.add_message("你好")
print(assistant.get_history())
```

### 学习资源
- B站搜索："Python 面向对象编程 入门"
- B站搜索："Python OOP 详解"

---

## 🌐 2. API基础知识

### 核心概念
- **REST API**：通过HTTP协议进行通信的接口
- **HTTP方法**：GET（获取）、POST（创建）、PUT（更新）、DELETE（删除）
- **JSON**：数据交换格式
- **API Key**：身份验证密钥

### 实践示例

```python
import requests
import json

# 简单的API调用示例
def call_llm_api(prompt, api_key):
    """调用LLM API"""
    url = "https://api.example.com/v1/chat"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查HTTP错误
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        print(f"API调用失败: {e}")
        return None

# 使用示例
# result = call_llm_api("你好", "your-api-key")
```

### 学习资源
- B站搜索："Python requests 库教程"
- B站搜索："REST API 入门"
- B站搜索："JSON 数据格式"

---

## 📦 3. Git基础

### 核心概念
- **仓库（Repository）**：项目的版本控制容器
- **提交（Commit）**：保存代码快照
- **分支（Branch）**：独立的开发线
- **合并（Merge）**：将分支合并到主线

### 常用命令

```bash
# 初始化仓库
git init

# 查看状态
git status

# 添加文件到暂存区
git add .

# 提交更改
git commit -m "描述信息"

# 查看历史
git log --oneline

# 创建分支
git branch feature-name

# 切换分支
git checkout feature-name

# 推送到远程
git push origin branch-name
```

### 学习资源
- B站搜索："Git 入门教程"
- B站搜索："Git 实战教程"

---

## 🔧 4. Python环境管理

### 虚拟环境

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

# 导出依赖
pip freeze > requirements.txt

# 退出虚拟环境
deactivate
```

### 配置文件

**requirements.txt示例：**
```
requests>=2.31.0
openai-whisper>=20230918
edge-tts>=6.1.0
pyyaml>=6.0
```

**.env示例（存储敏感信息）：**
```
QWEN_API_KEY=your_api_key_here
QWEN_API_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
```

### 学习资源
- B站搜索："Python 虚拟环境"
- B站搜索："pip 包管理"

---

## 🎯 实践建议

### 学习顺序
1. **先看视频教程**（每个主题1-2小时）
2. **跟着教程敲代码**（不要复制粘贴）
3. **做小练习**（下面有建议）
4. **应用到项目中**

### 小练习

#### 练习1：OOP基础
创建一个简单的学生管理类：
```python
class Student:
    def __init__(self, name, age):
        # 完成初始化
        pass

    def study(self, subject):
        # 完成学习方法
        pass
```

#### 练习2：API调用
使用免费API练习（如天气API）：
```python
import requests

def get_weather(city):
    # 调用天气API
    # 解析JSON响应
    # 返回天气信息
    pass
```

#### 练习3：Git操作
1. 创建一个测试仓库
2. 创建几个文件
3. 提交更改
4. 创建分支并切换
5. 合并分支

---

## 💡 学习技巧

1. **边学边做**：不要只看不练
2. **使用AI助手**：遇到问题问Qwen、DeepSeek等
3. **记录笔记**：写下关键概念和代码片段
4. **循序渐进**：不要急于求成
5. **实际应用**：立即在项目中使用学到的知识

---

## ✅ 检查清单

完成学习后，确保您能够：

- [ ] 理解类、对象、继承、封装的概念
- [ ] 能够创建简单的类和对象
- [ ] 理解API调用的基本流程
- [ ] 能够使用requests库发送HTTP请求
- [ ] 能够解析JSON数据
- [ ] 理解Git的基本操作
- [ ] 能够创建提交、分支、合并
- [ ] 能够创建和使用虚拟环境
- [ ] 能够管理Python依赖包
- [ ] 能够使用配置文件管理设置

---

## 🚀 准备好了吗？

完成上述学习后，您就可以开始项目的实际开发了！

下一步：开始测试语音识别和语音合成组件
