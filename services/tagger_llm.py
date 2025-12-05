import json
import logging
from services.llm_client import LLMClient

logger = logging.getLogger(__name__)

class TaggerLLM:
    """Extrae categorías, etiquetas, entidades y tono usando LLM"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def extract_tags(self, text):
        """
        Extract categories, tags, entities, and journalistic tone
        
        Args:
            text: Input text to analyze
        
        Returns:
            Dict with suggested_categories, suggested_tags, entities, tone
        """
        logger.info("Starting tag extraction with LLM")
        
        system_prompt = """You are a professional journalist AI assistant. 
        Analyze the provided text and extract:
        1. suggested_categories: List of relevant news categories (e.g., "Politics", "Sports", "Technology")
        2. suggested_tags: List of specific topic tags
        3. entities: Named entities found (persons, organizations, locations)
        4. tone: Journalistic tone (neutral, critical, positive, investigative, opinion)
        
        Return only valid JSON, no markdown formatting."""
        
        user_prompt = f"""Analyze this news text and extract metadata:

Text:
{text[:2000]}

Provide JSON with keys: suggested_categories, suggested_tags, entities, tone"""
        
        try:
            result = self.llm.generate_json(user_prompt, system_prompt)
            
            # Validate response
            if isinstance(result, dict):
                return {
                    "suggested_categories": result.get("suggested_categories", []),
                    "suggested_tags": result.get("suggested_tags", []),
                    "entities": result.get("entities", []),
                    "tone": result.get("tone", "neutral")
                }
            else:
                logger.warning("Invalid LLM response format")
                return self._default_response()
                
        except Exception as e:
            logger.error(f"Error in tag extraction: {e}")
            return self._default_response()
    
    def _default_response(self):
        """Return default response structure"""
        return {
            "suggested_categories": [],
            "suggested_tags": [],
            "entities": [],
            "tone": "neutral"
        }
