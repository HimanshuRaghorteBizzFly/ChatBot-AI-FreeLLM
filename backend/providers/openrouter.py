"""
OpenRouter provider adapter.
Supports NVIDIA Nemotron 3.5 Super VL, Microsoft MAI-Image-2.7 Flash, Llama 3.3, and reasoning.
"""
import json
import time
import requests
from typing import List, Dict, Any, Generator, Optional
from backend.providers.base import BaseProvider
from backend.schemas.types import ModelCatalogItem
from backend.config import get_config_var

OPENROUTER_MODELS = [
    "nvidia/nemotron-3.5-super-vl:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemini-2.0-flash-exp:free",
    "qwen/qwen-2.5-coder-32b-instruct:free",
    "microsoft/mai-image-2.7-flash"
]

class OpenRouterProvider(BaseProvider):
    def __init__(self, api_key: Optional[str] = None):
        key = api_key or get_config_var("OPENROUTER_API_KEY")
        super().__init__("OpenRouter", key)
        self.base_url = "https://openrouter.ai/api/v1"

    def validate_credentials(self) -> bool:
        if not self.api_key:
            return False
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            resp = requests.get(f"{self.base_url}/auth/key", headers=headers, timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    def list_models(self) -> List[ModelCatalogItem]:
        # Return primary verified models
        return [
            ModelCatalogItem(
                id="nvidia/nemotron-3.5-super-vl:free",
                name="NVIDIA: Nemotron 3.5 Super VL (Free)",
                provider="NVIDIA / OpenRouter",
                category="Multimodal",
                description="NVIDIA flagship multimodal reasoning and vision model with thinking chain.",
                context_length=131072,
                is_free=True,
                capabilities=["chat", "reasoning", "multimodal", "streaming"],
                icon="🟢"
            ),
            ModelCatalogItem(
                id="microsoft/mai-image-2.7-flash",
                name="Microsoft AI: MAI-Image-2.7 Flash",
                provider="Microsoft / OpenRouter",
                category="Image",
                description="Ultra-fast diffusion-based image synthesis and editing model.",
                context_length=None,
                is_free=False,
                capabilities=["image"],
                icon="🎨"
            ),
            ModelCatalogItem(
                id="nvidia/nemotron-3.5-lightning:free",
                name="NVIDIA: Nemotron 3.5 Lightning (Free)",
                provider="NVIDIA / OpenRouter",
                category="Text",
                description="High-throughput low-latency LLM optimized for conversational tasks.",
                context_length=65536,
                is_free=True,
                capabilities=["chat", "streaming"],
                icon="⚡"
            ),
            ModelCatalogItem(
                id="meta-llama/llama-3.3-70b-instruct:free",
                name="Meta Llama 3.3 70B (Free)",
                provider="Meta / OpenRouter",
                category="Coding",
                description="State-of-the-art open weights coding and complex problem-solving model.",
                context_length=131072,
                is_free=True,
                capabilities=["chat", "coding", "streaming"],
                icon="🦙"
            ),
            ModelCatalogItem(
                id="qwen/qwen-2.5-coder-32b-instruct:free",
                name="Qwen 2.5 Coder 32B (Free)",
                provider="Qwen / OpenRouter",
                category="Coding",
                description="Specialized high-performance programming assistant.",
                context_length=32768,
                is_free=True,
                capabilities=["chat", "coding", "streaming"],
                icon="💻"
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
            yield "⚠️ **OpenRouter API Key Missing.** Please configure it in Settings or Sidebar."
            return

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "AI ChatBot Studio"
        }

        formatted = []
        if system_prompt:
            formatted.append({"role": "system", "content": system_prompt})
        for m in messages:
            role = "user" if m.get("role") == "user" else "assistant"
            formatted.append({"role": role, "content": str(m.get("content", ""))})

        payload = {
            "model": model,
            "messages": formatted,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }

        try:
            resp = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, stream=True, timeout=60)
            if resp.status_code != 200:
                err_msg = resp.text
                try:
                    err_msg = resp.json().get("error", {}).get("message", resp.text)
                except Exception:
                    pass
                yield f"⚠️ **OpenRouter Error ({resp.status_code}):** {err_msg}"
                return

            thinking_open = False
            for line in resp.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue
                data_str = line[6:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    choices = chunk.get("choices", [])
                    if choices:
                        delta = choices[0].get("delta", {})
                        reasoning = delta.get("reasoning_content") or delta.get("reasoning")
                        if reasoning:
                            if not thinking_open:
                                yield "> 🧠 **Thinking Process:**\n> "
                                thinking_open = True
                            yield reasoning.replace("\n", "\n> ")
                        
                        content = delta.get("content")
                        if content:
                            if thinking_open:
                                yield "\n\n---\n\n"
                                thinking_open = False
                            yield content
                except Exception:
                    pass
        except Exception as e:
            yield f"⚠️ **Connection Error:** {str(e)}"

def format_openrouter_model_name(model_id: str) -> str:
    """Format an OpenRouter model ID into a user-friendly label."""
    labels = {
        "nvidia/nemotron-3.5-super-vl:free": "🟢 NVIDIA Nemotron 3.5 Super VL (Free)",
        "meta-llama/llama-3.3-70b-instruct:free": "🦙 Meta Llama 3.3 70B (Free)",
        "google/gemini-2.0-flash-exp:free": "✨ Google Gemini 2.0 Flash (Free)",
        "qwen/qwen-2.5-coder-32b-instruct:free": "💻 Qwen 2.5 Coder 32B (Free)",
        "microsoft/mai-image-2.7-flash": "🎨 Microsoft MAI-Image-2.7 Flash"
    }
    return labels.get(model_id, model_id.split("/")[-1].replace(":free", " (Free)").title())
