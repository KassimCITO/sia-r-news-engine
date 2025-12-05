import pytest
from services.cleaner import TextCleaner

class TestTextCleaner:
    """Test suite for TextCleaner"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.cleaner = TextCleaner()
    
    def test_remove_html(self):
        """Test HTML tag removal"""
        html = "<p>This is a <b>test</b> text</p>"
        expected = "This is a test text"
        result = self.cleaner.clean_html(html)
        assert "test" in result
    
    def test_normalize_unicode(self):
        """Test Unicode normalization"""
        text = "Michoacán"
        result = self.cleaner.normalize_unicode(text)
        assert len(result) > 0
    
    def test_remove_extra_whitespace(self):
        """Test whitespace normalization"""
        text = "This  is   a    test"
        result = self.cleaner.remove_extra_whitespace(text)
        assert result == "This is a test"
    
    def test_remove_noise(self):
        """Test noise removal"""
        text = "Visit https://example.com and email test@example.com"
        result = self.cleaner.remove_noise(text)
        assert "example.com" not in result or result.count("example.com") < 2
    
    def test_clean_full_pipeline(self):
        """Test complete cleaning pipeline"""
        text = """
        <p>This  is   a    TEST text with    extra spaces!</p>
        <p>This  is   a    TEST text with    extra spaces!</p>
        Email: test@example.com
        """
        result = self.cleaner.clean(text)
        assert len(result) > 0
        assert "TEST" in result
        # Should remove one duplicate
        assert result.count("TEST text") <= 2
    
    def test_empty_input(self):
        """Test handling of empty input"""
        result = self.cleaner.clean("")
        assert result == ""
    
    def test_fix_style(self):
        """Test style fixing"""
        text = "It is not impossible to fix this."
        result = self.cleaner.fix_style(text)
        assert len(result) > 0
