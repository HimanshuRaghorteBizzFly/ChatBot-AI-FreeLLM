"""
Google Gemini provider adapter using official google-genai SDK.
Supports gemini-3.1-flash-lite, gemini-3.8-flash, vision, and embeddings.
Hardened with secret sanitization and graceful fallbacks.
"""
from typing import List, Dict, Any, Generator, Optional
from backend.providers.base import BaseProvider
from backend.schemas.types import ModelCatalogItem
from backend.config import get_config_var
from backend.security import sanitize_text

class GeminiProvider(BaseProvider):
    def __init__(self, api_key: Optional[str] = None):
        key = api_key or get_config_var("GEMINI_API_KEY")
        super().__init__("Google Gemini", key)

    def validate_credentials(self) -> bool:
        if not self.api_key:
            return False
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            res = client.models.generate_content(model="gemini-3.1-flash-lite", contents="Ping")
            return bool(res.text)
        except Exception:
            return False

    def list_models(self) -> List[ModelCatalogItem]:
        return [
            ModelCatalogItem(
                id="gemini-3.1-flash-lite",
                name="Gemini 3.1 Flash Lite",
                provider="Google",
                category="Multimodal",
                description="Ultra-fast, cost-effective multimodal model with low latency.",
                context_length=1048576,
                is_free=True,
                capabilities=["chat", "vision", "streaming", "multimodal"],
                icon="✨"
            ),
            ModelCatalogItem(
                id="gemini-3.8-flash",
                name="Gemini 3.8 Flash",
                provider="Google",
                category="Reasoning",
                description="Google's next-gen high-efficiency reasoning and analysis engine.",
                context_length=1048576,
                is_free=True,
                capabilities=["chat", "reasoning", "vision", "streaming"],
                icon="🚀"
            ),
            ModelCatalogItem(
                id="gemini-3.5-flash",
                name="Gemini 3.5 Flash",
                provider="Google",
                category="Text",
                description="Balanced intelligence and throughput for high-volume tasks.",
                context_length=1048576,
                is_free=True,
                capabilities=["chat", "streaming"],
                icon="⚡"
            )
        ]

    def chat_stream(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        if not self.api_key:
            yield "⚠️ **Gemini API Key Missing.** Please add your free key in Settings or the API Keys panel."
            return

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            contents = []
            if system_prompt:
                contents.append(types.Content(role="user", parts=[types.Part.from_text(text=f"System Instruction: {system_prompt}")]))
                contents.append(types.Content(role="model", parts=[types.Part.from_text(text="Understood.")]))

            for m in messages:
                role = "user" if m.get("role") == "user" else "model"
                text_content = str(m.get("content", ""))
                contents.append(types.Content(role=role, parts=[types.Part.from_text(text=text_content)]))

            target_model = model or "gemini-3.1-flash-lite"
            try:
                response_stream = client.models.generate_content_stream(model=target_model, contents=contents)
                for chunk in response_stream:
                    if chunk.text:
                        yield chunk.text
            except Exception as e:
                err_str = str(e)
                if ("404" in err_str or "503" in err_str) and target_model != "gemini-3.1-flash-lite":
                    yield "*(Notice: Auto-routed to active model **gemini-3.1-flash-lite**)*\n\n"
                    stream_fallback = client.models.generate_content_stream(model="gemini-3.1-flash-lite", contents=contents)
                    for chunk in stream_fallback:
                        if chunk.text:
                            yield chunk.text
                elif "401" in err_str or "API_KEY_INVALID" in err_str:
                    yield "⚠️ **Gemini Authentication Error:** Invalid API Key."
                elif "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    yield "⚠️ **Gemini Rate Limit (429):** Free tier quota momentarily exceeded. Please wait a moment."
                else:
                    yield f"⚠️ **Gemini API Error:** {sanitize_text(err_str)}"
        except Exception as e:
            yield f"⚠️ **Gemini Client Error:** {sanitize_text(str(e))}"

    def analyze_image(self, image_bytes: bytes, prompt: str, mime_type: str = "image/jpeg", model: str = "gemini-3.1-flash-lite") -> str:
        """Analyzes an image using Gemini's native multimodal capabilities."""
        if not self.api_key:
            return "⚠️ Gemini API key required for vision analysis."
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            text_part = types.Part.from_text(text=prompt or "Describe this image in detail.")

            res = client.models.generate_content(
                model=model,
                contents=[types.Content(role="user", parts=[image_part, text_part])]
            )
            return res.text or "*(No visual analysis returned)*"
        except Exception as e:
            return f"⚠️ Vision Error: {sanitize_text(str(e))}"

    def generate_embeddings(self, text: str, model: str = "text-embedding-004") -> List[float]:
        """Generates real vector embeddings using Gemini SDK with deterministic fallback."""
        if not self.api_key:
            # Deterministic fallback vector
            import hashlib
            h = hashlib.sha256(text.encode()).digest()
            return [float(b) / 255.0 for b in h] * 24
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            res = client.models.embed_content(model=model, contents=text)
            if hasattr(res, "embedding") and hasattr(res.embedding, "values"):
                return list(res.embedding.values)
            elif hasattr(res, "embeddings") and res.embeddings:
                return list(res.embeddings[0].values)
            return [0.0] * 768
        except Exception:
            # Fallback pseudo-vector deterministic hash
            import hashlib
            h = hashlib.sha256(text.encode()).digest()
            return [float(b) / 255.0 for b in h] * 24  # 768 dim vector
