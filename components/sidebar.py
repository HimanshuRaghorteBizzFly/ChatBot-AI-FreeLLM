"""
SaaS Sidebar navigation component with 16 functional pages.
"""
import streamlit as st
from backend.repositories.storage import get_user_preferences, update_user_preferences

PAGES = [
    ("📊 Dashboard", "Dashboard"),
    ("💬 AI Chat Playground", "Chat Playground"),
    ("🤖 All AI Models", "All Models"),
    ("🎨 Image Studio", "Image Studio"),
    ("🎬 Video Studio", "Video Studio"),
    ("🎙️ Speech Studio", "Speech Studio"),
    ("👁️ Vision Studio", "Vision Studio"),
    ("🧬 Embeddings", "Embeddings"),
    ("📊 Reranking", "Reranking"),
    ("⚖️ Model Comparison", "Model Comparison"),
    ("🏢 Providers", "Providers"),
    ("🔑 API Key Management", "API Keys"),
    ("📈 Usage & Limits", "Usage & Limits"),
    ("💡 Saved Prompts", "Saved Prompts"),
    ("📜 Chat History", "Chat History"),
    ("⚙️ Settings", "Settings")
]

def render_sidebar():
    """Renders the comprehensive 16-page navigation sidebar."""
    with st.sidebar:
        # SaaS Branding
        st.markdown(
            """
            <div style="padding: 0.6rem 0.2rem 1.2rem 0.2rem;">
                <h2 style="margin: 0; font-size: 1.45rem; font-weight: 800; background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    🤖 AI Studio SaaS
                </h2>
                <p style="margin: 0.2rem 0 0 0; font-size: 0.85rem; color: #64748B;">
                    Universal Multi-LLM & Vision Suite
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Theme Selector
        current_theme = st.session_state.get("theme", "Light")
        theme_choice = st.radio(
            "🎨 Theme Mode",
            options=["☀️ Light Mode", "🌙 Dark Mode"],
            index=0 if current_theme == "Light" else 1,
            horizontal=True,
            key="theme_radio_sidebar"
        )
        st.session_state.theme = "Light" if "Light" in theme_choice else "Dark"

        st.markdown("---")

        # 16-Page Navigation Selector
        st.markdown("<p style='font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #64748B; margin-bottom: 0.4rem;'>Navigation</p>", unsafe_allow_html=True)
        page_labels = [p[0] for p in PAGES]
        page_keys = [p[1] for p in PAGES]

        current_page = st.session_state.get("current_page", "Dashboard")
        default_index = page_keys.index(current_page) if current_page in page_keys else 0

        selected_label = st.radio(
            "Select Page",
            options=page_labels,
            index=default_index,
            label_visibility="collapsed",
            key="sidebar_page_nav"
        )
        
        # Update active page
        for p in PAGES:
            if p[0] == selected_label:
                st.session_state.current_page = p[1]
                break

        st.markdown("---")

        # Quick System Status
        st.markdown(
            """
            <div style="padding: 0.6rem; border-radius: 10px; background: rgba(37, 99, 235, 0.08); border: 1px solid rgba(37, 99, 235, 0.15);">
                <div style="font-size: 0.8rem; font-weight: 700; color: #2563EB; margin-bottom: 0.2rem;">🟢 SYSTEM ONLINE</div>
                <div style="font-size: 0.75rem; color: #64748B;">Engines: OpenRouter • Gemini • Groq • Ollama</div>
            </div>
            """,
            unsafe_allow_html=True
        )
