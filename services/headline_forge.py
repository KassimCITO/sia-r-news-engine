import logging
import json
from services.llm_client import LLMClient

logger = logging.getLogger(__name__)

class HeadlineForge:
    def __init__(self):
        self.llm = LLMClient()

    def generate(self, topic_data: dict, count: int = 5) -> list:
        """
        Generate headlines based on expanded topic data.
        """
        prompt = f"""
        Based on this topic info:
        Angle: {topic_data.get('main_angle')}
        Key Points: {topic_data.get('key_points')}
        Tone: {topic_data.get('tone')}
        
        Generate {count} catchy, SEO-friendly headlines for a news article.
        Return ONLY valid JSON array of strings:
        ["Headline 1", "Headline 2", ...]
        """
        
        try:
            response = self.llm.generate(prompt, temperature=0.8)
            response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error generating headlines: {e}")
            return [f"News: {topic_data.get('main_angle')}"]
