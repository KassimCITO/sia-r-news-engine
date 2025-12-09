import logging
from services.llm_client import LLMClient

logger = logging.getLogger(__name__)

class SensitivityGuard:
    def __init__(self):
        self.llm = LLMClient()

    def check(self, content: str) -> dict:
        """
        Check content for sensitivity, hate speech, political bias, etc.
        """
        prompt = f"""
        Analyze the following content for sensitivity issues.
        Content: "{content[:2000]}..."
        
        Check for:
        1. Hate speech
        2. Explicit violence
        3. Adult content
        4. Extreme political bias
        5. Brand safety risks
        
        Return ONLY valid JSON:
        {{
            "is_safe": true/false,
            "risk_score": 0.0 to 1.0 (0 is safe),
            "issues": ["issue 1", "issue 2"]
        }}
        """
        
        try:
            import json
            response = self.llm.generate(prompt, temperature=0.1)
            response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error checking sensitivity: {e}")
            return {"is_safe": True, "risk_score": 0.0, "issues": []}
