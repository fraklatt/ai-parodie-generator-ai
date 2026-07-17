# Phase 2: Audio Analysis

## Features Implemented

### Audio Loading & Analysis
- ✅ Upload audio files (MP3, WAV, FLAC, etc.)
- ✅ Get audio metadata (sample rate, duration, channels)
- ✅ BPM detection using librosa
- ✅ Spectral analysis (frequency content)
- ✅ Comprehensive audio analysis endpoint

### API Endpoints

```
POST /api/v1/audio/upload        # Upload audio file
POST /api/v1/audio/info          # Get audio metadata
POST /api/v1/audio/bpm           # Detect BPM
POST /api/v1/audio/analysis       # Full audio analysis
```

### Example Usage

#### Upload and analyze audio:
```bash
curl -X POST -F "file=@song.mp3" http://localhost:8000/api/v1/audio/analysis
```

#### Get just BPM:
```bash
curl -X POST -F "file=@song.mp3" http://localhost:8000/api/v1/audio/bpm
```

#### Get audio info:
```bash
curl -X POST -F "file=@song.mp3" http://localhost:8000/api/v1/audio/info
```

### Response Example

```json
{
  "status": "success",
  "filename": "song.mp3",
  "audio": {
    "sample_rate": 44100,
    "duration_seconds": 180.5,
    "num_channels": 2,
    "total_samples": 7960500
  },
  "rhythm": {
    "bpm": 128.5,
    "beats": [0, 1, 2, ...],
    "num_beats": 256
  },
  "spectral": {
    "freq_range": [0, 22050],
    "spectral_centroid_mean": 2850.5,
    "spectral_centroid_std": 450.2
  }
}
```

## Coming in Phase 3

- Voice separation (Demucs) - *skeleton added*
- Voice cloning (OpenVoice)
- Pitch detection (CREPE)

## To Use Phase 2

1. Start backend:
   ```bash
   source venv/bin/activate
   python src/backend/main.py
   ```

2. Upload and analyze audio:
   ```bash
   curl -X POST -F "file=@your_song.mp3" http://localhost:8000/api/v1/audio/analysis
   ```

3. View API docs:
   ```
   http://localhost:8000/docs
   ```
