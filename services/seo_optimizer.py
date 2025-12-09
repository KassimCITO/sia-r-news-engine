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
        
        # Parallelize these if possible in future, for now sequential
        results = {
            "optimized_text": text,
            "h1": self._generate_h1(text),
            "h2_suggestions": self._generate_h2_suggestions(text),
            "meta_description": self._generate_meta_description(text),
            "schema_markup": self._generate_schema_markup(text),
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
            return h1.strip().strip('"')
        except Exception as e:
            logger.error(f"Error generating H1: {e}")
            # Fallback: use first sentence
            first_sentence = re.split(r'[.!?]', text)[0]
            return first_sentence[:60] if first_sentence else "News Article"
    
    def _generate_h2_suggestions(self, text):
        """Generate H2 subheading suggestions using LLM"""
        system_prompt = """Analyze the article text and suggest 3-4 logical H2 subheadings to break up the content.
        Return the response as a JSON list of strings. Example: ["Introduction context", "Main Event Details", "Implications"]"""
        
        user_prompt = f"""Suggest H2 subheadings for this text:
        
{text[:1500]}"""  # Send enough context
        
        try:
            response = self.llm.generate(user_prompt, system_prompt)
            # Try to parse JSON, if it fails, split by newlines
            import json
            try:
                # Clean potential markdown code blocks
                clean_json = response.replace("```json", "").replace("```", "").strip()
                h2_list = json.loads(clean_json)
                if isinstance(h2_list, list):
                    return [{"suggestion": h} for h in h2_list]
            except json.JSONDecodeError:
                pass
                
            # Fallback parsing
            lines = [line.strip().lstrip('- ').lstrip('1. ') for line in response.split('\n') if line.strip()]
            return [{"suggestion": line} for line in lines[:4]]
            
        except Exception as e:
            logger.error(f"Error generating H2s: {e}")
            return []

    def _generate_meta_description(self, text):
        """Generate SEO-friendly meta description using LLM"""
        system_prompt = """Write a compelling SEO meta description for this article.
        - Maximum 160 characters.
        - Include relevant keywords.
        - summarizing the main point.
        - Return ONLY the description text."""
        
        user_prompt = f"""Generate a meta description for:
        
{text[:1000]}"""

        try:
            desc = self.llm.generate(user_prompt, system_prompt)
            return desc.strip()
        except Exception as e:
            logger.error(f"Error generating meta description: {e}")
            return text[:157] + "..."
    
    def _generate_schema_markup(self, text):
        """Generate JSON-LD Schema Markup (NewsArticle)"""
        system_prompt = """Generate a valid JSON-LD Schema.org object for a 'NewsArticle'.
        Using the provided text, extract/generate:
        - headline
        - datePublished (use current ISO datetime if not found)
        - dateModified (use current ISO datetime)
        - description
        - articleBody (first 100 chars...)
        
        Return ONLY valid JSON. keys should be "headline", "datePublished", "description", etc."""
        
        user_prompt = f"""Generate JSON-LD schema for:
        
{text[:1000]}"""

        try:
            response = self.llm.generate(user_prompt, system_prompt)
            clean_json = response.replace("```json", "").replace("```", "").strip()
            # Verify it's valid json (lazy check)
            import json
            return json.loads(clean_json)
        except Exception as e:
            logger.error(f"Error generating schema: {e}")
            return {}
    
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
            
        if not results.get("schema_markup"):
             recommendations.append("Schema markup generation failed.")
        
        return recommendations
