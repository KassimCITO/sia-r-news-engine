import logging
import json
from services.llm_client import LLMClient

logger = logging.getLogger(__name__)

class TopicExpander:
    def __init__(self):
        self.llm = LLMClient()

    def expand(self, trend_title: str, trend_context: str = "") -> dict:
        """
        Expand a trend into a topic with angles, target audience, and key points.
        """
        prompt = f"""
        Analyze the following trend: "{trend_title}"
        Context: {trend_context}
        
        Generate a detailed expansion for a news article or blog post.
        Return ONLY valid JSON with this structure:
        {{
            "main_angle": "The primary angle/focus of the story",
            "alternative_angles": ["angle 1", "angle 2"],
            "target_audience": "Who should read this",
            "key_points": ["point 1", "point 2", "point 3"],
            "tone": "suggested tone (e.g., informative, critical, enthusiastic)"
        }}
        """
        
        try:
            response = self.llm.generate(prompt, temperature=0.7)
            # Simple cleanup if markdown code blocks are used
            response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error expanding topic: {e}")
            return {
                "main_angle": trend_title,
                "alternative_angles": [],
                "target_audience": "General",
                "key_points": [trend_context],
                "tone": "Neutral"
            }
