"""
Embeddings service.
Generates real dense vector embeddings using Google Gemini and computes similarities.
"""
import math
from typing import List, Dict, Any
from backend.providers.registry import registry
from backend.repositories.storage import log_usage

def generate_text_embedding(text: str, model: str = "text-embedding-004") -> Dict[str, Any]:
    if not text.strip():
        return {"vector": [], "dimensions": 0, "error": "Please provide text to embed."}

    gemini = registry.get_provider("Google Gemini")
    if not gemini:
        return {"vector": [], "dimensions": 0, "error": "Provider not available."}

    try:
        vec = gemini.generate_embeddings(text=text, model=model)
        log_usage("Google Gemini", model, "embeddings", input_tokens=len(text.split()))
        return {
            "vector": vec,
            "dimensions": len(vec),
            "model": model,
            "error": None
        }
    except Exception as e:
        return {"vector": [], "dimensions": 0, "error": str(e)}

def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Computes cosine similarity between two vectors."""
    if len(vec_a) != len(vec_b) or not vec_a:
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
