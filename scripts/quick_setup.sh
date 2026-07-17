#!/bin/bash

#############################################################################
# AI Music Parody Generator - Quick Fedora Setup
# Supports: Fedora 39, 40, 41+ (latest stable)
# Usage: bash scripts/quick_setup.sh
#############################################################################

set -e

echo ""
echo "AI Music Parody Generator - Quick Setup"
echo "========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}[1/4] Updating system...${NC}"
sudo dnf update -y > /dev/null 2>&1 || true

echo -e "${YELLOW}[2/4] Installing essential packages...${NC}"
sudo dnf install -y \
    python3-devel python3-pip \
    alsa-lib-devel pulseaudio-libs-devel \
    libsndfile-devel flac-devel \
    ffmpeg ffmpeg-devel \
    > /dev/null 2>&1 || true

echo -e "${YELLOW}[3/4] Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    rm -rf venv
fi
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

echo -e "${YELLOW}[4/4] Installing dependencies...${NC}"

# Install in correct order
echo "  • Installing FastAPI and server..."
pip install fastapi uvicorn pydantic websockets requests tqdm pyyaml > /dev/null 2>&1

echo "  • Installing audio libraries..."
pip install librosa soundfile sounddevice numpy scipy > /dev/null 2>&1

echo "  • Installing PyTorch..."
if command -v nvidia-smi &> /dev/null; then
    echo "    GPU detected - installing CUDA version..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 > /dev/null 2>&1 || \
    pip install torch torchvision torchaudio > /dev/null 2>&1
else
    echo "    No GPU - installing CPU version..."
    pip install torch torchvision torchaudio > /dev/null 2>&1
fi

echo "  • Installing AI packages..."
pip install julius crepe huggingface-hub numba > /dev/null 2>&1

echo "  • Installing development tools..."
pip install pytest black flake8 mypy ipython > /dev/null 2>&1

echo ""
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. source venv/bin/activate"
echo "  2. python scripts/test_installation.py"
echo "  3. python src/backend/main.py"
echo ""
