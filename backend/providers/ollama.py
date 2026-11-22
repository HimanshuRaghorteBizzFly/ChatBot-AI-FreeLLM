"""
Ollama provider adapter.
Supports local Ollama (http://localhost:11434) and Ollama Cloud.
"""
from typing import List, Dict, Any, Generator, Optional
from backend.providers.base import BaseProvider
from backend.schemas.types import ModelCatalogItem
from backend.config import get_config_var

class OllamaProvider(BaseProvider):
    def __init__(self, host: str = "http://localhost:11434", api_key: Optional[str] = None):
        key = api_key or get_config_var("OLLAMA_API_KEY")
        super().__init__("Ollama", key)
        self.host = host

    def validate_credentials(self) -> bool:
        try:
            from ollama import Client
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key and "ollama.com" in self.host else {}
            client = Client(host=self.host, headers=headers, timeout=2.0)
            client.list()
            return True
        except Exception:
            return False

    def list_models(self) -> List[ModelCatalogItem]:
        default_models = [
            ModelCatalogItem(
                id="llama3.3:latest",
                name="Llama 3.3 (Local)",
                provider="Ollama",
                category="Text",
                description="High performance local LLM running on your local machine.",
                context_length=131072,
                is_free=True,
                capabilities=["chat", "streaming"],
                icon="🦙"
            ),
            ModelCatalogItem(
                id="gpt-oss:20b",
                name="GPT-OSS 20B (Ollama)",
                provider="Ollama",
                category="Text",
                description="Open architecture conversational model for desktop hardware.",
                context_length=32768,
                is_free=True,
                capabilities=["chat", "streaming"],
                icon="🤖"
            )
        ]
        try:
            from ollama import Client
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key and "ollama.com" in self.host else {}
            client = Client(host=self.host, headers=headers, timeout=2.0)
            res = client.list()
            dynamic = []
            for m in res.models:
                m_name = getattr(m, "model", "")
                if m_name:
                    dynamic.append(
                        ModelCatalogItem(
                            id=m_name,
                            name=f"{m_name} (Ollama)",
                            provider="Ollama",
                            category="Text",
                            description=f"Model {m_name} discovered from {self.host}.",
                            context_length=32768,
                            is_free=True,
                            capabilities=["chat", "streaming"],
                            icon="🦙"
                        )
                    )
            return dynamic if dynamic else default_models
        except Exception:
            return default_models

    def chat_stream(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        try:
            from ollama import Client, ResponseError
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key and "ollama.com" in self.host else {}
            client = Client(host=self.host, headers=headers)

            formatted = []
            if system_prompt:
                formatted.append({"role": "system", "content": system_prompt})
            for m in messages:
                role = "user" if m.get("role") == "user" else "assistant"
                formatted.append({"role": role, "content": str(m.get("content", ""))})

            stream = client.chat(model=model, messages=formatted, stream=True)
            for chunk in stream:
                content = chunk.get("message", {}).get("content", "")
                if content:
                    yield content
        except ResponseError as e:
            if getattr(e, "status_code", None) == 402:
                yield "⚠️ **Ollama Cloud Credits Required (HTTP 402)**. Switch to **Google Gemini** or **NVIDIA Nemotron** for free access."
            else:
                yield f"⚠️ **Ollama Error:** {str(e)}"
        except Exception as e:
            yield f"⚠️ **Ollama Connection Error:** {str(e)}"
