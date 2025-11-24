#!/bin/bash
# Code quality check script for Semantica

set -e

echo "🔍 Running code quality checks..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check formatting
echo "Checking code formatting (black)..."
black --check semantica/ tests/ || { echo "❌ Code formatting issues found. Run: black semantica/ tests/"; exit 1; }

# Check import sorting
echo "Checking import sorting (isort)..."
isort --check-only semantica/ tests/ || { echo "❌ Import sorting issues found. Run: isort semantica/ tests/"; exit 1; }

# Lint with flake8
echo "Linting with flake8..."
flake8 semantica/ tests/ || { echo "❌ Linting issues found."; exit 1; }

# Type check with mypy
echo "Type checking with mypy..."
mypy semantica/ || { echo "⚠️  Type checking issues found (non-blocking)."; }

echo ""
echo "✅ All code quality checks passed!"

