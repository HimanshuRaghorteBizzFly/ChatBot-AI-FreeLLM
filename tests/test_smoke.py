"""
Smoke tests verifying that all 16 views load cleanly and Streamlit app runs without errors.
"""
import pytest
from streamlit.testing.v1 import AppTest
from views import (
    dashboard,
    chat,
    models,
    image_studio,
    video_studio,
    speech_studio,
    vision,
    embeddings,
    reranking,
    comparison,
    providers,
    api_keys,
    usage,
    billing,
    saved_prompts,
    history,
    settings
)

ALL_VIEWS = [
    dashboard,
    chat,
    models,
    image_studio,
    video_studio,
    speech_studio,
    vision,
    embeddings,
    reranking,
    comparison,
    providers,
    api_keys,
    usage,
    billing,
    saved_prompts,
    history,
    settings
]

def test_all_views_exposed():
    assert len(ALL_VIEWS) == 17
    for v in ALL_VIEWS:
        assert hasattr(v, "render"), f"View {v.__name__} missing render() function"
        assert callable(v.render), f"View {v.__name__}.render is not callable"

def test_streamlit_app_smoke():
    """Uses Streamlit AppTest to simulate starting Frontend.py and check for uncaught exceptions."""
    from pathlib import Path
    app_path = Path(__file__).parent.parent / "Frontend.py"
    at = AppTest.from_file(str(app_path), default_timeout=30)
    at.run()
    assert not at.exception, f"Streamlit application encountered uncaught exception: {at.exception}"
