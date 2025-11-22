"""
Tests for Redis caching layer.
Verifies caching and invalidation logic.
"""
import pytest
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from cache import (
    cache_messages, get_cached_messages, invalidate_message_cache,
    cache_jwt_validation, get_cached_jwt_validation, invalidate_jwt_cache
)
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    with patch('cache.redis_client') as mock:
        mock.setex = AsyncMock()
        mock.get = AsyncMock()
        mock.delete = AsyncMock()
        yield mock


@pytest.mark.asyncio
async def test_cache_messages(mock_redis):
    """Test message caching."""
    messages = [
        {
            "sender": "alice",
            "recipient": "bob",
            "encrypted_content": "encrypted",
            "timestamp": datetime.now()
        }
    ]

    await cache_messages("alice", messages, ttl=300)

    # Verify setex was called
    mock_redis.setex.assert_called_once()
    call_args = mock_redis.setex.call_args
    assert call_args[0][0] == "messages:alice"  # Key
    assert call_args[0][1] == 300  # TTL


@pytest.mark.asyncio
async def test_get_cached_messages(mock_redis):
    """Test retrieving cached messages."""
    # Mock Redis returning cached data
    mock_redis.get.return_value = '[{"sender":"alice","recipient":"bob","encrypted_content":"test","timestamp":"2024-01-01T00:00:00"}]'

    result = await get_cached_messages("alice")

    assert result is not None
    assert len(result) == 1
    assert result[0]["sender"] == "alice"


@pytest.mark.asyncio
async def test_get_cached_messages_miss(mock_redis):
    """Test cache miss."""
    mock_redis.get.return_value = None

    result = await get_cached_messages("alice")

    assert result is None


@pytest.mark.asyncio
async def test_invalidate_message_cache(mock_redis):
    """Test cache invalidation."""
    await invalidate_message_cache("alice")

    mock_redis.delete.assert_called_once_with("messages:alice")


@pytest.mark.asyncio
async def test_cache_jwt_validation(mock_redis):
    """Test JWT validation caching."""
    await cache_jwt_validation("token123", "alice", ttl=300)

    mock_redis.setex.assert_called_once_with("jwt:token123", 300, "alice")


@pytest.mark.asyncio
async def test_get_cached_jwt_validation(mock_redis):
    """Test retrieving cached JWT validation."""
    mock_redis.get.return_value = "alice"

    result = await get_cached_jwt_validation("token123")

    assert result == "alice"


@pytest.mark.asyncio
async def test_invalidate_jwt_cache(mock_redis):
    """Test JWT cache invalidation."""
    await invalidate_jwt_cache("token123")

    mock_redis.delete.assert_called_once_with("jwt:token123")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
