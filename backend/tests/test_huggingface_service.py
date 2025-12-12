"""
HuggingFace Service Unit Tests
Tests for classify_text with mocked HTTP responses
"""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import httpx


class TestClassifyText:
    """Tests for HuggingFace classify_text function"""
    
    @pytest.mark.asyncio
    @patch('app.services.huggingface_service.httpx.AsyncClient')
    async def test_classify_text_success_new_format(self, mock_client_class):
        """Test successful classification with new HuggingFace API format"""
        from app.services.huggingface_service import classify_text
        
        # Mock response with new format (list of {label, score})
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"label": "technology", "score": 0.8912},
            {"label": "business", "score": 0.0654},
            {"label": "science", "score": 0.0321}
        ]
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client_class.return_value = mock_client
        
        result = await classify_text("Test text about technology and innovation")
        
        assert result["category"] == "technology"
        assert result["confidence"] == 0.8912
        assert "scores" in result
        assert result["scores"]["technology"] == 0.8912
        assert "latency_ms" in result
    
    @pytest.mark.asyncio
    @patch('app.services.huggingface_service.httpx.AsyncClient')
    async def test_classify_text_success_old_format(self, mock_client_class):
        """Test successful classification with old HuggingFace API format"""
        from app.services.huggingface_service import classify_text
        
        # Mock response with old format ({labels, scores})
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "labels": ["technology", "business", "science"],
            "scores": [0.8912, 0.0654, 0.0321]
        }
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client_class.return_value = mock_client
        
        result = await classify_text("Test text about technology")
        
        assert result["category"] == "technology"
        assert result["confidence"] == 0.8912
    
    @pytest.mark.asyncio
    @patch('app.services.huggingface_service.httpx.AsyncClient')
    async def test_classify_text_model_loading(self, mock_client_class):
        """Test handling of model loading (503) response with retry"""
        from app.services.huggingface_service import classify_text, HuggingFaceError
        
        # First call returns 503 (model loading), second returns success
        mock_response_loading = MagicMock()
        mock_response_loading.status_code = 503
        mock_response_loading.json.return_value = {"estimated_time": 5}
        
        mock_response_success = MagicMock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = [
            {"label": "technology", "score": 0.85}
        ]
        
        mock_client = AsyncMock()
        mock_client.post.side_effect = [mock_response_loading, mock_response_success]
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client_class.return_value = mock_client
        
        result = await classify_text("Test text")
        
        assert result["category"] == "technology"
    
    @pytest.mark.asyncio
    @patch('app.services.huggingface_service.httpx.AsyncClient')
    async def test_classify_text_api_error(self, mock_client_class):
        """Test handling of API error response"""
        from app.services.huggingface_service import classify_text, HuggingFaceError
        
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client_class.return_value = mock_client
        
        with pytest.raises(HuggingFaceError) as exc_info:
            await classify_text("Test text")
        
        assert "API error: 500" in str(exc_info.value)
    
    @pytest.mark.asyncio
    @patch('app.services.huggingface_service.httpx.AsyncClient')
    async def test_classify_text_timeout(self, mock_client_class):
        """Test handling of request timeout"""
        from app.services.huggingface_service import classify_text, HuggingFaceError
        
        mock_client = AsyncMock()
        mock_client.post.side_effect = httpx.TimeoutException("Connection timeout")
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client_class.return_value = mock_client
        
        with pytest.raises(HuggingFaceError) as exc_info:
            await classify_text("Test text")
        
        assert "timeout" in str(exc_info.value).lower()
    
    @pytest.mark.asyncio
    @patch('app.services.huggingface_service.httpx.AsyncClient')
    async def test_classify_text_custom_labels(self, mock_client_class):
        """Test classification with custom labels"""
        from app.services.huggingface_service import classify_text
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"label": "positive", "score": 0.75},
            {"label": "negative", "score": 0.15},
            {"label": "neutral", "score": 0.10}
        ]
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client_class.return_value = mock_client
        
        result = await classify_text(
            "Great product!",
            candidate_labels=["positive", "negative", "neutral"]
        )
        
        assert result["category"] == "positive"
        assert result["confidence"] == 0.75
