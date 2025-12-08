"""
Gemini Summarization & Tone Analysis Service
Uses Google Gemini API for contextual text analysis
"""
import google.generativeai as genai
import time
import json
import logging
import re
from typing import Dict, Any
from app.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

TIMEOUT_SECONDS = 30
MAX_RETRIES = 2


class GeminiError(Exception):
    """Custom exception for Gemini API errors"""
    pass


def _parse_gemini_response(text: str) -> Dict[str, str]:
    """
    Parse Gemini response to extract summary and tone.
    Handles both JSON and plain text responses.
    """
    # Try to parse as JSON first
    try:
        # Find JSON in the response
        json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return {
                "summary": data.get("summary", "").strip(),
                "tone": data.get("tone", "neutre").strip().lower()
            }
    except json.JSONDecodeError:
        pass
    
    # Fallback: parse as plain text
    lines = text.strip().split('\n')
    summary = ""
    tone = "neutre"
    
    for line in lines:
        line_lower = line.lower()
        if "summary:" in line_lower or "résumé:" in line_lower:
            summary = line.split(":", 1)[-1].strip()
        elif "tone:" in line_lower or "ton:" in line_lower:
            tone_text = line.split(":", 1)[-1].strip().lower()
            if "positif" in tone_text or "positive" in tone_text:
                tone = "positif"
            elif "négatif" in tone_text or "negative" in tone_text or "negatif" in tone_text:
                tone = "négatif"
            else:
                tone = "neutre"
    
    # If no structured format, use the whole text as summary
    if not summary:
        summary = text.strip()[:500]  # Limit length
    
    return {"summary": summary, "tone": tone}


async def analyze_text(text: str, category: str) -> Dict[str, Any]:
    """
    Analyze text with Gemini: generate summary and detect tone.
    
    Args:
        text: The original text to analyze
        category: The category from HuggingFace classification
    
    Returns:
        Dict with summary, tone, and latency_ms
    """
    prompt = f"""Analyze the following text that has been classified as "{category}".

TEXT:
{text}

Respond in this exact JSON format:
{{
    "summary": "A clear, concise 2-3 sentence summary of the main points",
    "tone": "positif OR neutre OR négatif"
}}

Rules:
- Summary must be in the same language as the original text
- Tone must be exactly one of: positif, neutre, négatif
- Keep summary under 150 words
- Be objective in your analysis"""

    start_time = time.time()
    
    for attempt in range(MAX_RETRIES + 1):
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            if not response.text:
                raise GeminiError("Empty response from Gemini")
            
            result = _parse_gemini_response(response.text)
            
            # Validate tone
            if result["tone"] not in ["positif", "neutre", "négatif"]:
                result["tone"] = "neutre"
            
            logger.info(f"Gemini analysis complete: tone={result['tone']} in {latency_ms}ms")
            
            return {
                "summary": result["summary"],
                "tone": result["tone"],
                "latency_ms": latency_ms
            }
            
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            
            if attempt < MAX_RETRIES:
                logger.warning(f"Gemini attempt {attempt + 1} failed: {e}. Retrying...")
                continue
            
            logger.error(f"Gemini error after {attempt + 1} attempts: {e}")
            raise GeminiError(f"Analysis failed: {str(e)}")
    
    raise GeminiError("Max retries exceeded")
