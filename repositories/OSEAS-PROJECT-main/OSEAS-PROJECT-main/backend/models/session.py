"""Data model for a completed session record, as persisted to session_report.csv."""
from dataclasses import dataclass


@dataclass
class SessionRecord:
    """One row written to session_report.csv by the /stop route."""

    student: str
    date: str
    presence: int
    engagement_time: int
    engagement_score: int
    attention_score: int
    attendance: str
    grade: str

    def to_row(self) -> list:
        """Row order must match SESSION_CSV_HEADER in backend.utils.constants."""
        return [
            self.student,
            self.date,
            self.presence,
            self.engagement_time,
            self.engagement_score,
            self.attention_score,
            self.attendance,
            self.grade,
        ]
