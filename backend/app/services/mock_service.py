"""
Mock Services for Backend Testing
Returns fake responses without calling external APIs
"""
import random
import asyncio
from typing import Dict, Any, List

# Mock category labels
MOCK_CATEGORIES = [
    "technology", "business", "politics", "sports", "entertainment",
    "health", "science", "education", "travel", "food"
]

# Mock summaries based on category
MOCK_SUMMARIES = {
    "technology": "This text discusses technological innovations and digital advancements that are shaping the modern world.",
    "business": "The content covers business strategies, market trends, and economic developments in the corporate sector.",
    "politics": "This article analyzes political events, policy decisions, and governmental actions affecting society.",
    "sports": "The text reports on athletic competitions, team performances, and sports-related news.",
    "entertainment": "This content explores entertainment industry news, celebrity updates, and media productions.",
    "health": "The text provides insights on health topics, medical research, and wellness recommendations.",
    "science": "This article examines scientific discoveries, research findings, and technological breakthroughs.",
    "education": "The content discusses educational trends, learning methodologies, and academic developments.",
    "travel": "This text covers travel destinations, tourism experiences, and adventure recommendations.",
    "food": "The content explores culinary topics, recipes, and food industry trends."
}

# Mock tones
MOCK_TONES = ["positif", "neutre", "négatif"]


async def mock_classify_text(
    text: str,
    candidate_labels: List[str] = None
) -> Dict[str, Any]:
    """
    Mock HuggingFace classification - returns fake but realistic results.
    
    Args:
        text: The text to classify
        candidate_labels: List of possible categories
    
    Returns:
        Dict with category, confidence, and all scores
    """
    if candidate_labels is None:
        candidate_labels = MOCK_CATEGORIES
    
    # Simulate API latency (100-500ms)
    await asyncio.sleep(random.uniform(0.1, 0.5))
    
    # Generate random scores for each category
    scores = {}
    remaining = 1.0
    
    for i, label in enumerate(candidate_labels):
        if i == len(candidate_labels) - 1:
            scores[label] = round(remaining, 4)
        else:
            score = random.uniform(0, remaining * 0.8)
            scores[label] = round(score, 4)
            remaining -= score
    
    # Sort by score and get top category
    sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
    top_label = list(sorted_scores.keys())[0]
    top_score = sorted_scores[top_label]
    
    return {
        "category": top_label,
        "confidence": top_score,
        "scores": sorted_scores,
        "latency_ms": random.randint(100, 500)
    }


async def mock_analyze_text(text: str, category: str) -> Dict[str, Any]:
    """
    Mock Gemini analysis - returns fake summary and tone.
    
    Args:
        text: The original text to analyze
        category: The category from classification
    
    Returns:
        Dict with summary, tone, and latency_ms
    """
    # Simulate API latency (200-800ms)
    await asyncio.sleep(random.uniform(0.2, 0.8))
    
    # Get mock summary based on category
    summary = MOCK_SUMMARIES.get(
        category.lower(),
        "This text contains interesting content that has been analyzed by our AI system."
    )
    
    # Random tone
    tone = random.choice(MOCK_TONES)
    
    return {
        "summary": summary,
        "tone": tone,
        "latency_ms": random.randint(200, 800)
    }
