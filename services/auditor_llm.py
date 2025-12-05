import json
import logging
from services.llm_client import LLMClient

logger = logging.getLogger(__name__)

class AuditorLLM:
    """Audita calidad narrativa, factualidad, agresividad y neutralidad"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def audit(self, text):
        """
        Audit text for quality, factuality, aggressiveness, and neutrality
        
        Args:
            text: Input text to audit
        
        Returns:
            Dict with audit results and suggested improvements
        """
        logger.info("Starting LLM-based text audit")
        
        system_prompt = """You are a professional news editor and quality auditor.
        Analyze the provided text for:
        1. narrative_quality: Score 0-10 and brief explanation
        2. preliminary_factuality: Score 0-10 (based on language markers, citations)
        3. aggressiveness_level: Score 0-10 (how harsh/confrontational)
        4. neutrality_score: Score 0-10 (journalistic neutrality, 10=neutral, 0=very biased)
        5. improvements_suggested: List of specific improvements
        
        Return only valid JSON, no markdown."""
        
        user_prompt = f"""Audit this news text as a professional editor:

Text:
{text[:2000]}

Provide JSON with keys: narrative_quality, preliminary_factuality, 
aggressiveness_level, neutrality_score, improvements_suggested"""
        
        try:
            result = self.llm.generate_json(user_prompt, system_prompt)
            
            if isinstance(result, dict):
                return {
                    "narrative_quality": result.get("narrative_quality", {"score": 5, "reason": ""}),
                    "preliminary_factuality": result.get("preliminary_factuality", {"score": 5, "reason": ""}),
                    "aggressiveness_level": result.get("aggressiveness_level", {"score": 5, "reason": ""}),
                    "neutrality_score": result.get("neutrality_score", {"score": 5, "reason": ""}),
                    "improvements_suggested": result.get("improvements_suggested", [])
                }
            else:
                logger.warning("Invalid LLM response format")
                return self._default_response()
                
        except Exception as e:
            logger.error(f"Error in audit: {e}")
            return self._default_response()
    
    def _default_response(self):
        """Return default audit response"""
        return {
            "narrative_quality": {"score": 5, "reason": "Audit not completed"},
            "preliminary_factuality": {"score": 5, "reason": "Audit not completed"},
            "aggressiveness_level": {"score": 5, "reason": "Audit not completed"},
            "neutrality_score": {"score": 5, "reason": "Audit not completed"},
            "improvements_suggested": []
        }
