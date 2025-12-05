import json
import os
import logging
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)

class TaxonomyAutolearn:
    """Taxonomía completamente adaptativa con aprendizaje automático diario"""
    
    def __init__(self, profile_file="taxonomy_profile.json"):
        self.profile_file = profile_file
        self.profile = self._load_profile()
    
    def _load_profile(self):
        """Load learning profile from file"""
        if os.path.exists(self.profile_file):
            try:
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load profile: {e}")
        
        return self._default_profile()
    
    def _default_profile(self):
        """Return default profile structure"""
        return {
            "last_update": datetime.now().isoformat(),
            "categories": {},
            "tags": {},
            "synonyms": {},
            "associations": {},
            "statistics": {
                "total_articles": 0,
                "total_categories": 0,
                "learning_cycles": 0
            }
        }
    
    def learn_from_article(self, article_categories, article_tags, traffic_score=1.0):
        """
        Learn from a new article
        
        Args:
            article_categories: List of categories used
            article_tags: List of tags used
            traffic_score: Traffic/engagement score (0-1)
        """
        logger.info("Learning from new article")
        
        # Update category statistics
        for cat in article_categories:
            cat_lower = cat.lower()
            if cat_lower not in self.profile["categories"]:
                self.profile["categories"][cat_lower] = {
                    "count": 0,
                    "traffic_total": 0,
                    "last_used": None,
                    "associated_tags": []
                }
            
            self.profile["categories"][cat_lower]["count"] += 1
            self.profile["categories"][cat_lower]["traffic_total"] += traffic_score
            self.profile["categories"][cat_lower]["last_used"] = datetime.now().isoformat()
        
        # Update tag statistics
        for tag in article_tags:
            tag_lower = tag.lower()
            if tag_lower not in self.profile["tags"]:
                self.profile["tags"][tag_lower] = {
                    "count": 0,
                    "traffic_total": 0,
                    "associated_categories": []
                }
            
            self.profile["tags"][tag_lower]["count"] += 1
            self.profile["tags"][tag_lower]["traffic_total"] += traffic_score
        
        # Learn associations
        self._learn_associations(article_categories, article_tags)
        
        # Update counters
        self.profile["statistics"]["total_articles"] += 1
        
        self._save_profile()
        logger.info("Learning completed and profile saved")
    
    def _learn_associations(self, categories, tags):
        """Learn relationships between categories and tags"""
        for cat in categories:
            cat_lower = cat.lower()
            for tag in tags:
                tag_lower = tag.lower()
                
                if cat_lower not in self.profile["associations"]:
                    self.profile["associations"][cat_lower] = defaultdict(float)
                
                # Increase association weight
                self.profile["associations"][cat_lower][tag_lower] += 1.0
    
    def discover_synonyms(self):
        """Discover new synonyms based on co-occurrence patterns"""
        logger.info("Discovering potential synonyms")
        
        synonyms = {}
        categories = self.profile["categories"]
        
        # Look for categories with very similar usage patterns
        cat_list = list(categories.keys())
        
        for i, cat1 in enumerate(cat_list):
            for cat2 in cat_list[i+1:]:
                similarity = self._calculate_pattern_similarity(cat1, cat2)
                
                if similarity > 0.75:  # Synonym threshold
                    if cat1 not in synonyms:
                        synonyms[cat1] = []
                    synonyms[cat1].append({
                        "candidate": cat2,
                        "confidence": similarity
                    })
        
        self.profile["synonyms"] = synonyms
        return synonyms
    
    def _calculate_pattern_similarity(self, cat1, cat2):
        """Calculate similarity between two category usage patterns"""
        data1 = self.profile["categories"][cat1]
        data2 = self.profile["categories"][cat2]
        
        # Normalize traffic scores
        traffic1 = data1["traffic_total"] / max(data1["count"], 1)
        traffic2 = data2["traffic_total"] / max(data2["count"], 1)
        
        # Compare patterns
        if traffic1 == 0 and traffic2 == 0:
            return 0.0
        
        max_traffic = max(traffic1, traffic2)
        min_traffic = min(traffic1, traffic2)
        
        similarity = min_traffic / max(max_traffic, 0.001)
        return similarity
    
    def get_recommendations(self, text_context, category=None):
        """
        Get recommended categories and tags based on learning
        
        Args:
            text_context: Text context for matching
            category: Current category context
        
        Returns:
            List of recommendations with confidence scores
        """
        recommendations = []
        
        if category:
            cat_lower = category.lower()
            if cat_lower in self.profile["associations"]:
                # Get associated tags
                associations = self.profile["associations"][cat_lower]
                for tag, score in associations.items():
                    recommendations.append({
                        "type": "tag",
                        "value": tag,
                        "confidence": min(1.0, score / 10.0)  # Normalize
                    })
        
        return sorted(recommendations, key=lambda x: x["confidence"], reverse=True)
    
    def merge_similar_categories(self):
        """Automatically merge very similar categories"""
        logger.info("Checking for categories to merge")
        
        merges = []
        cat_list = list(self.profile["categories"].keys())
        
        for i, cat1 in enumerate(cat_list):
            for cat2 in cat_list[i+1:]:
                similarity = self._calculate_pattern_similarity(cat1, cat2)
                
                if similarity > 0.85:  # Merge threshold
                    # Merge cat2 into cat1
                    self._merge_categories(cat1, cat2)
                    merges.append({"merged": cat2, "into": cat1})
        
        if merges:
            self.profile["statistics"]["learning_cycles"] += 1
            self._save_profile()
            logger.info(f"Merged {len(merges)} categories")
        
        return merges
    
    def _merge_categories(self, target, source):
        """Merge source category into target"""
        target_data = self.profile["categories"][target]
        source_data = self.profile["categories"][source]
        
        # Combine statistics
        target_data["count"] += source_data["count"]
        target_data["traffic_total"] += source_data["traffic_total"]
        
        # Remove source
        del self.profile["categories"][source]
    
    def _save_profile(self):
        """Save profile to file"""
        self.profile["last_update"] = datetime.now().isoformat()
        
        try:
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(self.profile, f, indent=2, ensure_ascii=False)
            logger.info(f"Profile saved to {self.profile_file}")
        except Exception as e:
            logger.error(f"Error saving profile: {e}")
    
    def get_profile_summary(self):
        """Get summary of learned taxonomy"""
        return {
            "total_categories": len(self.profile["categories"]),
            "total_tags": len(self.profile["tags"]),
            "total_articles_learned": self.profile["statistics"]["total_articles"],
            "learning_cycles": self.profile["statistics"]["learning_cycles"],
            "last_update": self.profile["last_update"]
        }
