#!/bin/bash
# Start Frontend Script for Onco-Detect X
cd "$(dirname "$0")"

cd frontend
echo "Starting Next.js development server on http://localhost:3000"
npm run dev
