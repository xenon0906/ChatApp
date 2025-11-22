#!/bin/bash
# Quick deploy script for Railway.app

echo "============================================"
echo "  Railway.app Deployment Script"
echo "============================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "[ERROR] Railway CLI not found!"
    echo ""
    echo "Please install it first:"
    echo "  npm i -g @railway/cli"
    echo ""
    echo "Or using pip:"
    echo "  pip install railway"
    echo ""
    exit 1
fi

echo "[1/5] Logging into Railway..."
railway login

echo ""
echo "[2/5] Initializing project..."
railway init

echo ""
echo "[3/5] Setting environment variables..."
railway variables set MONGO_URI="mongodb+srv://superman:qwertyuiopmnbvcxz@cluster0.f0qim.mongodb.net/chatapp?retryWrites=true&w=majority"
railway variables set JWT_SECRET="hdLlUHIiau23Ib2hBfT4zK-lRZnz4xmdk6zFXdIynGk"
railway variables set REDIS_URL="redis://default:5g1xxGcfpu7nZGnY3UEk0TNo4Axwewmm@redis-12199.c99.us-east-1-4.ec2.cloud.redislabs.com:12199"

echo ""
echo "[4/5] Deploying to Railway..."
railway up

echo ""
echo "[5/5] Opening Railway dashboard..."
railway open

echo ""
echo "============================================"
echo "  Deployment Complete!"
echo "============================================"
echo ""
echo "Your backend is now live!"
echo ""
echo "Next steps:"
echo "1. Copy your Railway URL from the dashboard"
echo "2. Update chatapp/.env with: BACKEND_URL=https://your-app.railway.app"
echo "3. Run the client: cd chatapp && python main.py"
echo ""
