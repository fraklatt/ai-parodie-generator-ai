"""Backend utilities and helpers"""

import logging
import torch
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class DeviceManager:
    """Manage PyTorch device (CPU/GPU)"""
    
    _device = None
    
    @classmethod
    def get_device(cls):
        """Get current device"""
        if cls._device is None:
            cls._device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Device set to: {cls._device}")
        return cls._device
    
    @classmethod
    def to_device(cls, tensor):
        """Move tensor to device"""
        return tensor.to(cls.get_device())
    
    @classmethod
    def get_info(cls) -> Dict[str, Any]:
        """Get device info"""
        device = cls.get_device()
        info = {
            "device": device,
            "pytorch_version": torch.__version__,
        }
        
        if device == "cuda":
            info.update({
                "cuda_available": True,
                "cuda_version": torch.version.cuda,
                "gpu_count": torch.cuda.device_count(),
                "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.device_count() > 0 else None,
            })
        else:
            info["cuda_available"] = False
        
        return info


def setup_logging(name: str, level=logging.INFO) -> logging.Logger:
    """Setup logger"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
