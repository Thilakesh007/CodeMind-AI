"""Data-layer facade.

The original app.py used flat-file CSV storage directly; this module exposes
a single import point (`Database`) so a future swap to a real database
engine only requires changes here, not in every service that reads/writes
session or attendance data.
"""
from database import attendance_repository, session_repository


class Database:
    """Facade grouping the CSV-backed repositories used by the app."""

    sessions = session_repository
    attendance = attendance_repository
