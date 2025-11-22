"""
Auth utilities: password hashing with Argon2id and JWT token management.
Argon2id is the gold standard for password hashing - slower by design.
"""
import os
from datetime import datetime, timedelta, timezone
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt

# JWT configuration from env
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 1

# Argon2 hasher with reasonable defaults for free-tier performance
ph = PasswordHasher(
    time_cost=2,  # Iterations
    memory_cost=65536,  # 64 MB
    parallelism=1,  # Single thread for free tier
    hash_len=32,
    salt_len=16
)


def hash_password(password: str) -> str:
    """Hash a password using Argon2id. Returns the hash string."""
    return ph.hash(password)


def verify_password(stored_hash: str, provided_password: str) -> bool:
    """Verify a password against its hash. Returns True if match."""
    try:
        ph.verify(stored_hash, provided_password)
        # Check if hash needs rehashing (params changed)
        if ph.check_needs_rehash(stored_hash):
            # In production, you'd update the hash here
            pass
        return True
    except VerifyMismatchError:
        return False


def create_jwt_token(username: str) -> str:
    """Create a JWT token for a user. Expires in 1 hour."""
    expiration = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    payload = {
        "sub": username,  # Subject (username)
        "exp": expiration,  # Expiration time
        "iat": datetime.now(timezone.utc),  # Issued at
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_jwt_token(token: str) -> str | None:
    """
    Verify a JWT token and return the username.
    Returns None if invalid or expired.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
