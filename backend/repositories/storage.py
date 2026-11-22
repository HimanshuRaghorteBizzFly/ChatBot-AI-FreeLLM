"""
Database repository functions for CRUD operations using native SQLite connection.
Ensures zero C-extension DLL blocks and maximum performance.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from backend.database import get_db, init_db

# Ensure tables exist
init_db()

def get_or_create_default_user() -> int:
    """Ensures a default user exists."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = 'default_user';")
        row = cursor.fetchone()
        if row:
            return row["id"]
        cursor.execute("INSERT INTO users (username, email) VALUES ('default_user', 'user@ai-studio.local');")
        return cursor.lastrowid

# ============================================================
# Conversations & Messages
# ============================================================

def create_conversation(
    title: str = "New Chat",
    provider: str = "OpenRouter",
    model: str = "nvidia/nemotron-3.5-super-vl:free",
    system_prompt: str = ""
) -> int:
    user_id = get_or_create_default_user()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO conversations (user_id, title, provider, model, system_prompt, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP);
        """, (user_id, title, provider, model, system_prompt or "You are a helpful, expert AI assistant."))
        return cursor.lastrowid

def list_conversations(limit: int = 50) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, c.title, c.provider, c.model, c.updated_at,
                   COUNT(m.id) as message_count
            FROM conversations c
            LEFT JOIN messages m ON m.conversation_id = c.id
            GROUP BY c.id
            ORDER BY c.updated_at DESC
            LIMIT ?;
        """, (limit,))
        rows = cursor.fetchall()
        return [
            {
                "id": r["id"],
                "title": r["title"],
                "provider": r["provider"],
                "model": r["model"],
                "updated_at": str(r["updated_at"])[:16],
                "message_count": r["message_count"]
            }
            for r in rows
        ]

def get_conversation_messages(conversation_id: int) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, role, content, reasoning, image_path, media_url, token_count, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY created_at ASC;
        """, (conversation_id,))
        rows = cursor.fetchall()
        return [
            {
                "id": r["id"],
                "role": r["role"],
                "content": r["content"],
                "reasoning": r["reasoning"],
                "image_path": r["image_path"],
                "media_url": r["media_url"],
                "token_count": r["token_count"],
                "created_at": str(r["created_at"])[:16]
            }
            for r in rows
        ]

def add_message(
    conversation_id: int,
    role: str,
    content: str,
    reasoning: str = None,
    image_path: str = None,
    media_url: str = None,
    token_count: int = 0
) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (conversation_id, role, content, reasoning, image_path, media_url, token_count)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (conversation_id, role, content, reasoning, image_path, media_url, token_count))
        msg_id = cursor.lastrowid

        # Update conversation timestamp & auto-title if needed
        if role == "user":
            clean_title = " ".join(content.split()[:5])[:40]
            cursor.execute("""
                UPDATE conversations
                SET updated_at = CURRENT_TIMESTAMP,
                    title = CASE WHEN title = 'New Chat' THEN ? ELSE title END
                WHERE id = ?;
            """, (clean_title or "Chat", conversation_id))
        else:
            cursor.execute("""
                UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?;
            """, (conversation_id,))

        return msg_id

def rename_conversation(conversation_id: int, new_title: str) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE conversations SET title = ? WHERE id = ?;", (new_title.strip(), conversation_id))
        return cursor.rowcount > 0

def delete_conversation(conversation_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE conversation_id = ?;", (conversation_id,))
        cursor.execute("DELETE FROM conversations WHERE id = ?;", (conversation_id,))
        return cursor.rowcount > 0

# ============================================================
# Saved Prompts
# ============================================================

DEFAULT_PROMPTS = [
    {
        "title": "Code Explainer & Optimizer",
        "category": "Coding",
        "content": "Review the following code. Explain its architectural pattern, identify potential bugs or performance bottlenecks, and suggest clean modern refactoring.",
        "tags": "coding,python,review"
    },
    {
        "title": "System Architecture Design",
        "category": "Engineering",
        "content": "Design an enterprise high-throughput, low-latency microservices architecture for real-time AI processing with caching, pub/sub queues, and failover.",
        "tags": "architecture,system,cloud"
    },
    {
        "title": "FastAPI Production Template",
        "category": "Coding",
        "content": "Create a production-ready FastAPI boilerplate with CORS middleware, Pydantic validation, structured logging, and sample async CRUD routes.",
        "tags": "fastapi,python,api"
    },
    {
        "title": "Forward Deployed Engineer Career Guide",
        "category": "Career",
        "content": "Explain what a Forward Deployed Engineer (FDE) does, including client integrations, prototyping speed, and essential technical skills.",
        "tags": "career,engineering"
    }
]

def list_saved_prompts(category: str = None) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM saved_prompts;")
        if cursor.fetchone()["count"] == 0:
            # Seed defaults
            for p in DEFAULT_PROMPTS:
                cursor.execute("""
                    INSERT INTO saved_prompts (title, category, content, tags)
                    VALUES (?, ?, ?, ?);
                """, (p["title"], p["category"], p["content"], p["tags"]))

        if category and category != "All":
            cursor.execute("SELECT * FROM saved_prompts WHERE category = ? ORDER BY created_at DESC;", (category,))
        else:
            cursor.execute("SELECT * FROM saved_prompts ORDER BY created_at DESC;")
        
        rows = cursor.fetchall()
        return [
            {
                "id": r["id"],
                "title": r["title"],
                "category": r["category"],
                "content": r["content"],
                "tags": r["tags"].split(",") if r["tags"] else []
            }
            for r in rows
        ]

def create_saved_prompt(title: str, content: str, category: str = "General", tags: str = "") -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO saved_prompts (title, category, content, tags)
            VALUES (?, ?, ?, ?);
        """, (title, category, content, tags))
        return cursor.lastrowid

def delete_saved_prompt(prompt_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saved_prompts WHERE id = ?;", (prompt_id,))
        return cursor.rowcount > 0

# ============================================================
# Usage Tracking
# ============================================================

def log_usage(
    provider: str,
    model: str,
    operation: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    cost_estimate: float = 0.0,
    status: str = "success"
) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usage_records (provider, model, operation, input_tokens, output_tokens, cost_estimate, status)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (provider, model, operation, input_tokens, output_tokens, cost_estimate, status))
        return cursor.lastrowid

def get_usage_summary() -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_requests,
                SUM(input_tokens + output_tokens) as total_tokens,
                SUM(cost_estimate) as total_cost
            FROM usage_records;
        """)
        agg = cursor.fetchone()
        total_requests = agg["total_requests"] or 0
        total_tokens = agg["total_tokens"] or 0
        total_cost = agg["total_cost"] or 0.0

        cursor.execute("""
            SELECT provider, COUNT(*) as count
            FROM usage_records
            GROUP BY provider;
        """)
        by_prov_rows = cursor.fetchall()
        by_provider = {r["provider"]: r["count"] for r in by_prov_rows}

        cursor.execute("""
            SELECT id, provider, model, operation, (input_tokens + output_tokens) as tokens,
                   cost_estimate, status, created_at
            FROM usage_records
            ORDER BY created_at DESC
            LIMIT 50;
        """)
        recent_rows = cursor.fetchall()
        recent = [
            {
                "id": r["id"],
                "provider": r["provider"],
                "model": r["model"],
                "operation": r["operation"],
                "tokens": r["tokens"],
                "cost": f"${r['cost_estimate']:.4f}",
                "status": r["status"],
                "timestamp": str(r["created_at"])[:16]
            }
            for r in recent_rows
        ]

        return {
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "by_provider": by_provider,
            "recent": recent
        }

# ============================================================
# Media & Jobs
# ============================================================

def save_generated_media(media_type: str, prompt: str, provider: str, model: str, file_path: str = None, media_url: str = None) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO generated_media (media_type, prompt, provider, model, file_path, media_url)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (media_type, prompt, provider, model, file_path, media_url))
        return cursor.lastrowid

def list_generated_media(media_type: str = None, limit: int = 20) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        if media_type:
            cursor.execute("SELECT * FROM generated_media WHERE media_type = ? ORDER BY created_at DESC LIMIT ?;", (media_type, limit))
        else:
            cursor.execute("SELECT * FROM generated_media ORDER BY created_at DESC LIMIT ?;", (limit,))
        rows = cursor.fetchall()
        return [
            {
                "id": r["id"],
                "media_type": r["media_type"],
                "prompt": r["prompt"],
                "provider": r["provider"],
                "model": r["model"],
                "file_path": r["file_path"],
                "media_url": r["media_url"],
                "created_at": str(r["created_at"])[:16]
            }
            for r in rows
        ]

def save_generation_job(job_type: str, provider: str, model: str, prompt: str, status: str = "pending", result_path: str = None, error_message: str = None) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO generation_jobs (job_type, provider, model, prompt, status, result_path, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (job_type, provider, model, prompt, status, result_path, error_message))
        return cursor.lastrowid

def list_generation_jobs(limit: int = 20) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM generation_jobs ORDER BY created_at DESC LIMIT ?;", (limit,))
        rows = cursor.fetchall()
        return [
            {
                "id": r["id"],
                "type": r["job_type"],
                "provider": r["provider"],
                "model": r["model"],
                "prompt": r["prompt"],
                "status": r["status"],
                "created_at": str(r["created_at"])[:16]
            }
            for r in rows
        ]

# ============================================================
# User Preferences
# ============================================================

def get_user_preferences() -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_preferences WHERE user_id = 1;")
        row = cursor.fetchone()
        if row:
            return {
                "default_provider": row["default_provider"],
                "default_model": row["default_model"],
                "default_system_prompt": row["default_system_prompt"],
                "theme": row["theme"],
                "temperature": row["temperature"],
                "max_tokens": row["max_tokens"]
            }
        return {
            "default_provider": "OpenRouter",
            "default_model": "nvidia/nemotron-3.5-super-vl:free",
            "default_system_prompt": "You are a helpful AI assistant.",
            "theme": "Light",
            "temperature": 0.7,
            "max_tokens": 2048
        }

def update_user_preferences(**kwargs) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        fields = []
        values = []
        for k, v in kwargs.items():
            fields.append(f"{k} = ?")
            values.append(v)
        if not fields:
            return False
        values.append(1)  # user_id
        cursor.execute(f"UPDATE user_preferences SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?;", tuple(values))
        return cursor.rowcount > 0
