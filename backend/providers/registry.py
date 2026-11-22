"""
Central provider registry for discovering and executing AI adapters.
"""
from typing import Dict, Any, List, Optional
from backend.providers.base import BaseProvider
from backend.providers.openrouter import OpenRouterProvider
from backend.providers.gemini import GeminiProvider
from backend.providers.groq import GroqProvider
from backend.providers.ollama import OllamaProvider
from backend.providers.free_ai import FreeAIProvider
from backend.schemas.types import ModelCatalogItem

class ProviderRegistry:
    def __init__(self):
        self._providers: Dict[str, BaseProvider] = {}
        self._init_providers()

    def _init_providers(self):
        self._providers = {
            "OpenRouter": OpenRouterProvider(),
            "Google Gemini": GeminiProvider(),
            "Groq": GroqProvider(),
            "Ollama": OllamaProvider(),
            "Free AI": FreeAIProvider()
        }

    def get_provider(self, name: str) -> Optional[BaseProvider]:
        # Handle friendly names
        if "OpenRouter" in name or "NVIDIA" in name:
            return self._providers.get("OpenRouter")
        if "Gemini" in name:
            return self._providers.get("Google Gemini")
        if "Groq" in name:
            return self._providers.get("Groq")
        if "Ollama" in name:
            return self._providers.get("Ollama")
        if "Free" in name:
            return self._providers.get("Free AI")
        return self._providers.get(name)

    def list_all_models(self) -> List[ModelCatalogItem]:
        all_models = []
        for provider in self._providers.values():
            try:
                models = provider.list_models()
                all_models.extend(models)
            except Exception:
                pass
        return all_models

    def list_providers(self) -> List[str]:
        return list(self._providers.keys())

    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        status = {}
        for name, provider in self._providers.items():
            status[name] = {
                "name": name,
                "configured": bool(provider.api_key) or name == "Free AI",
                "valid": provider.validate_credentials() if (provider.api_key or name == "Free AI") else False,
                "model_count": len(provider.list_models())
            }
        return status

# Singleton registry
registry = ProviderRegistry()
