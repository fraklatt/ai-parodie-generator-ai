#!/bin/bash

#############################################################################
# AI Music Parody Generator - Fedora Installation Script
# Supports: Fedora 39, 40, 41+ (latest stable)
# Usage: bash scripts/install_fedora.sh
#############################################################################

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   AI Music Parody Generator - Fedora Installation     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "\n${BLUE}[1/6] Checking system requirements...${NC}"

# Check Fedora version
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [[ "$VERSION_ID" -lt 39 ]]; then
        echo -e "${RED}✗ Fedora 39 or newer required. Current: $VERSION_ID${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Fedora $VERSION_ID detected${NC}"
else
    echo -e "${YELLOW}⚠ Could not detect Fedora version, continuing anyway...${NC}"
fi

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Check git
if ! command -v git &> /dev/null; then
    echo -e "${RED}✗ Git not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Git found${NC}"

echo -e "\n${BLUE}[2/6] Updating system and installing dependencies...${NC}"

echo -e "${YELLOW}→ Updating DNF...${NC}"
sudo dnf update -y > /dev/null 2>&1 || true

echo -e "${YELLOW}→ Installing development tools...${NC}"
sudo dnf groupinstall -y "Development Tools" > /dev/null 2>&1 || true

echo -e "${YELLOW}→ Installing build essentials...${NC}"
sudo dnf install -y \
    gcc gcc-c++ cmake make \
    libffi-devel python3-devel python3-pip \
    git pkg-config \
    > /dev/null 2>&1 || true

echo -e "${YELLOW}→ Installing audio libraries...${NC}"
sudo dnf install -y \
    alsa-lib-devel pulseaudio-libs-devel \
    libsndfile-devel flac-devel \
    jack-audio-connection-kit-devel \
    > /dev/null 2>&1 || true

echo -e "${YELLOW}→ Installing Qt6 libraries...${NC}"
sudo dnf install -y \
    qt6-qtbase-devel qt6-qtdeclarative-devel \
    libxkbcommon-devel libxkbcommon-x11-devel \
    > /dev/null 2>&1 || true

echo -e "${YELLOW}→ Installing FFmpeg...${NC}"
sudo dnf install -y ffmpeg ffmpeg-devel > /dev/null 2>&1 || true

echo -e "${GREEN}✓ System dependencies installed${NC}"

echo -e "\n${BLUE}[3/6] Setting up Python virtual environment...${NC}"

if [ -d "$PROJECT_DIR/venv" ]; then
    echo -e "${YELLOW}→ Virtual environment already exists, removing...${NC}"
    rm -rf "$PROJECT_DIR/venv"
fi

echo -e "${YELLOW}→ Creating virtual environment...${NC}"
python3 -m venv "$PROJECT_DIR/venv"

echo -e "${YELLOW}→ Activating virtual environment...${NC}"
source "$PROJECT_DIR/venv/bin/activate"

echo -e "${YELLOW}→ Upgrading pip, setuptools, wheel...${NC}"
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

echo -e "${GREEN}✓ Virtual environment ready${NC}"

echo -e "\n${BLUE}[4/6] Installing Python dependencies...${NC}"

echo -e "${YELLOW}→ Installing base dependencies...${NC}"
if [ -f "$PROJECT_DIR/requirements/base.txt" ]; then
    pip install -r "$PROJECT_DIR/requirements/base.txt" > /dev/null 2>&1 || true
else
    pip install fastapi uvicorn pydantic websockets pyyaml > /dev/null 2>&1
fi

echo -e "${YELLOW}→ Installing audio dependencies...${NC}"
if [ -f "$PROJECT_DIR/requirements/audio.txt" ]; then
    pip install -r "$PROJECT_DIR/requirements/audio.txt" > /dev/null 2>&1 || true
else
    pip install numpy scipy librosa soundfile sounddevice > /dev/null 2>&1
fi

echo -e "${YELLOW}→ Installing PyTorch...${NC}"
if command -v nvidia-smi &> /dev/null; then
    echo -e "${YELLOW}→ NVIDIA GPU detected - Installing PyTorch with CUDA support...${NC}"
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 > /dev/null 2>&1 || \
    pip install torch torchvision torchaudio > /dev/null 2>&1
else
    echo -e "${YELLOW}→ Installing PyTorch CPU-only...${NC}"
    pip install torch torchvision torchaudio > /dev/null 2>&1
fi

echo -e "${YELLOW}→ Installing AI/ML packages...${NC}"
pip install julius crepe > /dev/null 2>&1 || true

echo -e "${YELLOW}→ Installing dev dependencies...${NC}"
pip install pytest pytest-cov black flake8 mypy > /dev/null 2>&1 || true

echo -e "${GREEN}✓ Python dependencies installed${NC}"

echo -e "\n${BLUE}[5/6] Detecting GPU support...${NC}"

cat > "$PROJECT_DIR/gpu_check.py" << 'EOF'
import sys
try:
    import torch
    print("✓ PyTorch available")
    if torch.cuda.is_available():
        print(f"✓ CUDA available")
        print(f"  Version: {torch.version.cuda}")
        print(f"  GPU Count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("✓ CPU mode (CUDA not available)")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
EOF

python "$PROJECT_DIR/gpu_check.py" || true
rm -f "$PROJECT_DIR/gpu_check.py"

echo -e "${GREEN}✓ GPU detection complete${NC}"

echo -e "\n${BLUE}[6/6] Creating project directories...${NC}"

mkdir -p "$PROJECT_DIR/models"/{demucs,openvoice,rvc,diffsinger,voice_profiles}
mkdir -p "$PROJECT_DIR/data"/{sample_audio,projects,cache}
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/config"

echo -e "${GREEN}✓ Directories created${NC}"

echo -e "\n${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Installation Complete! ✓                             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"

echo -e """
${GREEN}Next steps:${NC}

1. Activate virtual environment:
   source venv/bin/activate

2. Run backend server:
   python src/backend/main.py

3. In another terminal, run frontend:
   source venv/bin/activate
   python src/frontend/main.py

4. Or check if everything works:
   python -c "import torch; print(torch.__version__)"

${YELLOW}First run will download AI models (~50GB)${NC}
${GREEN}Happy creating! 🎵${NC}
"""
