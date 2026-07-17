"""Phase 2: Audio I/O and utilities"""

import logging
from pathlib import Path
from typing import Tuple, Union
import numpy as np

logger = logging.getLogger(__name__)


class AudioConfig:
    """Audio configuration"""
    SAMPLE_RATE = 44100
    CHANNELS = 2
    DTYPE = np.float32
    CHUNK_SIZE = 2048


class AudioIO:
    """Audio file I/O operations"""
    
    @staticmethod
    def load_audio(file_path: str, mono: bool = False) -> Tuple[np.ndarray, int]:
        """Load audio file
        
        Args:
            file_path: Path to audio file
            mono: Convert to mono if True
        
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            import librosa
            sr = AudioConfig.SAMPLE_RATE if mono else None
            y, sr = librosa.load(file_path, sr=sr, mono=mono)
            return y, sr
        except Exception as e:
            logger.error(f"Error loading audio: {e}")
            raise
    
    @staticmethod
    def save_audio(audio_data: np.ndarray, output_path: str, sr: int = AudioConfig.SAMPLE_RATE):
        """Save audio file
        
        Args:
            audio_data: Audio array
            output_path: Path to save
            sr: Sample rate
        """
        try:
            import soundfile as sf
            sf.write(output_path, audio_data.T if audio_data.ndim > 1 else audio_data, sr)
            logger.info(f"Audio saved: {output_path}")
        except Exception as e:
            logger.error(f"Error saving audio: {e}")
            raise
    
    @staticmethod
    def get_duration(file_path: str) -> float:
        """Get audio duration in seconds"""
        try:
            import librosa
            y, sr = librosa.load(file_path, sr=None)
            return librosa.get_duration(y=y, sr=sr)
        except Exception as e:
            logger.error(f"Error getting duration: {e}")
            raise


class AudioEffects:
    """Audio effects and processing (Phase 5)"""
    
    @staticmethod
    def normalize(audio: np.ndarray, target_db: float = -20.0) -> np.ndarray:
        """Normalize audio to target dB level"""
        try:
            rms = np.sqrt(np.mean(audio**2))
            if rms == 0:
                return audio
            
            target_linear = 10**(target_db / 20.0)
            return audio * (target_linear / rms)
        except Exception as e:
            logger.error(f"Error normalizing audio: {e}")
            return audio
    
    @staticmethod
    def fade_in(audio: np.ndarray, duration_samples: int) -> np.ndarray:
        """Apply fade in effect"""
        fade = np.linspace(0, 1, duration_samples)
        audio[:duration_samples] *= fade
        return audio
    
    @staticmethod
    def fade_out(audio: np.ndarray, duration_samples: int) -> np.ndarray:
        """Apply fade out effect"""
        fade = np.linspace(1, 0, duration_samples)
        audio[-duration_samples:] *= fade
        return audio
