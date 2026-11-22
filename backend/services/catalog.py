"""
Model Catalog Service.
Maintains live catalog across all modalities matching LLM Studio Pro reference catalog.
"""
from typing import List, Dict, Any, Optional
from backend.schemas.types import ModelCatalogItem

# Expanded Master Model Catalog matching reference layout
MASTER_CATALOG: List[ModelCatalogItem] = [
    # --- Top Row from Reference Image ---
    ModelCatalogItem(
        id="openai/gpt-4o",
        name="GPT-4o",
        provider="OpenAI",
        category="Multimodal",
        description="OpenAI's most capable multimodal model for text, vision, and reasoning.",
        context_length=128000,
        is_free=True,  # Free access via Free AI Cloud pipeline
        pricing="Free tier",
        capabilities=["text", "image", "vision", "chat"],
        icon="⚡"
    ),
    ModelCatalogItem(
        id="google/gemini-2.5-flash",
        name="Gemini 2.5 Flash",
        provider="Google Gemini",
        category="Multimodal",
        description="Google's latest fast and efficient multimodal model with strong reasoning.",
        context_length=1000000,
        is_free=True,
        pricing="Free",
        capabilities=["text", "image", "vision", "chat"],
        icon="✨"
    ),
    ModelCatalogItem(
        id="anthropic/claude-3.7-sonnet",
        name="Claude 3.7 Sonnet",
        provider="Anthropic",
        category="Reasoning",
        description="Anthropic's latest model for complex reasoning and long context tasks.",
        context_length=200000,
        is_free=False,
        pricing="$3 / 1M",
        capabilities=["text", "reasoning", "coding"],
        icon="🧠"
    ),
    ModelCatalogItem(
        id="meta-llama/llama-3.3-70b-instruct:free",
        name="Llama 3.3 70B",
        provider="Meta Llama",
        category="Multimodal",
        description="Meta's open, efficient model for broad AI applications and reasoning.",
        context_length=128000,
        is_free=True,
        pricing="Free",
        capabilities=["text", "multimodal", "code"],
        icon="🦙"
    ),

    # --- Second Row from Reference Image ---
    ModelCatalogItem(
        id="black-forest-labs/flux-1-schnell",
        name="Flux.1 Pro",
        provider="Black Forest Labs",
        category="Image",
        description="State-of-the-art image generation with photorealistic visual quality.",
        context_length=None,
        is_free=True,  # Supported via free studio pipeline
        pricing="$0.05 / image",
        capabilities=["image", "high-quality", "diffusion"],
        icon="🎨"
    ),
    ModelCatalogItem(
        id="openai/dall-e-3",
        name="DALL·E 3",
        provider="OpenAI",
        category="Image",
        description="Create high-quality, detailed images from natural language prompts.",
        context_length=None,
        is_free=True,
        pricing="$0.04 / image",
        capabilities=["image", "creative", "diffusion"],
        icon="🖼️"
    ),
    ModelCatalogItem(
        id="midjourney/v6.1",
        name="Midjourney v6.1",
        provider="Midjourney",
        category="Image",
        description="Industry-leading model for stunning and stylized artistic visuals.",
        context_length=None,
        is_free=True,
        pricing="$0.04 / image",
        capabilities=["image", "artistic", "visual"],
        icon="⛵"
    ),
    ModelCatalogItem(
        id="elevenlabs/v3",
        name="ElevenLabs v3",
        provider="ElevenLabs",
        category="Speech",
        description="High-quality, lifelike speech synthesis with multi-voice support.",
        context_length=None,
        is_free=True,
        pricing="$0.30 / 1M char",
        capabilities=["speech", "tts", "voice"],
        icon="🎙️"
    ),

    # --- Additional High-Speed Free Frontier Models ---
    ModelCatalogItem(
        id="nvidia/nemotron-3.5-super-vl:free",
        name="NVIDIA: Nemotron 3.5 Super VL",
        provider="NVIDIA",
        category="Reasoning",
        description="NVIDIA frontier multimodal vision-language model with native reasoning.",
        context_length=131072,
        is_free=True,
        pricing="Free",
        capabilities=["chat", "vision", "reasoning"],
        icon="🟢"
    ),
    ModelCatalogItem(
        id="openai/gpt-oss-120b",
        name="Groq: GPT-OSS 120B",
        provider="Groq",
        category="Reasoning",
        description="120B parameter reasoning model running at 500+ tok/sec on Groq LPUs.",
        context_length=131072,
        is_free=True,
        pricing="Free",
        capabilities=["chat", "reasoning", "coding"],
        icon="⚡"
    ),
    ModelCatalogItem(
        id="microsoft/mai-image-2.7-flash",
        name="Microsoft AI: MAI-Image-2.7 Flash",
        provider="Microsoft",
        category="Image",
        description="Ultra-fast diffusion visual synthesis with high prompt adherence.",
        context_length=None,
        is_free=True,
        pricing="Free",
        capabilities=["image", "text_to_image"],
        icon="🎨"
    ),
    ModelCatalogItem(
        id="whisper-large-v3",
        name="Groq: Whisper Large V3",
        provider="Groq",
        category="Speech",
        description="State-of-the-art multilingual speech-to-text audio transcription.",
        context_length=None,
        is_free=True,
        pricing="Free",
        capabilities=["speech_to_text", "speech"],
        icon="🎧"
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

def get_catalog_models() -> List[ModelCatalogItem]:
    return MASTER_CATALOG

def filter_catalog(
    category: str = "All",
    is_free: Optional[bool] = None,
    search: str = ""
) -> List[ModelCatalogItem]:
    if is_free is True:
        return get_model_catalog(category=category, search_query=search, free_only=True)
    elif is_free is False:
        return [m for m in get_model_catalog(category=category, search_query=search, free_only=False) if not m.is_free]
    return get_model_catalog(category=category, search_query=search, free_only=False)

def get_model_by_id(model_id: str) -> Optional[ModelCatalogItem]:
    for m in MASTER_CATALOG:
        if m.id == model_id:
            return m
    return None
