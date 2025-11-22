#!/bin/bash
# Linux/Mac shell script for local development

echo "Starting local development environment..."
echo ""

# Set environment variables
export MONGO_URI=mongodb://localhost:27017
export JWT_SECRET=dev-secret-change-in-production
export REDIS_URL=redis://localhost:6379
export BACKEND_URL=http://localhost:8000

echo "Environment variables set:"
echo "MONGO_URI=$MONGO_URI"
echo "JWT_SECRET=$JWT_SECRET"
echo "REDIS_URL=$REDIS_URL"
echo "BACKEND_URL=$BACKEND_URL"
echo ""

# Check if running backend or client
if [ "$1" = "backend" ]; then
    echo "Starting backend server..."
    cd backend
    uvicorn app:app --reload --host 0.0.0.0 --port 8000
elif [ "$1" = "client" ]; then
    echo "Starting client..."
    cd chatapp
    python main.py
else
    echo "Usage:"
    echo "  ./run_dev.sh backend  - Start backend server"
    echo "  ./run_dev.sh client   - Start client app"
    echo ""
    echo "Make sure MongoDB and Redis are running first!"
    echo "  docker run -d -p 27017:27017 mongo:latest"
    echo "  docker run -d -p 6379:6379 redis:latest"
fi
