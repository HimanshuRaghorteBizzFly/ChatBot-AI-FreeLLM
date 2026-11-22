"""
SaaS Sidebar navigation component matching LLM Studio Pro reference layout.
"""
import streamlit as st

SIDEBAR_PAGES = [
    ("🏠 All-in-One Hub", "Dashboard"),
    ("💬 Chat Playground", "Chat Playground"),
    ("🎨 Image Generation", "Image Studio"),
    ("🎬 Video Generation", "Video Studio"),
    ("🎙️ Voice & Speech", "Speech Studio"),
    ("🤖 All Models", "All Models"),
    ("🌐 Providers", "Providers"),
    ("🔑 My API Keys", "API Keys"),
    ("📈 Usage & Limits", "Usage & Limits"),
    ("💳 Plans & Billing", "Plans & Billing"),
    ("💡 Saved Prompts", "Saved Prompts"),
    ("📜 History", "Chat History"),
    ("⚙️ Settings", "Settings")
]

def render_sidebar():
    """Renders the sidebar navigation matching LLM Studio Pro."""
    with st.sidebar:
        # Top Logo
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 0.6rem; padding: 0.4rem 0.2rem 1rem 0.2rem;">
                <span style="font-size: 1.6rem;">🧠</span>
                <div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #0F172A; letter-spacing: -0.01em; line-height: 1.1;">
                        LLM Studio <span style="color: #2563EB;">Pro</span>
                    </div>
                    <div style="font-size: 0.75rem; color: #64748B; font-weight: 600;">100% Free Community Edition</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        current_page = st.session_state.get("current_page", "Dashboard")
        page_labels = [p[0] for p in SIDEBAR_PAGES]
        page_keys = [p[1] for p in SIDEBAR_PAGES]

        default_idx = page_keys.index(current_page) if current_page in page_keys else 0

        # Sidebar navigation items
        selected_label = st.radio(
            "Navigation",
            options=page_labels,
            index=default_idx,
            label_visibility="collapsed",
            key="sidebar_page_radio"
        )

        for p in SIDEBAR_PAGES:
            if p[0] == selected_label:
                st.session_state.current_page = p[1]
                break

        st.markdown("<br>", unsafe_allow_html=True)

        # Bottom "Go Pro / Free Active" Card from Reference Screenshot
        st.markdown(
            """
            <div class="sidebar-go-pro-card">
                <div class="sidebar-go-pro-title">
                    <span>👑</span> <span>Go Pro (Free Active)</span>
                </div>
                <div class="sidebar-go-pro-text">
                    All premium foundation models, high rate limits & parallel inference unlocked for free.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Upgrade Now ➔", key="btn_side_upgrade", use_container_width=True):
            st.session_state.current_page = "Plans & Billing"
            st.rerun()

        st.caption("🟢 All Systems Operational • 120+ Models")
