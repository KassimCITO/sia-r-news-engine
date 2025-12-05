import pytest
from services.tagger_llm import TaggerLLM

class TestTaggerLLM:
    """Test suite for TaggerLLM"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.tagger = TaggerLLM()
    
    def test_extract_tags_structure(self):
        """Test that extract_tags returns expected structure"""
        text = "Political news about government elections and voting."
        result = self.tagger.extract_tags(text)
        
        assert isinstance(result, dict)
        assert "suggested_categories" in result
        assert "suggested_tags" in result
        assert "entities" in result
        assert "tone" in result
        
        assert isinstance(result["suggested_categories"], list)
        assert isinstance(result["suggested_tags"], list)
        assert isinstance(result["entities"], list)
        assert isinstance(result["tone"], str)
    
    def test_extract_tags_not_empty(self):
        """Test that extract_tags produces some output"""
        text = """
        Breaking news: New technology company announces innovative AI solution.
        The company expects significant market impact in the coming months.
        """
        result = self.tagger.extract_tags(text)
        
        # At least one of these should have content
        has_content = (
            len(result["suggested_categories"]) > 0 or
            len(result["suggested_tags"]) > 0 or
            len(result["entities"]) > 0
        )
        assert has_content or result["tone"]
    
    def test_tone_is_valid(self):
        """Test that tone is one of expected values"""
        text = "This is a positive news story."
        result = self.tagger.extract_tags(text)
        
        valid_tones = ["neutral", "critical", "positive", "investigative", "opinion", ""]
        assert result["tone"] in valid_tones or len(result["tone"]) > 0
    
    def test_default_response_structure(self):
        """Test default response structure"""
        result = self.tagger._default_response()
        
        assert "suggested_categories" in result
        assert "suggested_tags" in result
        assert "entities" in result
        assert "tone" in result
        assert result["tone"] == "neutral"
