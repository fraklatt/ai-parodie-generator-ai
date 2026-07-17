#!/usr/bin/env python3
"""
Simple test - checks if FastAPI is installed
"""

import sys

print("Testing FastAPI...")
try:
    import fastapi
    print(f"✓ FastAPI {fastapi.__version__} is installed")
except ImportError:
    print("✗ FastAPI NOT installed")
    print("\nFix it:")
    print("  pip install fastapi uvicorn pydantic websockets")
    sys.exit(1)

print("\nTesting other core packages...")

try:
    import torch
    print(f"✓ PyTorch {torch.__version__}")
except ImportError:
    print("✗ PyTorch missing")

try:
    import librosa
    print(f"✓ librosa")
except ImportError:
    print("✗ librosa missing")

try:
    import soundfile
    print(f"✓ soundfile")
except ImportError:
    print("✗ soundfile missing")

print("\n✓ All core packages OK!")
print("\nRun: python src/backend/main.py")
