# Quick Start Guide

## Deployment and Setup

### 1. Setup MongoDB Atlas (2 minutes)

1. Visit https://www.mongodb.com/cloud/atlas/register
2. Create free account and M0 cluster
3. Database Access: Add user (save credentials)
4. Network Access: Add IP `0.0.0.0/0` (allow all)
5. Copy connection string (`mongodb+srv://...`)

### 2. Setup Redis (1 minute)

**Option A - Redis Labs**:
1. Visit https://redis.com/try-free/
2. Create free account and database
3. Copy connection string

**Option B - Local Docker**:
```bash
docker run -d -p 6379:6379 redis:latest
# Use: redis://localhost:6379
```

### 3. Deploy Backend to Railway (3 minutes)

1. Push code to GitHub
2. Visit https://railway.app/dashboard
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Configure service settings:
   - Navigate to Settings → **Root Directory**
   - Set value: `backend`
   - Click "Save"
6. Add Environment Variables (Settings → Variables):
   - `MONGO_URI`: Your MongoDB connection string
   - `JWT_SECRET`: Generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`
   - `REDIS_URL`: Your Redis connection string
7. Deploy from Deployments tab
8. Copy service URL from Settings → Domains (e.g., `https://chatapp-production-abc123.up.railway.app`)

### 4. Run Client Locally

```bash
cd chatapp
pip install -r requirements.txt

# Set backend URL (use your Railway service URL)
export BACKEND_URL=https://your-app.railway.app  # Linux/Mac
# OR
set BACKEND_URL=https://your-app.railway.app     # Windows CMD
# OR
$env:BACKEND_URL="https://your-app.railway.app"  # Windows PowerShell

python main.py
```

### 5. Usage

1. Create account with username and password (minimum 8 characters)
2. Start new chat with target username
3. Send encrypted messages in real-time
4. Messages automatically expire after 24 hours

## Development Mode (Local Backend)

### Terminal 1 - Run Backend Locally:
```bash
# Start local MongoDB and Redis (or use cloud)
docker run -d -p 27017:27017 mongo:latest
docker run -d -p 6379:6379 redis:latest

# Set env vars
export MONGO_URI=mongodb://localhost:27017
export JWT_SECRET=dev-secret
export REDIS_URL=redis://localhost:6379

# Run backend
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Run Client:
```bash
export BACKEND_URL=http://localhost:8000

cd chatapp
pip install -r requirements.txt
python main.py
```

## Install as Command

```bash
cd chatapp
pip install -e .

# Now run from anywhere
chatapp
```

## Run Tests

```bash
# Install test deps
pip install -r tests/requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=backend --cov=chatapp
```

## Common Issues

**"Connection refused" error**:
- Backend not running or wrong URL
- Check `BACKEND_URL` is set correctly

**"Authentication failed"**:
- Check JWT_SECRET is the same between deployments
- Token might be expired (1hr lifetime)

**Messages not showing**:
- Check WebSocket connection
- Verify Redis is accessible
- Check browser console/terminal for errors

**Import errors**:
- Make sure you're in the right directory
- Install requirements: `pip install -r requirements.txt`

## Next Steps

- Review README.md for complete architecture documentation
- Examine security implementation details
- Execute test suite to validate functionality
- Customize UI components in `chatapp/screens.py`
- Extend functionality as needed

## Free Tier Limits

**MongoDB Atlas Free (M0)**:
- 512 MB storage
- Shared CPU
- ~100 concurrent connections
- Suitable for moderate usage

**Redis Labs Free**:
- 30 MB storage
- 30 connections
- Adequate for message caching

**Railway Free Tier**:
- $5 monthly credit
- Usage-based pricing
- No sleep/spin-down delays
- Ideal for development and testing

**Estimated capacity: 10-20 concurrent users with typical chat patterns**
