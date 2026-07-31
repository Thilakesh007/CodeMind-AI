"""Attendance calculation.

Moved from the inline logic in the /metrics route:
    s["attendance"] = "Present" if s["presence"] >= ATTENDANCE_THRESHOLD else "Absent"
"""
from config import Config
from backend.utils.constants import ATTENDANCE_PRESENT, ATTENDANCE_ABSENT


def compute_attendance_status(presence: int, threshold: int = None) -> str:
    """Return the attendance label for a given presence duration (seconds)."""
    threshold = Config.ATTENDANCE_THRESHOLD if threshold is None else threshold
    return ATTENDANCE_PRESENT if presence >= threshold else ATTENDANCE_ABSENT
