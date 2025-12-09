import logging
import json
import random
from datetime import datetime

from services.llm_client import LLMClient
from services.topic_expander import TopicExpander
from services.headline_forge import HeadlineForge
from services.sensitivity_guard import SensitivityGuard
from pipeline.run_pipeline import Pipeline

logger = logging.getLogger(__name__)

class ArticleGenerator:
    def __init__(self):
        self.llm = LLMClient()
        self.topic_expander = TopicExpander()
        self.headline_forge = HeadlineForge()
        self.sensitivity_guard = SensitivityGuard()
        self.pipeline = Pipeline()

    def generate_from_trend(self, trend_data: dict, auto_publish: bool = False):
        """
        Full flow: Trend -> Topic -> Headline -> Draft -> Pipeline -> Publish (maybe)
        """
        try:
            logger.info(f"Generating article for trend: {trend_data.get('title')}")
            
            # 1. Expand Topic
            context = f"Source: {trend_data.get('source')}\nSnippet: {trend_data.get('snippet', '')}"
            topic = self.topic_expander.expand(trend_data.get('title'), context)
            
            # 2. Generate Headlines
            headlines = self.headline_forge.generate(topic)
            selected_headline = headlines[0] if headlines else trend_data.get('title')
            
            # 3. Generate Draft Content
            draft_content = self._write_draft(selected_headline, topic)
            
            # 4. Sensitivity Check
            sensitivity = self.sensitivity_guard.check(draft_content)
            if not sensitivity.get('is_safe', True) or sensitivity.get('risk_score', 0) > 0.7:
                logger.warning(f"Content blocked by sensitivity guard: {sensitivity}")
                return {
                    "status": "blocked",
                    "reason": "sensitivity",
                    "details": sensitivity
                }
            
            # 5. Run SIA-R Pipeline (Refinement, SEO, Facts, Taxonomy)
            pipeline_result = self.pipeline.run(
                title=selected_headline,
                content=draft_content,
                user_id=1, # System user
                auto_publish=auto_publish
            )
            
            return pipeline_result
            
        except Exception as e:
            logger.error(f"Error in article generation: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    def _write_draft(self, title: str, topic_data: dict) -> str:
        """
        Write the initial draft of the article.
        """
        prompt = f"""
        Write a comprehensive news article with the following details:
        Title: {title}
        Angle: {topic_data.get('main_angle')}
        Key Points: {', '.join(topic_data.get('key_points', []))}
        Tone: {topic_data.get('tone')}
        Target Audience: {topic_data.get('target_audience')}
        
        Requirements:
        - At least 800 words.
        - Use Markdown formatting (## Subheaders, **bold**, etc.).
        - Include an introduction, 3-4 body sections, and a conclusion.
        - Be engaging and factual.
        """
        
        return self.llm.generate(prompt, temperature=0.7)
