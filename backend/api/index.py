"""
Vercel Entry Point for FastAPI
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Set environment to indicate Vercel
os.environ["VERCEL"] = "1"

try:
    from app.main import app
    handler = app
except Exception as e:
    # Fallback: create a simple app that shows the error
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    app = FastAPI()
    error_message = str(e)
    
    @app.get("/{path:path}")
    async def catch_all(path: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Import failed",
                "detail": error_message,
                "path": path,
                "python_path": sys.path[:5]
            }
        )
    
    handler = app
