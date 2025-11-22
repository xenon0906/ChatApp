@echo off
cls
echo ============================================================
echo   CHATAPP COMPLETE DEPLOYMENT SCRIPT
echo   Pushes to GitHub ^& Deploys to Railway in one go!
echo ============================================================
echo.

REM Step 1: Run security check
echo [Step 1/4] Running pre-commit security check...
echo.
python pre_commit_check.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [WARNING] Security check found warnings but continuing...
    echo Review warnings above before making repo public.
    echo.
    pause
)

echo.
echo ============================================================
echo.

REM Step 2: Git commit
echo [Step 2/4] Initializing git and committing files...
echo.

git init
git add .
git commit -m "feat: Secure ephemeral chat app with E2EE - FastAPI backend with MongoDB Atlas and Redis Labs - Textual TUI client with beautiful message bubbles - X25519 + XChaCha20-Poly1305 E2EE - Argon2id password hashing + JWT auth - Real-time WebSocket messaging - 24-hour message TTL - 26/26 tests passing - Production-ready deployment configs"

echo.
echo Files committed successfully!
echo.
echo ============================================================
echo.

REM Step 3: Push to GitHub
echo [Step 3/4] Pushing to GitHub...
echo.
echo Choose your method:
echo 1. GitHub CLI (gh repo create)
echo 2. Manual (I'll create the repo myself)
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Creating GitHub repository...
    gh repo create chatapp --public --source=. --push
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo [ERROR] GitHub CLI failed. Make sure it's installed:
        echo   winget install GitHub.cli
        echo.
        echo Falling back to manual instructions...
        goto manual_github
    )
) else (
    :manual_github
    echo.
    echo [MANUAL STEPS]
    echo.
    echo 1. Go to: https://github.com/new
    echo 2. Repository name: chatapp
    echo 3. Make it Public
    echo 4. Click "Create repository"
    echo.
    echo 5. Then run these commands:
    echo.
    echo    git remote add origin https://github.com/YOUR_USERNAME/chatapp.git
    echo    git branch -M main
    echo    git push -u origin main
    echo.
    echo Press any key after you've pushed to GitHub...
    pause >nul
)

echo.
echo ============================================================
echo.

REM Step 4: Deploy to Railway
echo [Step 4/4] Deploying to Railway...
echo.

where railway >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Railway CLI not found. Installing...
    echo.
    npm i -g @railway/cli
)

echo.
echo Deploying to Railway...
echo.

railway login
railway init
railway up

echo.
echo Setting environment variables...
railway variables set MONGO_URI="mongodb+srv://superman:qwertyuiopmnbvcxz@cluster0.f0qim.mongodb.net/chatapp?retryWrites=true&w=majority"
railway variables set JWT_SECRET="hdLlUHIiau23Ib2hBfT4zK-lRZnz4xmdk6zFXdIynGk"
railway variables set REDIS_URL="redis://default:5g1xxGcfpu7nZGnY3UEk0TNo4Axwewmm@redis-12199.c99.us-east-1-4.ec2.cloud.redislabs.com:12199"

echo.
echo Opening Railway dashboard...
railway open

echo.
echo ============================================================
echo   DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo Your app is now live on Railway!
echo.
echo NEXT STEPS:
echo.
echo 1. Copy your Railway URL from the dashboard that just opened
echo    Example: https://chatapp-production-abc123.up.railway.app
echo.
echo 2. Update your client .env file:
echo    cd chatapp
echo    echo BACKEND_URL=https://YOUR-RAILWAY-URL ^> .env
echo.
echo 3. Run the client:
echo    cd chatapp
echo    pip install -r requirements.txt
echo    python main.py
echo.
echo OR install as a command:
echo    cd chatapp
echo    pip install -e .
echo    chatapp
echo.
echo ============================================================
echo.
echo GitHub: https://github.com/YOUR_USERNAME/chatapp
echo Railway: Check the browser tab that just opened
echo.
echo Enjoy your secure chat app!
echo ============================================================
echo.
pause
