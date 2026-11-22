"""
Top SaaS Navbar component.
"""
import streamlit as st

def render_navbar(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="saas-navbar">
            <div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #111827;">{title}</div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 2px;">{subtitle}</div>
            </div>
            <div style="display: flex; gap: 0.6rem; align-items: center;">
                <span class="badge-pill badge-primary">⚡ Super-Fast</span>
                <span class="badge-pill badge-secondary">✨ Active</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
