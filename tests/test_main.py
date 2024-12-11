# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Architecture Pattern Detector API",
        "status": "running"
    }

def test_detect_nextjs():
    payload = {
        "files": ["next.config.js"],
        "directories": ["pages"],
        "config_files": {}
    }
    response = client.post(
        "/detect",
        json=payload,
        headers={"api-key": settings.API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["detected_framework"] == "Next.js"
    assert data["confidence"] == 0.9

def test_detect_invalid_api_key():
    payload = {
        "files": ["next.config.js"],
        "directories": ["pages"],
        "config_files": {}
    }
    response = client.post(
        "/detect",
        json=payload,
        headers={"api-key": "invalid-key"}
    )
    assert response.status_code == 401