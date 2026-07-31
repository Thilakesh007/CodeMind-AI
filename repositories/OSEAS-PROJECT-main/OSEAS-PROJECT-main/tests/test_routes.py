import pytest

from backend import create_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    app = create_app("development")
    app.config["TESTING"] = True

    # Redirect CSV writes to a temp file so tests don't touch real data/.
    monkeypatch.setattr("config.Config.SESSION_REPORT_CSV", str(tmp_path / "session_report.csv"))

    with app.test_client() as client:
        yield client


def test_login_page_loads(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"Sign In" in resp.data


def test_home_redirects_when_not_logged_in(client):
    resp = client.get("/")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


def test_data_endpoint_returns_empty_for_unknown_student(client):
    resp = client.get("/data?student=ghost")
    assert resp.status_code == 200
    assert resp.get_json() == {}


def test_start_requires_student_name(client):
    resp = client.get("/start")
    assert resp.status_code == 400


def test_login_and_faculty_dashboard(client):
    login_resp = client.post(
        "/login",
        data={"username": "faculty1", "password": "faculty123", "role": "faculty"},
    )
    assert login_resp.status_code == 302

    faculty_resp = client.get("/faculty")
    assert faculty_resp.status_code == 200
    assert b"Faculty Engagement Dashboard" in faculty_resp.data
