# 🤖 AI ChatBot & Vision Studio

A modern, multi-engine conversational AI assistant and visual generator built with **Streamlit** and **Python**. Features real-time token streaming, chain-of-thought visualization, local image generation, and customizable **Dark & Light Mode** themes.

---

## ✨ Features

- **🚀 Multi-LLM Engine Switcher:** Seamlessly switch between top frontier models right from the sidebar:
  - **🟢 NVIDIA: Nemotron 3.5 Super VL (Free):** Frontier reasoning & multimodal capabilities.
  - **✨ Google Gemini (Free Tier):** Lightning-fast answers powered by `gemini-3.1-flash-lite` and `gemini-3.8-flash`.
  - **⚡ Groq Ultra-Fast LPU:** Microsecond inference speed via `openai/gpt-oss-120b` and `openai/gpt-oss-20b`.
  - **🌟 Free AI (Instant):** 100% free cloud GPT-4o Mini with zero setup or keys required.
  - **🦙 Ollama Support:** Connect to your local desktop Ollama models (`localhost:11434`) or Ollama Cloud.
- **🎨 Microsoft AI: MAI-Image-2.7 Flash:**
  - High-speed visual generation directly in chat.
  - **Local Disk Serving:** Images are downloaded directly to `generated_images/` and served locally, eliminating broken images and CORS issues.
  - **1-Click Download:** Built-in download button for every generated visual.
- **🧠 Chain-of-Thought (Thinking Trace):** Real-time rendering of reasoning traces (`> 🧠 Thinking Process:`) for reasoning models.
- **🌙 Dual Theme Customizer:** Toggle between cohesive **Dark Mode** and **Light Mode** anytime.
- **💾 In-App Key Manager:** Save and update API keys directly to `.env` from within the UI.

---

## 📁 Project Structure

```text
ChatBot-Gemini -AI/
├── .streamlit/
│   └── config.toml          # Native Streamlit dark mode theme settings
├── generated_images/        # Auto-created folder storing generated images locally
├── .env                     # Your private API keys (never commit this)
├── .env.example             # Safe template showing required environment variables
├── .gitignore               # Prevents sensitive keys & venv from leaking to git
├── Backend.py               # Streaming connectors for OpenRouter, Gemini, Groq, & Images
├── Frontend.py              # Modern Streamlit UI with Dark/Light CSS & Chat loop
├── requirements.txt         # Project dependencies
├── run.bat                  # 1-Click launcher script for Windows
└── README.md                # Project documentation
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- **Python 3.10+** installed on your system.
- (Optional) Git installed.

### 2. Clone or Navigate to the Project Folder
```powershell
cd "d:\OneDrive\Desktop\ChatBot-Gemini -AI"
```

### 3. Create & Activate Virtual Environment
```powershell
# Create virtual environment
python -m venv .venv

# Activate on Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Or on Windows (CMD)
.venv\Scripts\activate.bat
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 🔑 API Keys Configuration

Create a file named `.env` in the root folder (or copy from `.env.example`):

```env
# 1. OpenRouter API Key (For NVIDIA Nemotron & Microsoft MAI-Image-2.7 Flash)
# Get a free key at: https://openrouter.ai/keys
OPENROUTER_API_KEY=your_openrouter_key

# 2. Google Gemini API Key (100% Free Tier, No Credit Card Required)
# Get a free key at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_key

# 3. Groq API Key (Ultra-Fast Free Tier on LPU)
# Get a free key at: https://console.groq.com/keys
GROQ_API_KEY=your_groq_key

# 4. Ollama Cloud Key (Optional if running locally)
OLLAMA_API_KEY=
```

> **Tip:** You can also paste your keys directly into the sidebar in the running app and click **"💾 Save Key to .env"**.

---

## 🚀 Running the Chatbot

### Method 1: Using the 1-Click Launcher (Windows)
Double-click **`run.bat`** in the project folder.

### Method 2: Via Terminal
```powershell
.venv\Scripts\python -m streamlit run Frontend.py
```

The application will automatically open in your default browser at `http://localhost:8501`.

---

## 🤖 Supported Models Summary

| Provider | Default Model | Access Requirement |
| :--- | :--- | :--- |
| **🎨 Microsoft AI** | `microsoft/mai-image-2.7-flash` | OpenRouter Key (or instant free pipeline) |
| **🟢 NVIDIA Nemotron** | `nvidia/nemotron-3.5-super-vl:free` | Free OpenRouter Key |
| **✨ Google Gemini** | `gemini-3.1-flash-lite` / `gemini-3.8-flash` | Free Google AI Studio Key |
| **⚡ Groq** | `openai/gpt-oss-120b` | Free Groq API Key |
| **🌟 Free AI** | `Free GPT-4o Mini` | **Zero Setup** (No key required) |
| **🦙 Ollama** | Any local model (`localhost:11434`) | Free offline with Ollama Desktop |

---

## 🔧 Troubleshooting

- **`'streamlit' is not recognized`**:
  Run through your virtual environment's Python: `.venv\Scripts\python -m streamlit run Frontend.py`.
- **`[Errno 11001] getaddrinfo failed`**:
  This is a Windows DNS hiccup. Run `ipconfig /flushdns` in Command Prompt, or switch to Google Gemini or NVIDIA Nemotron in the sidebar.
- **Images showing broken icons**:
  Resolved! All visuals are now automatically saved to `generated_images/` and served locally with an instant download button.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
