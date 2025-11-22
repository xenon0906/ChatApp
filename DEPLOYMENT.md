# Deployment Guide

## Railway Deployment (Recommended)

### Prerequisites
- Railway account with active subscription ($5/month provides sufficient credits)
- MongoDB Atlas free tier account
- Redis Labs free tier account
- GitHub repository

### Step 1: Environment Setup

Create the following environment variables in Railway:

```bash
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/chatapp?retryWrites=true&w=majority
JWT_SECRET=<generate with: python -c "import secrets; print(secrets.token_urlsafe(32))">
REDIS_URL=redis://default:password@host:port
```

### Step 2: Railway Configuration

1. **Create New Project**
   - Visit https://railway.app/dashboard
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure Service Settings**
   - Navigate to Settings tab
   - Find "Root Directory" setting
   - Set value: `backend`
   - Click "Save"

3. **Add Environment Variables**
   - Go to Variables tab
   - Add the three environment variables listed above
   - Click "Add" for each

4. **Deploy**
   - Go to Deployments tab
   - Click "Deploy"
   - Monitor build logs for errors

### Step 3: Verify Deployment

Once deployed, test the health endpoint:

```bash
curl https://your-app.railway.app/

# Expected response:
{
  "status": "online",
  "service": "ephemeral-chat",
  "database": "connected",
  "cache": "connected",
  "env_configured": {
    "MONGO_URI": true,
    "JWT_SECRET": true,
    "REDIS_URL": true
  }
}
```

### Common Issues

**Healthcheck Failing**

If you see "service unavailable" errors:

1. Check deployment logs for error messages
2. Verify all environment variables are set
3. Test MongoDB connection string separately
4. Test Redis connection string separately
5. Check the health endpoint response for configuration status

**Database Connection Failed**

```
Database initialization failed: ServerSelectionTimeoutError
```

Solutions:
- Verify MongoDB URI is correct
- Check MongoDB Atlas IP whitelist (should include 0.0.0.0/0)
- Ensure MongoDB user has correct permissions
- Test connection using MongoDB Compass

**Cache Connection Failed**

```
Cache initialization failed: ConnectionError
```

Solutions:
- Verify Redis URL is correct
- Check Redis Labs allows external connections
- Test connection using redis-cli

**Build Succeeds but App Crashes**

Check logs for:
- Missing environment variables
- Import errors
- Syntax errors
- Port binding issues

---

## Alternative Deployment Options

### Option 1: Render.com (Limited Free Tier)

**Limitations:**
- 750 hours/month free tier
- Spins down after 15 minutes inactivity
- Limited to 3 free services

**Configuration:**
```yaml
# render.yaml
services:
  - type: web
    name: chatapp-backend
    env: python
    region: oregon
    buildCommand: "cd backend && pip install -r requirements.txt"
    startCommand: "cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: MONGO_URI
        sync: false
      - key: JWT_SECRET
        sync: false
      - key: REDIS_URL
        sync: false
```

### Option 2: Fly.io

**Features:**
- Free tier: 3GB persistent volumes
- Always-on applications
- Global deployment

**Setup:**
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login and initialize
fly auth login
cd backend
fly launch

# Set secrets
fly secrets set MONGO_URI="mongodb+srv://..."
fly secrets set JWT_SECRET="your-secret"
fly secrets set REDIS_URL="redis://..."

# Deploy
fly deploy
```

### Option 3: Google Cloud Run (Free Tier)

**Free Tier:**
- 2 million requests/month
- 180,000 GB-seconds memory
- 360,000 vCPU-seconds compute

**Deployment:**
```bash
# Build and deploy
gcloud run deploy chatapp-backend \
  --source=backend \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars="MONGO_URI=...,JWT_SECRET=...,REDIS_URL=..."
```

### Option 4: Local Deployment

For development or private use:

```bash
# Backend
cd backend
export MONGO_URI="mongodb+srv://..."
export JWT_SECRET="your-secret"
export REDIS_URL="redis://..."
uvicorn app:app --host 0.0.0.0 --port 8000

# Client
cd chatapp
export BACKEND_URL="http://localhost:8000"
python main.py
```

---

## Troubleshooting

### Check Environment Variables

The enhanced health endpoint now shows configuration status:

```bash
curl https://your-app/
```

Response includes:
- `database`: Connection status
- `cache`: Connection status
- `env_configured`: Which environment variables are set

### View Logs

**Railway:**
```bash
railway logs
```

**Render:**
View logs in dashboard under "Logs" tab

**Fly.io:**
```bash
fly logs
```

### Test Endpoints

```bash
# Health check
curl https://your-app/

# Signup
curl -X POST https://your-app/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# Login
curl -X POST https://your-app/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

### Database Connection Testing

Test MongoDB connection separately:

```python
python test_connection.py
```

Expected output:
```
MongoDB connection: SUCCESS
Redis connection: SUCCESS
All connections working properly
```

---

## Performance Optimization

### Free Tier Considerations

**MongoDB Atlas M0:**
- 512 MB storage
- Shared CPU
- Connection pooling enabled by default

**Redis Labs Free:**
- 30 MB storage
- 30 concurrent connections
- 5-minute cache TTL configured

**Railway Free Credits:**
- $5/month usage-based pricing
- Monitor usage in dashboard
- Optimize by reducing unnecessary requests

### Scaling Tips

1. **Enable caching** - Already configured for messages and JWT tokens
2. **Use connection pooling** - Implemented for MongoDB and Redis
3. **Rate limiting** - Configured via slowapi
4. **Optimize queries** - Indexes created on frequently queried fields

---

## Security Checklist

Before deploying to production:

- [ ] All environment variables set correctly
- [ ] MongoDB IP whitelist configured (0.0.0.0/0 for cloud deployments)
- [ ] JWT_SECRET is cryptographically secure (32+ bytes)
- [ ] MongoDB user has minimal required permissions
- [ ] Redis password is strong
- [ ] .env files not committed to git (check .gitignore)
- [ ] HTTPS enabled (automatic on Railway/Render/Fly.io)
- [ ] CORS configured appropriately for your domain

---

## Support

If deployment fails:

1. Check this guide's troubleshooting section
2. Review deployment platform logs
3. Test the health endpoint for configuration status
4. Verify all prerequisites are met
5. Test external services (MongoDB, Redis) separately

Common success indicators:
- Build completes without errors
- Health endpoint returns `"status": "online"`
- Database shows `"connected"`
- Cache shows `"connected"`
- All env variables show `true`
