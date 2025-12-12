"""
Gemini Service Unit Tests
Tests for analyze_text with mocked Gemini API
"""
import pytest
from unittest.mock import patch, MagicMock


class TestAnalyzeText:
    """Tests for Gemini analyze_text function"""
    
    @pytest.mark.asyncio
    @patch('app.services.gemini_service.genai.GenerativeModel')
    async def test_analyze_text_success_json_response(self, mock_model_class):
        """Test successful analysis with JSON response"""
        from app.services.gemini_service import analyze_text
        
        # Mock Gemini response with valid JSON
        mock_response = MagicMock()
        mock_response.text = '{"summary": "This is a technology article.", "tone": "positif"}'
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        result = await analyze_text("Test text about technology", "technology")
        
        assert result["summary"] == "This is a technology article."
        assert result["tone"] == "positif"
        assert "latency_ms" in result
    
    @pytest.mark.asyncio
    @patch('app.services.gemini_service.genai.GenerativeModel')
    async def test_analyze_text_success_plain_text_response(self, mock_model_class):
        """Test successful analysis with plain text response (fallback parsing)"""
        from app.services.gemini_service import analyze_text
        
        # Mock Gemini response with plain text format
        mock_response = MagicMock()
        mock_response.text = "Summary: This article discusses AI innovations.\nTone: positif"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        result = await analyze_text("Test text", "technology")
        
        assert "AI innovations" in result["summary"]
        assert result["tone"] == "positif"
    
    @pytest.mark.asyncio
    @patch('app.services.gemini_service.genai.GenerativeModel')
    async def test_analyze_text_negative_tone(self, mock_model_class):
        """Test detection of negative tone"""
        from app.services.gemini_service import analyze_text
        
        mock_response = MagicMock()
        mock_response.text = '{"summary": "The market crashed severely.", "tone": "négatif"}'
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        result = await analyze_text("Market crash news", "business")
        
        assert result["tone"] == "négatif"
    
    @pytest.mark.asyncio
    @patch('app.services.gemini_service.genai.GenerativeModel')
    async def test_analyze_text_neutral_tone(self, mock_model_class):
        """Test detection of neutral tone"""
        from app.services.gemini_service import analyze_text
        
        mock_response = MagicMock()
        mock_response.text = '{"summary": "The report presents data.", "tone": "neutre"}'
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        result = await analyze_text("Data report", "science")
        
        assert result["tone"] == "neutre"
    
    @pytest.mark.asyncio
    @patch('app.services.gemini_service.genai.GenerativeModel')
    async def test_analyze_text_invalid_tone_defaults_to_neutre(self, mock_model_class):
        """Test that invalid tone defaults to neutre"""
        from app.services.gemini_service import analyze_text
        
        mock_response = MagicMock()
        mock_response.text = '{"summary": "Some text", "tone": "unknown_tone"}'
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        result = await analyze_text("Test text", "technology")
        
        assert result["tone"] == "neutre"
    
    @pytest.mark.asyncio
    @patch('app.services.gemini_service.genai.GenerativeModel')
    async def test_analyze_text_empty_response_error(self, mock_model_class):
        """Test error handling for empty response"""
        from app.services.gemini_service import analyze_text, GeminiError
        
        mock_response = MagicMock()
        mock_response.text = ""
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        with pytest.raises(GeminiError) as exc_info:
            await analyze_text("Test text", "technology")
        
        assert "Empty response" in str(exc_info.value)
    
    @pytest.mark.asyncio
    @patch('app.services.gemini_service.genai.GenerativeModel')
    async def test_analyze_text_api_exception(self, mock_model_class):
        """Test error handling for API exceptions"""
        from app.services.gemini_service import analyze_text, GeminiError
        
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API quota exceeded")
        mock_model_class.return_value = mock_model
        
        with pytest.raises(GeminiError) as exc_info:
            await analyze_text("Test text", "technology")
        
        assert "API quota exceeded" in str(exc_info.value)


class TestParseGeminiResponse:
    """Tests for _parse_gemini_response helper function"""
    
    def test_parse_json_response(self):
        """Test parsing valid JSON response"""
        from app.services.gemini_service import _parse_gemini_response
        
        text = '{"summary": "Test summary", "tone": "positif"}'
        result = _parse_gemini_response(text)
        
        assert result["summary"] == "Test summary"
        assert result["tone"] == "positif"
    
    def test_parse_json_with_extra_text(self):
        """Test parsing JSON embedded in text"""
        from app.services.gemini_service import _parse_gemini_response
        
        text = 'Here is the analysis:\n{"summary": "Analysis result", "tone": "neutre"}\nEnd of response.'
        result = _parse_gemini_response(text)
        
        assert result["summary"] == "Analysis result"
        assert result["tone"] == "neutre"
    
    def test_parse_plain_text_fallback(self):
        """Test fallback to plain text parsing"""
        from app.services.gemini_service import _parse_gemini_response
        
        text = "Résumé: This is the summary.\nTon: positif"
        result = _parse_gemini_response(text)
        
        assert "summary" in result["summary"].lower() or len(result["summary"]) > 0
    
    def test_parse_unstructured_text(self):
        """Test parsing completely unstructured text"""
        from app.services.gemini_service import _parse_gemini_response
        
        text = "This is just some random analysis text without structure."
        result = _parse_gemini_response(text)
        
        # Should use the text as summary (up to 500 chars)
        assert result["summary"] == text
        assert result["tone"] == "neutre"  # Default
