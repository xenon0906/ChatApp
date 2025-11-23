@echo off
REM Development server startup script for Windows
REM Starts the backend on port 8000

echo ========================================
echo   Starting ChatApp Development Server
echo ========================================
echo.

cd backend

echo [1/2] Checking environment variables...
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please create backend/.env with:
    echo   MONGO_URI=your_mongodb_uri
    echo   JWT_SECRET=your_jwt_secret
    echo   REDIS_URL=your_redis_url
    pause
    exit /b 1
)
echo Environment file found!
echo.

echo [2/2] Starting FastAPI server on http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.

uvicorn app:app --host 127.0.0.1 --port 8000 --reload
