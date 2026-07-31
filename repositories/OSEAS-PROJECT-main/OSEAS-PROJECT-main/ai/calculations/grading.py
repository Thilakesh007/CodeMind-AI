"""Final performance grade calculation.

Moved verbatim from the inline logic in the /stop route:
    final = (avg_eng + avg_att) / 2
    grade = "A" if final >= 80 else "B" if final >= 60 else "C" if final >= 40 else "D"
"""
from config import Config
from backend.utils.constants import GRADE_A, GRADE_B, GRADE_C, GRADE_D


def compute_final_score(engagement_score: int, attention_score: int) -> float:
    """Average of engagement and attention scores."""
    return (engagement_score + attention_score) / 2


def calculate_grade(final_score: float) -> str:
    """Map a final (0-100) score to a letter grade."""
    if final_score >= Config.GRADE_A_MIN:
        return GRADE_A
    elif final_score >= Config.GRADE_B_MIN:
        return GRADE_B
    elif final_score >= Config.GRADE_C_MIN:
        return GRADE_C
    else:
        return GRADE_D
