"""
Tests for SQLAlchemy database repository and entities.
"""
import pytest
from backend.database import init_db, get_db
from backend.repositories.storage import (
    create_conversation,
    list_conversations,
    get_conversation_messages,
    add_message,
    create_saved_prompt,
    list_saved_prompts,
    delete_saved_prompt,
    log_usage,
    get_usage_summary,
    save_generated_media,
    list_generated_media
)

def test_database_initialization():
    init_db()
    with get_db() as db:
        assert db is not None

def test_conversation_lifecycle():
    conv_id = create_conversation(title="Test Pytest Session", provider="OpenRouter", model="nvidia/nemotron-3.5-super-vl:free")
    assert conv_id > 0

    msg_id = add_message(conv_id, role="user", content="Hello unit test")
    assert msg_id > 0

    assistant_id = add_message(conv_id, role="assistant", content="Unit test response", reasoning="Thinking step")
    assert assistant_id > 0

    messages = get_conversation_messages(conv_id)
    assert len(messages) >= 2
    assert messages[-1]["role"] == "assistant"
    assert messages[-1]["content"] == "Unit test response"
    assert messages[-1]["reasoning"] == "Thinking step"

    convs = list_conversations()
    assert any(c["id"] == conv_id for c in convs)

def test_saved_prompts_crud():
    prompt_id = create_saved_prompt("Pytest Test Prompt", "Test prompt instruction content", category="Coding")
    assert prompt_id > 0

    prompts = list_saved_prompts()
    assert any(p["id"] == prompt_id for p in prompts)

    deleted = delete_saved_prompt(prompt_id)
    assert deleted is True

def test_usage_logging_and_summary():
    rec_id = log_usage("TestProvider", "test-model-1", "chat", input_tokens=50, output_tokens=100, cost_estimate=0.001)
    assert rec_id > 0

    summary = get_usage_summary()
    assert summary["total_requests"] > 0
    assert summary["total_tokens"] >= 150
    assert summary["total_cost"] >= 0.001

def test_generated_media_storage():
    media_id = save_generated_media("image", "Test cyber city", "Microsoft AI", "microsoft/mai-image-2.7-flash", "test/path.jpg")
    assert media_id > 0

    media_list = list_generated_media("image")
    assert any(m["id"] == media_id for m in media_list)
