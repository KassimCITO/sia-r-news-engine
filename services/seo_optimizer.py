import re
import logging
from services.llm_client import LLMClient

logger = logging.getLogger(__name__)

class SEOOptimizer:
    """Optimiza para SEO: H1, H2, H3, metadescripción, densidad, etc"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def optimize(self, text, primary_entity=None):
        """
        Optimize text for SEO
        
        Args:
            text: Input text to optimize
            primary_entity: Main topic/entity for keyword density
        
        Returns:
            Dict with optimized text and SEO recommendations
        """
        logger.info("Starting SEO optimization")
        
        results = {
            "optimized_text": text,
            "h1": self._generate_h1(text),
            "h2_suggestions": self._generate_h2_suggestions(text),
            "meta_description": self._generate_meta_description(text),
            "keyword_density": self._analyze_keyword_density(text, primary_entity),
            "seo_recommendations": []
        }
        
        results["seo_recommendations"] = self._generate_recommendations(results)
        
        logger.info("SEO optimization completed")
        return results
    
    def _generate_h1(self, text):
        """Generate optimal H1 heading"""
        system_prompt = """Generate a compelling, SEO-friendly H1 heading for this news article.
        The heading should:
        - Be under 60 characters
        - Include the main topic
        - Be engaging
        - Use natural language
        
        Return only the heading, no markdown."""
        
        user_prompt = f"""Generate an H1 for this text:

{text[:500]}"""
        
        try:
            h1 = self.llm.generate(user_prompt, system_prompt)
            return h1.strip()
        except Exception as e:
            logger.error(f"Error generating H1: {e}")
            # Fallback: use first sentence
            first_sentence = re.split(r'[.!?]', text)[0]
            return first_sentence[:60] if first_sentence else "News Article"
    
    def _generate_h2_suggestions(self, text):
        """Generate H2 subheading suggestions"""
        # Split text into paragraphs
        paragraphs = text.split('\n\n')
        h2_suggestions = []
        
        for i, para in enumerate(paragraphs[:3]):  # Limit to first 3 paragraphs
            if len(para) > 50:
                # Simple approach: use first part of paragraph as H2
                h2 = para[:50] + "..."
                h2_suggestions.append({
                    "position": i,
                    "suggestion": h2
                })
        
        return h2_suggestions
    
    def _generate_meta_description(self, text):
        """Generate SEO-friendly meta description (150-160 chars)"""
        # Remove HTML tags and extra spaces
        clean_text = re.sub(r'<[^>]+>', '', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        # Take first 155-160 characters and end at a word boundary
        desc = clean_text[:160]
        last_space = desc.rfind(' ')
        if last_space > 0 and last_space > 120:
            desc = desc[:last_space] + "..."
        
        return desc
    
    def _analyze_keyword_density(self, text, primary_entity=None):
        """Analyze keyword density for optimization"""
        if not primary_entity:
            # Extract first noun as primary entity
            nouns = re.findall(r'\b[A-Z]\w+\b', text)
            primary_entity = nouns[0] if nouns else "news"
        
        # Count occurrences
        entity_lower = primary_entity.lower()
        total_words = len(text.split())
        occurrences = len(re.findall(r'\b' + re.escape(entity_lower) + r'\b', text, re.IGNORECASE))
        
        density = (occurrences / total_words * 100) if total_words > 0 else 0
        
        return {
            "primary_entity": primary_entity,
            "occurrences": occurrences,
            "total_words": total_words,
            "density_percent": round(density, 2),
            "is_optimal": 1.5 <= density <= 3.0
        }
    
    def _generate_recommendations(self, results):
        """Generate SEO recommendations"""
        recommendations = []
        
        density = results["keyword_density"]["density_percent"]
        if density < 1.5:
            recommendations.append(f"Increase keyword density for '{results['keyword_density']['primary_entity']}' (current: {density}%)")
        elif density > 3.0:
            recommendations.append(f"Reduce keyword density to avoid over-optimization (current: {density}%)")
        
        h1 = results["h1"]
        if len(h1) > 70:
            recommendations.append("H1 is too long. Aim for under 70 characters.")
        
        meta = results["meta_description"]
        if len(meta) < 120:
            recommendations.append("Meta description is too short. Aim for 120-160 characters.")
        elif len(meta) > 160:
            recommendations.append("Meta description is too long. Keep it under 160 characters.")
        
        if not results["h2_suggestions"]:
            recommendations.append("Add H2 subheadings to improve structure.")
        
        return recommendations
