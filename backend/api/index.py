"""
Vercel Entry Point for FastAPI
This file is used by Vercel's Python runtime to serve the FastAPI app
"""
from app.main import app

# Vercel expects a handler variable
handler = app
