"""In-memory runtime storage.

Moved from the module-level globals in app.py:
    students = {}
    presence_time = 0.0 ... engagement_history = [] ...

`students` backed real per-student behavior (used by /start, /stop, /data,
/metrics). The single-session globals below (presence_time, engagement_time,
etc.) were never mutated or read by any route in the original app.py except
by generate_session_report(), which itself was never called from a route —
they are preserved here unchanged for full behavioral parity, not repurposed.
"""
from dataclasses import dataclass, field
from typing import Dict, Optional

from backend.models.student import StudentRuntime
from backend.utils.constants import (
    ATTENDANCE_ABSENT,
    ENGAGEMENT_NOT_EVALUATED,
    EMOTION_NEUTRAL,
    MOVEMENT_IDLE,
    STATUS_IDLE,
)


class RuntimeStore:
    """Encapsulates the live `students` dictionary and its operations."""

    def __init__(self) -> None:
        self._students: Dict[str, StudentRuntime] = {}

    def start(self, name: str) -> StudentRuntime:
        """Create/reset runtime state for a student (mirrors original /start)."""
        runtime = StudentRuntime(name=name)
        self._students[name] = runtime
        return runtime

    def exists(self, name: str) -> bool:
        return name in self._students

    def get(self, name: str) -> Optional[StudentRuntime]:
        return self._students.get(name)

    def all(self) -> Dict[str, StudentRuntime]:
        return self._students


# Singleton shared across the whole app (routes/services import this instance).
runtime_store = RuntimeStore()


@dataclass
class GlobalSessionState:
    """Legacy single-session globals, preserved unchanged from app.py.

    Kept for parity with generate_session_report(); not wired into any route,
    exactly as in the original file.
    """

    last_metric_time: Optional[float] = None
    presence_time: float = 0.0
    engagement_time: float = 0.0
    attention_time: float = 0.0
    engagement_score: int = 0
    attention_score: int = 0
    status: str = STATUS_IDLE
    emotion: str = EMOTION_NEUTRAL
    attendance: str = ATTENDANCE_ABSENT
    movement_state: str = MOVEMENT_IDLE
    session_start_time: Optional[float] = None
    emotion_log: list = field(default_factory=list)
    current_student: str = ""
    engagement_level: str = ENGAGEMENT_NOT_EVALUATED
    running: bool = False
    performance_grade: str = "-"
    engagement_history: list = field(default_factory=list)
    attention_history: list = field(default_factory=list)


global_session_state = GlobalSessionState()
