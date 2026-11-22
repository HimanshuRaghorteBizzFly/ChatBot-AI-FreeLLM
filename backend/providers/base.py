"""
Abstract base class for all AI model providers.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Generator, Optional
from backend.schemas.types import ModelCatalogItem

class BaseProvider(ABC):
    """Common interface for AI providers."""
    
    def __init__(self, name: str, api_key: Optional[str] = None):
        self.name = name
        self.api_key = api_key or ""

    @abstractmethod
    def validate_credentials(self) -> bool:
        """Validates if the credentials are functional."""
        pass

    @abstractmethod
    def list_models(self) -> List[ModelCatalogItem]:
        """Returns catalog of supported models."""
        pass

    @abstractmethod
    def chat_stream(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        """Streams response tokens from the model."""
        pass

    def generate_image(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        """Generates an image if supported by the provider."""
        raise NotImplementedError(f"{self.name} does not support image generation.")

    def generate_embeddings(self, text: str, model: str) -> List[float]:
        """Generates vector embeddings if supported by the provider."""
        raise NotImplementedError(f"{self.name} does not support vector embeddings.")
