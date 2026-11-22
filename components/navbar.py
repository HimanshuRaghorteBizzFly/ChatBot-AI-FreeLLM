"""
Top SaaS Navbar component matching LLM Studio Pro reference layout.
"""
import streamlit as st

def render_navbar(active_tab: str = "Models"):
    col_logo, col_search, col_nav = st.columns([1.5, 2.5, 3])

    with col_logo:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 0.6rem; padding-top: 0.2rem;">
                <span style="font-size: 1.5rem;">🧠</span>
                <span style="font-size: 1.25rem; font-weight: 800; color: #0F172A; letter-spacing: -0.01em;">
                    LLM Studio <span style="color: #2563EB;">Pro</span>
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_search:
        # Global Search input styled like the reference
        st.text_input(
            "Global Search",
            placeholder="🔍 Search models, e.g. GPT-4o, Gemini, Flux... (Ctrl K)",
            label_visibility="collapsed",
            key="global_navbar_search"
        )

    with col_nav:
        n1, n2, n3, n4, n5, n6 = st.columns([1.2, 1.4, 1.2, 1.2, 0.8, 0.8])
        with n1:
            if st.button("📦 Models", key="nav_models_btn", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
        with n2:
            if st.button("🛒 Market", key="nav_market_btn", use_container_width=True):
                st.session_state.current_page = "All Models"
                st.rerun()
        with n3:
            if st.button("🔑 Keys", key="nav_keys_btn", use_container_width=True):
                st.session_state.current_page = "API Keys"
                st.rerun()
        with n4:
            if st.button("💳 Billing", key="nav_bill_btn", use_container_width=True):
                st.session_state.current_page = "Plans & Billing"
                st.rerun()
        with n5:
            current_theme = st.session_state.get("theme", "Light")
            icon = "🌙" if current_theme == "Light" else "☀️"
            if st.button(icon, key="nav_theme_btn", use_container_width=True, help="Toggle Light/Dark Theme"):
                st.session_state.theme = "Dark" if current_theme == "Light" else "Light"
                st.rerun()
        with n6:
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; padding-top: 0.2rem;">
                    <div class="avatar-badge" title="User Profile: Himanshu Raghorte">HR</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<hr style='margin: 0.6rem 0 1.2rem 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
