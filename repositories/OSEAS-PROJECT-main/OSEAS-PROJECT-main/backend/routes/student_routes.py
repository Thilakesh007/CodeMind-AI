"""Student dashboard routes: "/", /start, /stop. Moved verbatim from app.py."""
from flask import Blueprint, redirect, render_template, request, session

from backend.models.runtime_store import global_session_state, runtime_store
from backend.services import student_service
from backend.utils.validators import get_required_student_param

student_bp = Blueprint("student", __name__)


@student_bp.route("/")
def home():
    if "user" not in session or session.get("role") != "student":
        return redirect("/login")
    return render_template("dashboard.html", student_name=global_session_state.current_student)


@student_bp.route("/start")
def start():
    student = get_required_student_param(request.args)
    if not student:
        return "Student name missing", 400

    student_service.start_session(runtime_store, student)
    return "Started"


@student_bp.route("/stop")
def stop():
    student = get_required_student_param(request.args)
    record = student_service.stop_session(runtime_store, student)
    if record is None:
        return "Invalid student", 400
    return "Stopped & Saved ✅"
