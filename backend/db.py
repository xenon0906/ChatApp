"""
MongoDB connection and database operations.
Using motor (async PyMongo) for better performance with FastAPI.
"""
import os
import sys
import ssl
from typing import Optional, List
from datetime import datetime, timedelta, timezone
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, IndexModel
from pymongo.errors import DuplicateKeyError

# MongoDB connection from env
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "chatapp"

# Global client and database
client: Optional[AsyncIOMotorClient] = None
db: Optional[AsyncIOMotorDatabase] = None


async def init_db():
    """
    Initialize MongoDB connection and create indexes.
    Indexes are crucial for query performance on free tier.
    """
    global client, db

    # Check if we need to modify the URI for SSL compatibility
    # MongoDB Atlas requires specific SSL/TLS settings
    uri = MONGO_URI

    # If the URI doesn't already have SSL params, add them
    if 'tls=' not in uri.lower() and 'ssl=' not in uri.lower():
        # Add SSL parameters to the URI itself for better compatibility
        separator = '&' if '?' in uri else '?'
        uri = f"{uri}{separator}tls=true&tlsAllowInvalidCertificates=true"

    try:
        # Simplified connection - let MongoDB handle SSL via URI parameters
        # This approach works better across different environments
        client = AsyncIOMotorClient(
            uri,
            serverSelectionTimeoutMS=30000,  # Increased timeout for cloud connections
            connectTimeoutMS=30000,
            socketTimeoutMS=30000
        )

        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connected successfully!")

    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("⚠️  Attempting alternative connection method...")

        try:
            # Alternative: Try with explicit SSL context
            import certifi

            ssl_context = ssl.create_default_context(cafile=certifi.where())
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            client = AsyncIOMotorClient(
                MONGO_URI,
                serverSelectionTimeoutMS=30000,
                tlsCAFile=certifi.where(),
                ssl_cert_reqs=ssl.CERT_NONE,
                connectTimeoutMS=30000
            )

            await client.admin.command('ping')
            print("✅ MongoDB connected with alternative method!")

        except Exception as fallback_error:
            print(f"❌ Alternative connection also failed: {fallback_error}")
            print("⚠️  The app will start but database operations will fail.")
            print("💡 Check: 1) MongoDB URI is correct, 2) Network access allows 0.0.0.0/0")
            # Don't raise - let app start without DB
            return

    db = client[DB_NAME]

    # Create indexes for users collection
    await db.users.create_index([("username", ASCENDING)], unique=True)

    # Create indexes for messages collection
    # Compound index for efficient recipient+timestamp queries
    await db.messages.create_index([
        ("recipient", ASCENDING),
        ("timestamp", ASCENDING)
    ])
    await db.messages.create_index([("sender", ASCENDING)])

    # TTL index to auto-delete messages after 24 hours
    await db.messages.create_index(
        [("timestamp", ASCENDING)],
        expireAfterSeconds=86400  # 24 hours in seconds
    )


async def close_db():
    """Close MongoDB connection. Call this on shutdown."""
    if client:
        client.close()


async def create_user(username: str, hashed_password: str) -> bool:
    """
    Create a new user. Returns True if successful, False if username exists.
    """
    try:
        await db.users.insert_one({
            "username": username,
            "hashed_password": hashed_password,
            "contacts": [],
            "created_at": datetime.now(timezone.utc)
        })
        return True
    except DuplicateKeyError:
        return False


async def get_user(username: str) -> Optional[dict]:
    """Get a user by username. Returns None if not found."""
    return await db.users.find_one({"username": username})


async def add_contact(username: str, contact: str):
    """
    Add a contact to user's contact list (for recent chats).
    Uses $addToSet to avoid duplicates.
    """
    await db.users.update_one(
        {"username": username},
        {"$addToSet": {"contacts": contact}}
    )


async def get_contacts(username: str) -> List[str]:
    """Get user's contact list."""
    user = await get_user(username)
    return user.get("contacts", []) if user else []


async def save_message(sender: str, recipient: str, encrypted_content: str) -> dict:
    """
    Save an encrypted message. Returns the saved document.
    Auto-adds each user to the other's contacts.
    """
    timestamp = datetime.now(timezone.utc)

    message_doc = {
        "sender": sender,
        "recipient": recipient,
        "encrypted_content": encrypted_content,
        "timestamp": timestamp
    }

    result = await db.messages.insert_one(message_doc)
    message_doc["_id"] = result.inserted_id

    # Add contacts asynchronously (don't wait)
    await add_contact(sender, recipient)
    await add_contact(recipient, sender)

    return message_doc


async def get_messages_between(user1: str, user2: str, hours: int = 24) -> List[dict]:
    """
    Get messages between two users from the last N hours.
    Returns messages in chronological order.
    """
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)

    # Find messages in both directions
    cursor = db.messages.find({
        "$or": [
            {"sender": user1, "recipient": user2},
            {"sender": user2, "recipient": user1}
        ],
        "timestamp": {"$gte": cutoff_time}
    }).sort("timestamp", ASCENDING)

    return await cursor.to_list(length=None)


async def get_recent_messages_for_user(username: str, hours: int = 24) -> List[dict]:
    """
    Get all recent messages for a user (sent or received).
    Used for general message fetching.
    """
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)

    cursor = db.messages.find({
        "$or": [
            {"sender": username},
            {"recipient": username}
        ],
        "timestamp": {"$gte": cutoff_time}
    }).sort("timestamp", ASCENDING)

    return await cursor.to_list(length=None)
