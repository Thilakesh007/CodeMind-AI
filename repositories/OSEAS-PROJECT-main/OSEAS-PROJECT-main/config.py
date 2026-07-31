"""Application configuration.

Centralizes all environment-driven and static configuration values that were
previously scattered as module-level globals in app.py.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    """Base Flask configuration for the Online Student Engagement Analysis app."""

    # ---- Flask / session ----
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "engagement_secret_key")
    SESSION_COOKIE_SAMESITE: str = "None"
    SESSION_COOKIE_SECURE: bool = True

    # ---- Server ----
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", 5050))
    DEBUG: bool = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    USE_RELOADER: bool = False

    # ---- Paths ----
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    SESSION_REPORT_CSV: str = os.path.join(DATA_DIR, "session_report.csv")
    ATTENDANCE_CSV: str = os.path.join(DATA_DIR, "attendance.csv")
    LOG_DIR: str = os.path.join(BASE_DIR, "logs")
    LOG_FILE: str = os.path.join(LOG_DIR, "app.log")

    TEMPLATE_FOLDER: str = os.path.join(BASE_DIR, "frontend", "templates")
    STATIC_FOLDER: str = os.path.join(BASE_DIR, "frontend", "static")

    # ---- Engagement thresholds (moved from globals in app.py) ----
    ATTENDANCE_THRESHOLD: int = 20
    EAR_THRESHOLD: float = 0.22
    MAR_THRESHOLD: float = 0.6
    HEAD_TURN_THRESHOLD: float = 0.3
    METRIC_MIN_INTERVAL_SECONDS: float = 1.0

    # Grading bands (from original /stop route)
    GRADE_A_MIN: int = 80
    GRADE_B_MIN: int = 60
    GRADE_C_MIN: int = 40

    # Engagement classification bands (from classify_engagement)
    ENGAGEMENT_HIGH_MIN: int = 80
    ENGAGEMENT_MODERATE_MIN: int = 45


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
