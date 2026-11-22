"""
Model Catalog Service.
Maintains live catalog across all modalities, search, sorting, and comparison.
"""
from typing import List, Dict, Any, Optional
from backend.providers.registry import registry
from backend.schemas.types import ModelCatalogItem

# Expanded Master Model Catalog across all modalities
MASTER_CATALOG: List[ModelCatalogItem] = [
    # Multimodal & Vision
    ModelCatalogItem(
        id="nvidia/nemotron-3.5-super-vl:free",
        name="NVIDIA: Nemotron 3.5 Super VL",
        provider="NVIDIA / OpenRouter",
        category="Multimodal",
        description="NVIDIA frontier multimodal vision-language model with native chain-of-thought.",
        context_length=131072,
        is_free=True,
        capabilities=["chat", "vision", "reasoning", "multimodal", "streaming"],
        icon="🟢"
    ),
    ModelCatalogItem(
        id="gemini-3.1-flash-lite",
        name="Google: Gemini 3.1 Flash Lite",
        provider="Google Gemini",
        category="Multimodal",
        description="High speed multimodal model with 1M context, vision, and ultra-low TTFT.",
        context_length=1048576,
        is_free=True,
        capabilities=["chat", "vision", "multimodal", "streaming"],
        icon="✨"
    ),
    ModelCatalogItem(
        id="gemini-3.8-flash",
        name="Google: Gemini 3.8 Flash",
        provider="Google Gemini",
        category="Reasoning",
        description="Next-generation reasoning flagship from Google with multi-step analytical capabilities.",
        context_length=1048576,
        is_free=True,
        capabilities=["chat", "reasoning", "vision", "streaming"],
        icon="🚀"
    ),

    # Fast Inference & Reasoning
    ModelCatalogItem(
        id="openai/gpt-oss-120b",
        name="Groq: GPT-OSS 120B",
        provider="Groq",
        category="Reasoning",
        description="120-billion parameter reasoning model executing at 500+ tokens/sec on Groq LPUs.",
        context_length=131072,
        is_free=True,
        capabilities=["chat", "reasoning", "coding", "streaming"],
        icon="⚡"
    ),
    ModelCatalogItem(
        id="openai/gpt-oss-20b",
        name="Groq: GPT-OSS 20B",
        provider="Groq",
        category="Text",
        description="Ultra-responsive conversational model designed for real-time interactivity.",
        context_length=65536,
        is_free=True,
        capabilities=["chat", "streaming"],
        icon="🚀"
    ),
    ModelCatalogItem(
        id="Free GPT-4o Mini",
        name="Free AI: GPT-4o Mini (Cloud)",
        provider="Free AI",
        category="Text",
        description="Zero-setup free cloud intelligence accessible without keys or subscriptions.",
        context_length=16384,
        is_free=True,
        api_key_required=False,
        capabilities=["chat", "streaming"],
        icon="🌟"
    ),

    # Image Generation
    ModelCatalogItem(
        id="microsoft/mai-image-2.7-flash",
        name="Microsoft AI: MAI-Image-2.7 Flash",
        provider="Microsoft / OpenRouter",
        category="Image",
        description="Frontier diffusion visual synthesis model with high prompt adherence and low latency.",
        context_length=None,
        is_free=True,
        capabilities=["image", "text_to_image"],
        icon="🎨"
    ),

    # Video Generation
    ModelCatalogItem(
        id="video-diffusion-v1",
        name="VideoStudio AI: Cinematic Diffusion",
        provider="Open Media",
        category="Video",
        description="High-definition cinematic short-form video generation from text and image prompts.",
        context_length=None,
        is_free=True,
        capabilities=["video", "text_to_video"],
        icon="🎬"
    ),

    # Speech (TTS & STT)
    ModelCatalogItem(
        id="whisper-large-v3",
        name="Groq: Whisper Large V3 (Speech-to-Text)",
        provider="Groq",
        category="Speech",
        description="State-of-the-art multilingual audio transcription and translation engine.",
        context_length=None,
        is_free=True,
        capabilities=["speech_to_text"],
        icon="🎙️"
    ),
    ModelCatalogItem(
        id="tts-neural-hd",
        name="SpeechStudio: Neural Text-to-Speech",
        provider="Speech Studio",
        category="Speech",
        description="Natural human-sounding voice synthesis with multi-language and accent controls.",
        context_length=None,
        is_free=True,
        capabilities=["text_to_speech"],
        icon="🔊"
    ),

    # Coding
    ModelCatalogItem(
        id="meta-llama/llama-3.3-70b-instruct:free",
        name="Meta: Llama 3.3 70B Instruct",
        provider="Meta / OpenRouter",
        category="Coding",
        description="Versatile open foundation model fine-tuned for code generation and refactoring.",
        context_length=131072,
        is_free=True,
        capabilities=["chat", "coding", "streaming"],
        icon="🦙"
    ),
    ModelCatalogItem(
        id="qwen/qwen-2.5-coder-32b-instruct:free",
        name="Qwen: Qwen 2.5 Coder 32B",
        provider="Qwen / OpenRouter",
        category="Coding",
        description="Specialized high-accuracy programming assistant supporting 90+ programming languages.",
        context_length=32768,
        is_free=True,
        capabilities=["chat", "coding", "streaming"],
        icon="💻"
    ),

    # Embeddings & Reranking
    ModelCatalogItem(
        id="text-embedding-004",
        name="Google: Text Embedding 004",
        provider="Google Gemini",
        category="Embeddings",
        description="768-dimensional dense vector embeddings for semantic search and RAG.",
        context_length=2048,
        is_free=True,
        capabilities=["embeddings"],
        icon="🧬"
    ),
    ModelCatalogItem(
        id="cross-encoder-rerank-v1",
        name="Semantic Reranker Studio v1",
        provider="AI Studio",
        category="Reranking",
        description="Deep cross-attention document relevance scoring and precision reranking.",
        context_length=4096,
        is_free=True,
        capabilities=["reranking"],
        icon="📊"
    )
]

def get_model_catalog(
    category: str = "All",
    search_query: str = "",
    free_only: bool = False
) -> List[ModelCatalogItem]:
    """Filters model catalog based on category, search, and pricing."""
    results = MASTER_CATALOG
    if category and category != "All":
        cat_lower = category.lower()
        results = [
            m for m in results
            if m.category.lower() == cat_lower or any(cat_lower in c.lower() for c in m.capabilities)
        ]
    if free_only:
        results = [m for m in results if m.is_free]
    if search_query:
        q = search_query.lower().strip()
        results = [
            m for m in results
            if q in m.name.lower() or q in m.provider.lower() or q in m.description.lower() or q in m.id.lower()
        ]
    return results

def get_model_by_id(model_id: str) -> Optional[ModelCatalogItem]:
    for m in MASTER_CATALOG:
        if m.id == model_id:
            return m
    return None

def get_catalog_models() -> List[ModelCatalogItem]:
    """Returns the full master catalog list."""
    return MASTER_CATALOG

def filter_catalog(
    category: str = "All",
    is_free: Optional[bool] = None,
    search: str = ""
) -> List[ModelCatalogItem]:
    """Filters model catalog with flexible category, free/paid, and search parameters."""
    return get_model_catalog(
        category=category,
        search_query=search,
        free_only=(is_free is True)
    ) if is_free is not False else [
        m for m in get_model_catalog(category=category, search_query=search, free_only=False)
        if not m.is_free
    ]
