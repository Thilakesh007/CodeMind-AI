"""Static string / label constants used across services and routes.

Numeric thresholds live in config.Config so they stay environment-configurable;
this module holds the fixed display strings and CSV schema so they are defined
in exactly one place instead of being duplicated across app.py.
"""

# ---- Status / label strings (unchanged from original app.py) ----
STATUS_IDLE = "Idle"
EMOTION_NEUTRAL = "Neutral 😐"
ATTENDANCE_ABSENT = "Absent ❌"
ATTENDANCE_PRESENT = "Present ✅"
MOVEMENT_IDLE = "Idle 🟡"
MOVEMENT_ENGAGED = "Engaged 🟢"
MOVEMENT_DISTRACTED = "Distracted 🔴"
MOVEMENT_NO_FACE = "No Face ❌"
ENGAGEMENT_NOT_EVALUATED = "Not Evaluated ⏳"

ENGAGEMENT_HIGH_LABEL = "High Engagement 🔥"
ENGAGEMENT_MODERATE_LABEL = "Moderate Engagement 🙂"
ENGAGEMENT_LOW_LABEL = "Low Engagement 😴"

GRADE_A = "A 🏆"
GRADE_B = "B 🥈"
GRADE_C = "C 🥉"
GRADE_D = "D ❌"

# ---- CSV schema (session_report.csv, written from /stop and read by /faculty) ----
SESSION_CSV_HEADER = [
    "Student",
    "Date",
    "Presence",
    "Engagement Time",
    "Engagement %",
    "Attention %",
    "Attendance",
    "Grade",
]

# ---- CSV schema for the ad-hoc timestamped summary report (generate_session_report) ----
SUMMARY_REPORT_HEADER = ["Metric", "Value"]

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
REPORT_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
