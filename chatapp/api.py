"""
HTTP and WebSocket client helpers for communicating with the backend.
Uses httpx for async HTTP and websockets for real-time communication.
"""
import os
import asyncio
from typing import Optional, Callable, List, Dict
import httpx
from websockets.asyncio.client import connect as ws_connect
from websockets.exceptions import ConnectionClosed
import logging

# Backend URL from env or default to localhost
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
WS_URL = BACKEND_URL.replace("http://", "ws://").replace("https://", "wss://")

logger = logging.getLogger(__name__)


class APIClient:
    """Async HTTP client for backend API calls."""

    def __init__(self):
        self.token: Optional[str] = None
        self.username: Optional[str] = None
        self.client = httpx.AsyncClient(base_url=BACKEND_URL, timeout=10.0)

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    async def signup(self, username: str, password: str) -> bool:
        """Sign up a new user. Returns True if successful."""
        try:
            response = await self.client.post(
                "/signup",
                json={"username": username, "password": password}
            )
            if response.status_code == 201:
                data = response.json()
                self.token = data["access_token"]
                self.username = username.lower()
                return True
            return False
        except httpx.HTTPError as e:
            logger.error(f"Signup error: {e}")
            return False

    async def login(self, username: str, password: str) -> bool:
        """Log in a user. Returns True if successful."""
        try:
            response = await self.client.post(
                "/login",
                json={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                self.username = username.lower()
                return True
            return False
        except httpx.HTTPError as e:
            logger.error(f"Login error: {e}")
            return False

    async def send_message(self, recipient: str, encrypted_content: str) -> bool:
        """Send an encrypted message to a recipient."""
        if not self.token:
            return False

        try:
            response = await self.client.post(
                "/messages",
                json={"recipient": recipient, "encrypted_content": encrypted_content},
                params={"token": self.token}
            )
            return response.status_code == 201
        except httpx.HTTPError as e:
            logger.error(f"Send message error: {e}")
            return False

    async def get_messages(self, other_user: str) -> List[Dict]:
        """Fetch messages with another user."""
        if not self.token:
            return []

        try:
            response = await self.client.get(
                f"/messages/{other_user}",
                params={"token": self.token}
            )
            if response.status_code == 200:
                return response.json()
            return []
        except httpx.HTTPError as e:
            logger.error(f"Get messages error: {e}")
            return []

    async def get_contacts(self) -> List[str]:
        """Get list of recent chat contacts."""
        if not self.token:
            return []

        try:
            response = await self.client.get(
                "/contacts",
                params={"token": self.token}
            )
            if response.status_code == 200:
                return response.json()
            return []
        except httpx.HTTPError as e:
            logger.error(f"Get contacts error: {e}")
            return []


class WebSocketClient:
    """
    WebSocket client for real-time message updates.
    Reconnects automatically on disconnect.
    """

    def __init__(self, username: str, token: str, on_message: Callable):
        self.username = username
        self.token = token
        self.on_message = on_message
        self.ws = None
        self.running = False
        self.reconnect_delay = 2  # Seconds

    async def connect(self):
        """Connect to WebSocket and start listening."""
        self.running = True
        while self.running:
            try:
                ws_url = f"{WS_URL}/ws/{self.username}?token={self.token}"
                async with ws_connect(ws_url) as websocket:
                    self.ws = websocket
                    logger.info("WebSocket connected")

                    # Send periodic pings to keep connection alive
                    async def ping_loop():
                        while self.running:
                            try:
                                await websocket.send('{"type": "ping"}')
                                await asyncio.sleep(30)
                            except:
                                break

                    ping_task = asyncio.create_task(ping_loop())

                    # Listen for messages
                    try:
                        async for message in websocket:
                            if self.on_message:
                                await self.on_message(message)
                    except ConnectionClosed:
                        logger.warning("WebSocket connection closed")
                    finally:
                        ping_task.cancel()

            except Exception as e:
                logger.error(f"WebSocket error: {e}")

            # Reconnect after delay if still running
            if self.running:
                await asyncio.sleep(self.reconnect_delay)

    async def disconnect(self):
        """Disconnect from WebSocket."""
        self.running = False
        if self.ws:
            await self.ws.close()


# Global instances
api_client = APIClient()
ws_client: Optional[WebSocketClient] = None
