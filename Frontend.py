import os
import time
import streamlit as st
from backend import (
    stream_openrouter,
    generate_image,
    stream_free_ai,
    stream_gemini,
    stream_groq,
    ask_ollama_stream,
    get_gemini_models,
    get_groq_models,
    get_available_models,
    get_env_var,
    save_env_var,
    format_openrouter_model_name,
    OPENROUTER_MODELS
)

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="AI ChatBot • Microsoft MAI & NVIDIA Free",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "🌙 Dark Mode"

# ============================================================
# Sidebar Configuration & Theme Customization
# ============================================================

with st.sidebar:
    st.markdown("### 🎨 Theme Customizer")
    
    # Theme Mode Selector
    theme_choice = st.radio(
        "Appearance Mode",
        options=["🌙 Dark Mode", "☀️ Light Mode"],
        index=0 if st.session_state.theme_mode == "🌙 Dark Mode" else 1,
        horizontal=True
    )
    st.session_state.theme_mode = theme_choice

    st.markdown("---")
    st.markdown("### ⚡ AI Engines & Vision")

    provider = st.selectbox(
        "Choose AI Engine",
        options=[
            "🎨 Microsoft AI: MAI-Image-2.7 Flash",
            "🟢 NVIDIA Nemotron (Free - OpenRouter)",
            "✨ Google Gemini (Free Tier)",
            "⚡ Groq (Ultra-Fast Free Tier)",
            "🌟 Free AI (No Key Needed)",
            "🦙 Ollama (Local / Cloud)"
        ],
        index=0,
        help="Select which AI engine powers the chat or image generation"
    )

    selected_model = ""
    active_key = ""
    ollama_host = "https://ollama.com"

    # --- 1. Microsoft AI: MAI-Image-2.7 Flash ---
    if provider == "🎨 Microsoft AI: MAI-Image-2.7 Flash":
        env_or_key = get_env_var("OPENROUTER_API_KEY")
        active_key = st.text_input(
            "OpenRouter Key",
            value=env_or_key,
            type="password",
            placeholder="sk-or-v1-..."
        )
        if active_key and active_key != env_or_key:
            if st.button("💾 Save Key to .env", key="save_mai", use_container_width=True):
                save_env_var("OPENROUTER_API_KEY", active_key)
                st.success("OpenRouter API Key saved!")

        selected_model = "microsoft/mai-image-2.7-flash"
        st.success("⚡ **Super-Fast Image Generation Mode**\n\nType any image description or idea to generate photorealistic visuals in seconds.")

    # --- 2. NVIDIA Nemotron & OpenRouter Text ---
    elif provider == "🟢 NVIDIA Nemotron (Free - OpenRouter)":
        env_or_key = get_env_var("OPENROUTER_API_KEY")
        active_key = st.text_input(
            "OpenRouter Key",
            value=env_or_key,
            type="password",
            placeholder="sk-or-v1-..."
        )
        if active_key and active_key != env_or_key:
            if st.button("💾 Save Key to .env", key="save_or", use_container_width=True):
                save_env_var("OPENROUTER_API_KEY", active_key)
                st.success("OpenRouter API Key saved!")

        selected_model = st.selectbox(
            "Select Model",
            options=OPENROUTER_MODELS,
            index=0,
            format_func=format_openrouter_model_name,
            help="Free models hosted on OpenRouter"
        )
        st.caption("🟢 **NVIDIA Nemotron 3.5 Super VL** active.")

    # --- 3. Google Gemini ---
    elif provider == "✨ Google Gemini (Free Tier)":
        env_gemini_key = get_env_var("GEMINI_API_KEY")
        active_key = st.text_input(
            "Gemini API Key",
            value=env_gemini_key,
            type="password",
            placeholder="AI Studio API key"
        )
        if active_key and active_key != env_gemini_key:
            if st.button("💾 Save Key to .env", key="save_gemini", use_container_width=True):
                save_env_var("GEMINI_API_KEY", active_key)
                st.success("Saved GEMINI_API_KEY!")

        gemini_models = get_gemini_models(active_key)
        selected_model = st.selectbox("Select Gemini Model", options=gemini_models, index=0)
        st.caption("🎁 Free key from Google AI Studio configured.")

    # --- 4. Groq ---
    elif provider == "⚡ Groq (Ultra-Fast Free Tier)":
        env_groq_key = get_env_var("GROQ_API_KEY")
        active_key = st.text_input(
            "Groq API Key",
            value=env_groq_key,
            type="password",
            placeholder="gsk_..."
        )
        if active_key and active_key != env_groq_key:
            if st.button("💾 Save Key to .env", key="save_groq", use_container_width=True):
                save_env_var("GROQ_API_KEY", active_key)
                st.success("Saved GROQ_API_KEY!")

        groq_models = get_groq_models(active_key)
        selected_model = st.selectbox(
            "Select Groq Model",
            options=groq_models,
            index=0,
            help="High-speed free models on Groq LPU"
        )
        st.caption("⚡ Ultra-fast LPU inference configured.")

    # --- 5. Free Cloud AI ---
    elif provider == "🌟 Free AI (No Key Needed)":
        st.success("✅ **100% Free Forever**\n\nNo API key or setup needed! Powered by free cloud GPT-4o Mini.")
        selected_model = "Free GPT-4o Mini"

    # --- 6. Ollama ---
    else:
        ollama_type = st.radio("Ollama Host", ["Localhost (Free)", "Ollama Cloud"], index=0)
        ollama_host = "http://localhost:11434" if ollama_type == "Localhost (Free)" else "https://ollama.com"
        
        models = get_available_models(host=ollama_host)
        selected_model = st.selectbox("Ollama Model", options=models, index=0)
        if ollama_type == "Localhost (Free)":
            st.info("💡 Requires Ollama running locally.")

    st.markdown("---")

    # Clear Chat Button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("🚀 Multi-Turn Chatbot • Real-time Streaming & Image Gen")

# ============================================================
# Dynamic CSS (Dark Mode & Light Mode)
# ============================================================

DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #0b0d14 !important;
    color: #f1f5f9 !important;
}

[data-testid="stHeader"] {
    background-color: rgba(11, 13, 20, 0.8) !important;
    backdrop-filter: blur(8px);
}

section[data-testid="stSidebar"] {
    background-color: #111420 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown p {
    color: #cbd5e1 !important;
    font-weight: 500;
}

.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background-color: #181c2e !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
}

.main-header {
    background: linear-gradient(135deg, #131728 0%, #1c2238 50%, #261f3d 100%);
    padding: 1.4rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.09);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.main-header h1 {
    color: #ffffff !important;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0;
}

.main-header p {
    color: #94a3b8 !important;
    margin: 0.2rem 0 0 0;
    font-size: 0.95rem;
}

.status-badge {
    background: rgba(34, 197, 94, 0.18);
    color: #86efac !important;
    border: 1px solid rgba(34, 197, 94, 0.35);
    padding: 0.4rem 0.9rem;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 600;
}

.stChatMessage {
    border-radius: 16px !important;
    padding: 1rem 1.2rem !important;
    margin-bottom: 0.85rem !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #312e81 0%, #4338ca 100%) !important;
    border: 1px solid rgba(99, 102, 241, 0.35) !important;
    color: #ffffff !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #141726 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #f1f5f9 !important;
}

[data-testid="stChatInput"] {
    background-color: #141726 !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 14px !important;
    color: #ffffff !important;
}

.stButton > button {
    background: #161a2b !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
}
.stButton > button:hover {
    background: #20263d !important;
    border-color: #6366f1 !important;
    color: #ffffff !important;
}
</style>
"""

LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #f8fafc !important;
    color: #0f172a !important;
}

[data-testid="stHeader"] {
    background-color: rgba(248, 250, 252, 0.85) !important;
    backdrop-filter: blur(8px);
}

section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}

section[data-testid="stSidebar"] * {
    color: #0f172a;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown p {
    color: #334155 !important;
    font-weight: 600;
}

.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
}

.main-header {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    padding: 1.4rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.main-header h1 {
    color: #ffffff !important;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0;
}

.main-header p {
    color: #cbd5e1 !important;
    margin: 0.2rem 0 0 0;
    font-size: 0.95rem;
}

.status-badge {
    background: rgba(34, 197, 94, 0.2);
    color: #4ade80 !important;
    border: 1px solid rgba(34, 197, 94, 0.4);
    padding: 0.4rem 0.9rem;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 600;
}

.stChatMessage {
    border-radius: 16px !important;
    padding: 1rem 1.2rem !important;
    margin-bottom: 0.85rem !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
    border: 1px solid #3b82f6 !important;
    color: #ffffff !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) * {
    color: #ffffff !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    color: #1e293b !important;
}

[data-testid="stChatInput"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 14px !important;
    color: #0f172a !important;
}

.stButton > button {
    background: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
}
.stButton > button:hover {
    background: #f1f5f9 !important;
    border-color: #2563eb !important;
    color: #2563eb !important;
}
</style>
"""

# Apply Theme
if st.session_state.theme_mode == "☀️ Light Mode":
    st.markdown(LIGHT_CSS, unsafe_allow_html=True)
else:
    st.markdown(DARK_CSS, unsafe_allow_html=True)

# ============================================================
# Main Header Banner
# ============================================================

friendly_name = format_openrouter_model_name(selected_model) if "OpenRouter" in provider else selected_model

st.markdown(
    f"""
    <div class="main-header">
        <div>
            <h1>🤖 AI Chat & Vision Assistant</h1>
            <p>Engine: <b>{provider}</b> • Model: <b>{friendly_name}</b></p>
        </div>
        <div class="status-badge">
            ⚡ Super Fast Active
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# Welcome Screen & Quick Starter Prompts
# ============================================================

if len(st.session_state.messages) == 0:
    st.markdown("#### 👋 Welcome! Choose a starter prompt or type your request below:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎨 Generate Image: Cyberpunk City\n\nFuturistic skyline with neon lights", use_container_width=True):
            st.session_state.pending_prompt = "A high-detail cyberpunk city at night with neon lights, flying vehicles, and rain reflections"
            st.rerun()

    with col2:
        if st.button("🟢 NVIDIA Nemotron Chat\n\nAI architecture & engineering insights", use_container_width=True):
            st.session_state.pending_prompt = "Explain how modern AI model quantization works and why it accelerates inference."
            st.rerun()

    with col3:
        if st.button("⚡ Ultra-Fast Groq Speed\n\nTest microsecond inference speed", use_container_width=True):
            st.session_state.pending_prompt = "Write a Python script that scrapes headlines from a website using BeautifulSoup."
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# Display Chat & Image History
# ============================================================

for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        img_path = msg.get("image_path")
        if img_path and os.path.exists(img_path):
            st.image(img_path, caption=msg.get("caption", "Generated Image"), use_container_width=True)
            try:
                with open(img_path, "rb") as f:
                    st.download_button(
                        "📥 Download Image",
                        data=f.read(),
                        file_name=os.path.basename(img_path),
                        mime="image/jpeg",
                        key=f"dl_hist_{idx}"
                    )
            except Exception:
                pass

# ============================================================
# Handle User Input & Generation (Text or Image)
# ============================================================

input_hint = "Describe an image to generate..." if "Image" in provider else "Type your message here..."
user_prompt = st.chat_input(input_hint)

if st.session_state.pending_prompt:
    user_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if user_prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 1. IMAGE GENERATION MODE
    if "Image" in provider or selected_model == "microsoft/mai-image-2.7-flash":
        with st.chat_message("assistant"):
            with st.spinner("🎨 Creating and rendering your visual with Microsoft MAI-Image-2.7 Flash..."):
                img_data = generate_image(user_prompt, api_key=active_key)
                local_file = img_data.get("path")
                
                if local_file and os.path.exists(local_file):
                    st.image(local_file, caption=user_prompt, use_container_width=True)
                    st.caption(f"{img_data['notice']}")
                    
                    try:
                        with open(local_file, "rb") as f:
                            img_bytes = f.read()
                            st.download_button(
                                "📥 Download Image",
                                data=img_bytes,
                                file_name=os.path.basename(local_file),
                                mime="image/jpeg",
                                key=f"dl_live_{int(time.time()*1000)}"
                            )
                    except Exception:
                        pass
                    
                    # Save to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"✨ **Image Generated:** *{user_prompt}*\n\n{img_data['notice']}",
                        "image_path": local_file,
                        "caption": user_prompt
                    })
                else:
                    st.error(img_data.get("notice", "Failed to generate image."))
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": img_data.get("notice", "Failed to generate image.")
                    })

    # 2. TEXT CHAT STREAMING MODE
    else:
        api_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
            if "image_path" not in m and "image_url" not in m
        ]

        with st.chat_message("assistant"):
            if provider == "🟢 NVIDIA Nemotron (Free - OpenRouter)":
                stream_gen = stream_openrouter(api_messages, api_key=active_key, model=selected_model)
            elif provider == "✨ Google Gemini (Free Tier)":
                stream_gen = stream_gemini(api_messages, api_key=active_key, model=selected_model)
            elif provider == "⚡ Groq (Ultra-Fast Free Tier)":
                stream_gen = stream_groq(api_messages, api_key=active_key, model=selected_model)
            elif provider == "🌟 Free AI (No Key Needed)":
                stream_gen = stream_free_ai(api_messages)
            else:
                stream_gen = ask_ollama_stream(model=selected_model, messages=api_messages, host=ollama_host)

            response_text = st.write_stream(stream_gen)

        if response_text:
            st.session_state.messages.append({"role": "assistant", "content": response_text})
