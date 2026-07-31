"""Repository for data/attendance.csv.

NOTE: the original app.py shipped an attendance.csv data file but no route
in app.py ever read or wrote it directly (attendance status itself is
computed in-memory per student and persisted as a column inside
session_report.csv via session_repository.py). This repository is provided
for architectural completeness/parity with the target structure and future
use, without wiring it into any route that didn't use it originally.
"""
from typing import List

from config import Config
from database import csv_repository


def read_all(path: str = None) -> List[List[str]]:
    """Read all rows from attendance.csv (header row skipped)."""
    return csv_repository.read_rows(path or Config.ATTENDANCE_CSV, skip_header=True)


def append_row(row: List, header: List[str] = None, path: str = None) -> None:
    """Append a row to attendance.csv, writing the header first if the file is new."""
    csv_repository.append_row(path or Config.ATTENDANCE_CSV, row, header=header)
