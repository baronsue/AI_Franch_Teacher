# Project: AI-Powered Language Learning Assistant –

By Baptiste Dupuis
Verison 2.0

This is an evolving project that improves with each student group's contributions and feedback.

---

## **Overview**

The purpose of this student society project is to **create an intelligent language teacher** that can **speak and interact naturally** with Chinese learners who want to learn French.

**Target Audience:** Chinese-speaking students learning French  
**Interaction Language:** You communicate in **Chinese** (your native language)  
**Learning Language:** AI teaches **French** vocabulary, grammar, and pronunciation  
**Primary Interface:** **Voice-based interaction** for natural conversation practice

The project is designed with **two progressive phases**:

- **Phase 1:** A functional translation and conversation system to understand LLM integration
- **Phase 2:** A complete RAG-based teaching system that uses actual course materials

This **progressive approach** allows you to:

- Achieve quick wins and build confidence
- Master fundamental concepts before tackling advanced topics
- Build incrementally rather than facing overwhelming complexity
- Learn from practical experience at each stage

The system will eventually combine:

- A **speech-to-text module** for understanding spoken input
- A **text-to-speech module** for generating natural voice responses
- A **large language model (LLM)** accessed via API for intelligent conversation
- A **RAG (Retrieval-Augmented Generation) system** ensuring the AI teaches from actual course materials
- A **Lesson Controller (MCP)** that orchestrates all components

The project is designed to be **as generic as possible**, meaning its structure can be adapted to other subjects or languages without complete rework.

---

## **Two-Phase Development Approach**

### **Phase 1: Simple Translation & Conversation System ⭐⭐**

**Goal:** Build a working voice-based system where you (Chinese students) can learn French naturally.  
**Complexity:** Beginner-friendly  
**Interaction Mode:** Primarily voice-based (Chinese input, Chinese + French output)

You will create a functional bilingual voice assistant that can:

- Translate phrases between Chinese and French
- Explain French vocabulary and grammar in Chinese
- Provide French pronunciation with audio playback
- Have simple conversations in Chinese about French learning
- Remember conversation history for context

**No RAG, no vectors, no complex architecture** – just LLM + good prompts + simple logic + speech capabilities.

---

### **Phase 2: Complete RAG-Based Teaching System ⭐⭐⭐**

**Goal:** Transform the simple system into a curriculum-grounded teacher.  
**Complexity:** Advanced

You will add:

- RAG system to ground responses in course materials
- Vector database for semantic search
- Quality assurance mechanisms
- Full speech integration
- Advanced teaching features

This phase builds upon everything learned in Phase 1.

---

## **PHASE 1: Simple Translation & Conversation System**

### **What You Will Build**

A **voice interface** where you can interact naturally in Chinese while learning French:

```
You (speaking in Chinese): "你好，'bonjour'在法语里怎么发音？"
[Hello, how do you pronounce 'bonjour' in French?]

AI (responding in Chinese with French examples):
"'Bonjour'的发音是 [bɔ̃ʒuʁ]，重音在第二个音节上。
让我为你读一遍：[plays French pronunciation]
它用于白天的正式和非正式场合的问候。"

---

You (speaking in Chinese): "请把这句话翻译成法语：我很高兴见到你"
[Please translate this sentence to French: I am very happy to meet you]

AI (responding in Chinese):
"法语翻译：'Je suis très heureux de vous rencontrer'（正式）
或者 'Je suis très content de te rencontrer'（非正式）
[plays French pronunciation of both versions]"

---

You (speaking in Chinese): "'tu'和'vous'有什么区别？"
[What's the difference between 'tu' and 'vous'?]

AI (responding in Chinese):
"'Tu'用于非正式场合，比如朋友和家人之间。
'Vous'用于正式场合，比如陌生人或职业环境，
也用作复数形式称呼多人。"
```

**Key Features:**

- You speak naturally in **Chinese**
- AI responds in **Chinese** with French examples and pronunciations
- **Voice-based interaction** makes practice more natural and engaging
- AI can play **French pronunciation** for listening practice
- Supports both casual conversation and structured learning

---

### **Phase 1 Architecture**

```
┌─────────────────────────────────────┐
│   User Input (Voice or Text)       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Speech-to-Text          │
│   - Audio capture                   │
│   - Voice Activity Detection        │
│   - Speech recognition              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     Simple MCP (Intent Router)      │
│  - Detect: Translation request      │
│  - Detect: Explanation request      │
│  - Detect: Vocabulary question      │
│  - Detect: General conversation     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     Prompt Builder                  │
│  - Select appropriate prompt        │
│  - Add conversation history         │
│  - Format for LLM                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     LLM API Call                    │
│  (Qwen, DeepSeek etc.)          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     Response Processing             │
│  - Format output                    │
│  - Save to history                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Text-to-Speech     │
│   - Voice synthesis                 │
│   - Audio playback                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Output to User (Voice or Text)    │
└─────────────────────────────────────┘
```

---

### **Phase 1 Folder Structure**

```
language-assistant-phase1/
│
├── main.py                    # Application entry point
│
├── mcp/
│   ├── intent_detector.py     # Detect user intention
│   ├── conversation_manager.py # Store conversation history
│   └── response_formatter.py  # Format AI responses
│
├── llm/
│   ├── api_client.py          # LLM API communication
│   ├── prompt_templates.py    # Prompt templates
│   └── config.py              # API keys and settings
│
├── speech/
│   ├── speech_to_text/
│   │   ├── recognizer.py      # Speech recognition
│   │   ├── vad.py             # Voice Activity Detection
│   │   └── audio_capture.py   # Audio input handling
│   │
│   └── text_to_speech/
│       ├── synthesizer.py     # Speech synthesis
│       ├── voice_config.py    # Voice settings
│       └── audio_player.py    # Audio playback
│
├── prompts/
│   ├── translation.txt        # Translation prompts
│   ├── explanation.txt        # Explanation prompts
│   ├── vocabulary.txt         # Vocabulary prompts
│   └── conversation.txt       # General conversation prompts
│
├── ui/
│   ├── voice_interface.py     # Primary: Voice interaction mode
│   ├── cli_interface.py       # Alternative: Command-line interface
│   └── web_interface.py       # Optional: simple web UI
│
├── utils/
│   ├── logger.py              # Logging
│   └── error_handler.py       # Error management
│
└── config/
    └── settings.yaml          # Configuration file
```

---

### **Phase 1 Core Components**

#### **1. Intent Detector**

Identifies what the you wants based on keywords: translation, explanation, vocabulary, or general conversation.

#### **2. Prompt Templates**

Pre-written instructions for the LLM adapted to different situations (translation, explanation, conversation). Each template defines the AI's role and response format.

#### **3. Conversation Manager**

Stores message history and retrieves recent context for multi-turn conversations.

#### **4. LLM API Client**

Handles communication with the language model: sends prompts, receives responses, manages errors.

#### **5. Speech-to-Text Module**

Converts Chinese voice input to text through audio capture, voice detection, and speech recognition.

#### **6. Text-to-Speech Module**

Converts text responses to natural speech in Chinese and French with adjustable voice settings.

---

## **PHASE 2: Complete RAG-Based Teaching System ⭐⭐⭐**

Phase 2 transforms your simple translator into a **curriculum-grounded teacher** by adding:

**RAG System** - The AI uses actual course PDFs instead of inventing answers
**Quality Assurance** - Validates responses and detects hallucinations  
**Advanced Speech** - Pronunciation analysis and correction  
**Enhanced MCP** - Lesson tracking and adaptive difficulty  
**Full Teaching Features** - Structured lessons, exercises, and progress tracking

**The Problem Phase 1 Reveals:**

- AI sometimes gives wrong grammar rules
- Explanations don't match the textbook
- Can't cite specific lessons

---

## **Recommended Technologies**

**Large Language Model (API):**

- **Qwen 2.5 Instruct** (Alibaba Cloud) - Specifically optimized for Chinese-French language pairs, best choice for this project

**Speech-to-Text:**

- **Whisper** (OpenAI) - Multilingual, excellent for both Chinese and French
- **Paraformer** (Alibaba) - Optimized for Chinese, fast and accurate

**Text-to-Speech:**

- **MeloTTS** - Modern, multilingual, natural-sounding voices for Chinese and French
- **CosyVoice** (Alibaba) - High-quality Chinese and multilingual synthesis
- **Edge-TTS** (Microsoft) - Easy integration, good quality for both languages

**Embeddings (Phase 2):** BGE, M3E (optimized for Chinese)  
**Vector Database (Phase 2):** ChromaDB (simple), FAISS (fast)

**Note:** These are recommendations based on current best practices. You are **encouraged to research alternatives** and **test different solutions** to find what works best for your specific needs and hardware. The AI field evolves rapidly, and newer, better options may become available.

---

## **Next Steps for Phase 1**

### **Step 1: Build Your Knowledge Foundation**

Before starting the project, familiarize yourself with these essential concepts:

**Core Technologies:**

- **Python OOP** (Object-Oriented Programming) - Classes, methods, inheritance
- **API fundamentals** - REST APIs, HTTP requests, JSON handling
- **Git basics** - Clone, commit, push, branches, collaboration
- **Environment management** - Virtual environments, dependencies, configuration files

**Learning Resources:**

- Search Bilibili for tutorials on each topic
- Ask AI assistants (Qwen, DeepSeek) to explain concepts
- Practice with small examples before diving into the full project

---

### **Step 2: Test Speech Components Independently**

**Goal:** Verify that speech-to-text and text-to-speech work on your computer before integrating them.

**Speech-to-Text Testing:**

1. Follow the documentation or Bilibili tutorials for **Whisper** or **Paraformer**
2. Create a simple test script that:
   - Captures audio from your microphone
   - Converts your Chinese speech to text
   - Prints the recognized text
3. Test with different voices and background noise levels

**Text-to-Speech Testing:**

1. Follow the documentation or Bilibili tutorials for **MeloTTS**, **CosyVoice**, or **Edge-TTS**
2. Create a simple test script that:
   - Takes a Chinese text string
   - Generates audio speech
   - Plays the audio through your speakers
3. Test with Chinese and French text
4. Compare quality and naturalness of different TTS engines

**Deliverable:** Two working test scripts demonstrating speech capabilities

---

### **Step 3: Test Alibaba Cloud & Qwen API**

**Goal:** Successfully communicate with Qwen LLM before building the full system.

**Simple Qwen Test Project:**

1. Create an Alibaba Cloud account and get API credentials
2. Follow Qwen API documentation to understand:
   - Authentication methods
   - Request format (messages, system prompts, parameters)
   - Response parsing
3. Build a simple chat script that:
   - Sends a question to Qwen in Chinese
   - Receives and displays the response
   - Handles errors (network issues, rate limits, invalid responses)
4. Test with various prompts:
   - Simple translation requests
   - Grammar explanations
   - Multi-turn conversations with history

**Test Scenarios:**

```python
# Example tests to verify your API client works:
- "请把'你好'翻译成法语" (Translation test)
- "解释'être'动词的变位" (Explanation test)
- Multi-turn: Ask a question, then ask a follow-up based on the response
```

**Deliverable:** A working script that successfully communicates with Qwen API

---

### **Step 4: Assemble the Complete System**

Once all components work independently, start building the Phase 1 project:

**Integration Order:**

1. Start with LLM + Intent Detection (text input only)
2. Add Conversation Management (multi-turn conversations)
3. Integrate Speech-to-Text (voice input)
4. Integrate Text-to-Speech (voice output)
5. Polish and refine (error handling, UI, logging)

**Development Tips:**

- Build incrementally, test each component before moving forward
- Keep code modular and organized
- Use Git to commit progress regularly
- Ask AI assistants when stuck

**Deliverable:** Complete Phase 1 voice assistant system

---

---

**This progressive approach ensures you succeed by building confidence step by step.**
