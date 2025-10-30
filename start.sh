#!/usr/bin/env sh
set -eu

# Default PORT if not provided by Railway
export PORT="${PORT:-8080}"

# Move into the ml_service directory where the FastAPI app lives
cd "$(dirname "$0")/ml_service"

# Detect python and pip executables
if command -v python3 >/dev/null 2>&1; then
  PY=python3
else
  PY=python
fi

if command -v pip3 >/dev/null 2>&1; then
  PIP=pip3
else
  PIP=pip
fi

# Ensure Python dependencies are installed (handles Shell build via Railpack)
"$PY" -m pip install --upgrade pip
"$PIP" install -r requirements.txt

# Start the FastAPI server
exec "$PY" -m uvicorn main:app --host 0.0.0.0 --port "$PORT"


