"""Request-input validation helpers used by the route layer."""
from typing import Optional


def get_required_student_param(args) -> Optional[str]:
    """Extract the ``student`` query parameter, returning None if missing/blank.

    Mirrors the original inline checks in /start, /stop and /data:
        student = request.args.get("student")
        if not student: ...
    """
    student = args.get("student")
    return student if student else None


def validate_metrics_payload(data: dict) -> bool:
    """Validate the JSON body posted to /metrics contains the required keys.

    The original /metrics route accessed data["ear"], data["mar"], data["head"]
    directly (which would raise a KeyError/400 on malformed input); this
    validator lets the route fail the same way but with an explicit check.
    """
    if not data:
        return False
    if "student" not in data:
        return False
    # ear/mar/head are only required when a face was detected.
    if data.get("face"):
        return all(key in data for key in ("ear", "mar", "head"))
    return True
