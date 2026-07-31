"""Read-side services powering the /data JSON API and the faculty dashboard.

Moved from the bodies of the /data and /faculty routes in app.py.
"""
from typing import List, Optional

from backend.models.runtime_store import RuntimeStore
from database import session_repository


def get_live_data(store: RuntimeStore, student: str) -> Optional[dict]:
    """Return the live-metrics dict for a student, or None if untracked.

    Mirrors the original /data route: `if not student or student not in students: return {}`.
    """
    if not student or not store.exists(student):
        return None
    return store.get(student).to_data_dict()


def get_faculty_records() -> List[List[str]]:
    """All persisted session records, for the faculty dashboard table."""
    return session_repository.read_all_records()
