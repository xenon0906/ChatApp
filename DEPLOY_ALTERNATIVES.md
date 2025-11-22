# Alternative Free Deployment Options

Since you've hit Render's free limit, here are 5 excellent alternatives!

---

## 🚀 Option 1: Railway.app (RECOMMENDED)

**Free Tier:** $5 monthly credit (enough for this app)
**Pros:** Similar to Render, easy setup, great for FastAPI

### Setup Steps:

1. **Sign up:** https://railway.app/
2. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   # Or: pip install railway
   ```

3. **Login & Deploy:**
   ```bash
   cd C:\Users\siddh\OneDrive\Desktop\chatapp\backend
   railway login
   railway init
   railway up
   ```

4. **Add Environment Variables:**
   ```bash
   railway variables set MONGO_URI="mongodb+srv://superman:qwertyuiopmnbvcxz@cluster0.f0qim.mongodb.net/chatapp?retryWrites=true&w=majority"
   railway variables set JWT_SECRET="hdLlUHIiau23Ib2hBfT4zK-lRZnz4xmdk6zFXdIynGk"
   railway variables set REDIS_URL="redis://default:5g1xxGcfpu7nZGnY3UEk0TNo4Axwewmm@redis-12199.c99.us-east-1-4.ec2.cloud.redislabs.com:12199"
   ```

5. **Create `Procfile`** (in backend folder):
   ```
   web: uvicorn app:app --host 0.0.0.0 --port $PORT
   ```

6. **Deploy:** Railway auto-deploys. Get URL from dashboard.

---

## 🚀 Option 2: Fly.io

**Free Tier:** 3 VMs, plenty for this app
**Pros:** Fast, global edge network, Docker-based

### Setup Steps:

1. **Install Fly CLI:**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Sign up & Login:**
   ```bash
   fly auth signup
   fly auth login
   ```

3. **Create `Dockerfile`** in `backend/`:
   ```dockerfile
   FROM python:3.12-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8000

   CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

4. **Launch App:**
   ```bash
   cd backend
   fly launch
   # Answer prompts:
   # - App name: chatapp-yourname
   # - Region: Choose nearest
   # - PostgreSQL: No
   # - Redis: No (we have Redis Labs)
   ```

5. **Set Secrets:**
   ```bash
   fly secrets set MONGO_URI="mongodb+srv://superman:qwertyuiopmnbvcxz@cluster0.f0qim.mongodb.net/chatapp?retryWrites=true&w=majority"
   fly secrets set JWT_SECRET="hdLlUHIiau23Ib2hBfT4zK-lRZnz4xmdk6zFXdIynGk"
   fly secrets set REDIS_URL="redis://default:5g1xxGcfpu7nZGnY3UEk0TNo4Axwewmm@redis-12199.c99.us-east-1-4.ec2.cloud.redislabs.com:12199"
   ```

6. **Deploy:**
   ```bash
   fly deploy
   fly open
   ```

---

## 🚀 Option 3: Vercel (Serverless)

**Free Tier:** Generous, perfect for APIs
**Pros:** Fast, simple, serverless

### Setup Steps:

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Create `vercel.json`** in `backend/`:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ],
     "env": {
       "MONGO_URI": "@mongo_uri",
       "JWT_SECRET": "@jwt_secret",
       "REDIS_URL": "@redis_url"
     }
   }
   ```

3. **Deploy:**
   ```bash
   cd backend
   vercel
   # Follow prompts
   ```

4. **Add Secrets:**
   ```bash
   vercel env add MONGO_URI
   # Paste: mongodb+srv://superman:qwertyuiopmnbvcxz@cluster0.f0qim.mongodb.net/chatapp

   vercel env add JWT_SECRET
   # Paste: hdLlUHIiau23Ib2hBfT4zK-lRZnz4xmdk6zFXdIynGk

   vercel env add REDIS_URL
   # Paste: redis://default:5g1xxGcfpu7nZGnY3UEk0TNo4Axwewmm@...
   ```

5. **Redeploy:**
   ```bash
   vercel --prod
   ```

---

## 🚀 Option 4: PythonAnywhere

**Free Tier:** 1 web app, perfect for small projects
**Pros:** Python-specific, easy setup, no credit card

### Setup Steps:

1. **Sign up:** https://www.pythonanywhere.com/registration/register/beginner/

2. **Upload Code:**
   - Go to "Files" tab
   - Upload `backend/` folder contents
   - Or use Git:
     ```bash
     git clone https://github.com/YOUR_USERNAME/chatapp.git
     ```

3. **Setup Virtual Environment:**
   ```bash
   # In PythonAnywhere console:
   mkvirtualenv chatapp --python=/usr/bin/python3.12
   pip install -r requirements.txt
   ```

4. **Configure Web App:**
   - Go to "Web" tab → "Add a new web app"
   - Choose "Manual configuration" → Python 3.12
   - Set source code: `/home/yourusername/chatapp/backend`
   - Edit WSGI file:
     ```python
     import sys
     import os

     path = '/home/yourusername/chatapp/backend'
     if path not in sys.path:
         sys.path.append(path)

     # Set environment variables
     os.environ['MONGO_URI'] = 'mongodb+srv://superman:qwertyuiopmnbvcxz@cluster0.f0qim.mongodb.net/chatapp'
     os.environ['JWT_SECRET'] = 'hdLlUHIiau23Ib2hBfT4zK-lRZnz4xmdk6zFXdIynGk'
     os.environ['REDIS_URL'] = 'redis://default:5g1xxGcfpu7nZGnY3UEk0TNo4Axwewmm@redis-12199.c99.us-east-1-4.ec2.cloud.redislabs.com:12199'

     from app import app as application
     ```

5. **Reload & Test:**
   - Click "Reload" button
   - Visit: `https://yourusername.pythonanywhere.com/`

**Note:** PythonAnywhere free tier doesn't support WebSockets, so real-time messaging won't work. Use for testing HTTP endpoints only.

---

## 🚀 Option 5: Replit (EASIEST!)

**Free Tier:** Unlimited repls (with some limits)
**Pros:** Zero setup, built-in editor, instant deploy

### Setup Steps:

1. **Sign up:** https://replit.com/signup

2. **Create New Repl:**
   - Click "+ Create Repl"
   - Template: "Python"
   - Title: "chatapp-backend"

3. **Upload Code:**
   - Drag and drop `backend/` files
   - Or import from GitHub

4. **Add Secrets:**
   - Click "Secrets" (lock icon in sidebar)
   - Add:
     ```
     MONGO_URI = mongodb+srv://superman:qwertyuiopmnbvcxz@cluster0.f0qim.mongodb.net/chatapp
     JWT_SECRET = hdLlUHIiau23Ib2hBfT4zK-lRZnz4xmdk6zFXdIynGk
     REDIS_URL = redis://default:5g1xxGcfpu7nZGnY3UEk0TNo4Axwewmm@redis-12199.c99.us-east-1-4.ec2.cloud.redislabs.com:12199
     ```

5. **Configure Run:**
   - Create `.replit` file:
     ```toml
     run = "uvicorn app:app --host 0.0.0.0 --port 8000"

     [nix]
     channel = "stable-23_11"

     [deployment]
     run = ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
     ```

6. **Click "Run"** - Replit auto-deploys!
   - URL: `https://chatapp-backend.yourname.repl.co`

---

## 📊 Comparison Table

| Platform | Free Tier | WebSockets | Setup Difficulty | Speed |
|----------|-----------|------------|------------------|-------|
| **Railway** | $5/mo credit | ✅ Yes | ⭐⭐ Easy | ⚡ Fast |
| **Fly.io** | 3 VMs | ✅ Yes | ⭐⭐⭐ Medium | ⚡⚡ Very Fast |
| **Vercel** | Generous | ✅ Yes* | ⭐⭐ Easy | ⚡⚡ Very Fast |
| **PythonAnywhere** | 1 app | ❌ No | ⭐ Very Easy | ⚡ Moderate |
| **Replit** | Unlimited | ✅ Yes | ⭐ Easiest | ⚡ Moderate |

*Vercel WebSockets have 10-second timeout on free tier

---

## 🎯 **RECOMMENDED: Railway.app**

**Why Railway?**
- Almost identical to Render
- $5/month credit (plenty for this app)
- Supports WebSockets fully
- Easy CLI deployment
- Great dashboard

### Quick Railway Deploy (2 minutes):

```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
cd C:\Users\siddh\OneDrive\Desktop\chatapp\backend
railway login
railway init
railway up

# Add environment variables
railway variables set MONGO_URI="mongodb+srv://superman:qwertyuiopmnbvcxz@cluster0.f0qim.mongodb.net/chatapp?retryWrites=true&w=majority"
railway variables set JWT_SECRET="hdLlUHIiau23Ib2hBfT4zK-lRZnz4xmdk6zFXdIynGk"
railway variables set REDIS_URL="redis://default:5g1xxGcfpu7nZGnY3UEk0TNo4Axwewmm@redis-12199.c99.us-east-1-4.ec2.cloud.redislabs.com:12199"

# Get your URL
railway open
```

**Done!** Your app is live.

---

## 🚨 Alternative: Run Locally (Testing)

If you just want to test, run backend locally:

### Terminal 1 - Backend:
```bash
cd C:\Users\siddh\OneDrive\Desktop\chatapp\backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Terminal 2 - Client 1:
```bash
cd C:\Users\siddh\OneDrive\Desktop\chatapp\chatapp
set BACKEND_URL=http://localhost:8000
python main.py
```

### Terminal 3 - Client 2:
```bash
cd C:\Users\siddh\OneDrive\Desktop\chatapp\chatapp
set BACKEND_URL=http://localhost:8000
python main.py
```

**Note:** MongoDB may have SSL issues on Windows. If so, add to `backend/db.py`:
```python
client = AsyncIOMotorClient(
    MONGO_URI,
    tlsAllowInvalidCertificates=True  # For local dev only
)
```

---

## 💡 **My Recommendation**

### For Quick Testing:
→ **Replit** (click Run, instant deploy)

### For Production:
→ **Railway** (best Render alternative, same features)

### For Learning:
→ **Fly.io** (learn Docker, edge deployments)

Choose Railway if you want the fastest deployment with full features! 🚀
