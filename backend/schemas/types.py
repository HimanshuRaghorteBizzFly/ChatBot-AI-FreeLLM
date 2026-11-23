"""
Pydantic schemas for data validation, request sanitization, and API exchange.
Enforces strict boundaries, length limits, and typing across all application layers.
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator

class ChatMessageSchema(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str = Field(..., min_length=1, max_length=65536)
    reasoning: Optional[str] = Field(default=None, max_length=65536)
    image_path: Optional[str] = Field(default=None, max_length=1024)

    @field_validator("content")
    @classmethod
    def validate_content_not_empty(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Message content cannot be blank or only whitespace.")
        return cleaned

class ChatRequestSchema(BaseModel):
    conversation_id: int = Field(..., gt=0)
    provider_name: str = Field(..., min_length=1, max_length=64)
    model: str = Field(..., min_length=1, max_length=128)
    messages: List[ChatMessageSchema] = Field(..., min_length=1, max_length=100)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=1, le=8192)
    system_prompt: Optional[str] = Field(default=None, max_length=8192)

class ModelCatalogItem(BaseModel):
    id: str
    name: str
    provider: str
    category: str = "Text"  # Text, Image, Video, Speech, Vision, Reasoning, Embeddings, Reranking
    description: str = ""
    context_length: Optional[int] = None
    is_free: bool = True
    pricing: Optional[str] = None
    input_price: Optional[float] = 0.0  # per 1M tokens
    output_price: Optional[float] = 0.0
    capabilities: List[str] = Field(default_factory=lambda: ["chat"])
    api_key_required: bool = True
    icon: str = "🤖"

class ImageGenerationRequestSchema(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    model: str = Field(default="microsoft/mai-image-2.7-flash", max_length=128)
    aspect_ratio: Literal["1:1", "16:9", "9:16", "4:3"] = "1:1"

    @field_validator("prompt")
    @classmethod
    def sanitize_prompt(cls, v: str) -> str:
        cleaned = v.strip().replace("\x00", "")
        if not cleaned:
            raise ValueError("Image prompt cannot be empty.")
        return cleaned

class SpeechSynthesisRequestSchema(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    language: str = Field(default="en", max_length=10)
    accent: str = Field(default="com", max_length=10)
    slow: bool = False

class AudioUploadValidation(BaseModel):
    filename: str = Field(..., max_length=256)
    size_bytes: int = Field(..., gt=0, le=25 * 1024 * 1024)  # 25 MB max
    allowed_extensions: List[str] = Field(default_factory=lambda: [".mp3", ".wav", ".m4a", ".ogg", ".flac"])

    @field_validator("filename")
    @classmethod
    def validate_extension(cls, v: str) -> str:
        lower = v.lower()
        valid = any(lower.endswith(ext) for ext in [".mp3", ".wav", ".m4a", ".ogg", ".flac"])
        if not valid:
            raise ValueError(f"Unsupported audio format in filename: {v}")
        return v

class ImageUploadValidation(BaseModel):
    filename: str = Field(..., max_length=256)
    size_bytes: int = Field(..., gt=0, le=20 * 1024 * 1024)  # 20 MB max
    mime_type: Literal["image/png", "image/jpeg", "image/jpg", "image/webp"]

class GenerationJobSchema(BaseModel):
    id: Optional[int] = None
    job_type: str
    provider: str
    model: str
    prompt: str
    status: str = "pending"
    result_url: Optional[str] = None
    result_path: Optional[str] = None
    error_message: Optional[str] = None

class UsageRecordSchema(BaseModel):
    provider: str
    model: str
    operation: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_estimate: float = 0.0
    status: str = "success"

class RerankResultItem(BaseModel):
    document: str
    score: float
    rank: int
    original_index: int
