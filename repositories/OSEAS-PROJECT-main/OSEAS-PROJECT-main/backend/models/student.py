"""Runtime data model for a single student's live session.

Replaces the ad-hoc dict shape that was created inline in the original
/start route:
    students[student] = {
        "presence": 0, "engagement_time": 0, "attention_time": 0, ...
    }
"""
from dataclasses import dataclass, field
from typing import Optional

from backend.utils.constants import (
    ATTENDANCE_ABSENT,
    ENGAGEMENT_NOT_EVALUATED,
    MOVEMENT_IDLE,
)


@dataclass
class StudentRuntime:
    """In-memory runtime state tracked for a student during a live session."""

    name: str
    presence: int = 0
    engagement_time: int = 0
    attention_time: int = 0
    engagement_score: int = 0
    attention_score: int = 0
    attendance: str = ATTENDANCE_ABSENT
    movement: str = MOVEMENT_IDLE
    engagement_level: str = ENGAGEMENT_NOT_EVALUATED
    last_metric_time: Optional[float] = None
    running: bool = True

    def to_data_dict(self) -> dict:
        """Shape used by the /data JSON API endpoint (field names unchanged)."""
        return {
            "presence": self.presence,
            "engagement_time": self.engagement_time,
            "engagement": self.engagement_score,
            "engagement_level": self.engagement_level,
            "attention": self.attention_score,
            "movement": self.movement,
            "attendance": self.attendance,
            "student_name": self.name,
        }
