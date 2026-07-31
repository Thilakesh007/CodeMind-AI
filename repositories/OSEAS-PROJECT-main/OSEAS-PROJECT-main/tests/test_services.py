from backend.services import attendance_service, attention_service, engagement_service
from backend.models.runtime_store import RuntimeStore
from backend.services import student_service, metrics_service, dashboard_service


def test_compute_attendance_status():
    assert attendance_service.compute_attendance_status(25) == "Present ✅"
    assert attendance_service.compute_attendance_status(5) == "Absent ❌"


def test_compute_attention_and_engagement_scores():
    assert attention_service.compute_attention_score(10, 20) == 50
    assert engagement_service.compute_engagement_score(5, 20) == 25
    assert attention_service.compute_attention_score(0, 0) == 0


def test_start_and_stop_session_flow(tmp_path, monkeypatch):
    store = RuntimeStore()
    student_service.start_session(store, "alice")
    assert store.exists("alice")

    # Give alice some scores before stopping.
    runtime = store.get("alice")
    runtime.engagement_score = 90
    runtime.attention_score = 90

    csv_path = tmp_path / "session_report.csv"
    monkeypatch.setattr(
        "backend.services.student_service.session_repository.append_session_record",
        lambda record, path=None: None,
    )

    record = student_service.stop_session(store, "alice")
    assert record is not None
    assert record.grade == "A 🏆"
    assert store.get("alice").running is False


def test_process_metrics_invalid_student():
    store = RuntimeStore()
    result = metrics_service.process_metrics(store, "nobody", {})
    assert result.ok is False
    assert result.status_code == 400


def test_get_live_data_missing_student():
    store = RuntimeStore()
    assert dashboard_service.get_live_data(store, "ghost") is None
