#!/bin/bash
# Code formatting script for Semantica

set -e

echo "🎨 Formatting Semantica code..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Format with black
echo "Formatting with black..."
black semantica/ tests/

# Sort imports with isort
echo "Sorting imports with isort..."
isort semantica/ tests/

echo ""
echo "✅ Code formatting complete!"

