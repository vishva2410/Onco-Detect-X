#!/bin/bash
# Start Backend Script for Onco-Detect X
cd "$(dirname "$0")"

if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

cd backend
echo "Starting FastAPI server on http://localhost:8000"
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
