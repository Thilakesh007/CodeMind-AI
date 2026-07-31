import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to CodeMind AI 🚀"}

def test_get_settings():
    response = client.get("/settings")
    assert response.status_code == 200
    data = response.json()
    assert "ai_provider" in data
    assert "primary_model" in data

def test_update_settings():
    # Update settings to a mock value
    payload = {
        "ollama_host": "http://localhost:11434",
        "primary_model": "test-model",
        "ai_provider": "ollama",
        "openai_api_key": "",
        "anthropic_api_key": "",
        "gemini_api_key": ""
    }
    response = client.post("/settings/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "Settings saved successfully"}
    
    # Verify the update
    get_response = client.get("/settings")
    assert get_response.json()["primary_model"] == "test-model"
