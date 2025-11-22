"""
FastAPI backend for ephemeral chat app.
Handles auth, message storage, and WebSocket real-time communication.
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
from typing import Dict, Set
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from models import UserSignup, UserLogin, MessageSend, MessageResponse, TokenResponse
from auth import hash_password, verify_password, create_jwt_token, verify_jwt_token
from db import (
    init_db, close_db, create_user, get_user, save_message,
    get_messages_between, get_contacts
)
from cache import (
    init_redis, close_redis, cache_messages, get_cached_messages,
    invalidate_message_cache, cache_jwt_validation, get_cached_jwt_validation
)

# Configure logging (avoid sensitive data)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

# WebSocket connection manager
class ConnectionManager:
    """Manages active WebSocket connections for real-time messaging."""
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket
        logger.info(f"User {username} connected via WebSocket")

    def disconnect(self, username: str):
        if username in self.active_connections:
            del self.active_connections[username]
            logger.info(f"User {username} disconnected")

    async def send_message(self, username: str, message: dict):
        """Send a message to a specific user if they're online."""
        if username in self.active_connections:
            try:
                await self.active_connections[username].send_json(message)
            except Exception as e:
                logger.error(f"Error sending to {username}: {e}")
                self.disconnect(username)

manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events for database/cache connections."""
    # Startup
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        logger.warning("App will start but database operations will fail")

    try:
        await init_redis()
        logger.info("Cache initialized successfully")
    except Exception as e:
        logger.error(f"Cache initialization failed: {e}")
        logger.warning("App will start but caching will be disabled")

    yield

    # Shutdown
    try:
        await close_db()
        await close_redis()
        logger.info("Connections closed")
    except Exception as e:
        logger.error(f"Error closing connections: {e}")


# FastAPI app initialization
app = FastAPI(
    title="Ephemeral Chat API",
    description="Secure, E2EE chat with 24h message expiration",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS for development (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency for JWT authentication
async def get_current_user(token: str = Query(...)) -> str:
    """Validate JWT token and return username. Uses cache for speed."""
    # Check cache first
    cached_username = await get_cached_jwt_validation(token)
    if cached_username:
        return cached_username

    # Verify token
    username = verify_jwt_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Cache the result
    await cache_jwt_validation(token, username, ttl=3600)
    return username


@app.get("/")
async def root():
    """Health check endpoint with configuration status."""
    import os
    from db import db
    from cache import redis_client

    config_status = {
        "status": "online",
        "service": "ephemeral-chat",
        "database": "connected" if db is not None else "disconnected",
        "cache": "connected" if redis_client is not None else "disconnected",
        "env_configured": {
            "MONGO_URI": bool(os.getenv("MONGO_URI")),
            "JWT_SECRET": bool(os.getenv("JWT_SECRET")),
            "REDIS_URL": bool(os.getenv("REDIS_URL"))
        }
    }

    return config_status


@app.post("/signup", response_model=TokenResponse, status_code=201)
@limiter.limit("5/minute")  # Strict limit for signup to prevent abuse
async def signup(request, user: UserSignup):
    """
    Create a new user account.
    Returns JWT token immediately so user can start chatting.
    """
    # Hash password with Argon2id
    hashed_pw = hash_password(user.password)

    # Create user in database
    success = await create_user(user.username, hashed_pw)
    if not success:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Generate JWT token
    token = create_jwt_token(user.username)

    logger.info(f"New user created: {user.username}")
    return TokenResponse(access_token=token)


@app.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")  # Standard rate limit
async def login(request, user: UserLogin):
    """Authenticate user and return JWT token."""
    # Get user from database
    db_user = await get_user(user.username.lower())
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    if not verify_password(db_user["hashed_password"], user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token
    token = create_jwt_token(user.username.lower())

    return TokenResponse(access_token=token)


@app.post("/messages", status_code=201)
@limiter.limit("30/minute")  # Higher limit for actual messaging
async def send_message(request, message: MessageSend, username: str = Depends(get_current_user)):
    """
    Send an encrypted message to another user.
    Invalidates cache and notifies recipient via WebSocket if online.
    """
    # Save to database
    saved_msg = await save_message(username, message.recipient, message.encrypted_content)

    # Invalidate cache for both users
    await invalidate_message_cache(username)
    await invalidate_message_cache(message.recipient)

    # Notify recipient via WebSocket if online
    await manager.send_message(message.recipient, {
        "type": "new_message",
        "sender": username,
        "encrypted_content": message.encrypted_content,
        "timestamp": saved_msg["timestamp"].isoformat()
    })

    return {"status": "sent", "timestamp": saved_msg["timestamp"]}


@app.get("/messages/{other_user}", response_model=list[MessageResponse])
@limiter.limit("20/minute")
async def get_messages(request, other_user: str, username: str = Depends(get_current_user)):
    """
    Fetch messages between current user and another user.
    Uses cache for speed, falls back to database.
    """
    # Try cache first (cache key is per user, so we need to check both)
    cached = await get_cached_messages(username)
    if cached:
        # Filter for the specific conversation
        filtered = [
            msg for msg in cached
            if (msg["sender"] == other_user and msg["recipient"] == username) or
               (msg["sender"] == username and msg["recipient"] == other_user)
        ]
        if filtered:
            return filtered

    # Fetch from database
    messages = await get_messages_between(username, other_user)

    # Cache for next time
    if messages:
        await cache_messages(username, messages)

    return messages


@app.get("/contacts", response_model=list[str])
@limiter.limit("20/minute")
async def get_user_contacts(request, username: str = Depends(get_current_user)):
    """Get list of users the current user has chatted with."""
    contacts = await get_contacts(username)
    return contacts


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str, token: str = Query(...)):
    """
    WebSocket connection for real-time messaging.
    Authenticates via JWT token in query params.
    """
    # Verify token
    authenticated_user = verify_jwt_token(token)
    if not authenticated_user or authenticated_user != username:
        await websocket.close(code=1008)  # Policy violation
        return

    await manager.connect(username, websocket)

    try:
        while True:
            # Keep connection alive, handle ping/pong
            data = await websocket.receive_json()

            # Handle different message types if needed
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(username)
    except Exception as e:
        logger.error(f"WebSocket error for {username}: {e}")
        manager.disconnect(username)
