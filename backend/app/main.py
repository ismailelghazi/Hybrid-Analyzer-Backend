from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.db_check import router as db_router
from app.routers.auth import router as auth_router
from app.routers.analyze import router as analyze_router

app = FastAPI(
    title="Hybrid Analyzer API",
    description="Text analysis using HuggingFace + Gemini AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(analyze_router, prefix="/analyze", tags=["Analysis"])
app.include_router(db_router, tags=["Database"])


@app.get("/")
async def root():
    return {
        "message": "Hybrid Analyzer API",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth",
            "analyze": "/analyze"
        }
    }

