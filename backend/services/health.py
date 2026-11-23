"""
System Health & Diagnostics Service.
Provides comprehensive health checks across database, storage, provider configuration,
and runtime environment without leaking internal credentials.
"""
import os
import sys
import platform
import shutil
from typing import Dict, Any
from backend.database import check_db_health, DB_PATH
from backend.config import DATA_DIR, MEDIA_DIR, AUDIO_DIR, validate_environment
from backend.providers.registry import registry

def get_system_health() -> Dict[str, Any]:
    """
    Runs a full system health audit and returns status dictionary.
    """
    # 1. Database Check
    db_status = check_db_health()

    # 2. Storage Directory Check
    directories = {
        "data_dir": {"path": str(DATA_DIR), "exists": DATA_DIR.exists(), "writable": os.access(str(DATA_DIR), os.W_OK)},
        "media_dir": {"path": str(MEDIA_DIR), "exists": MEDIA_DIR.exists(), "writable": os.access(str(MEDIA_DIR), os.W_OK)},
        "audio_dir": {"path": str(AUDIO_DIR), "exists": AUDIO_DIR.exists(), "writable": os.access(str(AUDIO_DIR), os.W_OK)},
    }
    all_dirs_ok = all(d["exists"] and d["writable"] for d in directories.values())

    # 3. Environment & Provider Configuration
    env_info = validate_environment()

    # 4. Storage Disk Free Space (where supported)
    disk_free_gb = 0.0
    try:
        total, used, free = shutil.disk_usage(str(DATA_DIR))
        disk_free_gb = round(free / (1024 ** 3), 2)
    except Exception:
        pass

    # Overall System Status
    is_healthy = (db_status.get("status") == "healthy") and all_dirs_ok and env_info.get("ready", False)

    return {
        "status": "healthy" if is_healthy else "degraded",
        "runtime": {
            "python_version": sys.version.split()[0],
            "platform": f"{platform.system()} {platform.release()}",
            "environment": env_info.get("app_env", "development"),
            "is_production": env_info.get("is_production", False)
        },
        "database": db_status,
        "directories": directories,
        "disk_free_gb": disk_free_gb,
        "providers_status": env_info.get("providers_configured", {}),
        "warnings": env_info.get("warnings", [])
    }
