"""Repository for session_report.csv — the per-session record log.

Moved from the CSV read/write logic in the original /stop and /faculty
routes (CSV_FILE = "session_report.csv").
"""
from typing import List

from config import Config
from backend.models.session import SessionRecord
from backend.utils.constants import SESSION_CSV_HEADER
from database import csv_repository


def append_session_record(record: SessionRecord, path: str = None) -> None:
    """Append one completed session record, writing the header if the file is new."""
    csv_repository.append_row(
        path or Config.SESSION_REPORT_CSV, record.to_row(), header=SESSION_CSV_HEADER
    )


def read_all_records(path: str = None) -> List[List[str]]:
    """Read all session records (header row skipped), for the faculty dashboard."""
    return csv_repository.read_rows(path or Config.SESSION_REPORT_CSV, skip_header=True)
