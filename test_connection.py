#!/usr/bin/env python3
"""
Quick connection test script.
Verifies MongoDB and Redis connections work with your credentials.
"""
import os
import asyncio
from dotenv import load_dotenv

# Load .env file
load_dotenv()

async def test_mongodb():
    """Test MongoDB Atlas connection."""
    try:
        from motor.motor_asyncio import AsyncIOMotorClient

        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            print("[FAIL] MONGO_URI not found in environment")
            return False

        print(f"\nTesting MongoDB connection...")
        print(f"   URI: {mongo_uri[:50]}...")

        # Add TLS options for Windows compatibility
        client = AsyncIOMotorClient(
            mongo_uri,
            serverSelectionTimeoutMS=10000,
            tlsAllowInvalidCertificates=False  # Set to True for development if SSL issues persist
        )

        # Test connection
        await client.admin.command('ping')

        print("[OK] MongoDB connected successfully!")

        # List databases
        db_list = await client.list_database_names()
        print(f"   Databases: {db_list}")

        client.close()
        return True

    except Exception as e:
        print(f"[FAIL] MongoDB connection failed: {e}")
        return False


async def test_redis():
    """Test Redis Labs connection."""
    try:
        from redis.asyncio import Redis

        redis_url = os.getenv("REDIS_URL")
        if not redis_url:
            print("[FAIL] REDIS_URL not found in environment")
            return False

        print(f"\nTesting Redis connection...")
        print(f"   URL: {redis_url[:50]}...")

        redis_client = Redis.from_url(redis_url, decode_responses=True)

        # Test connection with ping
        result = await redis_client.ping()

        if result:
            print("[OK] Redis connected successfully!")

            # Test set/get
            await redis_client.set("test_key", "test_value", ex=10)
            value = await redis_client.get("test_key")
            print(f"   Test write/read: {value}")

        await redis_client.aclose()
        return True

    except Exception as e:
        print(f"[FAIL] Redis connection failed: {e}")
        return False


def test_jwt_secret():
    """Check JWT secret is set."""
    jwt_secret = os.getenv("JWT_SECRET")

    print(f"\nChecking JWT secret...")

    if not jwt_secret:
        print("[FAIL] JWT_SECRET not found in environment")
        return False

    if jwt_secret == "dev-secret-change-in-production":
        print("[WARN] Using development JWT secret (OK for testing)")
    else:
        print(f"[OK] Custom JWT secret set (length: {len(jwt_secret)})")

    return True


async def main():
    """Run all tests."""
    print("=" * 60)
    print("CONNECTION TEST FOR EPHEMERAL CHAT APP")
    print("=" * 60)

    # Test environment variables
    mongo_ok = await test_mongodb()
    redis_ok = await test_redis()
    jwt_ok = test_jwt_secret()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if mongo_ok and redis_ok and jwt_ok:
        print("[OK] All connections working! You're ready to run the app.")
        print("\nNext steps:")
        print("  1. Start backend: cd backend && uvicorn app:app --reload")
        print("  2. Start client:  cd chatapp && python main.py")
    else:
        print("[FAIL] Some connections failed. Check your .env file.")
        print("\nTroubleshooting:")
        if not mongo_ok:
            print("  * Verify MONGO_URI in .env file")
            print("  * Check MongoDB Atlas IP whitelist (allow 0.0.0.0/0)")
            print("  * Verify username and password are correct")
        if not redis_ok:
            print("  * Verify REDIS_URL in .env file")
            print("  * Check Redis Labs subscription is active")
        if not jwt_ok:
            print("  * Add JWT_SECRET to .env file")

    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
