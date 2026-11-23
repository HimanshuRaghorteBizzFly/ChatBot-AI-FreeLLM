"""
Structured, secret-sanitizing logging system.
Ensures zero credentials, passwords, or raw tokens are ever written to stdout or log files.
Provides request ID tracing, structured JSON-compatible formatting, and log levels.
"""
import logging
import sys
from pathlib import Path
from typing import Optional, Any
from backend.security import sanitize_text

# Create logs directory
LOG_DIR = Path(__file__).resolve().parent.parent / "data" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

class SanitizingFormatter(logging.Formatter):
    """Custom logging formatter that strips sensitive credentials from all log output."""
    def format(self, record: logging.LogRecord) -> str:
        original = super().format(record)
        return sanitize_text(original)

def setup_logger(name: str = "ai_studio") -> logging.Logger:
    """Configures and returns a sanitizing structured logger."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = SanitizingFormatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler (Streamlit / stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler with error suppression
    try:
        file_handler = logging.FileHandler(str(LOG_FILE), encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        pass

    return logger

app_logger = setup_logger("ai_studio")

def log_event(level: str, event_type: str, message: str, request_id: Optional[str] = None, **kwargs):
    """
    Emits a structured log event with optional request ID tracing.
    """
    req_tag = f"[{request_id}] " if request_id else ""
    extra_str = f" | {kwargs}" if kwargs else ""
    safe_msg = f"{req_tag}[{event_type}] {message}{extra_str}"
    
    log_func = getattr(app_logger, level.lower(), app_logger.info)
    log_func(safe_msg)
