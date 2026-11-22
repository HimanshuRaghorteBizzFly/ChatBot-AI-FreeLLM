"""
Pydantic schemas for data validation and API exchange.
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

class ChatMessageSchema(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    reasoning: Optional[str] = None
    image_path: Optional[str] = None

class ModelCatalogItem(BaseModel):
    id: str
    name: str
    provider: str
    category: str = "Text"  # Text, Image, Video, Speech, Vision, Reasoning, Embeddings, Reranking
    description: str = ""
    context_length: Optional[int] = None
    is_free: bool = True
    input_price: Optional[float] = 0.0  # per 1M tokens
    output_price: Optional[float] = 0.0
    capabilities: List[str] = Field(default_factory=lambda: ["chat"])
    api_key_required: bool = True
    icon: str = "🤖"

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
    index: int
