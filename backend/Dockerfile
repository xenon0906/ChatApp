FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Railway uses dynamic PORT env var)
EXPOSE 8000

# Run the application (uses PORT env var if available, defaults to 8000)
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
