# Quick Start Guide

## For the Impatient Developer

### 1. Setup MongoDB Atlas (2 minutes)

1. Go to https://www.mongodb.com/cloud/atlas/register
2. Create free account → Create free M0 cluster
3. Database Access → Add user (remember username/password)
4. Network Access → Add IP: `0.0.0.0/0` (allow all)
5. Copy connection string (looks like `mongodb+srv://...`)

### 2. Setup Redis (1 minute)

**Option A - Redis Labs**:
1. Go to https://redis.com/try-free/
2. Create free account → Create free database
3. Copy connection string

**Option B - Local Docker**:
```bash
docker run -d -p 6379:6379 redis:latest
# Use: redis://localhost:6379
```

### 3. Deploy Backend to Render (3 minutes)

1. Push this code to GitHub
2. Go to https://render.com → New Web Service
3. Connect your GitHub repo
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   - `MONGO_URI`: (your MongoDB connection string)
   - `JWT_SECRET`: (run `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
   - `REDIS_URL`: (your Redis connection string)
6. Click "Create Web Service"
7. Wait ~2 minutes for deployment
8. Copy your service URL (like `https://yourapp.onrender.com`)

### 4. Run Client Locally (30 seconds)

```bash
cd chatapp
pip install -r requirements.txt

# Set backend URL (use the URL from Render)
export BACKEND_URL=https://yourapp.onrender.com  # Linux/Mac
# OR
set BACKEND_URL=https://yourapp.onrender.com     # Windows CMD
# OR
$env:BACKEND_URL="https://yourapp.onrender.com"  # Windows PowerShell

python main.py
```

### 5. Start Chatting!

1. Sign up with a username and password
2. Start a new chat with another username
3. Open another terminal, run client again, sign up as different user
4. Chat between the two clients!

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

- Read full README.md for architecture details
- Check security considerations
- Run tests to verify everything works
- Customize the UI in `chatapp/screens.py`
- Add features you want!

## Free Tier Limits

**MongoDB Atlas Free (M0)**:
- 512 MB storage
- Shared CPU
- ~100 concurrent connections
- Perfect for this app

**Redis Labs Free**:
- 30 MB storage
- 30 connections
- Good for caching recent messages

**Render Free Tier**:
- Spins down after 15 min inactivity
- 750 hours/month free
- First request after spin-down takes ~30s

**For ~10 users chatting casually, free tier is plenty!**
