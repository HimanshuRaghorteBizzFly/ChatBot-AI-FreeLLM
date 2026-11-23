"""
Backend configuration and environment management.
Supports .env files, OS environment variables, and Streamlit Community Cloud st.secrets.
Includes production startup validation and security hardening.
"""
import os
from pathlib import Path
from dotenv import load_dotenv, set_key
from backend.security import mask_secret, sanitize_text, validate_environment

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

# Environment Mode: development | staging | production | testing
APP_ENV = os.getenv("APP_ENV", "development").lower()
IS_PRODUCTION = APP_ENV in ("production", "prod")

# Load local .env if present
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH, override=True)
else:
    load_dotenv(override=True)

# Data & media directories with automatic existence guarantee
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

MEDIA_DIR = ROOT_DIR / "generated_images"
MEDIA_DIR.mkdir(exist_ok=True)

AUDIO_DIR = ROOT_DIR / "generated_audio"
AUDIO_DIR.mkdir(exist_ok=True)

# Database URL with SQLite WAL default
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'app.db'}")

# Security configurations
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "25"))
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "45"))
ENABLE_RATE_LIMITING = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
ALLOWED_CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_CORS_ORIGINS", "http://localhost:8501,http://127.0.0.1:8501").split(",")
    if origin.strip()
]

def get_config_var(name: str, default: str = "") -> str:
    """
    Retrieves a configuration key safely from os.environ, .env, or Streamlit st.secrets.
    Guarantees no whitespace leaks and never prints secrets to stdout.
    """
    # 1. Environment / .env
    val = os.getenv(name, "").strip()
    if val:
        return val

    # 2. Streamlit Cloud Secrets (for cloud deployment fallback)
    try:
        import streamlit as st
        if hasattr(st, "secrets") and name in st.secrets:
            return str(st.secrets[name]).strip()
    except Exception:
        pass

    return default

def save_config_var(name: str, value: str) -> bool:
    """
    Persists a key to the local .env file securely.
    Sets restrictive file permissions where supported.
    """
    try:
        # Prevent injection of multiline or malformed key names
        clean_name = name.strip().replace("\n", "").replace("\r", "")
        clean_val = value.strip().replace("\n", "").replace("\r", "")

        if not ENV_PATH.exists():
            ENV_PATH.touch(mode=0o600, exist_ok=True)

        set_key(str(ENV_PATH), clean_name, clean_val)
        os.environ[clean_name] = clean_val

        # Try to restrict file permissions on POSIX systems
        try:
            os.chmod(str(ENV_PATH), 0o600)
        except Exception:
            pass

        return True
    except Exception:
        return False

def get_env_summary():
    """Returns safe summary of configured providers and environment state."""
    return validate_environment()
