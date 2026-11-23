"""
Vision Studio service.
Provides multimodal visual analysis using Gemini and OpenRouter vision models.
Hardened with image payload validation and secret sanitization.
"""
from typing import Dict, Any
from backend.providers.registry import registry
from backend.repositories.storage import log_usage
from backend.config import MAX_UPLOAD_SIZE_MB
from backend.security import sanitize_text

def analyze_vision_image(image_bytes: bytes, prompt: str, model: str = "gemini-3.1-flash-lite", mime_type: str = "image/jpeg") -> str:
    """
    Validates image payload and analyzes using Gemini Vision.
    """
    if not image_bytes:
        return "⚠️ Please provide an image to analyze."

    max_bytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(image_bytes) > max_bytes:
        return f"⚠️ Image exceeds maximum size of {MAX_UPLOAD_SIZE_MB}MB."

    gemini = registry.get_provider("Google Gemini")
    if not gemini:
        return "⚠️ Google Gemini provider not available for vision."

    clean_prompt = prompt.strip().replace("\x00", "")[:4000] if prompt else "Describe this image in detail."
    result = gemini.analyze_image(image_bytes=image_bytes, prompt=clean_prompt, mime_type=mime_type, model=model)
    log_usage("Google Gemini", model, "vision", cost_estimate=0.0)
    return sanitize_text(result)
