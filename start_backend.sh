#!/bin/bash
# Ensure we are in the project root
cd "$(dirname "$0")"

# Source virtual environment
source venv/bin/activate

# Navigate to backend directory
cd backend

# Run uvicorn
# Use python -m uvicorn to ensure it uses the venv's python
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
