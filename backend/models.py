"""
Pydantic models for request/response validation.
Keeping these separate makes the API cleaner and easier to test.
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime


class UserSignup(BaseModel):
    """Signup payload - just username and password."""
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()  # Normalize to lowercase for consistency


class UserLogin(BaseModel):
    """Login payload - same as signup."""
    username: str
    password: str


class MessageSend(BaseModel):
    """Send a message - recipient and encrypted content."""
    recipient: str
    encrypted_content: str  # Base64-encoded encrypted message

    @field_validator('recipient')
    @classmethod
    def recipient_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Recipient must be alphanumeric')
        return v.lower()


class MessageResponse(BaseModel):
    """What the client gets back when fetching messages."""
    sender: str
    recipient: str
    encrypted_content: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)  # For ORM compatibility if needed


class TokenResponse(BaseModel):
    """JWT token response after successful login."""
    access_token: str
    token_type: str = "bearer"
