"""Orchestrates processing of a single /metrics POST payload.

Moved from the body of the /metrics route in app.py, unchanged in behavior:
rate-limits to >=1s between updates, treats "no face" as a stop-counting
signal, otherwise updates presence/attention/engagement time and scores.
"""
import time
from typing import Optional

from config import Config
from backend.models.runtime_store import RuntimeStore
from backend.models.student import StudentRuntime
from backend.services import attendance_service, attention_service, engagement_service
from backend.utils.constants import MOVEMENT_NO_FACE, MOVEMENT_ENGAGED, MOVEMENT_DISTRACTED


class MetricsResult:
    """Simple result wrapper so the route can translate to the right HTTP response."""

    def __init__(self, ok: bool, message: str, status_code: int = 200):
        self.ok = ok
        self.message = message
        self.status_code = status_code


def process_metrics(store: RuntimeStore, student: str, data: dict) -> MetricsResult:
    if not student or not store.exists(student):
        return MetricsResult(False, "INVALID STUDENT", 400)

    s: StudentRuntime = store.get(student)

    if not s.running:
        return MetricsResult(True, "STOPPED")

    now = time.time()

    if s.last_metric_time is None:
        s.last_metric_time = now
        return MetricsResult(True, "OK")

    if now - s.last_metric_time < Config.METRIC_MIN_INTERVAL_SECONDS:
        return MetricsResult(True, "OK")

    s.last_metric_time = now

    if not data.get("face", False):
        s.movement = MOVEMENT_NO_FACE
        return MetricsResult(True, "NO_FACE")

    # Face present: increment presence and recompute attendance.
    s.presence += 1
    s.attendance = attendance_service.compute_attendance_status(s.presence)

    ear = data["ear"]
    mar = data["mar"]
    head = data["head"]

    attentive = attention_service.determine_attentive(ear, head)
    engaged = attention_service.determine_engaged(attentive, mar)

    if attentive:
        s.attention_time += 1
    if engaged:
        s.engagement_time += 1

    s.attention_score = attention_service.compute_attention_score(s.attention_time, s.presence)
    s.engagement_score = engagement_service.compute_engagement_score(s.engagement_time, s.presence)
    s.engagement_level = engagement_service.get_engagement_level(s.engagement_score)
    s.movement = MOVEMENT_ENGAGED if engaged else MOVEMENT_DISTRACTED

    return MetricsResult(True, "OK")
