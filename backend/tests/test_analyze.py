"""
Analyze Endpoint Tests
Tests for POST /analyze with mocked HuggingFace and Gemini services
"""
import pytest
from unittest.mock import patch, AsyncMock


class TestAnalyzeEndpoint:
    """Tests for POST /analyze endpoint"""
    
    @patch('app.routers.analyze.classify_text')
    @patch('app.routers.analyze.analyze_text')
    def test_analyze_success(
        self, 
        mock_gemini, 
        mock_hf, 
        client, 
        auth_headers, 
        sample_text,
        mock_huggingface_response,
        mock_gemini_response
    ):
        """Test successful text analysis with mocked APIs"""
        # Setup mocks
        mock_hf.return_value = mock_huggingface_response
        mock_gemini.return_value = mock_gemini_response
        
        response = client.post(
            "/analyze/",
            json={"text": sample_text},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert data["category"] == "technology"
        assert "hf_scores" in data
        assert data["summary"] is not None
        assert data["tone"] in ["positif", "neutre", "négatif"]
        assert "meta" in data
        assert "hf_latency_ms" in data["meta"]
        assert "gemini_latency_ms" in data["meta"]
        assert "total_execution_ms" in data["meta"]
    
    def test_analyze_no_auth(self, client, sample_text):
        """Test analyze fails without authentication"""
        response = client.post(
            "/analyze/",
            json={"text": sample_text}
        )
        
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]
    
    def test_analyze_text_too_short(self, client, auth_headers):
        """Test analyze fails with text shorter than minimum length"""
        response = client.post(
            "/analyze/",
            json={"text": "Too short"},
            headers=auth_headers
        )
        
        assert response.status_code in [400, 422]  # Validation error
    
    def test_analyze_empty_text(self, client, auth_headers):
        """Test analyze fails with empty text"""
        response = client.post(
            "/analyze/",
            json={"text": ""},
            headers=auth_headers
        )
        
        assert response.status_code == 422  # Validation error
    
    @patch('app.routers.analyze.classify_text')
    def test_analyze_huggingface_error(
        self, 
        mock_hf, 
        client, 
        auth_headers, 
        sample_text
    ):
        """Test analyze handles HuggingFace service error"""
        from app.services.huggingface_service import HuggingFaceError
        mock_hf.side_effect = HuggingFaceError("API timeout")
        
        response = client.post(
            "/analyze/",
            json={"text": sample_text},
            headers=auth_headers
        )
        
        assert response.status_code == 503
        assert "Classification service unavailable" in response.json()["detail"]
    
    @patch('app.routers.analyze.classify_text')
    @patch('app.routers.analyze.analyze_text')
    def test_analyze_gemini_error(
        self, 
        mock_gemini, 
        mock_hf, 
        client, 
        auth_headers, 
        sample_text,
        mock_huggingface_response
    ):
        """Test analyze handles Gemini service error"""
        from app.services.gemini_service import GeminiError
        
        mock_hf.return_value = mock_huggingface_response
        mock_gemini.side_effect = GeminiError("API error")
        
        response = client.post(
            "/analyze/",
            json={"text": sample_text},
            headers=auth_headers
        )
        
        assert response.status_code == 503
        assert "Summarization service unavailable" in response.json()["detail"]


class TestAnalyzeHealthCheck:
    """Tests for GET /analyze/health"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/analyze/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "analyze"
        assert "mock_mode" in data
