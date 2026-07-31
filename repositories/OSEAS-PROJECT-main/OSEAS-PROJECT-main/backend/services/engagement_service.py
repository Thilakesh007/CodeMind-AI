"""Engagement business logic — score aggregation + classification lookup."""
from ai.calculations import engagement as engagement_calc


def compute_engagement_score(engagement_time: int, presence: int) -> int:
    """Percentage of presence time spent engaged.

    Moved from: s["engagement_score"] = int((s["engagement_time"] / s["presence"]) * 100)
    """
    if presence == 0:
        return 0
    return int((engagement_time / presence) * 100)


def get_engagement_level(score: int) -> str:
    return engagement_calc.classify_engagement(score)
