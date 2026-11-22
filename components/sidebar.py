"""
Simple, user-friendly SaaS Sidebar navigation component.
Supports safe two-way synchronization between sidebar radio and button navigations.
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
    Safely navigates to a target page programmatically and keeps
    the sidebar navigation radio completely in sync.
    """
    st.session_state.current_page = page_name
    st.session_state._last_page = page_name
    for label, key in SIDEBAR_PAGES:
        if key == page_name:
            st.session_state["simple_sidebar_nav"] = label
            break

def render_sidebar():
    """Renders a clean, user-friendly sidebar."""
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
        page_labels = [p[0] for p in SIDEBAR_PAGES]
        page_keys = [p[1] for p in SIDEBAR_PAGES]

        # 1. Sync simple_sidebar_nav if current_page changed programmatically
        if "_last_page" not in st.session_state:
            st.session_state._last_page = current_page

        if st.session_state._last_page != current_page:
            for label, key in SIDEBAR_PAGES:
                if key == current_page:
                    st.session_state["simple_sidebar_nav"] = label
                    break
            st.session_state._last_page = current_page

        target_label = page_labels[0]
        for label, key in SIDEBAR_PAGES:
            if key == current_page:
                target_label = label
                break

        default_idx = page_labels.index(target_label) if target_label in page_labels else 0

        # Simple Navigation Radio
        selected_label = st.radio(
            "Navigation",
            options=page_labels,
            index=default_idx,
            label_visibility="collapsed",
            key="simple_sidebar_nav"
        )

        for p in SIDEBAR_PAGES:
            if p[0] == selected_label:
                st.session_state.current_page = p[1]
                st.session_state._last_page = p[1]
                break

        st.markdown("<br>", unsafe_allow_html=True)

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
