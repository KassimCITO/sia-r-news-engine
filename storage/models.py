from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.sql import func
from storage.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ApiKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    key_hash = Column(String, unique=True, index=True)
    key_prefix = Column(String)
    is_active = Column(Boolean, default=True)
    last_used = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

class PipelineLog(Base):
    __tablename__ = "pipeline_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    input_text = Column(Text)
    output_json = Column(JSON)
    status = Column(String)  # "success", "failed", "processing"
    error_message = Column(Text, nullable=True)
    execution_time = Column(Float)  # milliseconds
    model_used = Column(String)
    quality_score = Column(Float, default=0.0)
    category = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)  # List of tags
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    wp_post_id = Column(Integer, nullable=True)

class TaxonomyStats(Base):
    __tablename__ = "taxonomy_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, index=True)
    tag_name = Column(String, nullable=True)
    usage_count = Column(Integer, default=0)
    traffic_score = Column(Float, default=0.0)
    relevance_score = Column(Float, default=0.0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AutoLearnProfile(Base):
    __tablename__ = "autolearn_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, index=True)
    category_name = Column(String)
    synonyms = Column(JSON)  # ["syn1", "syn2", ...]
    related_categories = Column(JSON)  # [{"name": "cat", "weight": 0.85}, ...]
    patterns = Column(JSON)  # keyword patterns for detection
    weight = Column(Float, default=1.0)
    confidence = Column(Float, default=0.0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    trend_keywords = Column(Text, default="")
    wp_url = Column(String, default="")
    wp_categories = Column(JSON, default=list)  # List of selected category IDs/Names
    auto_publish_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

