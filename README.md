# 🤖 AI ChatBot & Vision Studio • Enterprise SaaS Platform

An enterprise-grade, multi-engine conversational AI assistant, multimodal vision laboratory, and generative media SaaS application built with **Streamlit**, **Python 3.10+**, and **SQLite (WAL Mode)**.

Features **16 distinct functional pages**, real-time streaming inference, deep reasoning visualization, local disk image generation with guaranteed zero broken image icons, structured secret-sanitizing logging, multi-tenant isolation, and a **White + Blue + Purple** modern SaaS design system with seamless light/dark theme switching.

---

## 🔒 Security & Architecture Standards

- **Zero Client-Side Secret Exposure:** API keys are never stored in browser `localStorage`, cookies, or prefilled into the browser DOM. Keys are loaded and validated strictly on the server backend.
- **Centralized Secret Masking & Sanitization:** All logs, stack traces, and error messages pass through `backend.security.sanitize_text()` to redact API keys (`sk-*`, `AIza*`, `gsk_*`, Bearer tokens, passwords) before output.
- **Strict Input & File Upload Validation:** Pydantic schemas enforce bounds on model parameters (temperature, max tokens, message length). Audio uploads are limited to 25MB and images to 20MB with MIME type verification.
- **SQL Injection & Column Injection Defense:** All database queries utilize parameterized queries (`?`). User preference updates enforce a strict column whitelist (`ALLOWED_PREF_COLUMNS`).
- **Data Isolation:** Conversations, messages, and prompt libraries enforce user tenant isolation (`user_id`).
- **Path Traversal Guards:** File paths are verified via `safe_resolve_path()` to ensure files remain strictly confined within designated directories.

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
| 16 | **⚙️ Settings** | Inference defaults, system health check (database integrity, directory writeability), and storage diagnostics. |

---

## 🏗️ Architecture & Technology Stack

- **Frontend:** Streamlit 1.35+, Custom SaaS CSS (`styles/theme.css`), Responsive Navigation Components.
- **Backend Architecture:**
  - `backend/security.py`: Zero-leak credential masking, text sanitization, path security, environment auditing.
  - `backend/logger.py`: Structured logging with automatic secret redaction and request tracing.
  - `backend/config.py`: Environment configuration and validation.
  - `backend/database.py`: Thread-safe SQLite engine with WAL mode, foreign keys, and performance indices.
  - `backend/repositories/storage.py`: Repository CRUD pattern with parameterized queries and tenant isolation.
  - `backend/schemas/types.py`: Pydantic request models with input boundaries and size validation.
  - `backend/services/`: Modular domain services (`chat`, `images`, `speech`, `vision`, `embeddings`, `reranking`, `health`, `catalog`).
  - `backend/providers/`: Provider adapters (`OpenRouter`, `Google Gemini`, `Groq`, `Ollama`, `Free AI`).
- **Testing:** Pytest automated test suite covering database operations, security masking, input validation, and provider registry.

---

## 🔑 Environment Variables Reference

| Variable | Description | Required | Default |
|---|---|---|---|
| `APP_ENV` | Environment mode (`development`, `production`, `testing`) | No | `development` |
| `OPENROUTER_API_KEY` | Key for NVIDIA Nemotron, Llama 3.3, Microsoft MAI | Optional | None |
| `GEMINI_API_KEY` | Key for Google Gemini 3.1 Flash Lite, 3.8 Flash, Vision | Optional | None |
| `GROQ_API_KEY` | Key for ultra-fast GPT-OSS 120B/20B & Whisper STT | Optional | None |
| `OLLAMA_API_KEY` | Key for Ollama Cloud (leave blank for local Ollama) | Optional | None |
| `OLLAMA_HOST` | Ollama service endpoint | No | `http://localhost:11434` |
| `DATABASE_URL` | Database connection string | No | `sqlite:///data/app.db` |
| `MAX_UPLOAD_SIZE_MB` | Maximum allowed file upload size | No | `25` |
| `REQUEST_TIMEOUT_SECONDS`| Network request timeout | No | `45` |

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- **Python 3.10+** (or use the included VS Code Dev Container / GitHub Codespaces)
- Git

### 2. Clone Repository
```bash
git clone https://github.com/HimanshuRaghorteBizzFly/ChatBot-AI-FreeLLM.git
cd ChatBot-AI-FreeLLM
```

### 3. Create & Activate Virtual Environment
```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Secrets
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` and paste your provider API keys.

---

## 🚀 Running the Application

### Option 1: 1-Click Launcher (Windows)
Double-click **`run.bat`**.

### Option 2: Command Line
```bash
streamlit run Frontend.py
# Or using the app alias
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Running the Automated Test Suite

```bash
pytest -v
```

Tests include:
- `tests/test_security.py`: Key masking, text sanitization, path traversal defense, and input validation schemas.
- `tests/test_health.py`: Database quick check and full system health audit.
- `tests/test_database.py`: CRUD operations, multi-tenant isolation, and performance indexing.
- `tests/test_providers.py`: Provider discovery and streaming resilience.
- `tests/test_services.py`: Reranking, embeddings similarity, catalog filters, and image fallback guarantees.
- `tests/test_smoke.py`: Verification that all 17 views expose `render()`.

---

## ☁️ Deployment on Streamlit Community Cloud

1. Push your repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a New App.
3. Select your repository, branch `main`, and set the entry file to `Frontend.py`.
4. In **App Settings > Secrets**, configure your keys:
   ```toml
   OPENROUTER_API_KEY = "your_openrouter_api_key_here"
   GEMINI_API_KEY = "your_gemini_api_key_here"
   GROQ_API_KEY = "your_groq_api_key_here"
   OLLAMA_API_KEY = ""
   ```
5. Deploy!

---

## 📄 License
This project is open-source and distributed under the [MIT License](LICENSE).
