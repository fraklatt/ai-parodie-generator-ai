# 🎵 AI Music Parody Generator

> Profesjonalna aplikacja AI do tworzenia parodii muzycznych z automatycznym klonowaniem głosu, syntezą śpiewu i inteligentnym dopasowaniem tekstu.

**Status**: 🚧 **W Rozwoju (Phase 1)**

![Fedora](https://img.shields.io/badge/OS-Fedora%2039+-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=flat-square)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

## ✨ Główne Możliwości

### Możliwości Podstawowe
- 🎤 **Separacja Wokalu** - Izolacja wokalu od instrumentalu (Demucs)
- 📊 **Analiza Audio** - Detekcja BPM, analiza wysokości, liczenie sylab
- 🗣️ **Klonowanie Głosu** - Tworzenie profili głosu z krótkich próbek (OpenVoice)
- 🎵 **Synteza Śpiewu** - Generowanie wokalu AI z zachowaniem prosodie (DiffSinger)
- 📝 **Dopasowanie Tekstu** - Automatyczna synchronizacja tekstu z melodią
- 🎛️ **Miksowanie Audio** - Edytor podobny do DAW z efektami (reverb, EQ, kompresja)
- 🚀 **Akceleracja GPU** - CUDA, ROCm lub fallback na CPU

## 🏗️ Stos Technologiczny

| Warstwa | Technologia | Cel |
|---------|-----------|-----|
| **Frontend** | PySide6 (Qt6) | Natywny interfejs Linux DAW |
| **Backend** | FastAPI + AsyncIO | REST API + WebSocket |
| **Audio** | librosa, torchaudio, scipy | Przetwarzanie sygnału |
| **Separacja Wokalu** | Demucs v4 | Izolacja wokalu |
| **Detekcja Wysokości** | CREPE | Precyzyjna analiza pitch |
| **Klonowanie Głosu** | OpenVoice | Zero-shot voice conversion |
| **Konwersja Głosu** | RVC v3 | Real-time transformacja |
| **Synteza Śpiewu** | DiffSinger | Generowanie vokali AI |
| **GPU** | PyTorch + CUDA/ROCm | Przyspieszenie |
| **IPC** | WebSocket + JSON-RPC | Komunikacja Frontend-Backend |

## 🚀 Szybki Start

### Wymagania Systemowe
- **OS**: Fedora 39+ (Linux-only)
- **CPU**: 4+ rdzenie (8+ rekomendowane)
- **RAM**: 8GB minimum, 16GB+ polecane
- **Storage**: 60GB+ (na modele + zależności)
- **GPU**: NVIDIA (CUDA) lub AMD (ROCm) - opcjonalnie ale rekomendowane

### Instalacja

```bash
# Klonuj repozytorium
git clone https://github.com/fraklatt/ai-parodie-generator-ai.git
cd ai-parodie-generator-ai

# Uruchom instalator Fedory
bash scripts/install_fedora.sh

# Aktywuj środowisko
source venv/bin/activate

# Uruchom aplikację
python src/frontend/main.py
```

**Pierwszy start**: Modele pobiorą się automatycznie (~10-15 minut)

### Szczegółowa Instalacja
Zobacz [docs/INSTALLATION_FEDORA.md](docs/INSTALLATION_FEDORA.md)

## 📚 Dokumentacja

- [Przewodnik Instalacji](docs/INSTALLATION_FEDORA.md) - Krok po kroku
- [Przewodnik Użytkownika](docs/USER_GUIDE.md) - Jak używać
- [Architektura](docs/ARCHITECTURE.md) - Design systemu
- [Referncja API](docs/API_REFERENCE.md) - Dokumentacja API
- [Przewodnik Modeli](docs/MODEL_GUIDE.md) - Info o modelach AI
- [Rozwiązywanie Problemów](docs/TROUBLESHOOTING.md) - FAQ

## 🎯 Plan Wdrażania

### Phase 1: Fundamenty ✅ W TOKU
- [x] Struktura projektu & CI/CD
- [x] Backend skeleton (FastAPI)
- [x] Detekcja GPU & inicjalizacja
- [ ] Audio I/O & utilities

### Phase 2: Analiza Audio (Następnie)
- [ ] Detekcja BPM & rytmu
- [ ] Detekcja pitch (CREPE)
- [ ] Analiza sylab
- [ ] Separacja wokalu (Demucs)

### Phase 3: Klonowanie Głosu
- [ ] Interfejs nagrywania głosu
- [ ] Integracja OpenVoice
- [ ] Zarządzanie profilami głosu

### Phase 4: Synteza Śpiewu
- [ ] Integracja DiffSinger
- [ ] Silnik dopasowania tekstu
- [ ] Zachowanie prosodie

### Phase 5: Frontend UI
- [ ] Edytor waveform
- [ ] Timeline & mixer
- [ ] Panel efektów
- [ ] Podgląd real-time

### Phase 6: Polish & Dystrybucja
- [ ] Optymalizacja wydajności
- [ ] Pakowanie Flatpak
- [ ] Kompleksowe testy
- [ ] Pełna dokumentacja

## 🏗️ Struktura Projektu

```
ai-parodie-generator-ai/
├── src/
│   ├── frontend/           # UI PySide6
│   ├── backend/            # Serwer FastAPI
│   ├── ai/                 # Wrappery modeli AI
│   └── utils/              # Utilities
├── docs/                   # Dokumentacja
├── tests/                  # Test suite
├── scripts/                # Instalacja & utilities
├── config/                 # Pliki konfiguracyjne
├── models/                 # Pobrane modele AI (auto-managed)
└── data/                   # Projekty użytkownika & próbki
```

## 🤝 Współpraca

Projekt jest w wczesnym etapie. Zapraszamy do współpracy!

1. Fork repozytorium
2. Utwórz branch feature
3. Wyślij pull request

## 📄 Licencja

MIT License - Zajrzyj do pliku LICENSE

## ⚠️ Zastrzeżenie

To narzędzie jest do użytku edukacyjnego i osobistego. Szanuj prawo autorskie i prawa własności intelektualnej przy tworzeniu parodii.

## 🙏 Podziękowania

- [Demucs](https://github.com/adefossez/demucs) - Separacja wokalu
- [OpenVoice](https://github.com/myshell-ai/OpenVoice) - Klonowanie głosu
- [RVC](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion) - Konwersja głosu
- [DiffSinger](https://github.com/MoonInTheRiver/DiffSinger) - Synteza śpiewu
- [CREPE](https://github.com/JVass/crepe) - Detekcja pitch
- [librosa](https://github.com/librosa/librosa) - Analiza audio

---

**Stworzony z ❤️ dla Linuxa & Kochających Muzykę**
