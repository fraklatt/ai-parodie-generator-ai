#!/bin/bash

#############################################################################
# AI Music Parody Generator - Full Fedora Installation Script
# Supports: Fedora 39, 40, 41+ (latest stable)
# Usage: bash scripts/install_fedora.sh
#############################################################################

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}
╔════════════════════════════════════════════════════════╗
║   AI Music Parody Generator - Fedora Installation     ║
╚════════════════════════════════════════════════════════╝${NC}\n"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}[1/7] Checking system requirements...${NC}"

# Check if Fedora
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo -e "${GREEN}✓ OS: $PRETTY_NAME${NC}"
else
    echo -e "${YELLOW}⚠ Could not verify Fedora version${NC}"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"

echo -e "\n${BLUE}[2/7] Installing system packages...${NC}"

echo -e "${YELLOW}→ Updating DNF${NC}"
sudo dnf update -y > /dev/null 2>&1 || true

echo -e "${YELLOW}→ Development tools${NC}"
sudo dnf groupinstall -y "Development Tools" > /dev/null 2>&1 || true

echo -e "${YELLOW}→ Core dependencies${NC}"
sudo dnf install -y \
    gcc gcc-c++ cmake make \
    libffi-devel python3-devel python3-pip \
    git pkg-config \
    > /dev/null 2>&1 || true

echo -e "${YELLOW}→ Audio libraries${NC}"
sudo dnf install -y \
    alsa-lib-devel pulseaudio-libs-devel \
    libsndfile-devel flac-devel \
    jack-audio-connection-kit-devel \
    > /dev/null 2>&1 || true

echo -e "${YELLOW}→ Qt6 (for future frontend)${NC}"
sudo dnf install -y \
    qt6-qtbase-devel qt6-qtdeclarative-devel \
    libxkbcommon-devel libxkbcommon-x11-devel \
    > /dev/null 2>&1 || true

echo -e "${YELLOW}→ FFmpeg${NC}"
sudo dnf install -y ffmpeg ffmpeg-devel > /dev/null 2>&1 || true

echo -e "${GREEN}✓ System packages installed${NC}"

echo -e "\n${BLUE}[3/7] Setting up Python virtual environment...${NC}"

if [ -d "$PROJECT_DIR/venv" ]; then
    echo -e "${YELLOW}→ Removing old venv${NC}"
    rm -rf "$PROJECT_DIR/venv"
fi

echo -e "${YELLOW}→ Creating venv${NC}"
python3 -m venv "$PROJECT_DIR/venv"

echo -e "${YELLOW}→ Activating venv${NC}"
source "$PROJECT_DIR/venv/bin/activate"

echo -e "${YELLOW}→ Upgrading pip${NC}"
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

echo -e "${GREEN}✓ Virtual environment ready${NC}"

echo -e "\n${BLUE}[4/7] Installing Python dependencies...${NC}"

echo -e "${YELLOW}→ FastAPI & Web${NC}"
pip install fastapi uvicorn pydantic websockets requests tqdm pyyaml python-multipart click > /dev/null 2>&1 || true

echo -e "${YELLOW}→ Audio libraries${NC}"
pip install librosa soundfile sounddevice numpy scipy > /dev/null 2>&1 || true

echo -e "${YELLOW}→ PyTorch (this may take a while)${NC}"
if command -v nvidia-smi &> /dev/null; then
    echo -e "${YELLOW}  NVIDIA GPU detected${NC}"
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 > /dev/null 2>&1 || \
    pip install torch torchvision torchaudio > /dev/null 2>&1
else
    echo -e "${YELLOW}  No GPU - CPU only${NC}"
    pip install torch torchvision torchaudio > /dev/null 2>&1
fi

echo -e "${YELLOW}→ AI packages${NC}"
pip install julius crepe huggingface-hub numba > /dev/null 2>&1 || true

echo -e "${YELLOW}→ Dev tools${NC}"
pip install pytest black flake8 mypy ipython > /dev/null 2>&1 || true

echo -e "${GREEN}✓ Python dependencies installed${NC}"

echo -e "\n${BLUE}[5/7] Verifying installation...${NC}"

echo -e "${YELLOW}→ Testing imports${NC}"
python3 << 'EOF'
import sys
errors = []

try:
    import fastapi
except:
    errors.append("FastAPI")

try:
    import librosa
except:
    errors.append("librosa")

try:
    import soundfile
except:
    errors.append("soundfile")

try:
    import torch
except:
    errors.append("PyTorch")

if errors:
    print(f"Missing: {', '.join(errors)}")
    sys.exit(1)
else:
    print("All core packages OK")
EOF

echo -e "${GREEN}✓ Imports verified${NC}"

echo -e "\n${BLUE}[6/7] Detecting GPU...${NC}"

python3 << 'EOF'
import torch
if torch.cuda.is_available():
    print(f"✓ CUDA available")
    print(f"  GPU: {torch.cuda.get_device_name(0)}")
else:
    print("✓ CPU mode (no CUDA)")
EOF

echo -e "\n${BLUE}[7/7] Creating directories...${NC}"

mkdir -p "$PROJECT_DIR/models"/{demucs,openvoice,rvc,diffsinger}
mkdir -p "$PROJECT_DIR/data"/{sample_audio,projects,cache}
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/config"

echo -e "${GREEN}✓ Directories created${NC}"

echo -e "${BLUE}\n╔════════════════════════════════════════════════════════╗
║   Installation Complete! ✓                             ║
╚════════════════════════════════════════════════════════╝${NC}"

echo -e ""
echo -e "${GREEN}Next steps:${NC}"
echo -e ""
echo -e "  1. Activate environment:"
echo -e "     ${YELLOW}source venv/bin/activate${NC}"
echo -e ""
echo -e "  2. Test installation:"
echo -e "     ${YELLOW}python scripts/test_installation.py${NC}"
echo -e ""
echo -e "  3. Run backend server:"
echo -e "     ${YELLOW}python src/backend/main.py${NC}"
echo -e ""
echo -e "  4. In browser, visit:"
echo -e "     ${YELLOW}http://localhost:8000/docs${NC}"
echo -e ""
echo -e "${GREEN}Happy creating! 🎵${NC}"
echo -e ""
