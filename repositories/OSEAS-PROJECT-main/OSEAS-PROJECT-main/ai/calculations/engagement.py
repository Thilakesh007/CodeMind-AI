"""Engagement score classification.

Moved verbatim from the original classify_engagement() function in app.py.
"""
from config import Config
from backend.utils.constants import (
    ENGAGEMENT_HIGH_LABEL,
    ENGAGEMENT_MODERATE_LABEL,
    ENGAGEMENT_LOW_LABEL,
)


def classify_engagement(score: int) -> str:
    """Classify a 0-100 engagement score into a display label."""
    if score >= Config.ENGAGEMENT_HIGH_MIN:
        return ENGAGEMENT_HIGH_LABEL
    elif score >= Config.ENGAGEMENT_MODERATE_MIN:
        return ENGAGEMENT_MODERATE_LABEL
    else:
        return ENGAGEMENT_LOW_LABEL
