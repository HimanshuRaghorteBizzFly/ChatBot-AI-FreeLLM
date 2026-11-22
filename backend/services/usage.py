"""
Usage and analytics service.
"""
import io
import csv
from typing import Dict, Any
from backend.repositories.storage import get_usage_summary

def get_analytics_metrics() -> Dict[str, Any]:
    return get_usage_summary()

def export_csv() -> str:
    """Exports usage records to CSV string."""
    summary = get_usage_summary()
    recent = summary.get("recent", [])
    if not recent:
        return "id,provider,model,operation,tokens,cost,status,timestamp\n"

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "provider", "model", "operation", "tokens", "cost", "status", "timestamp"])
    writer.writeheader()
    for row in recent:
        writer.writerow(row)
    return output.getvalue()
