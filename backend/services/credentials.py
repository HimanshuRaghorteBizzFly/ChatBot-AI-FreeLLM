"""
Credentials management service.
Handles safe key masking, persistence to .env, and validation.
"""
from typing import Dict, Any
from backend.config import get_config_var, save_config_var
from backend.providers.registry import registry

def get_masked_key(key: str) -> str:
    """Safely masks an API key (e.g. sk-or...b446)."""
    if not key:
        return "Not Configured"
    if len(key) <= 8:
        return "****"
    return f"{key[:6]}...{key[-4:]}"

def get_all_credentials_info() -> Dict[str, Dict[str, Any]]:
    providers = [
        {"name": "OpenRouter", "env_var": "OPENROUTER_API_KEY", "desc": "For NVIDIA Nemotron & Microsoft MAI-Image-2.7 Flash"},
        {"name": "Google Gemini", "env_var": "GEMINI_API_KEY", "desc": "For Gemini 3.1 Flash Lite, 3.8 Flash & Vision"},
        {"name": "Groq", "env_var": "GROQ_API_KEY", "desc": "For GPT-OSS 120B/20B & Whisper Speech-to-Text"},
        {"name": "Ollama", "env_var": "OLLAMA_API_KEY", "desc": "For Ollama Cloud (optional for local)"}
    ]

    result = {}
    for p in providers:
        raw_key = get_config_var(p["env_var"])
        provider_obj = registry.get_provider(p["name"])
        is_valid = provider_obj.validate_credentials() if (raw_key and provider_obj) else False
        
        result[p["name"]] = {
            "name": p["name"],
            "env_var": p["env_var"],
            "description": p["desc"],
            "has_key": bool(raw_key),
            "masked_key": get_masked_key(raw_key),
            "is_valid": is_valid
        }
    return result

def update_credential(env_var: str, key_value: str) -> bool:
    return save_config_var(env_var, key_value)
