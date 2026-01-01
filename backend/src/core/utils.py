"""
Utility Functions.

Contains common helper functions used across the application.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import hashlib
import json


def generate_hash(data: Dict[str, Any]) -> str:
    """Generates a deterministic hash for a dictionary."""
    serialized = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode()).hexdigest()[:12]


def format_currency(amount: float, currency: str = "USD") -> str:
    """Formats a number as currency."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, "")
    return f"{symbol}{amount:,.2f}"


def calculate_lead_time(origin: str, destination: str, mode: str = "sea") -> int:
    """
    Estimates lead time in days based on transport mode.
    Uses simplified region-based heuristics.
    """
    base_times = {
        "sea": {"Asia-Europe": 28, "Asia-Americas": 21, "Europe-Americas": 14, "default": 20},
        "air": {"Asia-Europe": 3, "Asia-Americas": 2, "Europe-Americas": 1, "default": 2},
        "rail": {"Asia-Europe": 18, "default": 15},
        "road": {"default": 5}
    }
    
    mode_times = base_times.get(mode, base_times["sea"])
    
    for route, days in mode_times.items():
        if route != "default" and (origin in route or destination in route):
            return days
    
    return mode_times.get("default", 14)


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """Splits a list into chunks of specified size."""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Performs division with a fallback for zero denominators."""
    if denominator == 0:
        return default
    return numerator / denominator


def date_range(start: datetime, end: datetime, step_days: int = 1) -> List[datetime]:
    """Generates a list of dates between start and end."""
    dates = []
    current = start
    while current <= end:
        dates.append(current)
        current += timedelta(days=step_days)
    return dates


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merges two dictionaries."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncates a string to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def validate_sku_format(sku: str) -> bool:
    """Validates that a SKU follows the expected format (e.g., SKU-00001)."""
    if not sku.startswith("SKU-"):
        return False
    suffix = sku[4:]
    return suffix.isdigit() and len(suffix) == 5


def parse_location_string(location: str) -> Dict[str, str]:
    """Parses a location string like 'Industrial Zone, Europe' into components."""
    parts = [p.strip() for p in location.split(",")]
    if len(parts) >= 2:
        return {"area": parts[0], "region": parts[-1]}
    return {"area": location, "region": "Unknown"}
