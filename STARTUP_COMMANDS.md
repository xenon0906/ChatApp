# 🚀 ChatApp - Custom Startup Commands

Quick reference for starting your ChatApp backend with custom terminal commands.

---

## 📋 Available Commands

### Windows (`.bat` files)
| Command | Purpose | Port |
|---------|---------|------|
| `start-dev.bat` | Development server with auto-reload | 8000 |
| `start-prod.bat` | Production server (no reload) | 10000 |
| `run-tests.bat` | Run full test suite | - |

### Linux/Mac (`.sh` files)
| Command | Purpose | Port |
|---------|---------|------|
| `./start-dev.sh` | Development server with auto-reload | 8000 |
| `./start-prod.sh` | Production server (no reload) | 10000 |
| `./run-tests.sh` | Run full test suite | - |

---

## 🖥️ Usage

### On Windows

```bash
# Start development server
start-dev.bat

# Start production server (testing production config locally)
start-prod.bat

# Run tests
run-tests.bat
```

### On Linux/Mac

```bash
# Start development server
./start-dev.sh

# Start production server
./start-prod.sh

# Run tests
./run-tests.sh
```

---

## 🔧 What Each Script Does

### Development Server (`start-dev`)
- ✅ Checks for `.env` file in `backend/` directory
- ✅ Starts server with **auto-reload** (code changes restart server)
- ✅ Runs on `http://127.0.0.1:8000` (local only)
- ✅ Shows detailed startup messages
- ⚠️ **Only use for development, not production**

**Example:**
```
========================================
  Starting ChatApp Development Server
========================================

[1/2] Checking environment variables...
Environment file found!

[2/2] Starting FastAPI server on http://127.0.0.1:8000
Press Ctrl+C to stop the server

INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Production Server (`start-prod`)
- ✅ Warns if no `.env` file (uses environment variables from platform)
- ✅ Starts server **without auto-reload** (faster, production-ready)
- ✅ Runs on `http://0.0.0.0:10000` (accessible from network)
- ⚠️ Use this to test production configuration locally
- ⚠️ On Render, the port is automatically set via `$PORT` env variable

**Example:**
```
========================================
  Starting ChatApp Production Server
========================================

[1/2] Checking environment variables...
WARNING: .env file not found!
Make sure environment variables are set in your hosting platform

[2/2] Starting FastAPI server on http://0.0.0.0:10000
Production mode (no auto-reload)
```

### Test Runner (`run-tests`)
- ✅ Runs all 35 tests in the test suite
- ✅ Shows verbose output with test results
- ✅ Displays summary at the end

**Example:**
```
========================================
  Running ChatApp Test Suite
========================================

[1/2] Running all tests...
======================= 35 passed in 2.69s =======================

[2/2] Test Summary
========================================
Total tests: 35
```

---

## ⚙️ Environment Variables Required

All servers need these environment variables:

### For Local Development (create `backend/.env`)
```bash
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/chatapp?retryWrites=true&w=majority
JWT_SECRET=your-secret-key-here
REDIS_URL=redis://localhost:6379
# Or use Upstash Redis URL
REDIS_URL=rediss://default:password@host.upstash.io:6379
```

### For Render Deployment
Set these in Render dashboard (Environment tab):
- `MONGO_URI` - Your MongoDB Atlas connection string
- `JWT_SECRET` - Your JWT secret key
- `REDIS_URL` - Your Upstash Redis URL

---

## 🔍 Troubleshooting

### Error: "command not found" (Linux/Mac)
**Problem:** Scripts are not executable

**Solution:**
```bash
chmod +x start-dev.sh start-prod.sh run-tests.sh
```

### Error: ".env file not found" (Development)
**Problem:** Missing environment configuration

**Solution:**
1. Go to `backend/` directory
2. Create `.env` file with required variables (see above)
3. Verify file exists: `ls backend/.env` (Linux/Mac) or `dir backend\.env` (Windows)

### Error: "MongoDB connection failed"
**Problem:** MongoDB connection string is incorrect or MongoDB Atlas is blocking your IP

**Solution:**
1. Check `MONGO_URI` in `.env` is correct
2. In MongoDB Atlas, go to Network Access → Add Current IP Address
3. Verify username and password are correct
4. Check if cluster is running (MongoDB Atlas dashboard)

### Error: "Redis connection failed"
**Problem:** Redis URL is incorrect or Upstash is unreachable

**Solution:**
1. Check `REDIS_URL` in `.env` is correct
2. Verify Upstash Redis database is active
3. Test Redis connection separately

### Port Already in Use
**Problem:** Another process is using port 8000 or 10000

**Windows Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Linux/Mac Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

---

## 🎯 Quick Start Guide

### First Time Setup

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Create `.env` file:**
   ```bash
   cd backend
   # Windows
   copy .env.example .env
   # Linux/Mac
   cp .env.example .env
   ```

3. **Edit `.env` with your credentials:**
   - MongoDB URI
   - JWT Secret
   - Redis URL

4. **Run tests to verify setup:**
   ```bash
   # Windows
   run-tests.bat

   # Linux/Mac
   ./run-tests.sh
   ```

5. **Start development server:**
   ```bash
   # Windows
   start-dev.bat

   # Linux/Mac
   ./start-dev.sh
   ```

6. **Test the API:**
   - Open browser: http://127.0.0.1:8000
   - Should see: `{"status":"online","service":"ephemeral-chat",...}`

---

## 📚 Additional Commands

### Manual Commands (if scripts don't work)

**Development:**
```bash
cd backend
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

**Production:**
```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 10000
```

**Tests:**
```bash
python -m pytest tests/ -v
```

**Tests with coverage:**
```bash
python -m pytest tests/ --cov=backend --cov-report=html
```

---

## 🌐 Accessing Your Server

### Local Development
- **Backend API:** http://127.0.0.1:8000
- **API Docs:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/

### Production (Render)
- **Backend API:** https://chatapp-cd3r.onrender.com
- **API Docs:** https://chatapp-cd3r.onrender.com/docs
- **Health Check:** https://chatapp-cd3r.onrender.com/

---

## 🎉 Success Indicators

### Development Server Started Successfully
```
INFO:     Will watch for changes in these directories: ['C:\\...\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [####] using WatchFiles
MongoDB connected successfully!
INFO:app:Cache initialized successfully
INFO:     Application startup complete.
```

### Production Server Started Successfully
```
INFO:     Started server process [####]
INFO:     Waiting for application startup.
MongoDB connected successfully!
INFO:app:Cache initialized successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
```

---

## 📖 Related Documentation

- **Deployment:** See `FINAL_RENDER_DEPLOYMENT.md`
- **Test Results:** See `TEST_RESULTS.md`
- **Main README:** See `README.md`
- **Windows SSL Fix:** See `WINDOWS_SSL_FIXED.md`

---

## 💡 Tips

1. **Use development server for coding** - auto-reload saves time
2. **Use production server to test before deploying** - catches production-specific issues
3. **Run tests before committing code** - ensures nothing breaks
4. **Check MongoDB Atlas IP whitelist** - if connection fails
5. **Keep `.env` file secret** - never commit to git (already in `.gitignore`)

---

Happy coding! 🚀
