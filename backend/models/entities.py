"""
Domain Entities and Data Models.
Pure Python dataclasses for all core database entities.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    email: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class Conversation:
    id: int
    user_id: int
    title: str
    provider: str = "OpenRouter"
    model: str = "nvidia/nemotron-3.5-super-vl:free"
    system_prompt: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Message:
    id: int
    conversation_id: int
    role: str
    content: str
    reasoning: Optional[str] = None
    image_path: Optional[str] = None
    media_url: Optional[str] = None
    token_count: int = 0
    created_at: Optional[datetime] = None

@dataclass
class SavedPrompt:
    id: int
    title: str
    content: str
    category: str = "General"
    tags: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class GenerationJob:
    id: int
    job_type: str
    provider: str
    model: str
    prompt: str
    status: str = "pending"
    result_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class GeneratedMedia:
    id: int
    media_type: str
    prompt: str
    provider: str
    model: str
    file_path: Optional[str] = None
    media_url: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class UsageRecord:
    id: int
    provider: str
    model: str
    operation: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_estimate: float = 0.0
    status: str = "success"
    created_at: Optional[datetime] = None

@dataclass
class UserPreference:
    id: int
    user_id: int
    default_provider: str = "OpenRouter"
    default_model: str = "nvidia/nemotron-3.5-super-vl:free"
    default_system_prompt: str = "You are a helpful AI assistant."
    theme: str = "Light"
    temperature: float = 0.7
    max_tokens: int = 2048
    updated_at: Optional[datetime] = None

@dataclass
class ProviderCredential:
    id: int
    user_id: int
    provider_name: str
    api_key_encrypted: Optional[str] = None
    is_valid: bool = False
    last_verified_at: Optional[datetime] = None
