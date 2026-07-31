"""Generic, low-level CSV file operations.

Moved from the inline `open()`/`csv.writer`/`csv.reader` calls that were
scattered across the /stop and /faculty routes and generate_session_report()
in the original app.py.
"""
import csv
import os
from typing import List


def file_exists(path: str) -> bool:
    return os.path.isfile(path)


def append_row(path: str, row: List, header: List[str] = None) -> None:
    """Append a single row to a CSV file, writing the header first if the file is new.

    Equivalent to the original /stop route logic:
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, "a", newline="") as f:
            w = csv.writer(f)
            if not file_exists: w.writerow([...header...])
            w.writerow([...row...])
    """
    needs_header = header is not None and not file_exists(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if needs_header:
            writer.writerow(header)
        writer.writerow(row)


def write_rows(path: str, rows: List[List], header: List[str] = None) -> None:
    """Overwrite a CSV file with the given rows (used for one-shot summary reports)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(header)
        writer.writerows(rows)


def read_rows(path: str, skip_header: bool = True) -> List[List[str]]:
    """Read all rows from a CSV file, optionally skipping the header row.

    Equivalent to the original /faculty route logic:
        with open(CSV_FILE) as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            for row in reader: records.append(row)
    """
    if not file_exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        if skip_header:
            next(reader, None)
        return [row for row in reader]
