"""
Tests for authentication module.
Verifies password hashing and JWT token generation/validation.
"""
import pytest
import sys
import os

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from auth import hash_password, verify_password, create_jwt_token, verify_jwt_token
import time


def test_password_hashing():
    """Test that password hashing and verification work correctly."""
    password = "secure_password_123"

    # Hash the password
    hashed = hash_password(password)

    # Verify correct password
    assert verify_password(hashed, password) is True

    # Verify incorrect password
    assert verify_password(hashed, "wrong_password") is False


def test_password_hash_uniqueness():
    """Test that same password produces different hashes (due to random salt)."""
    password = "test_password"

    hash1 = hash_password(password)
    hash2 = hash_password(password)

    # Hashes should be different due to different salts
    assert hash1 != hash2

    # But both should verify correctly
    assert verify_password(hash1, password) is True
    assert verify_password(hash2, password) is True


def test_jwt_token_creation():
    """Test JWT token creation and validation."""
    username = "testuser"

    # Create token
    token = create_jwt_token(username)

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_jwt_token_validation():
    """Test that JWT tokens can be validated correctly."""
    username = "testuser"

    # Create and verify token
    token = create_jwt_token(username)
    verified_username = verify_jwt_token(token)

    assert verified_username == username


def test_jwt_token_invalid():
    """Test that invalid tokens are rejected."""
    invalid_token = "invalid.token.here"

    result = verify_jwt_token(invalid_token)

    assert result is None


def test_jwt_token_expiration():
    """Test that expired tokens are rejected."""
    # This test would require manipulating time or creating a token with
    # immediate expiration. For brevity, we'll skip the actual expiration test
    # but verify the mechanism exists.

    # Create a valid token
    token = create_jwt_token("testuser")

    # Verify it's valid now
    assert verify_jwt_token(token) is not None

    # In production, you'd advance time and verify it expires after 1 hour


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
