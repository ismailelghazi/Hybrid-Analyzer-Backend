"""
Vercel Entry Point for FastAPI - Minimal Test Version
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Create minimal app for testing
app = FastAPI(title="Hybrid Analyzer API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Vercel FastAPI is working!", "mock_mode": True}

@app.get("/analyze/health")
async def health():
    return {
        "status": "ok",
        "service": "analyze",
        "mock_mode": True,
        "database_url_set": bool(os.environ.get("DATABASE_URL")),
        "environment": "vercel"
    }

@app.get("/test")
async def test():
    return {"test": "success"}

# Handler for Vercel
handler = app

