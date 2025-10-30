#!/usr/bin/env sh
set -eu

# Default PORT if not provided by Railway
export PORT="${PORT:-8080}"

# Move into the ml_service directory where the FastAPI app lives
cd "$(dirname "$0")/ml_service"

# Ensure Python dependencies are installed (handles Shell build via Railpack)
python -m pip install --upgrade pip
pip install -r requirements.txt

# Start the FastAPI server
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"


