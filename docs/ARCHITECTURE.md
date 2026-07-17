# docs/ARCHITECTURE.md

# AI Music Parody Generator - System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI MUSIC PARODY GENERATOR                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  FRONTEND - PySide6 (Qt6) [Phase 5]                     │  │
│  │  • Waveform editor + Timeline                           │  │
│  │  • Real-time audio preview                              │  │
│  │  • Voice cloning interface                              │  │
│  │  • Lyrics text editor                                   │  │
│  │  • DAW-like mixing panel                                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  IPC Layer - WebSocket + JSON-RPC [Phase 3]            │  │
│  │  (Local communication: TCP:8000, Unix socket)          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  BACKEND - FastAPI + AsyncIO [Phase 1] ✓              │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ Audio Analysis Module [Phase 2]                │   │  │
│  │  │  • BPM detection (librosa)                     │   │  │
│  │  │  • Pitch detection (CREPE)                     │   │  │
│  │  │  • Syllable counting (phonetics + spaCy)       │   │  │
│  │  │  • Rhythm analysis                             │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ Voice Separation (Demucs) [Phase 2]            │   │  │
│  │  │  • Vocal isolation from instrumental           │   │  │
│  │  │  • Stem extraction (drums, bass, other)        │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ AI Voice Processing [Phase 3-4]               │   │  │
│  │  │  • Voice cloning (OpenVoice)                  │   │  │
│  │  │  • Voice conversion (RVC v3)                  │   │  │
│  │  │  • Singing synthesis (DiffSinger)             │   │  │
│  │  │  • Real-time autotune                         │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ Lyric Alignment Engine [Phase 4]              │   │  │
│  │  │  • Syllable-to-note mapping                    │   │  │
│  │  │  • Time stretching (librosa)                   │   │  │
│  │  │  • Phoneme alignment                           │   │  │
│  │  │  • Rhythm matching                             │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ Audio Effects Pipeline [Phase 5]              │   │  │
│  │  │  • Reverb, EQ, Compressor (scipy)             │   │  │
│  │  │  • Pitch correction (librosa + aligner)       │   │  │
│  │  │  • Mixing & mastering                          │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │ Storage Layer [Phase 2]                        │   │  │
│  │  │  • SQLite (projects metadata)                   │   │  │
│  │  │  • Audio cache (WAV files)                      │   │  │
│  │  │  • Voice profiles (PyTorch models)              │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  AI MODELS (GPU Accelerated - CUDA/ROCm/CPU)            │  │
│  │  • PyTorch 2.0+ + TorchAudio                            │  │
│  │  • HuggingFace models (automatic download)              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Current Phase (Phase 1): Foundation

### Implemented ✓
- FastAPI backend server
- GPU detection (CUDA, ROCm, CPU)
- Health check endpoints
- System info API
- Device manager
- Project structure
- Requirements management
- Installation script

### Endpoints

```
GET  /                      # Root
GET  /health                # Health check
GET  /api/v1/system/info    # System info + GPU details
GET  /api/v1/gpu/info       # GPU details only
POST /api/v1/test/gpu       # GPU performance test
GET  /docs                  # API documentation (Swagger)
GET  /redoc                 # ReDoc documentation
```

## Phases Overview

### Phase 1: Foundation ✓ IN PROGRESS
- Backend skeleton
- GPU detection
- Server endpoints
- Error handling

### Phase 2: Audio Analysis
- BPM detection (librosa)
- Pitch detection (CREPE)
- Voice separation (Demucs)
- Audio loading/saving

### Phase 3: Voice Cloning
- OpenVoice integration
- Voice profile management
- Real-time preview

### Phase 4: Singing Synthesis
- DiffSinger integration
- Lyric alignment
- Prosody preservation

### Phase 5: Frontend UI
- PySide6 application
- Waveform editor
- Real-time mixer
- Project management

### Phase 6: Polish
- Performance optimization
- Flatpak packaging
- Full testing
- Documentation

## Technology Stack

### Backend
- **Framework**: FastAPI + AsyncIO
- **Server**: Uvicorn
- **Async Tasks**: Celery (planned Phase 3)

### Audio Processing
- **Core**: librosa, scipy, numpy
- **Recording**: sounddevice
- **File I/O**: soundfile
- **PyTorch Audio**: torchaudio

### AI Models
- **Base**: PyTorch 2.0+
- **Voice Separation**: Demucs
- **Pitch Detection**: CREPE
- **Voice Cloning**: OpenVoice
- **Voice Conversion**: RVC v3
- **Singing**: DiffSinger

### Frontend (Phase 5)
- **Framework**: PySide6 (Qt6)
- **Plotting**: Matplotlib or PyQtGraph
- **IPC**: WebSocket

### GPU Support
- **NVIDIA**: CUDA 12.1+
- **AMD**: ROCm (optional)
- **CPU**: Fallback

## Data Flow

```
1. User loads audio file
   ↓
2. Backend analyzes audio
   ├─ BPM detection
   ├─ Pitch tracking
   ├─ Voice separation
   └─ Syllable analysis
   ↓
3. User inputs lyrics
   ↓
4. AI aligns lyrics to melody
   ├─ Syllable matching
   ├─ Rhythm alignment
   └─ Prosody adjustment
   ↓
5. Voice cloning/synthesis
   ├─ Clone user voice (if provided)
   ├─ Generate singing
   └─ Apply effects
   ↓
6. Mixing & export
   ├─ Combine vocal + instrumental
   ├─ Apply audio effects
   └─ Export result
```

## File Structure (Detailed)

```
ai-parodie-generator-ai/
│
├── src/
│   ├── backend/
│   │   ├── main.py                  # FastAPI server entry
│   │   ├── utils.py                 # Backend utilities
│   │   ├── config.py                # Configuration (planned)
│   │   ├── core/
│   │   │   ├── models.py            # Pydantic models (planned)
│   │   │   ├── exceptions.py        # Custom exceptions (planned)
│   │   │   └── logger.py            # Logging setup (planned)
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── audio.py         # Audio endpoints (Phase 2)
│   │   │       ├── voice.py         # Voice endpoints (Phase 3)
│   │   │       └── project.py       # Project endpoints (Phase 2)
│   │   ├── services/                # Service layer (Phase 2+)
│   │   │   ├── audio_processor.py
│   │   │   ├── voice_separator.py
│   │   │   └── ...
│   │   ├── models/                  # Model management (Phase 2)
│   │   ├── storage/                 # Database/cache (Phase 2)
│   │   └── workers/                 # Async workers (Phase 3)
│   │
│   ├── frontend/
│   │   ├── main.py                  # Entry point (Phase 5)
│   │   ├── ui/
│   │   │   ├── main_window.py      # Main window (Phase 5)
│   │   │   ├── waveform_widget.py  # Waveform display (Phase 5)
│   │   │   └── ...
│   │   └── controllers/             # UI controllers (Phase 5)
│   │
│   ├── ai/
│   │   ├── demucs_wrapper.py        # Voice separation (Phase 2)
│   │   ├── crepe_wrapper.py         # Pitch detection (Phase 2)
│   │   ├── openvoice_wrapper.py     # Voice cloning (Phase 3)
│   │   ├── rvc_wrapper.py           # Voice conversion (Phase 3)
│   │   ├── diffsinger_wrapper.py    # Singing synthesis (Phase 4)
│   │   └── ...
│   │
│   └── utils/
│       ├── audio.py                 # Audio utilities
│       ├── gpu.py                   # GPU utilities
│       ├── metrics.py               # Performance metrics (planned)
│       └── validators.py            # Validation (planned)
│
├── docs/
│   ├── ARCHITECTURE.md              # This file
│   ├── INSTALLATION_FEDORA.md       # Installation guide
│   ├── API_REFERENCE.md             # API docs (Phase 1+)
│   ├── USER_GUIDE.md                # User guide (Phase 5+)
│   └── MODEL_GUIDE.md               # Model info (Phase 2+)
│
├── tests/
│   ├── test_gpu.py
│   ├── test_audio_io.py             # Phase 2
│   ├── test_models.py               # Phase 2+
│   └── ...
│
├── scripts/
│   ├── install_fedora.sh            # Main installer
│   ├── quick_setup.sh               # Quick setup
│   ├── test_installation.py         # Verify install
│   └── ...
│
├── models/                          # Downloaded AI models
├── data/                            # User data
├── config/                          # Configuration
├── logs/                            # Application logs
│
├── requirements/
│   ├── base.txt
│   ├── audio.txt
│   ├── ai.txt
│   ├── frontend.txt
│   └── dev.txt
│
├── README.md
├── LICENSE
├── pyproject.toml
└── .gitignore
```

## Development Notes

### GPU Memory Management
- Models cache in `~/.cache/ai_parodie_generator/`
- Use gradient checkpointing for large models
- Implement memory pooling for repeated inference

### Performance Targets (Phase 1+)
- Audio loading: < 1 second
- BPM detection: < 2 seconds per minute
- Voice separation: 2-3x realtime (GPU), 0.5x realtime (CPU)
- Pitch detection: 10x realtime
- Singing synthesis: 1-2x realtime

### Error Handling
- Graceful degradation to CPU if GPU fails
- Comprehensive logging throughout
- User-friendly error messages
- Validation at API boundaries

---

**Current Status**: Phase 1 Complete ✓
**Next Phase**: Phase 2 (Audio Analysis)
