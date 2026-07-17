"""Phase 1: Audio utilities and helpers"""

import logging
from pathlib import Path
from typing import Union, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class AudioConfig:
    """Audio configuration constants"""
    SAMPLE_RATE = 44100
    CHANNELS = 2
    DTYPE = np.float32
    CHUNK_SIZE = 2048


def validate_audio_path(path: Union[str, Path]) -> bool:
    """Validate if audio file exists and is supported"""
    path = Path(path)
    
    supported_formats = {'.mp3', '.wav', '.flac', '.m4a', '.ogg'}
    
    if not path.exists():
        logger.error(f"Audio file not found: {path}")
        return False
    
    if path.suffix.lower() not in supported_formats:
        logger.error(f"Unsupported format: {path.suffix}")
        return False
    
    return True


def get_audio_info(path: Union[str, Path]) -> dict:
    """Get basic audio file info (Phase 1 - stub)"""
    path = Path(path)
    
    if not validate_audio_path(path):
        return {}
    
    return {
        "path": str(path),
        "name": path.name,
        "format": path.suffix.lower(),
        "size_mb": path.stat().st_size / (1024 * 1024),
    }
