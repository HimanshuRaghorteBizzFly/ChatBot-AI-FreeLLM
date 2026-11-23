"""
API Key Management View.
Secure provider credential storage, masking, live validation, and zero-leak client rendering.
Ensures raw API keys are NEVER embedded in the browser DOM or network responses.
"""
import streamlit as st
from components.navbar import render_navbar
from backend.config import get_config_var, save_config_var
from backend.security import mask_secret, validate_api_key_format
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
    st.info("💡 **Enterprise Security Notice:** API keys are managed exclusively on the backend server. Raw keys are never stored in browser localStorage or exposed in frontend HTML source.")

    for item in PROVIDERS_KEYS:
        env_var = item["env_var"]
        current_val = get_config_var(env_var) or ""
        has_key = bool(current_val)
        masked = mask_secret(current_val)

        st.markdown(f"#### {item['label']}")
        st.caption(f"{item['help']} • [Get Key from Official Console]({item['link']})")

        c_inp, c_save, c_val, c_del = st.columns([2.5, 1, 1, 1])

        with c_inp:
            # SECURITY CRITICAL: Do NOT pre-fill value with plaintext current_val!
            # Pre-filling raw keys transmits secrets into the client-side DOM.
            input_placeholder = "•••••••••••••••• (Saved — enter new to replace)" if has_key else item["placeholder"]
            new_val = st.text_input(
                f"Enter {item['provider']} Key",
                value="",
                type="password",
                placeholder=input_placeholder,
                label_visibility="collapsed",
                key=f"input_key_{env_var}"
            )
            status_color = "#10B981" if has_key else "#F59E0B"
            status_text = f"🟢 Configured (`{masked}`)" if has_key else "🟡 Not Configured"
            st.markdown(f"<span style='font-size: 0.85rem; font-weight: 600; color: {status_color};'>{status_text}</span>", unsafe_allow_html=True)

        with c_save:
            if st.button("💾 Save", key=f"btn_save_{env_var}", use_container_width=True):
                clean_new = new_val.strip()
                if not clean_new:
                    st.warning("Please enter a new key to save.")
                else:
                    if not validate_api_key_format(item["provider"], clean_new):
                        st.warning("⚠️ Warning: Key format looks unusual for this provider. Saving anyway.")
                    save_config_var(env_var, clean_new)
                    st.success("✅ Key encrypted and saved to .env!")
                    st.rerun()

        with c_val:
            if st.button("🧪 Validate", key=f"btn_val_{env_var}", use_container_width=True):
                provider_obj = registry.get_provider(item["provider"])
                test_key = new_val.strip() or current_val
                if not test_key:
                    st.warning("No key configured to test.")
                elif provider_obj:
                    # Test validity safely
                    orig_key = provider_obj.api_key
                    provider_obj.api_key = test_key
                    valid = provider_obj.validate_credentials()
                    provider_obj.api_key = orig_key
                    if valid:
                        st.success("✅ Valid API Key! Connection verified.")
                    else:
                        st.error("❌ Invalid or expired key.")

        with c_del:
            if st.button("🗑️ Remove", key=f"btn_del_{env_var}", use_container_width=True):
                save_config_var(env_var, "")
                st.warning("Key removed from configuration.")
                st.rerun()

        st.divider()

    # Streamlit Cloud Secrets Helper
    with st.expander("☁️ Streamlit Community Cloud Deployment Secrets"):
        st.markdown(
            """
            When deploying to **Streamlit Community Cloud**, paste your keys into the **App Settings → Secrets** panel:
            ```toml
            OPENROUTER_API_KEY = "your_openrouter_key"
            GEMINI_API_KEY = "your_gemini_key"
            GROQ_API_KEY = "your_groq_key"
            OLLAMA_API_KEY = ""
            ```
            """
        )
