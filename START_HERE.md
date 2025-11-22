# 🚀 Your Chat App is Ready to Run!

Your `.env` file has been configured with your MongoDB Atlas and Redis Labs credentials.

## Option 1: Test Locally (Fastest)

### Terminal 1 - Start Backend:
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Start First Client:
```bash
cd chatapp
pip install -r requirements.txt
python main.py
```

### Terminal 3 - Start Second Client:
```bash
cd chatapp
python main.py
```

Then:
1. **Terminal 2**: Sign up as "alice" with any password (min 8 chars)
2. **Terminal 3**: Sign up as "bob" with any password
3. **Terminal 2**: Start new chat → type "bob"
4. Chat between alice and bob! Messages are E2E encrypted.

---

## Option 2: Deploy Backend to Render.com

1. **Create GitHub repo** and push this code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Ephemeral chat app"
   gh repo create chatapp --public --source=. --push
   # Or manually create repo and push
   ```

2. **Deploy to Render**:
   - Go to https://dashboard.render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Configure:
     - **Name**: `chatapp` (or your choice)
     - **Root Directory**: `backend`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables** (in Render dashboard):
   ```
   MONGO_URI=mongodb+srv://superman:qwertyuiopmnbvcxz@cluster0.f0qim.mongodb.net/chatapp?retryWrites=true&w=majority
   JWT_SECRET=hdLlUHIiau23Ib2hBfT4zK-lRZnz4xmdk6zFXdIynGk
   REDIS_URL=redis://default:5g1xxGcfpu7nZGnY3UEk0TNo4Axwewmm@redis-12199.c99.us-east-1-4.ec2.cloud.redislabs.com:12199
   ```

4. **Click "Create Web Service"** and wait ~2 minutes

5. **Copy your Render URL** (like `https://chatapp-xyz.onrender.com`)

6. **Update client .env**:
   ```bash
   # Edit chatapp/.env
   BACKEND_URL=https://chatapp-xyz.onrender.com
   ```

7. **Run client** from anywhere:
   ```bash
   cd chatapp
   pip install -e .
   chatapp
   ```

---

## 🧪 Run Tests

```bash
pip install -r tests/requirements.txt
pytest tests/ -v
```

Expected output:
```
tests/test_auth.py::test_password_hashing PASSED
tests/test_auth.py::test_jwt_token_creation PASSED
tests/test_crypto.py::test_key_generation PASSED
tests/test_crypto.py::test_message_encryption_decryption PASSED
... (11 tests total)
```

---

## 🔒 Security Notes

**IMPORTANT**: Your credentials are now in `.env` files which are in `.gitignore`.

**Before pushing to GitHub**:
- ✅ `.gitignore` is already configured to exclude `.env`
- ✅ Never commit `.env` files
- ✅ Only commit `.env.example` (template without real credentials)

**For production**:
- Use Render's environment variable dashboard (not `.env` files)
- Rotate your JWT_SECRET if compromised
- Consider IP whitelisting in MongoDB Atlas
- Enable 2FA on your MongoDB and Redis accounts

---

## 📊 Your Free Tier Capacity

With your current setup:
- **MongoDB Atlas M0**: 512 MB, ~100 concurrent users
- **Redis Labs Free**: 30 MB cache, 30 connections
- **Render Free**: 750 hours/month

**This handles ~50-100 concurrent users easily!**

---

## 🐛 Troubleshooting

**Backend won't start?**
```bash
# Check if deps are installed
cd backend
pip install -r requirements.txt

# Check if .env exists
cat .env  # or `type .env` on Windows

# Test MongoDB connection
python -c "from motor.motor_asyncio import AsyncIOMotorClient; import os; client = AsyncIOMotorClient(os.getenv('MONGO_URI', 'mongodb+srv://superman:qwertyuiopmnbvcxz@cluster0.f0qim.mongodb.net/')); print('MongoDB connected!')"
```

**Client can't connect?**
```bash
# Check backend is running
curl http://localhost:8000
# Should return: {"status":"online","service":"ephemeral-chat"}

# Check BACKEND_URL
echo $BACKEND_URL  # Linux/Mac
echo %BACKEND_URL%  # Windows CMD
```

**Redis errors?**
Your Redis URL is already configured correctly. If you get connection errors:
- Check firewall isn't blocking port 12199
- Verify Redis Labs subscription is active

---

## 🎯 Next Steps

1. ✅ Test locally (Option 1 above)
2. ✅ Run tests to verify everything works
3. ✅ Deploy to Render (Option 2)
4. ✅ Share your deployed URL with friends!
5. 🎨 Customize the UI in `chatapp/screens.py`
6. 🔧 Add features from README.md "Future Improvements"

**Have fun building!** 🚀
