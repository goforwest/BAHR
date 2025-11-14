#!/bin/bash
set -e

echo "Moving backend/ and frontend/ to src/..."

# Create src/ directory
mkdir -p src

# Move backend to src/
if [[ -d "backend" ]]; then
    git mv backend src/backend
    echo "  Moved: backend/ → src/backend/"
fi

# Move frontend to src/
if [[ -d "frontend" ]]; then
    git mv frontend src/frontend
    echo "  Moved: frontend/ → src/frontend/"
fi

echo "✓ Backend and frontend moved to src/"
