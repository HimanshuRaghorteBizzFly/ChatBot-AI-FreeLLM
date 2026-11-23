"""
Enterprise Security & Secret Management Module.
Provides zero-leak secret masking, text sanitization, API key validation,
path traversal defense, and environment configuration audits.
"""
import os
import re
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional, Set

# Regex patterns for popular API key formats and credentials
SENSITIVE_PATTERNS = [
    # OpenRouter / OpenAI-style secret keys
    (re.compile(r"sk-[a-zA-Z0-9_\-]{16,}", re.IGNORECASE), "[REDACTED_API_KEY]"),
    # Google AI Studio / Gemini API keys
    (re.compile(r"AIza[0-9A-Za-z\-_]{35}", re.IGNORECASE), "[REDACTED_GEMINI_KEY]"),
    # Groq API keys
    (re.compile(r"gsk_[a-zA-Z0-9]{20,}", re.IGNORECASE), "[REDACTED_GROQ_KEY]"),
    # Bearer tokens in headers or URLs
    (re.compile(r"Bearer\s+([a-zA-Z0-9_\.\-]+)", re.IGNORECASE), "Bearer [REDACTED_TOKEN]"),
    # Query parameter or JSON field api_key=...
    (re.compile(r"(?:api[_-]?key|token|secret|password)[\"'\s:=]+([a-zA-Z0-9_\-\.]{8,})", re.IGNORECASE), r"key=[REDACTED]"),
]

def mask_secret(secret: str, prefix_len: int = 4, suffix_len: int = 4) -> str:
    """
    Safely masks a sensitive secret string.
    Never exposes full contents: returns 'Not Configured', '****', or 'sk-o...446'.
    """
    if not secret or not isinstance(secret, str):
        return "Not Configured"
    secret = secret.strip()
    if not secret:
        return "Not Configured"
    if len(secret) <= (prefix_len + suffix_len):
        return "****"
    return f"{secret[:prefix_len]}...{secret[-suffix_len:]}"

def get_active_secrets() -> Set[str]:
    """Retrieves all non-empty secret values loaded in current environment."""
    known_secret_names = [
        "OPENROUTER_API_KEY",
        "GEMINI_API_KEY",
        "GROQ_API_KEY",
        "OLLAMA_API_KEY",
        "DATABASE_URL",
        "SECRET_KEY",
        "JWT_SECRET",
    ]
    secrets = set()
    for name in known_secret_names:
        val = os.getenv(name, "").strip()
        if val and len(val) >= 4:
            secrets.add(val)
    return secrets

def sanitize_text(text: Any, extra_secrets: Optional[List[str]] = None) -> str:
    """
    Strips and redacts any known secrets or regex patterns from text,
    ensuring that errors, logs, or stack traces never leak credentials.
    """
    if text is None:
        return ""
    clean_str = str(text)

    # 1. Redact known environment secrets explicitly
    all_secrets = get_active_secrets()
    if extra_secrets:
        for s in extra_secrets:
            if s and len(s) >= 4:
                all_secrets.add(s.strip())

    for secret in all_secrets:
        if secret in clean_str:
            clean_str = clean_str.replace(secret, f"[REDACTED_{mask_secret(secret, 2, 2)}]")

    # 2. Redact patterns matching regexes
    for pattern, replacement in SENSITIVE_PATTERNS:
        clean_str = pattern.sub(replacement, clean_str)

    return clean_str

def validate_api_key_format(provider: str, key: str) -> bool:
    """
    Validates structural format of an API key without making network requests.
    """
    if not key or not isinstance(key, str):
        return False
    k = key.strip()
    if len(k) < 8:
        return False

    prov_lower = provider.lower()
    if "openrouter" in prov_lower:
        return k.startswith("sk-or-") or k.startswith("sk-")
    elif "gemini" in prov_lower or "google" in prov_lower:
        return k.startswith("AIza") or len(k) >= 20
    elif "groq" in prov_lower:
        return k.startswith("gsk_") or len(k) >= 20
    elif "ollama" in prov_lower:
        return len(k) >= 6
    return len(k) >= 10

def safe_resolve_path(base_directory: Path, user_filename: str) -> Path:
    """
    Validates that a resolved path remains strictly confined within base_directory.
    Guards against directory traversal attacks (e.g., ../../path).
    """
    base_dir = Path(base_directory).resolve()
    # Remove null bytes and strip separators
    clean_filename = user_filename.replace("\x00", "").strip("/\\")
    target_path = (base_dir / clean_filename).resolve()

    if not str(target_path).startswith(str(base_dir)):
        raise ValueError(f"Path traversal detected: {user_filename} escapes boundary {base_dir}")

    return target_path

def generate_request_id() -> str:
    """Generates a unique request tracing identifier."""
    return f"req_{uuid.uuid4().hex[:12]}"

def validate_environment() -> Dict[str, Any]:
    """
    Validates backend environment configuration and reports health
    without exposing any secret values.
    """
    app_env = os.getenv("APP_ENV", "development").lower()
    
    providers_config = {
        "OpenRouter": bool(os.getenv("OPENROUTER_API_KEY", "").strip()),
        "Google Gemini": bool(os.getenv("GEMINI_API_KEY", "").strip()),
        "Groq": bool(os.getenv("GROQ_API_KEY", "").strip()),
        "Ollama": bool(os.getenv("OLLAMA_API_KEY", "").strip()),
        "Free AI": True,  # 100% free with no credentials required
    }
    
    has_at_least_one = any(providers_config.values())
    
    return {
        "app_env": app_env,
        "is_production": app_env in ("production", "prod"),
        "providers_configured": providers_config,
        "ready": has_at_least_one,
        "warnings": [] if has_at_least_one else ["No API keys configured. Running on Free AI (Instant) only."]
    }
