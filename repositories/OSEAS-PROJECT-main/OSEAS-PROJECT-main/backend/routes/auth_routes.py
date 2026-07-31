"""Authentication routes: /login and /logout. Moved verbatim from app.py."""
from flask import Blueprint, redirect, render_template, request, session

from backend.auth.authentication import authenticate

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        if authenticate(username, password, role):
            session["user"] = username
            session["role"] = role

            if role == "faculty":
                return redirect("/faculty")
            else:
                return redirect("/")
        else:
            return render_template("login.html", error="Invalid login")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
