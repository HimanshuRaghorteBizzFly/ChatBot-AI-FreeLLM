"""
Simple, user-friendly SaaS Sidebar navigation component.
Uses sleek full-width menu navigation buttons matching modern SaaS applications,
completely immune to widget instantiation errors.
"""
import streamlit as st

SIDEBAR_PAGES = [
    ("🏠 All-in-One Hub", "Dashboard"),
    ("💬 AI Chat Playground", "Chat Playground"),
    ("🎨 Image Studio", "Image Studio"),
    ("👁️ Vision Studio", "Vision Studio"),
    ("🎙️ Speech Studio", "Speech Studio"),
    ("🤖 All Models Catalog", "All Models"),
    ("🔑 API Key Settings", "API Keys"),
    ("📜 Chat History", "Chat History"),
    ("⚙️ Platform Settings", "Settings")
]

def set_page(page_name: str):
    """
    Safely navigates to a target page programmatically without widget conflicts.
    """
    st.session_state.current_page = page_name
    st.rerun()

def render_sidebar():
    """Renders a clean, user-friendly SaaS sidebar."""
    with st.sidebar:
        # Top Logo & Title
        st.markdown(
            """
            <div style="padding: 0.2rem 0 0.8rem 0;">
                <div style="font-size: 1.35rem; font-weight: 800; display: flex; align-items: center; gap: 0.5rem;">
                    <span>🤖</span> <span>AI Studio</span>
                </div>
                <div style="font-size: 0.8rem; opacity: 0.7; font-weight: 600;">100% Free Community Edition</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Simple Theme Selector
        current_theme = st.session_state.get("theme", "Light")
        theme_pick = st.radio(
            "Theme Mode",
            options=["☀️ Light Mode", "🌙 Dark Mode"],
            index=0 if current_theme == "Light" else 1,
            horizontal=True,
            key="simple_sidebar_theme"
        )
        new_theme = "Light" if "Light" in theme_pick else "Dark"
        if new_theme != current_theme:
            st.session_state.theme = new_theme
            st.rerun()

        st.markdown("<hr style='margin: 0.6rem 0; opacity: 0.15;'>", unsafe_allow_html=True)

        current_page = st.session_state.get("current_page", "Dashboard")

        # SaaS Vertical Navigation Menu
        st.markdown(
            "<div style='font-size: 0.75rem; font-weight: 700; opacity: 0.6; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.05em;'>Navigation</div>",
            unsafe_allow_html=True
        )

        for label, page_key in SIDEBAR_PAGES:
            is_active = (current_page == page_key)
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"sidebar_nav_{page_key}", use_container_width=True, type=btn_type):
                if current_page != page_key:
                    set_page(page_key)

        st.markdown("<hr style='margin: 0.8rem 0 0.6rem 0; opacity: 0.15;'>", unsafe_allow_html=True)

        # Quick System Status Box
        st.markdown(
            """
            <div style="padding: 0.75rem; border-radius: 10px; background: rgba(37, 99, 235, 0.08); border: 1px solid rgba(37, 99, 235, 0.15);">
                <div style="font-size: 0.82rem; font-weight: 700; color: #2563EB; margin-bottom: 0.2rem;">🟢 SYSTEM ONLINE</div>
                <div style="font-size: 0.75rem; opacity: 0.75;">OpenRouter • Gemini • Groq • Local Ollama</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        if st.button("🗑️ Clear Current Chat", key="btn_clear_chat_side", use_container_width=True):
            st.session_state.messages = []
            st.session_state.active_conversation_id = None
            st.success("Chat cleared!")
            st.rerun()
