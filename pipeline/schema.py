from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# === INPUT SCHEMAS ===

class PipelineRunRequest(BaseModel):
    """Pipeline execution request"""
    title: str = Field(..., min_length=5, description="Article title")
    content: str = Field(..., min_length=50, description="Article content")
    author: Optional[str] = None
    source: Optional[str] = None
    auto_publish: Optional[bool] = False
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Breaking News",
                "content": "Article content here...",
                "author": "John Doe",
                "auto_publish": False
            }
        }

class PipelineSimulateRequest(BaseModel):
    """Pipeline simulation request (dry-run)"""
    title: str = Field(..., min_length=5)
    content: str = Field(..., min_length=50)

# === OUTPUT SCHEMAS ===

class CleanerOutput(BaseModel):
    """Cleaner module output"""
    original_length: int
    cleaned_length: int
    cleaned_text: str
    quality_score: float = Field(default=0.5, ge=0, le=1)

class TaggerOutput(BaseModel):
    """Tagger module output"""
    suggested_categories: List[str]
    suggested_tags: List[str]
    entities: List[Dict[str, Any]]
    tone: str

class AuditorOutput(BaseModel):
    """Auditor module output"""
    narrative_quality: Dict[str, Any]
    preliminary_factuality: Dict[str, Any]
    aggressiveness_level: Dict[str, Any]
    neutrality_score: Dict[str, Any]
    improvements_suggested: List[str]

class FactCheckerOutput(BaseModel):
    """Fact checker module output"""
    red_flags: List[Dict[str, Any]]
    date_consistency: Dict[str, Any]
    numerical_consistency: Dict[str, Any]
    citation_count: int
    risk_score: float = Field(ge=0, le=1)
    warnings: List[str]

class VerifierOutput(BaseModel):
    """Verifier module output"""
    coherence_score: float = Field(ge=0, le=1)
    contradiction_detected: bool
    duplicate_ideas: List[Dict[str, Any]]
    logical_issues: List[str]
    sentence_flow: Dict[str, Any]
    overall_valid: bool

class HumanizerOutput(BaseModel):
    """Humanizer module output"""
    humanized_text: str
    readability_improvements: List[str]

class SEOOutput(BaseModel):
    """SEO optimizer module output"""
    optimized_text: str
    h1: str
    h2_suggestions: List[Dict[str, Any]]
    meta_description: str
    keyword_density: Dict[str, Any]
    seo_recommendations: List[str]

class PlannerOutput(BaseModel):
    """Planner module output"""
    publication_date: str
    publication_time: str
    final_categories: List[str]
    final_tags: List[str]
    auto_publish: bool
    distribution_strategy: Dict[str, Any]
    seo_priority: Dict[str, Any]
    expected_reach: Dict[str, Any]

class PipelineOutput(BaseModel):
    """Complete pipeline output"""
    status: str = Field(default="success")
    execution_time_ms: float
    pipeline_stages: Dict[str, Any] = Field(default_factory=dict)
    
    # Individual module outputs
    cleaner: Optional[CleanerOutput] = None
    tagger: Optional[TaggerOutput] = None
    auditor: Optional[AuditorOutput] = None
    fact_checker: Optional[FactCheckerOutput] = None
    verifier: Optional[VerifierOutput] = None
    humanizer: Optional[HumanizerOutput] = None
    seo: Optional[SEOOutput] = None
    planner: Optional[PlannerOutput] = None
    
    # Final output
    final_text: str
    final_categories: List[str]
    final_tags: List[str]
    quality_score: float = Field(ge=0, le=1)
    ready_for_publication: bool
    warnings: List[str] = Field(default_factory=list)

class PipelineStatus(BaseModel):
    """Pipeline status check"""
    status: str
    message: str
    uptime_seconds: float = 0
