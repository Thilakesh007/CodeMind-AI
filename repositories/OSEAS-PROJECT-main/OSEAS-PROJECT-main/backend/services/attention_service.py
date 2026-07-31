"""Attention business logic — wraps the raw threshold math in ai.calculations.attention
with the score-aggregation logic from the original /metrics route.
"""
from ai.calculations import attention as attention_calc


def determine_attentive(ear: float, head_turn: float) -> bool:
    return attention_calc.is_attentive(ear, head_turn)


def determine_engaged(attentive: bool, mar: float) -> bool:
    return attention_calc.is_engaged(attentive, mar)


def compute_attention_score(attention_time: int, presence: int) -> int:
    """Percentage of presence time spent attentive.

    Moved from: s["attention_score"] = int((s["attention_time"] / s["presence"]) * 100)
    """
    if presence == 0:
        return 0
    return int((attention_time / presence) * 100)
