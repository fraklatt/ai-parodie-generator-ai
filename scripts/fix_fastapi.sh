#!/bin/bash

# Szybka naprawka - uruchom gdy backend nie chce pracować

echo "Fixing FastAPI installation..."

source venv/bin/activate

echo "Installing FastAPI and dependencies..."
pip install --force-reinstall fastapi uvicorn pydantic websockets

echo "Verifying..."
python -c "import fastapi; print(f'FastAPI {fastapi.__version__} OK')"

echo "Done! Try again: python src/backend/main.py"
