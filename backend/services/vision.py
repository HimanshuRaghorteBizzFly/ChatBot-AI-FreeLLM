"""
Vision Studio service.
Provides multimodal visual analysis using Gemini and OpenRouter vision models.
"""
from typing import Dict, Any
from backend.providers.registry import registry
from backend.repositories.storage import log_usage

def analyze_vision_image(image_bytes: bytes, prompt: str, model: str = "gemini-3.1-flash-lite", mime_type: str = "image/jpeg") -> str:
    gemini = registry.get_provider("Google Gemini")
    if not gemini:
        return "⚠️ Google Gemini provider not available for vision."

    result = gemini.analyze_image(image_bytes=image_bytes, prompt=prompt, mime_type=mime_type, model=model)
    log_usage("Google Gemini", model, "vision", cost_estimate=0.0)
    return result
