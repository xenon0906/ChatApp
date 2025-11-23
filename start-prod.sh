#!/bin/bash
# Production server startup script for Linux/Mac
# Starts the backend on port 10000 (Render default)

echo "========================================"
echo "  Starting ChatApp Production Server"
echo "========================================"
echo ""

cd backend

echo "[1/2] Checking environment variables..."
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Make sure environment variables are set in your hosting platform"
    echo ""
fi

echo "[2/2] Starting FastAPI server on http://0.0.0.0:10000"
echo "Production mode (no auto-reload)"
echo ""

uvicorn app:app --host 0.0.0.0 --port 10000
