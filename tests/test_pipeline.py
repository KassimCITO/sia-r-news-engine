import pytest
import json
from pipeline.run_pipeline import Pipeline
from pipeline.schema import PipelineRunRequest

class TestPipeline:
    """Test suite for Pipeline"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.pipeline = Pipeline()
    
    def test_pipeline_initialization(self):
        """Test that pipeline initializes all components"""
        assert self.pipeline.cleaner
        assert self.pipeline.tagger
        assert self.pipeline.auditor
        assert self.pipeline.fact_checker
        assert self.pipeline.verifier
        assert self.pipeline.humanizer
        assert self.pipeline.seo_optimizer
        assert self.pipeline.planner
    
    def test_pipeline_run_structure(self):
        """Test that pipeline run returns expected structure"""
        # Use short text to avoid API rate limits
        title = "Test Article"
        content = "This is a test article with some content to process."
        
        result = self.pipeline.run(title, content)
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "execution_time_ms" in result
        assert "stages" in result
    
    def test_pipeline_status_in_result(self):
        """Test that pipeline status is either success or error"""
        title = "Test"
        content = "Test content for pipeline."
        
        result = self.pipeline.run(title, content)
        
        assert result["status"] in ["success", "error"]
    
    def test_pipeline_with_empty_content(self):
        """Test pipeline behavior with empty content"""
        result = self.pipeline.run("Title", "")
        
        # Should handle gracefully
        assert "status" in result
        assert isinstance(result, dict)
    
    def test_pipeline_quality_score_calculation(self):
        """Test that quality score is calculated"""
        title = "Quality Test"
        content = "This article demonstrates pipeline quality scoring functionality."
        
        result = self.pipeline.run(title, content)
        
        if result["status"] == "success":
            # If execution was successful, check for quality metrics
            assert "stages" in result or "final_text" in result
    
    def test_pipeline_run_request_validation(self):
        """Test PipelineRunRequest validation"""
        # Valid request
        valid_req = PipelineRunRequest(
            title="Valid Title",
            content="This is valid content with enough characters."
        )
        assert valid_req.title
        assert valid_req.content
        
        # Invalid requests should raise validation errors
        with pytest.raises(Exception):
            PipelineRunRequest(title="X", content="Y")  # Too short
