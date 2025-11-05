"""
AI法语老师 - Flask后端服务
提供API接口用于前端交互
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import sys
import logging
from datetime import datetime

# 添加项目路径到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)

# 启用CORS（跨域资源共享）
CORS(app)

# 配置
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大16MB上传

# 对话历史存储（实际应用中应该使用数据库）
conversation_sessions = {}


@app.route('/')
def index():
    """主页路由"""
    logger.info("访问主页")
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    聊天API接口
    接收用户消息，返回AI回复
    """
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({
                'error': '请求格式错误：缺少message字段'
            }), 400

        user_message = data['message'].strip()
        conversation_history = data.get('history', [])

        if not user_message:
            return jsonify({
                'error': '消息不能为空'
            }), 400

        logger.info(f"收到用户消息: {user_message}")

        # 检测用户意图
        intent = detect_intent(user_message)
        logger.info(f"检测到意图: {intent}")

        # 生成AI回复（目前使用模拟响应，后续集成实际LLM API）
        response = generate_response(user_message, intent, conversation_history)

        return jsonify({
            'response': response,
            'intent': intent,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"处理聊天请求时发生错误: {str(e)}", exc_info=True)
        return jsonify({
            'error': f'服务器错误: {str(e)}'
        }), 500


@app.route('/api/translate', methods=['POST'])
def translate():
    """
    翻译API接口
    中文 <-> 法语翻译
    """
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'zh')
        target_lang = data.get('target_lang', 'fr')

        if not text:
            return jsonify({'error': '文本不能为空'}), 400

        # 这里应该调用实际的翻译API
        # 目前返回模拟数据
        translation = f"[翻译结果: {text}]"

        return jsonify({
            'translation': translation,
            'source_lang': source_lang,
            'target_lang': target_lang
        })

    except Exception as e:
        logger.error(f"翻译错误: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/pronunciation', methods=['POST'])
def pronunciation():
    """
    发音API接口
    返回法语单词/句子的发音音频
    """
    try:
        data = request.get_json()
        text = data.get('text', '').strip()

        if not text:
            return jsonify({'error': '文本不能为空'}), 400

        # 这里应该调用TTS API生成音频
        # 目前返回模拟数据
        audio_url = f"/api/audio/{text}"

        return jsonify({
            'audio_url': audio_url,
            'text': text
        })

    except Exception as e:
        logger.error(f"发音生成错误: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI French Teacher',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


# ===== 辅助函数 =====

def detect_intent(message):
    """
    检测用户意图
    返回: translation, explanation, pronunciation, vocabulary, conversation
    """
    message_lower = message.lower()

    # 翻译意图
    if any(keyword in message_lower for keyword in ['翻译', '怎么说', '用法语', '法语怎么', 'translate']):
        return 'translation'

    # 发音意图
    if any(keyword in message_lower for keyword in ['发音', '怎么读', '读音', 'pronunciation', 'pronounce']):
        return 'pronunciation'

    # 解释意图
    if any(keyword in message_lower for keyword in ['是什么意思', '什么意思', '解释', '含义', 'explain', 'meaning']):
        return 'explanation'

    # 词汇学习
    if any(keyword in message_lower for keyword in ['单词', '词汇', '动词', '名词', '形容词', 'word', 'vocabulary']):
        return 'vocabulary'

    # 语法问题
    if any(keyword in message_lower for keyword in ['语法', '区别', '用法', '变位', 'grammar', 'difference']):
        return 'explanation'

    # 默认为对话模式
    return 'conversation'


def generate_response(message, intent, history):
    """
    生成AI回复
    根据意图返回不同类型的响应

    注意：这是一个模拟版本，实际应用中需要集成真实的LLM API
    """
    message_lower = message.lower()

    # 翻译类响应
    if intent == 'translation':
        if '你好' in message or 'hello' in message_lower:
            return """法语翻译：**Bonjour** 或 **Salut**

📝 说明：
- **Bonjour** [bɔ̃ʒuʁ] - 正式用语，适用于任何时间的问候
- **Salut** [saly] - 非正式用语，用于朋友之间

🎯 使用场景：
- 见到陌生人或长辈时用 "Bonjour"
- 见到朋友或同龄人时可以用 "Salut"

💡 例句：
- Bonjour, comment allez-vous ? （您好，您好吗？）
- Salut, ça va ? （嗨，你好吗？）"""

        elif '我很高兴' in message:
            return """法语翻译：

**正式用法：**
Je suis très heureux(se) de vous rencontrer.
[ʒə sɥi tʁɛ øʁø də vu ʁɑ̃kɔ̃tʁe]

**非正式用法：**
Je suis très content(e) de te rencontrer.
[ʒə sɥi tʁɛ kɔ̃tɑ̃ də tə ʁɑ̃kɔ̃tʁe]

📝 语法说明：
- 如果说话者是男性，用 heureux/content
- 如果说话者是女性，用 heureuse/contente
- "vous" 用于正式场合，"te" 用于非正式场合"""

    # 发音类响应
    elif intent == 'pronunciation':
        if 'bonjour' in message_lower:
            return """**Bonjour** 的发音：

🔊 音标：[bɔ̃ʒuʁ]

📖 发音指导：
1. **bon** [bɔ̃] - 鼻化元音，类似"崩"但更柔和
2. **jour** [ʒuʁ] - "日"的意思，发音时舌尖后缩

💡 发音技巧：
- "on" 是鼻化元音，需要气流从鼻腔通过
- "j" 发音像英语的 "s" 在 "pleasure" 中的音
- 重音在第二个音节 "jour" 上

🎯 常见错误：
- ❌ 把 "bon" 读成 "蹦"（太硬）
- ✅ 应该是柔和的鼻化音

试着多练习几次吧！😊"""

    # 解释类响应
    elif intent == 'explanation':
        if 'tu' in message_lower and 'vous' in message_lower:
            return """**Tu 和 Vous 的区别：**

🔹 **Tu**（你）：
- 用于非正式场合
- 对象：家人、朋友、同学、孩子
- 表达亲密和随意的关系
- 例：Tu es mon ami. (你是我的朋友)

🔹 **Vous**（您/你们）：
- 用于正式场合或复数
- 对象：
  1. 陌生人、长辈、上司（表示尊重）
  2. 多个人（复数）
- 例：Vous êtes mon professeur. (您是我的老师)

📝 使用规则：
1. 初次见面一般用 "vous"
2. 对方提议用 "tu" 后才能改用
3. 工作环境中通常用 "vous"
4. 家庭聚会中用 "tu"

💡 记忆技巧：
Vous = 正式 + 尊重 + 复数
Tu = 非正式 + 亲密 + 单数"""

    # 词汇学习响应
    elif intent == 'vocabulary':
        return """📚 **法语词汇学习**

我可以帮你学习各种法语词汇！请告诉我：
- 你想学习哪个主题的词汇？（例如：食物、颜色、数字、日常用语）
- 或者给我一个具体的法语单词，我来详细解释

一些常用主题：
🍎 食物和饮料
🎨 颜色
🔢 数字
👨‍👩‍👧 家庭成员
🏠 日常用品
🌈 情感和感觉

你想从哪里开始呢？"""

    # 默认对话响应
    else:
        return """我理解了你的问题。作为你的AI法语老师，我可以帮助你：

1. 📝 **翻译**：中文和法语互译
   - 例："请把'谢谢'翻译成法语"

2. 🗣️ **发音**：法语发音指导
   - 例："bonjour怎么发音？"

3. 📖 **解释**：词汇和语法解释
   - 例："tu和vous有什么区别？"

4. 💬 **对话**：用中文讨论法语学习

请告诉我你想学习什么，我会尽力帮助你！😊"""

    return response


# ===== 错误处理 =====

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'error': '请求的资源不存在'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    logger.error(f"服务器内部错误: {str(error)}")
    return jsonify({'error': '服务器内部错误'}), 500


# ===== 主程序入口 =====

if __name__ == '__main__':
    logger.info("启动AI法语老师后端服务...")
    logger.info("访问 http://localhost:5000 开始使用")

    # 开发模式运行
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
