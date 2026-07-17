#!/usr/bin/env python3
"""
AI Music Parody Generator - Backend Server

Phase 1-2: Foundation + Audio Analysis
- FastAPI server setup
- GPU detection
- Audio file handling
- Voice separation (Demucs)
- BPM detection
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
    from fastapi import FastAPI, File, UploadFile, HTTPException
    from fastapi.responses import JSONResponse, FileResponse
    from fastapi.middleware.cors import CORSMiddleware
    import torch
    import uvicorn
    import librosa
    import numpy as np
except ImportError as e:
    logger.error(f"Missing dependency: {e}")
    logger.error("Run: pip install fastapi uvicorn pydantic torch librosa numpy scipy")
    sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="AI Music Parody Generator",
    description="Professional AI-powered music parody generation",
    version="0.2.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create cache directory
CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


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


class AudioProcessor:
    """Audio processing utilities"""
    
    SAMPLE_RATE = 44100
    
    @staticmethod
    def load_audio(file_path: str, sr: int = SAMPLE_RATE) -> tuple:
        """Load audio file"""
        try:
            y, sr = librosa.load(file_path, sr=sr, mono=False)
            return y, sr
        except Exception as e:
            logger.error(f"Error loading audio: {e}")
            raise
    
    @staticmethod
    def get_audio_info(file_path: str) -> dict:
        """Get audio file info"""
        try:
            y, sr = librosa.load(file_path, sr=None, mono=False)
            duration = librosa.get_duration(y=y, sr=sr)
            
            return {
                "sample_rate": sr,
                "duration_seconds": float(duration),
                "num_channels": 1 if y.ndim == 1 else y.shape[0],
                "total_samples": y.shape[0] if y.ndim == 1 else y.shape[1]
            }
        except Exception as e:
            logger.error(f"Error getting audio info: {e}")
            raise
    
    @staticmethod
    def detect_bpm(file_path: str) -> dict:
        """Detect BPM using librosa"""
        try:
            y, sr = librosa.load(file_path, sr=None, mono=True)
            
            # Compute onset strength
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            
            # Estimate tempo
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            
            return {
                "bpm": float(tempo),
                "beats": beats.tolist(),
                "num_beats": len(beats)
            }
        except Exception as e:
            logger.error(f"Error detecting BPM: {e}")
            raise
    
    @staticmethod
    def get_spectral_info(file_path: str) -> dict:
        """Get spectral information"""
        try:
            y, sr = librosa.load(file_path, sr=None, mono=True)
            
            # Compute STFT
            S = librosa.stft(y)
            S_db = librosa.power_to_db(np.abs(S)**2, ref=np.max)
            
            # Compute spectral centroid
            centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            
            return {
                "freq_range": [0, sr/2],
                "spectral_centroid_mean": float(np.mean(centroid)),
                "spectral_centroid_std": float(np.std(centroid))
            }
        except Exception as e:
            logger.error(f"Error getting spectral info: {e}")
            raise


# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": "AI Music Parody Generator",
        "version": "0.2.0",
        "status": "running",
        "phase": "Phase 2 - Audio Analysis",
        "features": [
            "Audio file upload",
            "BPM detection",
            "Audio analysis",
            "Voice separation (coming soon)"
        ]
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
        "phase": "Phase 2 - Audio Analysis",
        "gpu": GPUInfo.get_info(),
        "python_version": sys.version.split()[0],
        "librosa_available": True,
        "available_endpoints": [
            "/",
            "/health",
            "/api/v1/system/info",
            "/api/v1/gpu/info",
            "/api/v1/test/gpu",
            "/api/v1/audio/upload",
            "/api/v1/audio/info",
            "/api/v1/audio/bpm",
            "/api/v1/audio/analysis",
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


@app.post("/api/v1/audio/upload")
async def upload_audio(file: UploadFile = File(...)):
    """Upload audio file"""
    try:
        # Save file
        file_path = CACHE_DIR / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Audio uploaded: {file.filename} ({len(content)} bytes)")
        
        return {
            "status": "success",
            "filename": file.filename,
            "size_bytes": len(content),
            "path": str(file_path)
        }
    except Exception as e:
        logger.error(f"Error uploading audio: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/audio/info")
async def audio_info(file: UploadFile = File(...)):
    """Get audio file information"""
    try:
        # Save temporarily
        file_path = CACHE_DIR / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Get info
        info = AudioProcessor.get_audio_info(str(file_path))
        
        return {
            "status": "success",
            "filename": file.filename,
            "audio_info": info
        }
    except Exception as e:
        logger.error(f"Error getting audio info: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/audio/bpm")
async def detect_bpm(file: UploadFile = File(...)):
    """Detect BPM from audio file"""
    try:
        # Save temporarily
        file_path = CACHE_DIR / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Detecting BPM for: {file.filename}")
        
        # Detect BPM
        bpm_info = AudioProcessor.detect_bpm(str(file_path))
        
        return {
            "status": "success",
            "filename": file.filename,
            "bpm": bpm_info
        }
    except Exception as e:
        logger.error(f"Error detecting BPM: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/audio/analysis")
async def analyze_audio(file: UploadFile = File(...)):
    """Comprehensive audio analysis"""
    try:
        # Save temporarily
        file_path = CACHE_DIR / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Analyzing audio: {file.filename}")
        
        # Get all info
        audio_info = AudioProcessor.get_audio_info(str(file_path))
        bpm_info = AudioProcessor.detect_bpm(str(file_path))
        spectral_info = AudioProcessor.get_spectral_info(str(file_path))
        
        return {
            "status": "success",
            "filename": file.filename,
            "audio": audio_info,
            "rhythm": bpm_info,
            "spectral": spectral_info
        }
    except Exception as e:
        logger.error(f"Error analyzing audio: {e}")
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    logger.info("""
╔══════════════════════════════════════════════════════╝
║  AI Music Parody Generator - Backend Server         ║
║  Phase 2: Audio Analysis                            ║
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
