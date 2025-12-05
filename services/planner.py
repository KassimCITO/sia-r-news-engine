from datetime import datetime, timedelta
import logging
from config import AUTO_PUBLISH_ENABLED

logger = logging.getLogger(__name__)

class Planner:
    """Determina fecha de publicación, categorías y estrategia de distribución"""
    
    def plan(self, text, suggested_categories=None, suggested_tags=None):
        """
        Plan publication strategy
        
        Args:
            text: Article text
            suggested_categories: List of suggested categories
            suggested_tags: List of suggested tags
        
        Returns:
            Dict with publication plan
        """
        logger.info("Starting publication planning")
        
        plan = {
            "publication_date": self._determine_publication_date(),
            "publication_time": self._determine_publication_time(),
            "final_categories": suggested_categories or [],
            "final_tags": suggested_tags or [],
            "auto_publish": AUTO_PUBLISH_ENABLED,
            "distribution_strategy": self._plan_distribution(text),
            "seo_priority": self._calculate_seo_priority(text),
            "expected_reach": self._estimate_reach(text)
        }
        
        logger.info(f"Planning completed. Publication date: {plan['publication_date']}")
        return plan
    
    def _determine_publication_date(self):
        """Determine optimal publication date"""
        # Default: publish today
        now = datetime.now()
        
        # Could be enhanced with traffic analytics
        # For now, publish immediately
        return now.strftime("%Y-%m-%d")
    
    def _determine_publication_time(self):
        """Determine optimal publication time"""
        # Peak hours for news: 8am, 12pm, 6pm
        now = datetime.now()
        current_hour = now.hour
        
        # Simple strategy: publish in next peak hour
        peak_hours = [8, 12, 18]
        
        for hour in peak_hours:
            if hour > current_hour:
                return f"{hour:02d}:00"
        
        # If it's late, publish tomorrow at 8am
        return "08:00"
    
    def _plan_distribution(self, text):
        """Plan content distribution strategy"""
        text_length = len(text.split())
        
        distribution = {
            "channels": ["wordpress", "social_media"],
            "social_platforms": ["facebook", "twitter", "linkedin"],
            "promotion_hours": 12,  # hours to actively promote
            "priority": "high" if text_length > 500 else "normal"
        }
        
        return distribution
    
    def _calculate_seo_priority(self, text):
        """Calculate SEO priority for this content"""
        # Factors: length, keyword density, structure
        words = len(text.split())
        sentences = len(text.split('.'))
        
        priority_score = 0.0
        
        if words > 500:
            priority_score += 0.3
        if words > 1000:
            priority_score += 0.2
        if sentences > 20:
            priority_score += 0.2
        
        # Normalize to 0-1
        priority_score = min(1.0, priority_score)
        
        return {
            "score": round(priority_score, 2),
            "level": "high" if priority_score > 0.6 else "normal"
        }
    
    def _estimate_reach(self, text):
        """Estimate potential reach"""
        words = len(text.split())
        
        # Simple estimation based on article quality indicators
        base_reach = 500
        
        if words > 300:
            base_reach = 1000
        if words > 800:
            base_reach = 2000
        
        return {
            "estimated_views": base_reach,
            "estimated_shares": base_reach // 10,
            "confidence": 0.5  # Low confidence without actual data
        }
