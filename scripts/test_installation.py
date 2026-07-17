#!/usr/bin/env python3
"""
Quick test script to verify installation
"""

import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

print("\n" + "="*60)
print("AI Music Parody Generator - Installation Test")
print("="*60 + "\n")

checks_passed = 0
checks_total = 0

# Test 1: Python version
checks_total += 1
print("[1] Checking Python version...")
if sys.version_info >= (3, 10):
    logger.info(f"✓ Python {sys.version.split()[0]} OK\n")
    checks_passed += 1
else:
    logger.error(f"✗ Python 3.10+ required, got {sys.version.split()[0]}\n")

# Test 2: FastAPI
checks_total += 1
print("[2] Checking FastAPI...")
try:
    import fastapi
    logger.info(f"✓ FastAPI {fastapi.__version__} OK\n")
    checks_passed += 1
except ImportError:
    logger.error("✗ FastAPI not found\n")

# Test 3: PyTorch
checks_total += 1
print("[3] Checking PyTorch...")
try:
    import torch
    logger.info(f"✓ PyTorch {torch.__version__} OK\n")
    checks_passed += 1
except ImportError:
    logger.error("✗ PyTorch not found\n")

# Test 4: Audio libraries
checks_total += 1
print("[4] Checking audio libraries...")
try:
    import librosa
    import soundfile
    logger.info(f"✓ Audio libraries OK (librosa, soundfile)\n")
    checks_passed += 1
except ImportError:
    logger.error("✗ Audio libraries missing\n")

# Test 5: CUDA/GPU
checks_total += 1
print("[5] Checking GPU support...")
try:
    import torch
    if torch.cuda.is_available():
        logger.info(f"✓ CUDA available (GPU: {torch.cuda.get_device_name(0)})\n")
    else:
        logger.info("✓ CUDA not available (CPU mode)\n")
    checks_passed += 1
except Exception as e:
    logger.error(f"✗ GPU check failed: {e}\n")

# Test 6: Qt6 (Frontend)
checks_total += 1
print("[6] Checking Qt6...")
try:
    from PySide6 import QtCore
    logger.info(f"✓ PySide6 {QtCore.__version__} OK\n")
    checks_passed += 1
except ImportError:
    logger.warning("⚠ PySide6 not found (not critical for Phase 1)\n")

# Summary
print("="*60)
print(f"Tests Passed: {checks_passed}/{checks_total}")
print("="*60 + "\n")

if checks_passed >= 5:
    logger.info("✓ Installation OK! Backend should work.")
    logger.info("\nNext steps:")
    logger.info("  1. Run backend: python src/backend/main.py")
    logger.info("  2. Test API: curl http://localhost:8000/docs")
    print()
    sys.exit(0)
else:
    logger.error("✗ Installation incomplete. Run install script:")
    logger.error("  bash scripts/install_fedora.sh")
    print()
    sys.exit(1)
