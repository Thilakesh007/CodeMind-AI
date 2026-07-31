"""Timestamped session summary report generation.

Moved verbatim (behaviorally) from generate_session_report() in app.py.
NOTE: as in the original file, this function is not called from any route —
it is preserved here, unwired, for full behavioral parity.
"""
import os

from backend.models.runtime_store import GlobalSessionState
from backend.utils.constants import SUMMARY_REPORT_HEADER
from backend.utils.helpers import average, most_common, report_filename
from database import csv_repository


def generate_session_report(state: GlobalSessionState, output_dir: str = ".") -> str:
    """Write a one-off timestamped summary CSV from the legacy global session state.

    Returns the generated filename (matches the original function's return value).
    """
    filename = report_filename()
    path = os.path.join(output_dir, filename)

    avg_engagement = average(state.engagement_history)
    avg_attention = average(state.attention_history)
    dominant_emotion = most_common(state.emotion_log)

    rows = [
        ["Total Presence Time (sec)", int(state.presence_time)],
        ["Average Engagement (%)", avg_engagement],
        ["Average Attention (%)", avg_attention],
        ["Final Attendance", state.attendance],
        ["Dominant Emotion", dominant_emotion],
    ]
    csv_repository.write_rows(path, rows, header=SUMMARY_REPORT_HEADER)

    return filename
