"""
Backend configuration and environment management.
Supports .env files, OS environment variables, and Streamlit Community Cloud st.secrets.
"""
import os
from pathlib import Path
from dotenv import load_dotenv, set_key

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

# Load local .env if present
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    load_dotenv()

# Data & media directories
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

MEDIA_DIR = ROOT_DIR / "generated_images"
MEDIA_DIR.mkdir(exist_ok=True)

AUDIO_DIR = ROOT_DIR / "generated_audio"
AUDIO_DIR.mkdir(exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'app.db'}")

def get_config_var(name: str, default: str = "") -> str:
    """Retrieves a configuration key from os.environ, .env, or Streamlit st.secrets."""
    # 1. Environment / .env
    val = os.getenv(name, "").strip()
    if val:
        return val

    # 2. Streamlit Cloud Secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and name in st.secrets:
            return str(st.secrets[name]).strip()
    except Exception:
        pass

    return default

def save_config_var(name: str, value: str) -> bool:
    """Persists a key to the local .env file."""
    try:
        if not ENV_PATH.exists():
            ENV_PATH.touch()
        set_key(str(ENV_PATH), name, value.strip())
        os.environ[name] = value.strip()
        return True
    except Exception:
        return False
