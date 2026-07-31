from ai.calculations.engagement import classify_engagement
from ai.calculations.grading import calculate_grade, compute_final_score
from ai.calculations.attention import is_attentive, is_engaged


def test_classify_engagement_bands():
    assert classify_engagement(90) == "High Engagement 🔥"
    assert classify_engagement(80) == "High Engagement 🔥"
    assert classify_engagement(60) == "Moderate Engagement 🙂"
    assert classify_engagement(45) == "Moderate Engagement 🙂"
    assert classify_engagement(10) == "Low Engagement 😴"


def test_calculate_grade_bands():
    assert calculate_grade(90) == "A 🏆"
    assert calculate_grade(65) == "B 🥈"
    assert calculate_grade(45) == "C 🥉"
    assert calculate_grade(20) == "D ❌"


def test_compute_final_score():
    assert compute_final_score(80, 60) == 70


def test_is_attentive_and_engaged():
    assert is_attentive(ear=0.3, head_turn=0.1) is True
    assert is_attentive(ear=0.1, head_turn=0.1) is False
    assert is_engaged(attentive=True, mar=0.2) is True
    assert is_engaged(attentive=False, mar=0.2) is False
