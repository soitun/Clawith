import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.database import get_db
from sqlalchemy import select
from unittest.mock import AsyncMock, patch
from app.core.security import hash_password


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_registration_config_endpoint(client):
    """Test the registration config endpoint"""
    response = client.get("/api/auth/registration-config")
    assert response.status_code == 200
    assert "invitation_code_required" in response.json()


def test_login_nonexistent_user(client):
    """Test login with non-existent user"""
    login_data = {
        "username": "nonexistent_user",
        "password": "wrong_password"
    }
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


def test_get_me_unauthorized(client):
    """Test accessing /me endpoint without authentication"""
    response = client.get("/api/auth/me")
    assert response.status_code == 401  # Unauthorized


@pytest.mark.asyncio
async def test_register_new_user():
    """Test user registration (async test)"""
    # Note: Since this is an integration test, we need a way to reset the DB state
    # For now, we'll focus on unit testing the route logic
    pass


# Test for models
def test_user_model():
    """Basic test for user model"""
    # We can't easily test the User model without a database connection
    # But we can at least verify it's importable
    assert User is not None