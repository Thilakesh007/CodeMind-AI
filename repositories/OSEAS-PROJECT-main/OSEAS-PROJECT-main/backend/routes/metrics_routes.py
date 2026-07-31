"""Live metrics ingestion route: POST /metrics. Moved verbatim from app.py."""
from flask import Blueprint, request

from backend.models.runtime_store import runtime_store
from backend.services import metrics_service

metrics_bp = Blueprint("metrics_bp", __name__)


@metrics_bp.route("/metrics", methods=["POST"])
def metrics():
    data = request.json
    student = data.get("student")

    result = metrics_service.process_metrics(runtime_store, student, data)
    return result.message, result.status_code
