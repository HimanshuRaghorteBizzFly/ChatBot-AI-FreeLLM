"""
Clean, Simple Top Navbar component.
"""
import streamlit as st

def render_navbar(active_title: str = "AI Studio", subtitle: str = ""):
    """Renders a simple, elegant top header bar."""
    current_theme = st.session_state.get("theme", "Light")
    theme_icon = "🌙 Dark Mode" if current_theme == "Light" else "☀️ Light Mode"

    c_left, c_right = st.columns([3, 1])

    with c_left:
        st.markdown(
            f"""
            <div style="padding: 0.2rem 0 0.6rem 0;">
                <div style="font-size: 1.4rem; font-weight: 800; display: flex; align-items: center; gap: 0.5rem;">
                    <span>🤖</span> <span>{active_title}</span>
                </div>
                <div style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.1rem;">
                    {subtitle or "Multi-Provider Generative AI & Vision Studio • 100% Free Forever"}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c_right:
        c1, c2 = st.columns([1.2, 1])
        with c1:
            if st.button(theme_icon, key=f"nav_theme_btn_{active_title}", use_container_width=True):
                st.session_state.theme = "Dark" if current_theme == "Light" else "Light"
                st.rerun()
        with c2:
            st.markdown(
                """
                <div style="text-align: right; padding-top: 0.35rem;">
                    <span class="badge-free">🟢 Active (Free)</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<hr style='margin: 0.4rem 0 1rem 0; opacity: 0.15;'>", unsafe_allow_html=True)
