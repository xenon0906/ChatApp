"""
Redis caching layer for speed optimization on free tier.
Caches recent messages and JWT validation results to reduce DB hits.
This was a bit fiddly to get the async right, but it pays off in perf.
"""
import os
import json
from typing import Optional, List
from redis.asyncio import Redis, ConnectionPool
from datetime import datetime

# Redis connection from env
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Connection pool for async operations
pool: Optional[ConnectionPool] = None
redis_client: Optional[Redis] = None


async def init_redis():
    """Initialize Redis connection pool. Call this on startup."""
    global pool, redis_client
    pool = ConnectionPool.from_url(REDIS_URL, decode_responses=True)
    redis_client = Redis(connection_pool=pool)


async def close_redis():
    """Close Redis connections. Call this on shutdown."""
    if redis_client:
        await redis_client.aclose()
    if pool:
        await pool.aclose()


async def cache_messages(username: str, messages: List[dict], ttl: int = 300):
    """
    Cache messages for a user. TTL defaults to 5 minutes.
    Stores as JSON string for simplicity.
    """
    if not redis_client:
        return

    key = f"messages:{username}"
    # Convert datetime objects to ISO strings for JSON serialization
    serializable_msgs = []
    for msg in messages:
        msg_copy = msg.copy()
        if isinstance(msg_copy.get('timestamp'), datetime):
            msg_copy['timestamp'] = msg_copy['timestamp'].isoformat()
        serializable_msgs.append(msg_copy)

    await redis_client.setex(key, ttl, json.dumps(serializable_msgs))


async def get_cached_messages(username: str) -> Optional[List[dict]]:
    """Retrieve cached messages for a user. Returns None if not cached."""
    if not redis_client:
        return None

    key = f"messages:{username}"
    data = await redis_client.get(key)
    if not data:
        return None

    messages = json.loads(data)
    # Convert ISO strings back to datetime objects
    for msg in messages:
        if 'timestamp' in msg and isinstance(msg['timestamp'], str):
            msg['timestamp'] = datetime.fromisoformat(msg['timestamp'])

    return messages


async def invalidate_message_cache(username: str):
    """Invalidate cached messages when new messages arrive."""
    if not redis_client:
        return

    key = f"messages:{username}"
    await redis_client.delete(key)


async def cache_jwt_validation(token: str, username: str, ttl: int = 300):
    """Cache JWT validation result. TTL matches token lifetime."""
    if not redis_client:
        return

    key = f"jwt:{token}"
    await redis_client.setex(key, ttl, username)


async def get_cached_jwt_validation(token: str) -> Optional[str]:
    """Get cached JWT validation. Returns username or None."""
    if not redis_client:
        return None

    key = f"jwt:{token}"
    return await redis_client.get(key)


async def invalidate_jwt_cache(token: str):
    """Invalidate JWT cache on logout."""
    if not redis_client:
        return

    key = f"jwt:{token}"
    await redis_client.delete(key)
