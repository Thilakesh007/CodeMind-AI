"""JSON data API: /data. Moved verbatim from app.py."""
from flask import Blueprint, jsonify, request

from backend.models.runtime_store import runtime_store
from backend.services import dashboard_service
from backend.utils.validators import get_required_student_param

api_bp = Blueprint("api", __name__)


@api_bp.route("/data")
def data():
    student = get_required_student_param(request.args)
    live_data = dashboard_service.get_live_data(runtime_store, student) if student else None

    if live_data is None:
        return jsonify({})
    return jsonify(live_data)
