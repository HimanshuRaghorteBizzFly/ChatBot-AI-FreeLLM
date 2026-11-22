"""
Groq provider adapter.
Supports ultra-fast LPU inference (GPT-OSS 120B/20B, Qwen 3.8) and Whisper Speech-to-Text.
"""
import io
import json
import time
import requests
from typing import List, Dict, Any, Generator, Optional
from backend.providers.base import BaseProvider
from backend.schemas.types import ModelCatalogItem
from backend.config import get_config_var

class GroqProvider(BaseProvider):
    def __init__(self, api_key: Optional[str] = None):
        key = api_key or get_config_var("GROQ_API_KEY")
        super().__init__("Groq", key)
        self.base_url = "https://api.groq.com/openai/v1"

    def validate_credentials(self) -> bool:
        if not self.api_key:
            return False
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            resp = requests.get(f"{self.base_url}/models", headers=headers, timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    def list_models(self) -> List[ModelCatalogItem]:
        return [
            ModelCatalogItem(
                id="openai/gpt-oss-120b",
                name="GPT-OSS 120B (Groq LPU)",
                provider="Groq",
                category="Reasoning",
                description="120B flagship open architecture running at 500+ tokens/sec on Groq LPU.",
                context_length=131072,
                is_free=True,
                capabilities=["chat", "reasoning", "streaming", "coding"],
                icon="⚡"
            ),
            ModelCatalogItem(
                id="openai/gpt-oss-20b",
                name="GPT-OSS 20B (Groq LPU)",
                provider="Groq",
                category="Text",
                description="Ultra-low latency model for instant conversational turnarounds.",
                context_length=65536,
                is_free=True,
                capabilities=["chat", "streaming"],
                icon="🚀"
            ),
            ModelCatalogItem(
                id="qwen/qwen3.8-27b",
                name="Qwen 3.8 27B",
                provider="Groq",
                category="Coding",
                description="High performance multilingual coding and math model.",
                context_length=32768,
                is_free=True,
                capabilities=["chat", "coding", "streaming"],
                icon="💻"
            ),
            ModelCatalogItem(
                id="whisper-large-v3",
                name="Whisper Large V3 (Speech-to-Text)",
                provider="Groq",
                category="Speech",
                description="Near-instantaneous audio transcription and speech-to-text.",
                context_length=None,
                is_free=True,
                capabilities=["speech_to_text"],
                icon="🎙️"
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
            yield "⚠️ **Groq API Key Missing.** Please configure it in Settings or Sidebar."
            return

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        formatted = []
        if system_prompt:
            formatted.append({"role": "system", "content": system_prompt})
        for m in messages:
            role = "user" if m.get("role") == "user" else "assistant"
            formatted.append({"role": role, "content": str(m.get("content", ""))})

        target_model = model or "openai/gpt-oss-120b"
        payload = {
            "model": target_model,
            "messages": formatted,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }

        # Automatic retry for network/DNS glitches
        resp = None
        for attempt in range(3):
            try:
                resp = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, stream=True, timeout=30)
                break
            except Exception as e:
                if attempt == 2:
                    yield f"⚠️ **Groq Network Error:** {str(e)}"
                    return
                time.sleep(1)

        if resp.status_code != 200:
            err_msg = resp.text
            try:
                err_msg = resp.json().get("error", {}).get("message", resp.text)
            except Exception:
                pass
            yield f"⚠️ **Groq API Error ({resp.status_code}):** {err_msg}"
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

    def transcribe_audio(self, audio_bytes: bytes, filename: str = "audio.wav") -> str:
        """Transcribes speech to text using Groq's ultra-fast Whisper Large V3."""
        if not self.api_key:
            return "⚠️ Groq API Key required for Whisper speech transcription."
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            files = {"file": (filename, audio_bytes, "audio/wav")}
            data = {"model": "whisper-large-v3", "response_format": "json"}
            resp = requests.post(f"{self.base_url}/audio/transcriptions", headers=headers, files=files, data=data, timeout=60)
            if resp.status_code == 200:
                return resp.json().get("text", "")
            return f"⚠️ Transcription failed ({resp.status_code}): {resp.text}"
        except Exception as e:
            return f"⚠️ Speech Error: {str(e)}"
