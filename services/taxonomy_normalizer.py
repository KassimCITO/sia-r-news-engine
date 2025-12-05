import json
import logging
import re
from unidecode import unidecode

logger = logging.getLogger(__name__)

class TaxonomyNormalizer:
    """Taxonomía moderada: correción de acentos, duplicados, sinónimos base"""
    
    def __init__(self):
        # Base synonyms mapping
        self.base_synonyms = {
            "politica": ["política", "politicas", "políticas", "politics"],
            "deporte": ["deportes", "sport", "sports", "athletic"],
            "tecnologia": ["tecnología", "technology", "tech"],
            "economia": ["economía", "economy", "economic"],
            "salud": ["health", "sanidad", "médica"],
            "educacion": ["educación", "education", "escuela"],
            "cultura": ["cultura", "cultural", "arte"],
            "ambiente": ["environment", "ambiental", "ecologia"],
        }
        
        # WordPress category mapping (1:1)
        self.wp_category_map = {}
    
    def normalize(self, categories, tags):
        """
        Normalize categories and tags
        
        Args:
            categories: List of category names
            tags: List of tag names
        
        Returns:
            Dict with normalized categories and tags
        """
        logger.info("Starting taxonomy normalization")
        
        normalized = {
            "categories": self._normalize_list(categories),
            "tags": self._normalize_list(tags),
            "applied_normalizations": []
        }
        
        # Track what was normalized
        for orig, norm in zip(categories, normalized["categories"]):
            if orig != norm:
                normalized["applied_normalizations"].append({
                    "original": orig,
                    "normalized": norm,
                    "type": "category"
                })
        
        logger.info(f"Normalization completed. {len(normalized['applied_normalizations'])} changes made")
        return normalized
    
    def _normalize_list(self, items):
        """Normalize a list of categories/tags"""
        if not items:
            return []
        
        normalized = []
        seen = set()
        
        for item in items:
            # Step 1: Remove accents
            clean = self._remove_accents(item)
            
            # Step 2: Handle duplicates
            if clean.lower() in seen:
                continue
            seen.add(clean.lower())
            
            # Step 3: Apply synonym mapping
            mapped = self._apply_synonym_mapping(clean)
            
            # Step 4: Capitalize properly
            normalized_item = self._capitalize_properly(mapped)
            
            normalized.append(normalized_item)
        
        return normalized
    
    def _remove_accents(self, text):
        """Remove accents and normalize unicode"""
        # Convert to base ASCII
        text = unidecode(text)
        # Clean extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _apply_synonym_mapping(self, text):
        """Apply base synonym mapping"""
        text_lower = text.lower()
        
        for canonical, synonyms in self.base_synonyms.items():
            for synonym in synonyms:
                if synonym.lower() == text_lower:
                    return canonical
        
        return text
    
    def _capitalize_properly(self, text):
        """Capitalize text properly for taxonomy"""
        # Title case for categories
        return text.title()
    
    def map_to_wp_category(self, category_name):
        """
        Map normalized category to WordPress category ID
        
        Args:
            category_name: Normalized category name
        
        Returns:
            WordPress category ID or None if not found
        """
        return self.wp_category_map.get(category_name.lower())
    
    def set_wp_category_mapping(self, mapping_dict):
        """
        Set WordPress category mapping
        
        Args:
            mapping_dict: Dict like {"category_name": wp_id}
        """
        self.wp_category_map = {k.lower(): v for k, v in mapping_dict.items()}
