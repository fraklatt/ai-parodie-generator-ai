"""Minimal frontend stub for Phase 1"""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("""
╔══════════════════════════════════════════════════════╗
║  AI Music Parody Generator - Frontend                ║
║  Phase 1: Foundation (Stub)                          ║
╚══════════════════════════════════════════════════════╝

Frontend development starts in Phase 5.

For now, use the backend API:

  Backend: http://localhost:8000
  API Docs: http://localhost:8000/docs
  API Tests: http://localhost:8000/redoc

To start backend:
  python src/backend/main.py

Then test with:
  curl http://localhost:8000/api/v1/system/info
  curl -X POST http://localhost:8000/api/v1/test/gpu
""")

logger.info("Phase 1 is for backend foundation only.")
logger.info("PySide6 UI will be implemented in Phase 5.")
