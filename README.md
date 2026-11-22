# 🤖 AI ChatBot & Vision Studio • SaaS Platform

An enterprise-grade, multi-engine conversational AI assistant, multimodal vision laboratory, and generative media SaaS application built with **Streamlit**, **Python 3.12+**, and **SQLite**.

Features **16 distinct functional pages**, real-time streaming inference, deep reasoning visualization, local disk image generation with guaranteed zero broken image icons, and a **White + Blue + Purple** modern SaaS design system with light/dark theme switching.

---

## 🌟 16 Core SaaS Application Views

| # | Page Name | Description |
|---|---|---|
| 1 | **📊 Dashboard** | Operational overview, live metrics, fast actions, dynamic model explorer, and recent sessions. |
| 2 | **💬 AI Chat Playground** | Multi-turn chat interface with real-time streaming, deep reasoning traces, parameter sliders, and conversation export (.md/.json). |
| 3 | **🤖 All AI Models** | Master catalog across 10 modalities (Text, Image, Video, Speech, Vision, Reasoning, Coding, Embeddings, Reranking, Multimodal). |
| 4 | **🎨 Image Studio** | High-resolution text-to-image synthesis (Microsoft MAI-Image-2.7 Flash, FLUX), aspect ratio controls, negative prompts, and local disk rendering. |
| 5 | **🎬 Video Studio** | Text-to-Video and Image-to-Video neural animation, asynchronous job tracking, and video playback. |
| 6 | **🎙️ Speech Studio** | Dual-mode audio suite: Text-to-Speech (gTTS multi-language synthesis) and Speech-to-Text (Groq Whisper Large V3 transcription). |
| 7 | **👁️ Vision Studio** | Multimodal visual reasoning, document OCR, object breakdown, and visual Q&A via Google Gemini Vision. |
| 8 | **🧬 Embeddings** | Dense 768-dimensional vector embeddings and semantic cosine similarity tester. |
| 9 | **📊 Reranking** | Cross-attention candidate document reranking with semantic relevance scoring (0.0 to 1.0). |
| 10 | **⚖️ Model Comparison** | Side-by-side benchmarking of two foundation models on identical prompts with latency and token metrics. |
| 11 | **🏢 Providers** | Health check diagnostics, connection status, and official developer links for 5+ provider backends. |
| 12 | **🔑 API Key Management** | Masked credential management, live key validation, removal, and Streamlit Secrets sync. |
| 13 | **📈 Usage & Limits** | Real-time token consumption, request count audit, estimated spend tracking, and CSV export. |
| 14 | **💡 Saved Prompts** | Pre-engineered prompt templates (Coding, Architecture, Career) and custom library manager with 1-click execution. |
| 15 | **📜 Chat History** | Conversation session auditor, title search, message inspection, and JSON/Markdown export. |
| 16 | **⚙️ Settings** | Inference defaults (provider, model, system prompt, temperature, max tokens) and database diagnostics. |

---

## 🎨 UI/UX SaaS Design System

- **Primary:** `#2563EB` (Royal Blue)
- **Secondary:** `#7C3AED` (Deep Violet)
- **Accent:** `#06B6D4` (Cyan)
- **Background Light:** `#F8FAFF` | **Background Dark:** `#0B0D14`
- **Surface Light:** `#FFFFFF` | **Surface Dark:** `#131622`
- **Typography:** Plus Jakarta Sans
- **Theme Toggle:** Live switching between ☀️ Light Mode and 🌙 Dark Mode.

---

## 🏗️ Architecture & Technology Stack

- **Frontend:** Streamlit 1.67+, Custom SaaS CSS (`styles/theme.css`), Responsive Navigation Components.
- **Backend:** Modular Service Architecture (`backend/services/`), Provider Adapters (`backend/providers/`).
- **Database:** Thread-safe SQLite engine (`backend/database.py`) with WAL mode and repository CRUD pattern (`backend/repositories/storage.py`).
- **Testing:** Pytest with 100% passing unit, integration, and Streamlit AppTest smoke tests (`tests/`).

---

## 🚀 Quickstart Guide

### 1. Clone & Setup Environment
```bash
git clone https://github.com/HimanshuRaghorteBizzFly/ChatBot-AI-FreeLLM.git
cd ChatBot-AI-FreeLLM

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # On Windows
# source .venv/bin/activate  # On Linux/macOS
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Copy `.env.example` to `.env` or configure via the in-app **API Key Management** view:
```env
OPENROUTER_API_KEY=your_openrouter_key_here
GEMINI_API_KEY=your_gemini_key_here
GROQ_API_KEY=your_groq_key_here
```

### 4. Run the Application
```bash
streamlit run Frontend.py
# Or run via alias
streamlit run app.py
```

### 5. Run Automated Tests
```bash
pytest tests -v
```

---

## ☁️ Deployment on Streamlit Community Cloud

1. Push your repository to GitHub: `github.com/<your-username>/ChatBot-AI-FreeLLM`.
2. Visit [share.streamlit.io](https://share.streamlit.io) and create a New App.
3. Select your repository, branch `main`, and set the Main file path to `Frontend.py` (or `app.py`).
4. In **App Settings > Secrets**, paste your provider API keys:
   ```toml
   OPENROUTER_API_KEY = "sk-or-v1-..."
   GEMINI_API_KEY = "AIzaSy..."
   GROQ_API_KEY = "gsk_..."
   ```
5. Deploy!
