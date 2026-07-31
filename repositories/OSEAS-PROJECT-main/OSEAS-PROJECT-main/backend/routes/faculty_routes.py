"""Faculty dashboard route: /faculty. Moved verbatim from app.py."""
from flask import Blueprint, redirect, render_template, session

from backend.services import dashboard_service

faculty_bp = Blueprint("faculty", __name__)


@faculty_bp.route("/faculty")
def faculty_dashboard():
    if "user" not in session or session.get("role") != "faculty":
        return redirect("/login")

    records = dashboard_service.get_faculty_records()
    return render_template("faculty.html", records=records)
