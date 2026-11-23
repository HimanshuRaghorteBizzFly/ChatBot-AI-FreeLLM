"""
Tests for security, key masking, text sanitization, path traversal, and input validation.
"""
import pytest
from pathlib import Path
from backend.security import (
    mask_secret,
    sanitize_text,
    validate_api_key_format,
    safe_resolve_path,
    validate_environment,
    generate_request_id
)
from backend.schemas.types import (
    ChatMessageSchema,
    ChatRequestSchema,
    ImageGenerationRequestSchema,
    AudioUploadValidation
)
from backend.repositories.storage import update_user_preferences, get_user_preferences

def test_mask_secret():
    assert mask_secret("") == "Not Configured"
    assert mask_secret(None) == "Not Configured"
    assert mask_secret("   ") == "Not Configured"
    assert mask_secret("123") == "****"
    assert mask_secret("short") == "****"

    key = "sk-or-v1-abcdef1234567890abcdef"
    masked = mask_secret(key)
    assert masked.startswith("sk-o")
    assert masked.endswith("cdef")
    assert "..." in masked
    assert "1234567890" not in masked

def test_sanitize_text_redaction():
    # Test redaction of standard key patterns
    raw_error = "Failed to authenticate request for Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xyz with sk-or-v1-9876543210fedcba123456 and AIzaSyD9876543210123456789012345678901"
    sanitized = sanitize_text(raw_error)

    assert "sk-or-v1-9876543210fedcba123456" not in sanitized
    assert "AIzaSyD9876543210123456789012345678901" not in sanitized
    assert "[REDACTED_API_KEY]" in sanitized
    assert "[REDACTED_GEMINI_KEY]" in sanitized

def test_validate_api_key_format():
    assert validate_api_key_format("OpenRouter", "sk-or-v1-12345678901234567890") is True
    assert validate_api_key_format("OpenRouter", "invalid_short") is False

    assert validate_api_key_format("Google Gemini", "AIzaSyD1234567890123456789012345678901") is True
    assert validate_api_key_format("Google Gemini", "short") is False

    assert validate_api_key_format("Groq", "gsk_1234567890abcdef1234567890") is True
    assert validate_api_key_format("Groq", "bad") is False

def test_safe_resolve_path_defense(tmp_path):
    base = tmp_path / "sandbox"
    base.mkdir()

    # Valid relative filename
    valid_path = safe_resolve_path(base, "report.pdf")
    assert str(valid_path).startswith(str(base))

    # Path traversal attempt
    with pytest.raises(ValueError, match="Path traversal detected"):
        safe_resolve_path(base, "../../etc/passwd")

    with pytest.raises(ValueError, match="Path traversal detected"):
        safe_resolve_path(base, "..\\..\\Windows\\System32\\cmd.exe")

def test_update_user_preferences_sql_injection_defense():
    # Valid preference update
    success = update_user_preferences(temperature=0.85, theme="Dark")
    assert success is True
    prefs = get_user_preferences()
    assert prefs["temperature"] == 0.85
    assert prefs["theme"] == "Dark"

    # Attempted SQL / Column injection via kwargs
    malicious_kwargs = {
        "theme": "Light",
        "malicious_col; DROP TABLE users; --": "bad_value",
        "nonexistent_column": 123
    }
    # Should safely ignore unwhitelisted column and update only whitelisted 'theme'
    update_user_preferences(**malicious_kwargs)
    prefs_after = get_user_preferences()
    assert prefs_after["theme"] == "Light"

def test_chat_message_schema_validation():
    # Valid message
    msg = ChatMessageSchema(role="user", content="Hello AI")
    assert msg.content == "Hello AI"

    # Blank message should fail
    with pytest.raises(ValueError):
        ChatMessageSchema(role="user", content="   ")

def test_image_request_schema_validation():
    # Valid schema
    req = ImageGenerationRequestSchema(prompt="A futuristic neon city", aspect_ratio="16:9")
    assert req.aspect_ratio == "16:9"

    # Invalid aspect ratio should fail
    with pytest.raises(ValueError):
        ImageGenerationRequestSchema(prompt="City", aspect_ratio="21:9")

def test_audio_upload_validation():
    # Valid audio
    audio = AudioUploadValidation(filename="voice.mp3", size_bytes=1024)
    assert audio.filename == "voice.mp3"

    # Invalid extension
    with pytest.raises(ValueError, match="Unsupported audio format"):
        AudioUploadValidation(filename="exploit.exe", size_bytes=1024)

    # Oversized payload
    with pytest.raises(ValueError):
        AudioUploadValidation(filename="huge.mp3", size_bytes=30 * 1024 * 1024)

def test_request_id_generation():
    req_id = generate_request_id()
    assert req_id.startswith("req_")
    assert len(req_id) >= 12
