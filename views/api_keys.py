"""
API Key Management View.
Secure provider credential storage, masking, live validation, and Streamlit Secrets sync.
"""
import streamlit as st
from components.navbar import render_navbar
from backend.config import get_config_var, save_config_var
from backend.services.credentials import get_masked_key, get_all_credentials_info
from backend.providers.registry import registry

PROVIDERS_KEYS = [
    {
        "provider": "OpenRouter",
        "env_var": "OPENROUTER_API_KEY",
        "label": "OpenRouter API Key",
        "placeholder": "sk-or-v1-...",
        "help": "Used for NVIDIA Nemotron, Microsoft MAI-Image-2.7 Flash, and 100+ open models.",
        "link": "https://openrouter.ai/keys"
    },
    {
        "provider": "Google Gemini",
        "env_var": "GEMINI_API_KEY",
        "label": "Google Gemini API Key",
        "placeholder": "AIzaSy...",
        "help": "Used for Gemini 3.1 Flash Lite, Gemini 3.8 Flash, Vision, and Embeddings.",
        "link": "https://aistudio.google.com/app/apikey"
    },
    {
        "provider": "Groq",
        "env_var": "GROQ_API_KEY",
        "label": "Groq API Key",
        "placeholder": "gsk_...",
        "help": "Used for ultra-fast GPT-OSS 120B/20B and Whisper Speech-to-Text.",
        "link": "https://console.groq.com/keys"
    },
    {
        "provider": "Ollama",
        "env_var": "OLLAMA_API_KEY",
        "label": "Ollama Cloud API Key (Optional)",
        "placeholder": "ollama_...",
        "help": "Used if connecting to remote Ollama Cloud instances.",
        "link": "https://ollama.com"
    }
]

def render():
    render_navbar("🔑 API Key Management", "Secure Credential Encryption, Live Verification & Cloud Sync")

    st.markdown("### 🔒 Provider Authentication")
    st.info("💡 **Security Notice:** Your API keys are stored locally in your environment or Streamlit Secrets. Keys are never transmitted to third parties or logged.")

    for item in PROVIDERS_KEYS:
        env_var = item["env_var"]
        current_val = get_config_var(env_var) or ""
        masked = get_masked_key(current_val)

        st.markdown(f"#### {item['label']}")
        st.caption(f"{item['help']} • [Get Key from Official Console]({item['link']})")

        c_inp, c_save, c_val, c_del = st.columns([2.5, 1, 1, 1])

        with c_inp:
            new_val = st.text_input(
                f"Enter {item['provider']} Key",
                value=current_val,
                type="password",
                placeholder=item["placeholder"],
                label_visibility="collapsed",
                key=f"input_key_{env_var}"
            )
            st.caption(f"Current Value: `{masked}`")

        with c_save:
            if st.button("💾 Save", key=f"btn_save_{env_var}", use_container_width=True):
                save_config_var(env_var, new_val.strip())
                st.success("Key saved to .env!")
                st.rerun()

        with c_val:
            if st.button("🧪 Validate", key=f"btn_val_{env_var}", use_container_width=True):
                provider_obj = registry.get_provider(item["provider"])
                if provider_obj:
                    provider_obj.api_key = new_val.strip() or current_val
                    if provider_obj.validate_credentials():
                        st.success("✅ Valid API Key!")
                    else:
                        st.error("❌ Invalid or expired key.")

        with c_del:
            if st.button("🗑️ Remove", key=f"btn_del_{env_var}", use_container_width=True):
                save_config_var(env_var, "")
                st.warning("Key removed.")
                st.rerun()

        st.divider()

    # Streamlit Cloud Secrets Helper
    with st.expander("☁️ Streamlit Community Cloud Deployment Secrets"):
        st.markdown(
            """
            When deploying on **Streamlit Community Cloud**, paste these secrets into your App Settings > Secrets:
            ```toml
            OPENROUTER_API_KEY = "your_openrouter_key_here"
            GEMINI_API_KEY = "your_gemini_key_here"
            GROQ_API_KEY = "your_groq_key_here"
            ```
            """
        )
