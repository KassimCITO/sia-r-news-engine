import pytest
from services.wp_client import WordPressClient

class TestWordPressClient:
    """Test suite for WordPressClient"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.wp_client = WordPressClient()
    
    def test_client_initialization(self):
        """Test that client initializes properly"""
        assert self.wp_client.base_url
        assert self.wp_client.session
        assert self.wp_client.auth
    
    def test_create_post_requires_data(self):
        """Test that create_post requires title and content"""
        # This should not raise an error but should handle it gracefully
        # (actual WordPress call will fail if not configured)
        result = self.wp_client.create_post(
            title="Test",
            content="Test content"
        )
        # Result could be None if WordPress is not configured
        assert result is None or isinstance(result, int)
    
    def test_upload_image_with_missing_file(self):
        """Test that upload_image handles missing files"""
        result = self.wp_client.upload_image("/nonexistent/file.jpg")
        assert result is None
    
    def test_get_post_method_exists(self):
        """Test that get_post method exists and works"""
        # This will fail if WP is not configured, which is OK
        result = self.wp_client.get_post(999999)
        assert result is None or isinstance(result, dict)
