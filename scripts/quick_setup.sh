#!/bin/bash

# Quick setup script - minimal version
set -e

echo "Installing AI Music Parody Generator..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found. Please install Python 3.10+"
    exit 1
fi

# Create venv
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "Installing dependencies..."
pip install fastapi uvicorn pydantic websockets pyyaml
pip install numpy scipy librosa soundfile sounddevice
pip install torch torchvision torchaudio
pip install julius crepe

echo "Done! Run: source venv/bin/activate && python src/backend/main.py"
