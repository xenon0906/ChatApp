"""
Simplified API tests focusing on core business logic.
Tests auth, crypto, and cache modules directly without FastAPI complexities.
"""
import pytest
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models import UserSignup, UserLogin, MessageSend
from auth import hash_password, verify_password, create_jwt_token, verify_jwt_token


def test_user_signup_model_validation():
    """Test UserSignup model validation."""
    # Valid signup
    signup = UserSignup(username="testuser", password="password123")
    assert signup.username == "testuser"

    # Invalid - username too short
    with pytest.raises(Exception):
        UserSignup(username="ab", password="password123")

    # Invalid - password too short
    with pytest.raises(Exception):
        UserSignup(username="testuser", password="short")


def test_user_login_model():
    """Test UserLogin model."""
    login = UserLogin(username="testuser", password="password123")
    assert login.username == "testuser"
    assert login.password == "password123"


def test_message_send_model():
    """Test MessageSend model validation."""
    msg = MessageSend(recipient="recipient", encrypted_content="encrypted_text")
    assert msg.recipient == "recipient"


def test_auth_flow():
    """Test complete authentication flow."""
    # Signup: hash password
    password = "securepassword123"
    hashed = hash_password(password)

    # Login: verify password
    assert verify_password(hashed, password) is True
    assert verify_password(hashed, "wrongpassword") is False

    # Create JWT token
    token = create_jwt_token("testuser")
    assert token is not None

    # Verify token
    username = verify_jwt_token(token)
    assert username == "testuser"


def test_password_requirements():
    """Test password hashing and verification."""
    passwords = [
        "simple123",
        "complex!@#$%^&*()",
        "longerpasswordwithlotsofcharacters123456789",
    ]

    for pwd in passwords:
        hashed = hash_password(pwd)
        assert verify_password(hashed, pwd) is True
        assert verify_password(hashed, pwd + "wrong") is False


def test_jwt_token_integrity():
    """Test JWT token cannot be tampered with."""
    token = create_jwt_token("alice")

    # Valid token
    assert verify_jwt_token(token) == "alice"

    # Tampered token
    tampered = token[:-5] + "XXXXX"
    assert verify_jwt_token(tampered) is None

    # Invalid format
    assert verify_jwt_token("not.a.token") is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
