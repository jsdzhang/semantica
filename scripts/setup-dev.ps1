# Development environment setup script for Semantica (PowerShell)

Write-Host "🚀 Setting up Semantica development environment..." -ForegroundColor Cyan

# Check Python version
$pythonVersion = python --version 2>&1
Write-Host "📦 $pythonVersion" -ForegroundColor Green

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install project in editable mode with dev dependencies
Write-Host "📥 Installing Semantica with dev dependencies..." -ForegroundColor Yellow
pip install -e ".[dev]"

# Install pre-commit hooks
Write-Host "🪝 Installing pre-commit hooks..." -ForegroundColor Yellow
pre-commit install

# Verify installation
Write-Host "✅ Verifying installation..." -ForegroundColor Yellow
python -c "import semantica; print(f'Semantica version: {semantica.__version__}')"

Write-Host ""
Write-Host "✨ Development environment setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the virtual environment in the future, run:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To run tests:" -ForegroundColor Cyan
Write-Host "  pytest" -ForegroundColor White
Write-Host ""
Write-Host "To format code:" -ForegroundColor Cyan
Write-Host "  black semantica/ tests/" -ForegroundColor White
Write-Host "  isort semantica/ tests/" -ForegroundColor White
Write-Host ""
Write-Host "To run all checks:" -ForegroundColor Cyan
Write-Host "  pre-commit run --all-files" -ForegroundColor White

