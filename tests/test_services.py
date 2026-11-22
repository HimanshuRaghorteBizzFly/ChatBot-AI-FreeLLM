"""
Tests for AI Studio business services.
"""
import os
from pathlib import Path
import pytest
from backend.services.catalog import get_catalog_models, filter_catalog
from backend.services.images import generate_image_studio, create_fallback_image
from backend.services.embeddings import cosine_similarity
from backend.services.reranking import rerank_documents
from backend.config import MEDIA_DIR

def test_catalog_services():
    models = get_catalog_models()
    assert len(models) >= 8

    # Filter by category
    vision_models = filter_catalog(category="Vision")
    assert any("vision" in m.capabilities for m in vision_models)

    # Filter by free
    free_models = filter_catalog(is_free=True)
    assert all(m.is_free is True for m in free_models)

def test_image_generation_guarantee():
    # Test guaranteed fallback image generation
    test_path = MEDIA_DIR / "test_pytest_canvas.jpg"
    created = create_fallback_image("A futuristic cyber canvas", test_path, 512, 512)
    assert os.path.exists(created)
    assert os.path.getsize(created) > 1000

    # Test studio generation pipeline
    res = generate_image_studio("Test prompt for unit testing", aspect_ratio="1:1")
    assert res.get("path") is not None
    assert os.path.exists(res["path"])

def test_cosine_similarity():
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [1.0, 0.0, 0.0]
    vec3 = [0.0, 1.0, 0.0]

    assert pytest.approx(cosine_similarity(vec1, vec2), 0.001) == 1.0
    assert pytest.approx(cosine_similarity(vec1, vec3), 0.001) == 0.0

def test_reranking_logic():
    query = "GPU quantization LLM acceleration"
    docs = [
        "Baking cake requires eggs, flour, and sugar.",
        "Quantization reduces precision from 16-bit to 4-bit, saving GPU memory bandwidth and speeding up matrix multiplications.",
        "Paris is the capital of France."
    ]
    results = rerank_documents(query, docs)
    assert len(results) == 3
    # Top ranked document should be the quantization document
    assert "Quantization" in results[0]["document"]
    assert results[0]["score"] > results[1]["score"]
