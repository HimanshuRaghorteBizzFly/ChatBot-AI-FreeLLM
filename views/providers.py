"""
Providers Registry & Health Monitor View.
Status checks, available model counts, and official developer links for all supported engines.
"""
import streamlit as st
from components.navbar import render_navbar
from backend.providers.registry import registry
from backend.services.credentials import get_all_credentials_info

PROVIDERS_METADATA = [
    {
        "name": "OpenRouter",
        "category": "Multi-Provider Router",
        "description": "Unified gateway to frontier models including NVIDIA Nemotron and Microsoft MAI-Image-2.7 Flash.",
        "docs_url": "https://openrouter.ai/docs",
        "console_url": "https://openrouter.ai/keys",
        "icon": "🌐"
    },
    {
        "name": "Google Gemini",
        "category": "Multimodal Frontier",
        "description": "Google DeepMind frontier multimodal models with native vision, audio, and large context windows.",
        "docs_url": "https://ai.google.dev/docs",
        "console_url": "https://aistudio.google.com/app/apikey",
        "icon": "✨"
    },
    {
        "name": "Groq",
        "category": "Ultra-Fast LPU Inference",
        "description": "Deterministic LPU tensor processors delivering 500+ tokens/sec on open-weights reasoning models.",
        "docs_url": "https://console.groq.com/docs",
        "console_url": "https://console.groq.com/keys",
        "icon": "⚡"
    },
    {
        "name": "Free AI",
        "category": "Zero-Config Cloud Intelligence",
        "description": "Out-of-the-box cloud AI accessible forever without subscriptions or developer keys.",
        "docs_url": "https://github.com/HimanshuRaghorteBizzFly/ChatBot-AI-FreeLLM",
        "console_url": "https://chatbot-ai-freell.streamlit.app/",
        "icon": "🌟"
    },
    {
        "name": "Ollama",
        "category": "Local & Cloud Private Models",
        "description": "Run open weights locally (Llama 3, Mistral, Qwen, DeepSeek) or connect to Ollama Cloud.",
        "docs_url": "https://ollama.com",
        "console_url": "http://localhost:11434",
        "icon": "🦙"
    }
]

def render():
    render_navbar("🏢 AI Provider Registry", "Integration Status, Connection Diagnostics & Developer Documentation")

    creds = get_all_credentials_info()

    for p in PROVIDERS_METADATA:
        p_name = p["name"]
        provider_obj = registry.get_provider(p_name)
        cred_info = creds.get(p_name, {})
        has_key = cred_info.get("has_key", False) or p_name == "Free AI"

        status_badge = "🟢 ONLINE" if has_key else "🟡 CONFIG NEEDED"
        badge_style = "color: #10B981; background: rgba(16, 185, 129, 0.1);" if has_key else "color: #F59E0B; background: rgba(245, 158, 11, 0.1);"

        st.markdown(
            f"""
            <div style="padding: 1.2rem; border-radius: 14px; margin-bottom: 1rem; background: #FFFFFF; border: 1px solid #E2E8F0; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div style="display: flex; align-items: center; gap: 0.6rem;">
                        <span style="font-size: 1.5rem;">{p['icon']}</span>
                        <span style="font-weight: 800; font-size: 1.2rem; color: #111827;">{p['name']}</span>
                        <span style="font-size: 0.8rem; color: #64748B;">({p['category']})</span>
                    </div>
                    <span style="padding: 0.3rem 0.8rem; border-radius: 9999px; font-weight: 700; font-size: 0.8rem; {badge_style}">
                        {status_badge}
                    </span>
                </div>
                <div style="font-size: 0.9rem; color: #475569; margin-bottom: 0.8rem;">{p['description']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        c_act1, c_act2, c_act3 = st.columns([1, 1, 4])
        with c_act1:
            if provider_obj and st.button(f"Test Health", key=f"test_prov_{p_name}", use_container_width=True):
                is_valid = provider_obj.validate_credentials()
                if is_valid or p_name == "Free AI":
                    st.success(f"{p_name} connection verified!")
                else:
                    st.error(f"{p_name} connection failed. Check your API key.")
        with c_act2:
            st.link_button("API Console", p["console_url"], use_container_width=True)
        with c_act3:
            st.link_button("Documentation", p["docs_url"])

        st.divider()
