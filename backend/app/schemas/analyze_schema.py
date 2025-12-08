"""
Schemas for /analyze endpoint
"""
from pydantic import BaseModel, Field
from typing import Dict, Optional


class AnalyzeRequest(BaseModel):
    """Request body for /analyze endpoint"""
    text: str = Field(
        ...,
        min_length=20,
        description="Text to analyze (minimum 20 characters)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "The new smartphone features an innovative AI chip that processes data 50% faster than previous models."
            }
        }


class MetaInfo(BaseModel):
    """Latency metrics for the analysis"""
    hf_latency_ms: int = Field(..., description="HuggingFace API latency in milliseconds")
    gemini_latency_ms: int = Field(..., description="Gemini API latency in milliseconds")
    total_execution_ms: int = Field(..., description="Total execution time in milliseconds")


class AnalyzeResponse(BaseModel):
    """Response from /analyze endpoint"""
    category: str = Field(..., description="Classification category from HuggingFace")
    hf_scores: Dict[str, float] = Field(..., description="All classification scores")
    summary: str = Field(..., description="Text summary from Gemini")
    tone: str = Field(..., description="Detected tone: positif, neutre, or négatif")
    meta: MetaInfo = Field(..., description="Execution metrics")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "technology",
                "hf_scores": {"technology": 0.85, "business": 0.10, "science": 0.05},
                "summary": "This article discusses a new smartphone with advanced AI capabilities...",
                "tone": "positif",
                "meta": {
                    "hf_latency_ms": 450,
                    "gemini_latency_ms": 800,
                    "total_execution_ms": 1250
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
    error_type: Optional[str] = None
