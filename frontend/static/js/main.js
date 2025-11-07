// ===== 全局变量 =====
let conversationHistory = [];
let isProcessing = false;

// ===== DOM 元素 =====
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const settingsBtn = document.getElementById('settingsBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const settingsModal = document.getElementById('settingsModal');
const closeModal = document.getElementById('closeModal');
const saveSettings = document.getElementById('saveSettings');
const voiceBtn = document.getElementById('voiceBtn');

// ===== 初始化 =====
document.addEventListener('DOMContentLoaded', () => {
    // 验证DOM元素存在
    if (!chatMessages || !userInput || !sendBtn) {
        console.error('Required DOM elements not found');
        return;
    }

    initializeEventListeners();
    loadSettings();
    autoResizeTextarea();
});

// ===== 事件监听器 =====
function initializeEventListeners() {
    // 发送按钮
    sendBtn.addEventListener('click', handleSendMessage);

    // 回车键发送消息
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    // 自动调整文本框高度
    userInput.addEventListener('input', autoResizeTextarea);

    // 清除历史按钮
    clearBtn.addEventListener('click', handleClearHistory);

    // 设置按钮
    settingsBtn.addEventListener('click', () => {
        settingsModal.style.display = 'flex';
    });

    // 关闭模态框
    closeModal.addEventListener('click', () => {
        settingsModal.style.display = 'none';
    });

    // 保存设置
    saveSettings.addEventListener('click', handleSaveSettings);

    // 点击模态框外部关闭
    settingsModal.addEventListener('click', (e) => {
        if (e.target === settingsModal) {
            settingsModal.style.display = 'none';
        }
    });

    // 快捷示例按钮
    document.querySelectorAll('.example-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            userInput.value = e.target.textContent.replace(/"/g, '');
            userInput.focus();
            autoResizeTextarea();
        });
    });

    // 语音按钮（待实现）
    voiceBtn.addEventListener('click', handleVoiceInput);
}

// ===== 消息处理 =====
async function handleSendMessage() {
    const message = userInput.value.trim();

    if (!message || isProcessing) {
        return;
    }

    // 限制消息长度
    if (message.length > 5000) {
        showNotification('消息过长，最多5000个字符', 'error');
        return;
    }

    // 显示用户消息
    addMessage('user', message);

    // 清空输入框
    userInput.value = '';
    autoResizeTextarea();

    // 显示加载动画
    showLoading();
    isProcessing = true;
    sendBtn.disabled = true;

    try {
        // 发送请求到后端
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: conversationHistory
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // 隐藏加载动画
        hideLoading();

        // 显示AI回复
        if (data.response) {
            addMessage('assistant', data.response);

            // 如果有音频，播放音频
            if (data.audio_url && getAutoPlaySetting()) {
                playAudio(data.audio_url);
            }
        } else if (data.error) {
            addMessage('assistant', `❌ 错误：${data.error}`);
        }

    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        addMessage('assistant', `❌ 抱歉，发生了错误：${error.message}\n\n请检查：\n1. 后端服务是否正在运行\n2. API配置是否正确\n3. 网络连接是否正常`);
    } finally {
        isProcessing = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// ===== 添加消息到聊天界面 =====
function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    const messageText = document.createElement('div');
    messageText.className = 'message-text';

    // 处理Markdown格式（简单版本）
    const formattedContent = formatMessage(content);
    messageText.innerHTML = formattedContent;

    messageContent.appendChild(messageText);

    if (role === 'user') {
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(avatar);
    } else {
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
    }

    chatMessages.appendChild(messageDiv);

    // 滚动到底部
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // 添加到对话历史
    conversationHistory.push({
        role: role,
        content: content
    });

    // 限制历史记录长度
    if (conversationHistory.length > 20) {
        conversationHistory = conversationHistory.slice(-20);
    }
}

// ===== 消息格式化 =====
function formatMessage(content) {
    // 严格转义所有HTML字符，防止XSS攻击
    let formatted = escapeHtml(content);

    // 处理换行
    formatted = formatted.replace(/\n/g, '<br>');

    // 安全地处理Markdown格式（使用非贪婪匹配并限制长度）
    // 处理加粗 **text** (限制在200字符内)
    formatted = formatted.replace(/\*\*(.{1,200}?)\*\*/g, '<strong>$1</strong>');

    // 处理斜体 *text* (限制在100字符内)
    formatted = formatted.replace(/\*(.{1,100}?)\*(?!\*)/g, '<em>$1</em>');

    // 处理代码 `code` (限制在50字符内)
    formatted = formatted.replace(/`(.{1,50}?)`/g, '<code style="background: #f0f0f0; padding: 2px 6px; border-radius: 4px;">$1</code>');

    // 高亮法语文本（更安全的实现）
    formatted = highlightFrenchText(formatted);

    return formatted;
}

// HTML转义函数
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 安全地高亮法语文本
function highlightFrenchText(text) {
    // 使用更简单、更安全的正则，避免ReDoS攻击
    // 只匹配包含法语特殊字符的短语（限制在100字符内）
    const frenchPattern = /\b([A-Za-zÀ-ÿ]{3,}(?:\s+[A-Za-zÀ-ÿ]{2,}){1,5})\b/g;

    return text.replace(frenchPattern, (match) => {
        // 严格限制匹配长度，防止性能问题
        if (match.length > 100) {
            return match;
        }
        // 检查是否包含法语特殊字符
        if (/[À-ÿ]/.test(match)) {
            // 再次转义以防注入
            const escaped = escapeHtml(match);
            return `<span style="color: var(--primary-color); font-weight: 500;">${escaped}</span>`;
        }
        return match;
    });
}

// ===== 显示/隐藏加载动画 =====
function showLoading() {
    loadingIndicator.style.display = 'flex';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideLoading() {
    loadingIndicator.style.display = 'none';
}

// ===== 清除对话历史 =====
function handleClearHistory() {
    if (confirm('确定要清除所有对话历史吗？')) {
        conversationHistory = [];

        // 清除消息（保留欢迎消息）
        const messages = chatMessages.querySelectorAll('.message:not(.welcome-message)');
        messages.forEach(msg => msg.remove());

        // 显示提示
        addMessage('assistant', '✨ 对话历史已清除，让我们开始新的学习吧！');
    }
}

// ===== 自动调整文本框高度 =====
function autoResizeTextarea() {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 150) + 'px';
}

// ===== 语音输入（待实现） =====
function handleVoiceInput() {
    alert('语音输入功能即将推出！🎤\n\n目前正在开发中，敬请期待。');
}

// ===== 播放音频 =====
function playAudio(audioUrl) {
    // 验证URL是否安全（只允许相对路径）
    if (!audioUrl.startsWith('/api/audio/')) {
        console.error('Invalid audio URL');
        return;
    }

    const audio = new Audio(audioUrl);

    // 添加错误处理
    audio.addEventListener('error', () => {
        console.error('Failed to load audio');
        showNotification('音频加载失败', 'error');
    });

    // 播放完成后清理
    audio.addEventListener('ended', () => {
        audio.src = '';
    });

    audio.play().catch(err => {
        console.error('Audio playback error:', err);
    });
}

// ===== 设置管理 =====
function loadSettings() {
    try {
        const settingsStr = localStorage.getItem('frenchTeacherSettings');

        // 验证存储的数据不为空且不过大
        if (!settingsStr || settingsStr.length > 10000) {
            return;
        }

        const settings = JSON.parse(settingsStr);

        // 验证settings是对象类型
        if (typeof settings !== 'object' || settings === null) {
            return;
        }

        // 注意：API密钥不应存储在前端localStorage中
        // 已移除API密钥相关代码以提高安全性

        // 只加载安全的设置项
        if (settings.language && typeof settings.language === 'string') {
            const languageSelect = document.getElementById('languageSelect');
            if (languageSelect && ['zh', 'fr', 'en'].includes(settings.language)) {
                languageSelect.value = settings.language;
            }
        }

        if (typeof settings.autoPlayAudio === 'boolean') {
            const autoPlayCheckbox = document.getElementById('autoPlayAudio');
            if (autoPlayCheckbox) {
                autoPlayCheckbox.checked = settings.autoPlayAudio;
            }
        }
    } catch (e) {
        console.error('Failed to load settings:', e);
        // 清除可能损坏的设置
        localStorage.removeItem('frenchTeacherSettings');
    }
}

function handleSaveSettings() {
    try {
        // 只保存安全的非敏感设置
        const settings = {
            language: document.getElementById('languageSelect')?.value || 'zh',
            autoPlayAudio: document.getElementById('autoPlayAudio')?.checked || false
        };

        // 注意：API密钥应该通过后端认证管理，不存储在前端
        // 已移除API密钥存储以提高安全性

        // 验证设置值
        if (!['zh', 'fr', 'en'].includes(settings.language)) {
            settings.language = 'zh';
        }

        localStorage.setItem('frenchTeacherSettings', JSON.stringify(settings));
        settingsModal.style.display = 'none';

        // 显示保存成功提示
        addMessage('assistant', '✅ 设置已保存！');
    } catch (e) {
        console.error('Failed to save settings:', e);
        showNotification('设置保存失败', 'error');
    }
}

function getAutoPlaySetting() {
    try {
        const settingsStr = localStorage.getItem('frenchTeacherSettings');
        if (!settingsStr) {
            return true; // 默认值
        }

        const settings = JSON.parse(settingsStr);
        return settings.autoPlayAudio !== false; // 默认为true
    } catch (e) {
        console.error('Failed to read auto-play setting:', e);
        return true;
    }
}

// ===== 工具函数 =====
function showNotification(message, type = 'info') {
    // 简单的通知系统（可以后续增强）
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'error' ? '#FF6B6B' : '#51CF66'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        animation: slideInRight 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ===== 错误处理 =====
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});

// ===== 调试信息 =====
console.log('%c🎓 AI法语老师前端已加载', 'color: #4A90E2; font-size: 16px; font-weight: bold;');
console.log('%c准备开始学习法语！', 'color: #51CF66; font-size: 14px;');
