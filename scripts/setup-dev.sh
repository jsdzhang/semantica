#!/bin/bash
# Development environment setup script for Semantica

set -e

echo "🚀 Setting up Semantica development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "📦 Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install project in editable mode with dev dependencies
echo "📥 Installing Semantica with dev dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install

# Verify installation
echo "✅ Verifying installation..."
python -c "import semantica; print(f'Semantica version: {semantica.__version__}')"

echo ""
echo "✨ Development environment setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run tests:"
echo "  pytest"
echo ""
echo "To format code:"
echo "  black semantica/ tests/"
echo "  isort semantica/ tests/"
echo ""
echo "To run all checks:"
echo "  pre-commit run --all-files"

