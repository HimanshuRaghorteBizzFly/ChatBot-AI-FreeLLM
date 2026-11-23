"""
Tests for system health check and database diagnostics.
"""
import pytest
from backend.services.health import get_system_health
from backend.database import check_db_health

def test_database_health_check():
    db_health = check_db_health()
    assert db_health["status"] == "healthy"
    assert db_health["quick_check"] == "ok"
    assert db_health["exists"] is True

def test_full_system_health_audit():
    health = get_system_health()
    assert health["status"] in ("healthy", "degraded")
    assert "runtime" in health
    assert "database" in health
    assert "directories" in health
    assert "data_dir" in health["directories"]
    assert health["directories"]["data_dir"]["exists"] is True
    assert health["directories"]["data_dir"]["writable"] is True
