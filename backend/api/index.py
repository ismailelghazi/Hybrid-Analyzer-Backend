"""
Vercel Entry Point for FastAPI
This file is used by Vercel's Python runtime to serve the FastAPI app
"""
import sys
from pathlib import Path

# Add parent directory to path so 'app' module can be found
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app

# Vercel expects the app to be named 'app' or 'handler'
handler = app
