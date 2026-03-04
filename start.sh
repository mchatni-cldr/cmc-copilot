#!/bin/bash
set -e

echo "=== CMC Co-Pilot Startup ==="

if [ ! -f "frontend/dist/index.html" ]; then
    echo "ERROR: frontend/dist/index.html not found. Run 'cd frontend && npm run build' first."
    exit 1
fi

echo "Frontend dist found. Starting Flask on port ${CDSW_APP_PORT:-5001}..."
cd backend
python app.py
