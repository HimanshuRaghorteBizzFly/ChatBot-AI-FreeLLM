"""
Settings & Preferences View.
User preferences, default engine configuration, system diagnostics, and database maintenance.
"""
import os
import sys
import platform
import streamlit as st
from components.navbar import render_navbar
from backend.repositories.storage import get_user_preferences, update_user_preferences
from backend.database import DB_PATH

def render():
    render_navbar("⚙️ Platform Settings", "Configure Defaults, System Diagnostics & Storage Maintenance")

    prefs = get_user_preferences()

    tab1, tab2 = st.tabs(["🎛️ Default Model & Engine", "🛠️ System Diagnostics & Storage"])

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
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown(f"**Python Runtime:** `{sys.version.split()[0]}`")
            st.markdown(f"**Operating System:** `{platform.system()} {platform.release()}`")
            st.markdown(f"**Streamlit Version:** `{st.__version__}`")
        with col_d2:
            db_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
            st.markdown(f"**Database Engine:** `SQLite / SQLAlchemy ORM`")
            st.markdown(f"**Database Path:** `{DB_PATH}`")
            st.markdown(f"**Database Size:** `{db_size / 1024:.2f} KB`")

        st.divider()
        st.markdown("### ⚠️ Storage Maintenance")
        if st.button("🧹 Clear Conversation History Cache", use_container_width=True):
            st.session_state.messages = []
            st.success("Session state cache cleared.")
