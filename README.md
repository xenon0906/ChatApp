# Ephemeral Chat - Secure Terminal Chat Application

A cross-platform, secure, ephemeral chat application with end-to-end encryption. Messages automatically expire after 24 hours. Built for free-tier cloud services with performance optimization via Redis caching.

## Features

- **End-to-End Encryption**: X25519 key exchange with XChaCha20-Poly1305 AEAD
- **Ephemeral Messages**: Auto-deletion after 24 hours via MongoDB TTL indexes
- **Real-time Communication**: WebSocket-based instant messaging
- **Terminal UI**: Clean Textual-based interface for cross-platform use
- **Secure Authentication**: Argon2id password hashing with JWT tokens
- **Performance Optimized**: Redis caching for free-tier speed
- **Rate Limited**: Protection against abuse with slowapi

## Architecture

```
┌─────────────┐          ┌──────────────┐          ┌─────────────┐
│   Textual   │  HTTPS   │   FastAPI    │  Async   │   MongoDB   │
│     TUI     │◄────────►│   Backend    │◄────────►│    Atlas    │
│   Client    │  WSS     │              │          │             │
└─────────────┘          └──────────────┘          └─────────────┘
      │                         │
      │                         │
      │                         ▼
      │                  ┌─────────────┐
      │                  │    Redis    │
      └─────────────────►│   Cache     │
        E2EE Keys         │             │
                          └─────────────┘
```

## Security Model

- **Client-side E2EE**: Server sees only encrypted blobs
- **Key Exchange**: Ephemeral X25519 keypairs per session
- **Authentication**: JWT tokens (1hr expiry), Argon2id password hashing
- **Transport Security**: TLS/HTTPS (provided by hosting platform)
- **No Data Logging**: Sensitive data never logged

## Project Structure

```
chatapp/
├── backend/
│   ├── app.py           # FastAPI application
│   ├── models.py        # Pydantic validation models
│   ├── db.py            # MongoDB operations
│   ├── auth.py          # Authentication utilities
│   ├── cache.py         # Redis caching layer
│   └── requirements.txt
├── chatapp/
│   ├── main.py          # TUI entry point
│   ├── screens.py       # Textual UI screens
│   ├── crypto.py        # E2EE implementation
│   ├── api.py           # HTTP/WebSocket client
│   ├── setup.py         # Package setup
│   └── requirements.txt
└── tests/
    ├── test_auth.py     # Auth tests
    ├── test_crypto.py   # E2EE tests
    ├── test_api.py      # API endpoint tests
    └── test_cache.py    # Redis caching tests
```

## Installation

### Backend Deployment (Railway.app)

1. **Setup MongoDB Atlas** (free tier):
   - Create account at mongodb.com/cloud/atlas
   - Create free M0 cluster
   - Add database user and IP whitelist (0.0.0.0/0)
   - Copy connection string

2. **Setup Redis** (free tier):
   - Create account at redis.com
   - Create free database instance
   - Copy connection string

3. **Deploy to Railway**:
   - Push code to GitHub
   - Visit railway.app/dashboard and create new project
   - Select "Deploy from GitHub repo"
   - In service settings, set **Root Directory** to `backend`
   - Add environment variables:
     ```
     MONGO_URI=mongodb+srv://...
     JWT_SECRET=<generate with: python -c "import secrets; print(secrets.token_urlsafe(32))">
     REDIS_URL=redis://...
     ```
   - Deploy from Deployments tab
   - Copy service URL from Settings → Domains

### Client Installation

**Local Development**:
```bash
cd chatapp
pip install -r requirements.txt

# Set backend URL (use your Railway service URL)
export BACKEND_URL=https://your-app.railway.app

# Run directly
python main.py
```

**Install as Command** (recommended):
```bash
cd chatapp
pip install -e .

# Now you can run from anywhere
chatapp
```

**Cross-platform Distribution**:
```bash
# Create wheel
cd chatapp
python setup.py bdist_wheel

# Install on any system
pip install dist/chatapp-1.0.0-py3-none-any.whl
```

## Usage

1. **Launch the app**:
   ```bash
   chatapp
   ```

2. **Sign up or log in**:
   - Enter username (3-30 chars, alphanumeric)
   - Enter password (8+ chars)

3. **Main menu options**:
   - **1. Start new chat**: Enter username to chat with
   - **2. View recent chats**: See your contact list
   - **3. Logout**: Return to login screen

4. **Chatting**:
   - Type message and press Enter or click Send
   - Messages are E2E encrypted automatically
   - Real-time delivery when recipient is online
   - History shows last 24 hours only

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_crypto.py -v

# Run with coverage
pytest tests/ --cov=backend --cov=chatapp
```

## Performance Optimization

The app is optimized for free-tier performance:

- **Redis Caching**:
  - Recent messages cached for 5 minutes
  - JWT validation cached to reduce crypto overhead
  - Automatic cache invalidation on new messages

- **Database Indexes**:
  - Compound index on (recipient, timestamp) for fast queries
  - TTL index for automatic message expiration
  - Unique index on username

- **Async Throughout**:
  - Motor (async PyMongo) for non-blocking DB operations
  - HTTPX async client for fast HTTP requests
  - WebSocket connection pooling

- **Connection Pooling**:
  - MongoDB connection pool (motor default)
  - Redis connection pool
  - HTTP client reuse

## Development

### Local Development Setup

1. **Start local services** (optional, or use cloud):
   ```bash
   # MongoDB (Docker)
   docker run -d -p 27017:27017 --name mongo mongo:latest

   # Redis (Docker)
   docker run -d -p 6379:6379 --name redis redis:latest
   ```

2. **Set environment variables**:
   ```bash
   export MONGO_URI=mongodb://localhost:27017
   export JWT_SECRET=dev-secret-change-in-production
   export REDIS_URL=redis://localhost:6379
   ```

3. **Run backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app:app --reload
   ```

4. **Run client** (in another terminal):
   ```bash
   cd chatapp
   export BACKEND_URL=http://localhost:8000
   python main.py
   ```

### Code Quality

The codebase follows best practices:

- **Clean, human-written code**: No AI boilerplate
- **Descriptive variables**: Clear intent at a glance
- **Modular functions**: Single responsibility principle
- **Inline comments**: Explain "why", not "what"
- **Type hints**: Python 3.12 modern syntax
- **Async-first**: Non-blocking where it matters

## Limitations & Future Improvements

Current limitations (by design for simplicity):
- No message editing or deletion
- No file attachments
- No group chats
- No message read receipts
- No persistent key storage (keys lost on restart)

Future improvements:
- Secure key persistence (encrypted local storage)
- Push notifications for offline messages
- Desktop notifications
- Message reactions
- Typing indicators
- User presence (online/offline status)

## Security Considerations

**What's Protected**:
- ✅ Passwords (Argon2id hashed)
- ✅ Message content (E2EE, server never sees plaintext)
- ✅ JWT tokens (signed, expiring)
- ✅ Transport (TLS via hosting platform)

**What's Not Protected** (intentionally for MVP):
- ⚠️ Metadata (who talks to whom, when)
- ⚠️ User enumeration (can check if username exists)
- ⚠️ Timing attacks (not hardened against)
- ⚠️ Key persistence (keys regenerated on restart)

For production use, consider:
- Rate limiting by IP (behind reverse proxy)
- CAPTCHA for signup
- Email verification
- Secure key backup mechanism
- Forward secrecy (rotating keys)

## License

MIT License - feel free to use, modify, and distribute.

## Contributing

This is a demonstration project. For production use:
1. Add comprehensive error handling
2. Implement proper key persistence
3. Add input validation on all fields
4. Set up monitoring and logging (without sensitive data)
5. Conduct security audit
6. Add integration tests
7. Implement backup and recovery

## Troubleshooting

**Backend won't start**:
- Check environment variables are set
- Verify MongoDB and Redis URLs are correct
- Check firewall/network access to databases

**Client can't connect**:
- Verify `BACKEND_URL` is set correctly
- Check backend is running and accessible
- Ensure TLS certificates are valid (for HTTPS)

**Messages not delivering**:
- Check WebSocket connection (look for errors in logs)
- Verify both users have valid JWT tokens
- Check Redis is accessible for caching

**Tests failing**:
- Ensure pytest and pytest-asyncio are installed
- Run from project root directory
- Check Python version is 3.12+

## Credits

Built with:
- [Textual](https://textual.textualize.io/) - Terminal UI framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [cryptography](https://cryptography.io/) - Cryptographic primitives
- [Motor](https://motor.readthedocs.io/) - Async MongoDB driver
- [Redis](https://redis.io/) - In-memory data store

---

**Made for learning and demonstration purposes. Use at your own risk.**
# ChatApp
