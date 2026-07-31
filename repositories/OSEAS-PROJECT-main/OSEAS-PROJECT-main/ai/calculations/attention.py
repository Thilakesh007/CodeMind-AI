"""Pure attention/engagement threshold calculations.

Moved verbatim from the inline logic in the /metrics route:
    attentive = ear > 0.22 and head < 0.3
    engaged = attentive and mar < 0.6
"""
from config import Config


def is_attentive(ear: float, head_turn: float) -> bool:
    """Whether eye-aspect-ratio and head-turn indicate the student is attentive."""
    return ear > Config.EAR_THRESHOLD and head_turn < Config.HEAD_TURN_THRESHOLD


def is_engaged(attentive: bool, mar: float) -> bool:
    """Whether an already-attentive student is also engaged (mouth not indicating talk/yawn)."""
    return attentive and mar < Config.MAR_THRESHOLD
