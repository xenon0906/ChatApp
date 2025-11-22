"""
Tests for FastAPI endpoints.
Uses TestClient for testing with proper mocking.
"""
import pytest
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Mock database and cache before importing app
from unittest.mock import patch, AsyncMock, MagicMock

# Create mock modules
sys.modules['db'] = MagicMock()
sys.modules['cache'] = MagicMock()

# Mock the database functions
async def mock_create_user(username, hashed_password):
    return username != "existing"

async def mock_get_user(username):
    if username == "testuser":
        return {
            "username": "testuser",
            "hashed_password": "$argon2id$v=19$m=65536,t=2,p=1$SomeValidHash"
        }
    return None

async def mock_save_message(sender, recipient, encrypted_content):
    return {
        "_id": "123",
        "sender": sender,
        "recipient": recipient,
        "encrypted_content": encrypted_content,
        "timestamp": datetime.now()
    }

async def mock_get_messages_between(user1, user2, hours=24):
    return []

async def mock_get_contacts(username):
    return []

async def mock_init_db():
    pass

async def mock_close_db():
    pass

async def mock_init_redis():
    pass

async def mock_close_redis():
    pass

# Patch db module
sys.modules['db'].init_db = mock_init_db
sys.modules['db'].close_db = mock_close_db
sys.modules['db'].create_user = mock_create_user
sys.modules['db'].get_user = mock_get_user
sys.modules['db'].save_message = mock_save_message
sys.modules['db'].get_messages_between = mock_get_messages_between
sys.modules['db'].get_contacts = mock_get_contacts

# Patch cache module
sys.modules['cache'].init_redis = mock_init_redis
sys.modules['cache'].close_redis = mock_close_redis
sys.modules['cache'].cache_messages = AsyncMock()
sys.modules['cache'].get_cached_messages = AsyncMock(return_value=None)
sys.modules['cache'].invalidate_message_cache = AsyncMock()
sys.modules['cache'].cache_jwt_validation = AsyncMock()
sys.modules['cache'].get_cached_jwt_validation = AsyncMock(return_value=None)

# Now import app
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    """Create a test client with disabled rate limiting."""
    # Disable rate limiting for tests
    app.state.limiter = MagicMock()
    return TestClient(app)


def test_root_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_signup_success(client):
    """Test successful user signup."""
    response = client.post("/signup", json={
        "username": "newuser",
        "password": "securepass123"
    })

    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_signup_duplicate_username(client):
    """Test signup with duplicate username."""
    response = client.post("/signup", json={
        "username": "existing",
        "password": "securepass123"
    })

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_signup_invalid_username(client):
    """Test signup with invalid username."""
    response = client.post("/signup", json={
        "username": "ab",  # Too short
        "password": "securepass123"
    })

    assert response.status_code == 422  # Validation error


def test_signup_invalid_password(client):
    """Test signup with invalid password."""
    response = client.post("/signup", json={
        "username": "validuser",
        "password": "short"  # Too short
    })

    assert response.status_code == 422  # Validation error


def test_login_success(client):
    """Test successful login."""
    # Mock password verification
    with patch('app.verify_password', return_value=True):
        response = client.post("/login", json={
            "username": "testuser",
            "password": "correctpassword"
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post("/login", json={
        "username": "nonexistent",
        "password": "wrongpassword"
    })

    assert response.status_code == 401


def test_send_message_unauthorized(client):
    """Test sending message without authentication."""
    response = client.post("/messages", json={
        "recipient": "otheruser",
        "encrypted_content": "encrypted_data"
    })

    assert response.status_code == 422  # Missing token parameter


def test_get_messages_unauthorized(client):
    """Test getting messages without authentication."""
    response = client.get("/messages/otheruser")

    assert response.status_code == 422  # Missing token parameter


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
