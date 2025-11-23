"""
Tests for Redis caching layer.
Verifies caching and invalidation logic.
"""
import pytest
import sys
import os
from datetime import datetime
import json
from unittest.mock import AsyncMock, MagicMock, patch
from importlib import reload

# Add backend to path FIRST
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


@pytest.fixture
def fresh_cache_module():
    """Get a fresh cache module instance for each test."""
    # Remove cache from sys.modules if it exists
    if 'cache' in sys.modules:
        del sys.modules['cache']

    # Import fresh cache module
    import cache

    # Create mock redis client
    mock_redis = MagicMock()
    mock_redis.setex = AsyncMock()
    mock_redis.get = AsyncMock()
    mock_redis.delete = AsyncMock()
    mock_redis.aclose = AsyncMock()

    # Replace the redis_client in the module
    cache.redis_client = mock_redis

    return cache, mock_redis


@pytest.mark.asyncio
async def test_cache_messages(fresh_cache_module):
    """Test message caching."""
    cache_module, mock_redis = fresh_cache_module

    messages = [
        {
            "sender": "alice",
            "recipient": "bob",
            "encrypted_content": "encrypted",
            "timestamp": datetime.now()
        }
    ]

    await cache_module.cache_messages("alice", messages, ttl=300)

    # Verify setex was called
    mock_redis.setex.assert_called_once()
    call_args = mock_redis.setex.call_args
    assert call_args[0][0] == "messages:alice"  # Key
    assert call_args[0][1] == 300  # TTL


@pytest.mark.asyncio
async def test_get_cached_messages(fresh_cache_module):
    """Test retrieving cached messages."""
    cache_module, mock_redis = fresh_cache_module

    # Mock Redis returning cached data
    cached_data = json.dumps([{
        "sender": "alice",
        "recipient": "bob",
        "encrypted_content": "test",
        "timestamp": "2024-01-01T00:00:00"
    }])
    mock_redis.get.return_value = cached_data

    result = await cache_module.get_cached_messages("alice")

    assert result is not None
    assert len(result) == 1
    assert result[0]["sender"] == "alice"


@pytest.mark.asyncio
async def test_get_cached_messages_miss(fresh_cache_module):
    """Test cache miss."""
    cache_module, mock_redis = fresh_cache_module

    mock_redis.get.return_value = None

    result = await cache_module.get_cached_messages("alice")

    assert result is None


@pytest.mark.asyncio
async def test_invalidate_message_cache(fresh_cache_module):
    """Test cache invalidation."""
    cache_module, mock_redis = fresh_cache_module

    await cache_module.invalidate_message_cache("alice")

    mock_redis.delete.assert_called_once_with("messages:alice")


@pytest.mark.asyncio
async def test_cache_jwt_validation(fresh_cache_module):
    """Test JWT validation caching."""
    cache_module, mock_redis = fresh_cache_module

    await cache_module.cache_jwt_validation("token123", "alice", ttl=300)

    mock_redis.setex.assert_called_once_with("jwt:token123", 300, "alice")


@pytest.mark.asyncio
async def test_get_cached_jwt_validation(fresh_cache_module):
    """Test retrieving cached JWT validation."""
    cache_module, mock_redis = fresh_cache_module

    mock_redis.get.return_value = "alice"

    result = await cache_module.get_cached_jwt_validation("token123")

    assert result == "alice"


@pytest.mark.asyncio
async def test_invalidate_jwt_cache(fresh_cache_module):
    """Test JWT cache invalidation."""
    cache_module, mock_redis = fresh_cache_module

    await cache_module.invalidate_jwt_cache("token123")

    mock_redis.delete.assert_called_once_with("jwt:token123")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
