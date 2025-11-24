#!/bin/bash
# Test runner script for Semantica

set -e

echo "🧪 Running Semantica tests..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with coverage
echo "Running pytest with coverage..."
pytest --cov=semantica --cov-report=html --cov-report=term-missing -v

echo ""
echo "✅ Tests complete!"
echo "📊 Coverage report generated in htmlcov/index.html"

