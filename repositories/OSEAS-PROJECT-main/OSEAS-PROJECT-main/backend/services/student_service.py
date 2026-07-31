"""Student session lifecycle: start and stop, moved from the /start and /stop routes."""
from typing import Optional

from backend.models.runtime_store import RuntimeStore
from backend.models.session import SessionRecord
from backend.utils.helpers import now_formatted
from ai.calculations import grading
from database import session_repository


def start_session(store: RuntimeStore, student: str) -> None:
    """Create fresh runtime state for a student. Mirrors the original /start route."""
    store.start(student)


def stop_session(store: RuntimeStore, student: str) -> Optional[SessionRecord]:
    """Stop a student's session, compute the final grade, and persist the record.

    Returns None if the student has no active runtime (caller returns 400),
    mirroring the original /stop route's `if not student or student not in students`.
    """
    if not student or not store.exists(student):
        return None

    s = store.get(student)
    s.running = False

    final_score = grading.compute_final_score(s.engagement_score, s.attention_score)
    grade = grading.calculate_grade(final_score)

    record = SessionRecord(
        student=student,
        date=now_formatted(),
        presence=s.presence,
        engagement_time=s.engagement_time,
        engagement_score=s.engagement_score,
        attention_score=s.attention_score,
        attendance=s.attendance,
        grade=grade,
    )
    session_repository.append_session_record(record)
    return record
