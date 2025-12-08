"""
HuggingFace Zero-Shot Classification Service
Uses facebook/bart-large-mnli for text classification
"""
import httpx
import time
import logging
from typing import Dict, Any, List
from app.config import HF_TOKEN

logger = logging.getLogger(__name__)

HF_API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
DEFAULT_LABELS = [
    "technology", "business", "politics", "sports", "entertainment",
    "health", "science", "education", "travel", "food"
]
TIMEOUT_SECONDS = 30


class HuggingFaceError(Exception):
    """Custom exception for HuggingFace API errors"""
    pass


async def classify_text(
    text: str,
    candidate_labels: List[str] = None
) -> Dict[str, Any]:
    """
    Classify text using HuggingFace BART-MNLI zero-shot classification.
    
    Args:
        text: The text to classify
        candidate_labels: List of possible categories (uses defaults if not provided)
    
    Returns:
        Dict with category, confidence, and all scores
    """
    if candidate_labels is None:
        candidate_labels = DEFAULT_LABELS
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": candidate_labels
        }
    }
    
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.post(HF_API_URL, headers=headers, json=payload)
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            if response.status_code == 503:
                # Model is loading
                error_data = response.json()
                estimated_time = error_data.get("estimated_time", 20)
                raise HuggingFaceError(f"Model is loading. Estimated time: {estimated_time}s")
            
            if response.status_code != 200:
                logger.error(f"HuggingFace API error: {response.status_code} - {response.text}")
                raise HuggingFaceError(f"API error: {response.status_code}")
            
            data = response.json()
            
            # Handle new HuggingFace router API format (list of {label, score} objects)
            scores = {}
            if isinstance(data, list):
                # New format: [{"label": "tech", "score": 0.99}, ...]
                for item in data:
                    scores[item.get("label", "unknown")] = round(item.get("score", 0.0), 4)
                top_label = data[0].get("label", "unknown") if data else "unknown"
                top_score = data[0].get("score", 0.0) if data else 0.0
            else:
                # Old format: {"labels": [], "scores": []}
                for label, score in zip(data.get("labels", []), data.get("scores", [])):
                    scores[label] = round(score, 4)
                top_label = data.get("labels", ["unknown"])[0]
                top_score = data.get("scores", [0.0])[0]
            
            logger.info(f"HuggingFace classification: {top_label} ({top_score:.2%}) in {latency_ms}ms")
            
            return {
                "category": top_label,
                "confidence": round(top_score, 4),
                "scores": scores,
                "latency_ms": latency_ms
            }
            
    except httpx.TimeoutException:
        latency_ms = int((time.time() - start_time) * 1000)
        logger.error(f"HuggingFace timeout after {latency_ms}ms")
        raise HuggingFaceError(f"Request timeout after {TIMEOUT_SECONDS}s")
    
    except httpx.RequestError as e:
        latency_ms = int((time.time() - start_time) * 1000)
        logger.error(f"HuggingFace request error: {e}")
        raise HuggingFaceError(f"Connection error: {str(e)}")
