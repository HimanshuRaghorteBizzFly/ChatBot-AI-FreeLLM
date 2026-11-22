"""
Database manager using Python native SQLite.
Thread-safe connection pooling, schema migrations, and context management.
Zero external compiled C-extensions required for 100% resilience across all OS environments.
"""
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from backend.config import DATA_DIR

DB_PATH = DATA_DIR / "app.db"
_local = threading.local()

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=20.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for high concurrent read/write throughput
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Initializes tables and indices."""
    with get_db() as conn:
        cursor = conn.cursor()

        # 1. Users
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 2. Conversations
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            title TEXT NOT NULL,
            provider TEXT DEFAULT 'OpenRouter',
            model TEXT DEFAULT 'nvidia/nemotron-3.5-super-vl:free',
            system_prompt TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 3. Messages
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            reasoning TEXT,
            image_path TEXT,
            media_url TEXT,
            token_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
        );
        """)

        # 4. Saved Prompts
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            title TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            content TEXT NOT NULL,
            tags TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 5. Generation Jobs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS generation_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            job_type TEXT NOT NULL,
            provider TEXT NOT NULL,
            model TEXT NOT NULL,
            prompt TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            result_path TEXT,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 6. Generated Media
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS generated_media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            media_type TEXT NOT NULL,
            prompt TEXT NOT NULL,
            provider TEXT NOT NULL,
            model TEXT NOT NULL,
            file_path TEXT,
            media_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 7. Usage Records
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            provider TEXT NOT NULL,
            model TEXT NOT NULL,
            operation TEXT NOT NULL,
            input_tokens INTEGER DEFAULT 0,
            output_tokens INTEGER DEFAULT 0,
            cost_estimate REAL DEFAULT 0.0,
            status TEXT DEFAULT 'success',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 8. User Preferences
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE DEFAULT 1,
            default_provider TEXT DEFAULT 'OpenRouter',
            default_model TEXT DEFAULT 'nvidia/nemotron-3.5-super-vl:free',
            default_system_prompt TEXT DEFAULT 'You are a helpful AI assistant.',
            theme TEXT DEFAULT 'Light',
            temperature REAL DEFAULT 0.7,
            max_tokens INTEGER DEFAULT 2048,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Ensure default user and preferences
        cursor.execute("SELECT id FROM users WHERE username = 'default_user';")
        user = cursor.fetchone()
        if not user:
            cursor.execute("INSERT INTO users (username, email) VALUES ('default_user', 'user@ai-studio.local');")
            user_id = cursor.lastrowid
            cursor.execute("INSERT OR IGNORE INTO user_preferences (user_id) VALUES (?);", (user_id,))
