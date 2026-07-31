"""Small, reusable helper functions shared across services and routes."""
from datetime import datetime

from backend.utils.constants import DATE_FORMAT, REPORT_TIMESTAMP_FORMAT


def now_formatted() -> str:
    """Return the current timestamp formatted as used in session CSV rows."""
    return datetime.now().strftime(DATE_FORMAT)


def report_filename(prefix: str = "session_report") -> str:
    """Build a unique timestamped report filename, e.g. session_report_20260723_101500.csv."""
    return f"{prefix}_{datetime.now().strftime(REPORT_TIMESTAMP_FORMAT)}.csv"


def average(values: list) -> int:
    """Integer average of a list of numbers, or 0 for an empty list."""
    if not values:
        return 0
    return int(sum(values) / len(values))


def most_common(values: list, default: str = "Unknown"):
    """Return the most frequent item in a list, or a default if the list is empty."""
    if not values:
        return default
    return max(set(values), key=values.count)
