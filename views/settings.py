"""
Settings & Preferences View.
User preferences, default engine configuration, system diagnostics, and database maintenance.
Hardened with live system health auditing and storage verification.
"""
import os
import sys
import platform
import streamlit as st
from components.navbar import render_navbar
from backend.repositories.storage import get_user_preferences, update_user_preferences
from backend.database import DB_PATH
from backend.services.health import get_system_health

def render():
    render_navbar("⚙️ Platform Settings", "Configure Defaults, System Diagnostics & Storage Maintenance")

    prefs = get_user_preferences()

    tab1, tab2 = st.tabs(["🎛️ Default Model & Engine", "🛠️ System Diagnostics & Health"])

    with tab1:
        st.markdown("### ⚙️ Inference Defaults")
        def_provider = st.selectbox(
            "Default Provider",
            options=["OpenRouter", "Google Gemini", "Groq", "Free AI", "Ollama"],
            index=0,
            key="set_def_provider"
        )
        def_model = st.text_input(
            "Default Model Identifier",
            value=prefs.get("default_model", "nvidia/nemotron-3.5-super-vl:free"),
            key="set_def_model"
        )
        def_prompt = st.text_area(
            "Global System Prompt",
            value=prefs.get("default_system_prompt", "You are an expert AI assistant."),
            height=100,
            key="set_def_prompt"
        )

        c_t, c_m = st.columns(2)
        with c_t:
            def_temp = st.slider("Default Temperature", 0.0, 2.0, float(prefs.get("temperature", 0.7)), 0.05, key="set_def_temp")
        with c_m:
            def_tokens = st.slider("Default Max Tokens", 256, 4096, int(prefs.get("max_tokens", 2048)), 128, key="set_def_tokens")

        if st.button("💾 Save Preferences", type="primary", use_container_width=True, key="btn_save_prefs"):
            update_user_preferences(
                default_provider=def_provider,
                default_model=def_model,
                default_system_prompt=def_prompt,
                temperature=def_temp,
                max_tokens=def_tokens
            )
            st.success("User preferences saved successfully!")

    with tab2:
        st.markdown("### 🖥️ System & Environment Diagnostics")
        health = get_system_health()

        # Health status badge
        status_color = "#10B981" if health["status"] == "healthy" else "#F59E0B"
        st.markdown(
            f"<div style='margin-bottom: 1rem;'><span style='font-size: 1.1rem; font-weight: 700; color: {status_color};'>● System Status: {health['status'].upper()}</span></div>",
            unsafe_allow_html=True
        )

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown(f"**Python Runtime:** `{health['runtime']['python_version']}`")
            st.markdown(f"**Operating System:** `{health['runtime']['platform']}`")
            st.markdown(f"**Environment:** `{health['runtime']['environment']}`")
            st.markdown(f"**Streamlit Version:** `{st.__version__}`")
        with col_d2:
            db_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
            st.markdown(f"**Database Engine:** `SQLite (WAL Mode)`")
            st.markdown(f"**Database Integrity:** `{health['database'].get('quick_check', 'ok')}`")
            st.markdown(f"**Database Size:** `{db_size / 1024:.2f} KB`")
            st.markdown(f"**Free Disk Space:** `{health.get('disk_free_gb', 0)} GB`")

        st.divider()
        st.markdown("### 🔌 Provider Connectivity Readiness")
        p_cols = st.columns(5)
        for idx, (p_name, configured) in enumerate(health.get("providers_status", {}).items()):
            with p_cols[idx % 5]:
                badge = "🟢 Ready" if configured else "🟡 No Key"
                st.metric(label=p_name, value=badge)

        st.divider()
        st.markdown("### ⚠️ Storage Maintenance")
        if st.button("🧹 Clear Conversation History Cache", use_container_width=True):
            st.session_state.messages = []
            st.success("Session state cache cleared.")
