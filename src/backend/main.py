#!/usr/bin/env python3
"""
AI Music Parody Generator - Backend Server

Phase 1: Foundation
- FastAPI server setup
- GPU detection
- Health check endpoints
"""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    import torch
    import uvicorn
except ImportError as e:
    logger.error(f"Missing dependency: {e}")
    logger.error("Run: pip install -r requirements/base.txt")
    sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="AI Music Parody Generator",
    description="Professional AI-powered music parody generation",
    version="0.1.0"
)


class GPUInfo:
    """GPU detection and info"""
    
    @staticmethod
    def get_device():
        """Get available device (GPU or CPU)"""
        if torch.cuda.is_available():
            return "cuda"
        return "cpu"
    
    @staticmethod
    def get_info():
        """Get detailed GPU info"""
        info = {
            "pytorch_version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "device": GPUInfo.get_device(),
        }
        
        if torch.cuda.is_available():
            info.update({
                "cuda_version": torch.version.cuda,
                "gpu_count": torch.cuda.device_count(),
                "gpus": [
                    {
                        "id": i,
                        "name": torch.cuda.get_device_name(i),
                        "memory_gb": torch.cuda.get_device_properties(i).total_memory / 1e9
                    }
                    for i in range(torch.cuda.device_count())
                ]
            })
        
        return info


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": "AI Music Parody Generator",
        "version": "0.1.0",
        "status": "running",
        "phase": "Phase 1 - Foundation"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "backend"
    }


@app.get("/api/v1/system/info")
async def system_info():
    """Get system information including GPU status"""
    return {
        "system": "AI Music Parody Generator",
        "phase": "Phase 1 - Foundation",
        "gpu": GPUInfo.get_info(),
        "python_version": sys.version.split()[0],
        "available_endpoints": [
            "/",
            "/health",
            "/api/v1/system/info",
            "/docs",
            "/redoc"
        ]
    }


@app.get("/api/v1/gpu/info")
async def gpu_info():
    """Get GPU information"""
    return GPUInfo.get_info()


@app.post("/api/v1/test/gpu")
async def test_gpu():
    """Test GPU availability and performance"""
    try:
        device = GPUInfo.get_device()
        
        # Test tensor operations
        x = torch.randn(1000, 1000).to(device)
        y = torch.randn(1000, 1000).to(device)
        z = torch.matmul(x, y)
        
        return {
            "status": "success",
            "device": device,
            "test": "GPU computation successful"
        }
    except Exception as e:
        logger.error(f"GPU test failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(e)
            }
        )


if __name__ == "__main__":
    logger.info("""\n
╔══════════════════════════════════════════════════════╗
║  AI Music Parody Generator - Backend Server         ║
║  Phase 1: Foundation                                ║
╚══════════════════════════════════════════════════════╝
    """)
    
    # Print GPU info
    gpu_info = GPUInfo.get_info()
    logger.info(f"PyTorch Version: {gpu_info['pytorch_version']}")
    logger.info(f"Device: {gpu_info['device'].upper()}")
    
    if gpu_info["cuda_available"]:
        logger.info(f"CUDA Version: {gpu_info['cuda_version']}")
        logger.info(f"GPU Count: {gpu_info['gpu_count']}")
        for gpu in gpu_info['gpus']:
            logger.info(f"  GPU {gpu['id']}: {gpu['name']} ({gpu['memory_gb']:.2f} GB)")
    else:
        logger.warning("CUDA not available - running in CPU mode")
    
    logger.info("\nStarting server...\n")
    
    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
