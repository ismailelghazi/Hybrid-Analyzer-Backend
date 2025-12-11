"""
Analyze Endpoint - Full HuggingFace → Gemini Pipeline
Protected by JWT authentication
Supports MOCK_MODE for testing without external APIs
"""
import time
import logging
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.analyze_schema import AnalyzeRequest, AnalyzeResponse, MetaInfo
from app.routers.auth import get_current_user
from app.services.huggingface_service import classify_text, HuggingFaceError
from app.services.gemini_service import analyze_text, GeminiError
from app.services.mock_service import mock_classify_text, mock_analyze_text
from app.config import MIN_TEXT_LENGTH, MOCK_MODE

router = APIRouter()
logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if MOCK_MODE:
    logger.info("🔶 MOCK MODE ENABLED - Using fake API responses")


@router.post("/", response_model=AnalyzeResponse)
async def analyze(
    request: AnalyzeRequest,
    current_user=Depends(get_current_user)
):
    """
    Analyze text using HuggingFace classification + Gemini summarization.
    
    Requires JWT authentication.
    
    Flow:
    1. Validate text length
    2. Classify text with HuggingFace BART-MNLI (or mock)
    3. Analyze with Gemini (summary + tone) (or mock)
    4. Return combined results with latency metrics
    """
    start_time = time.time()
    
    # Validate text length
    if len(request.text.strip()) < MIN_TEXT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Text must be at least {MIN_TEXT_LENGTH} characters long"
        )
    
    logger.info(f"Analysis started for user {current_user.email} (mock={MOCK_MODE})")
    
    # Step 1: Classification (HuggingFace or Mock)
    try:
        if MOCK_MODE:
            hf_result = await mock_classify_text(request.text)
            logger.info(f"[MOCK] Classification: {hf_result['category']}")
        else:
            hf_result = await classify_text(request.text)
        
        category = hf_result["category"]
        hf_scores = hf_result["scores"]
        hf_latency = hf_result["latency_ms"]
        
        logger.info(f"Classification: {category} (latency: {hf_latency}ms)")
        
    except HuggingFaceError as e:
        logger.error(f"HuggingFace error: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Classification service unavailable: {str(e)}"
        )
    
    # Step 2: Analysis (Gemini or Mock)
    try:
        if MOCK_MODE:
            gemini_result = await mock_analyze_text(request.text, category)
            logger.info(f"[MOCK] Analysis: tone={gemini_result['tone']}")
        else:
            gemini_result = await analyze_text(request.text, category)
        
        summary = gemini_result["summary"]
        tone = gemini_result["tone"]
        gemini_latency = gemini_result["latency_ms"]
        
        logger.info(f"Analysis: tone={tone} (latency: {gemini_latency}ms)")
        
    except GeminiError as e:
        logger.error(f"Gemini error: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Summarization service unavailable: {str(e)}"
        )
    
    # Calculate total execution time
    total_execution_ms = int((time.time() - start_time) * 1000)
    
    logger.info(f"Analysis complete. Total execution: {total_execution_ms}ms")
    
    return AnalyzeResponse(
        category=category,
        hf_scores=hf_scores,
        summary=summary,
        tone=tone,
        meta=MetaInfo(
            hf_latency_ms=hf_latency,
            gemini_latency_ms=gemini_latency,
            total_execution_ms=total_execution_ms
        )
    )


@router.get("/health")
async def health_check():
    """Health check endpoint for the analyze service"""
    return {
        "status": "ok",
        "service": "analyze",
        "mock_mode": MOCK_MODE
    }

