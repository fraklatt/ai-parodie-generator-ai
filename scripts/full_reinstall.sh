#!/bin/bash
set -e

echo "Complete reinstall of all dependencies..."

source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

echo "Installing all dependencies from scratch..."

# Base
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install pydantic==2.5.0
pip install websockets==12.0

# Audio
pip install numpy==1.24.3
pip install scipy==1.11.4
pip install librosa==0.10.0
pip install soundfile==0.12.1
pip install sounddevice==0.4.6

# PyTorch (choose one)
echo "Installing PyTorch with CUDA support..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 || \
pip install torch torchvision torchaudio

# AI packages
pip install julius==0.2.7
pip install crepe==0.0.15

echo "Verifying installation..."
python -c "import fastapi; import torch; import librosa; print('All OK')"

echo "Done! Try: python src/backend/main.py"
