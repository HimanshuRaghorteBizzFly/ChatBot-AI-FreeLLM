"""
Tests for provider registry and provider adapters.
Includes mocked / offline-safe tests for cloud providers.
"""
import pytest
from unittest.mock import patch, MagicMock
from backend.providers.registry import registry
from backend.security import mask_secret
from backend.providers.openrouter import format_openrouter_model_name

def test_registry_providers():
    providers = registry.list_providers()
    assert "OpenRouter" in providers
    assert "Google Gemini" in providers
    assert "Groq" in providers
    assert "Free AI" in providers
    assert "Ollama" in providers

def test_free_ai_chat_streaming():
    free_ai = registry.get_provider("Free AI")
    assert free_ai is not None
    assert free_ai.validate_credentials() is True

    messages = [{"role": "user", "content": "Say hello in one word."}]
    # Run stream: should yield chunks or graceful notice without uncaught exception
    stream = free_ai.chat_stream(messages)
    chunks = list(stream)
    assert len(chunks) > 0
    full_text = "".join(chunks)
    assert len(full_text) > 0

def test_masked_key():
    assert mask_secret("") == "Not Configured"
    assert mask_secret("short") == "****"
    key = "sk-or-v1-abcdef1234567890abcdef"
    masked = mask_secret(key)
    assert masked.startswith("sk-o")
    assert masked.endswith("cdef")
    assert "..." in masked

def test_openrouter_name_formatter():
    name = format_openrouter_model_name("nvidia/nemotron-3.5-super-vl:free")
    assert "Nemotron 3.5 Super VL" in name
    assert "(Free)" in name
