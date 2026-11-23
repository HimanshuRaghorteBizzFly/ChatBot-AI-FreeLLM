"""
Free AI provider adapter (zero setup, no API key required).
Provides instant cloud LLM with zero-config pipeline and offline resilience.
"""
import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Generator, Optional
from backend.providers.base import BaseProvider
from backend.schemas.types import ModelCatalogItem
from backend.security import sanitize_text

class FreeAIProvider(BaseProvider):
    def __init__(self):
        super().__init__("Free AI", "")
        self.endpoint = "https://text.pollinations.ai/"

    def validate_credentials(self) -> bool:
        return True

    def list_models(self) -> List[ModelCatalogItem]:
        return [
            ModelCatalogItem(
                id="Free GPT-4o Mini",
                name="Free GPT-4o Mini (Cloud)",
                provider="Free AI",
                category="Text",
                description="Instant free cloud LLM with zero setup, zero credit card, and zero API key.",
                context_length=16384,
                is_free=True,
                api_key_required=False,
                capabilities=["chat", "streaming"],
                icon="🌟"
            )
        ]

    def chat_stream(
        self,
        messages: List[Dict[str, Any]],
        model: str = "Free GPT-4o Mini",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        formatted = []
        if system_prompt:
            formatted.append({"role": "system", "content": system_prompt})
        for m in messages:
            role = "user" if m.get("role") == "user" else "assistant"
            formatted.append({"role": role, "content": str(m.get("content", ""))})

        payload = {"messages": formatted, "model": "openai", "stream": True}
        try:
            req = urllib.request.Request(
                self.endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ChatBot-AI/1.0"
                }
            )
            with urllib.request.urlopen(req, timeout=25) as resp:
                for line in resp:
                    line_str = line.decode("utf-8", errors="ignore").strip()
                    if line_str.startswith("data: "):
                        data_str = line_str[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            choices = chunk.get("choices", [])
                            if choices:
                                delta = choices[0].get("delta", {})
                                content = delta.get("content")
                                if content:
                                    yield content
                        except Exception:
                            pass
        except urllib.error.URLError as e:
            # Clean network offline or DNS block handling
            yield f"⚠️ **Free AI Service Notice:** Unable to reach free cloud endpoint ({sanitize_text(str(e))}). Please check your internet connection or use an API key for Google Gemini, Groq, or OpenRouter in the sidebar."
        except Exception as e:
            yield f"⚠️ **Free AI Service Error:** {sanitize_text(str(e))}"
