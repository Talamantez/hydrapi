# tests/test_main.py
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import requests
from dotenv import load_dotenv
load_dotenv(".env.test")

# Environment variables for deployed testing
DEPLOY_URL = os.getenv("DEPLOY_URL")
DEPLOY_API_KEY = os.getenv("DEPLOY_API_KEY")

# Test client fixtures
@pytest.fixture
def local_client():
    return TestClient(app)

@pytest.fixture
def deploy_client():
    class DeployedAPIClient:
        def __init__(self):
            self.base_url = DEPLOY_URL
            self.api_key = DEPLOY_API_KEY

        def get(self, path):
            return requests.get(f"{self.base_url}{path}")

        def post(self, path, json, headers):
            return requests.post(
                f"{self.base_url}{path}", 
                json=json,
                headers=headers
            )

    return DeployedAPIClient() if DEPLOY_URL else None

# Local Tests
def test_local_health_check(local_client):
    response = local_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_local_root_endpoint(local_client):
    response = local_client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Architecture Pattern Detector API",
        "status": "running"
    }

def test_local_detect_nextjs(local_client):
    payload = {
        "files": ["next.config.js"],
        "directories": ["pages"],
        "config_files": {}
    }
    response = local_client.post(
        "/detect",
        json=payload,
        headers={"api-key": settings.API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["detected_framework"] == "Next.js"
    assert data["confidence"] == 0.9

def test_local_invalid_api_key(local_client):
    payload = {
        "files": ["next.config.js"],
        "directories": ["pages"],
        "config_files": {}
    }
    response = local_client.post(
        "/detect",
        json=payload,
        headers={"api-key": "invalid-key"}
    )
    assert response.status_code == 401

# Deployment Tests
@pytest.mark.skipif(not DEPLOY_URL, reason="Deployment URL not configured")
def test_deploy_health_check(deploy_client):
    response = deploy_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.skipif(not DEPLOY_URL, reason="Deployment URL not configured")
def test_deploy_root_endpoint(deploy_client):
    response = deploy_client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Architecture Pattern Detector API",
        "status": "running"
    }

@pytest.mark.skipif(not DEPLOY_URL, reason="Deployment URL not configured")
def test_deploy_detect_nextjs(deploy_client):
    payload = {
        "files": ["next.config.js"],
        "directories": ["pages"],
        "config_files": {}
    }
    response = deploy_client.post(
        "/detect",
        json=payload,
        headers={"api-key": DEPLOY_API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["detected_framework"] == "Next.js"
    assert data["confidence"] == 0.9

@pytest.mark.skipif(not DEPLOY_URL, reason="Deployment URL not configured")
def test_deploy_invalid_api_key(deploy_client):
    payload = {
        "files": ["next.config.js"],
        "directories": ["pages"],
        "config_files": {}
    }
    response = deploy_client.post(
        "/detect",
        json=payload,
        headers={"api-key": "invalid-key"}
    )
    assert response.status_code == 401

# Parametrized tests for both environments
@pytest.mark.parametrize("env", ["local", "deploy"])
def test_health_check_both_envs(env, local_client, deploy_client):
    if env == "deploy" and not deploy_client:
        pytest.skip("Deployment environment not configured")
        
    client = local_client if env == "local" else deploy_client
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}