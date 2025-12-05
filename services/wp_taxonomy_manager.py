import requests
import logging
from config import WP_API_ENDPOINT, WP_USERNAME, WP_PASSWORD
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)

class WordPressTaxonomyManager:
    """Gestiona categorías y tags en WordPress"""
    
    def __init__(self):
        self.base_url = WP_API_ENDPOINT
        self.auth = HTTPBasicAuth(WP_USERNAME, WP_PASSWORD)
        self.session = requests.Session()
        self.session.auth = self.auth
        self._category_cache = {}
        self._tag_cache = {}
    
    def ensure_category(self, category_name):
        """
        Ensure category exists in WordPress, create if needed
        
        Args:
            category_name: Category name
        
        Returns:
            Category ID or None if failed
        """
        logger.info(f"Ensuring category exists: {category_name}")
        
        # Check cache first
        if category_name in self._category_cache:
            return self._category_cache[category_name]
        
        # Try to find existing category
        category_id = self._find_category(category_name)
        if category_id:
            self._category_cache[category_name] = category_id
            return category_id
        
        # Create new category
        category_id = self._create_category(category_name)
        if category_id:
            self._category_cache[category_name] = category_id
        
        return category_id
    
    def ensure_tag(self, tag_name):
        """
        Ensure tag exists in WordPress, create if needed
        
        Args:
            tag_name: Tag name
        
        Returns:
            Tag ID or None if failed
        """
        logger.info(f"Ensuring tag exists: {tag_name}")
        
        # Check cache first
        if tag_name in self._tag_cache:
            return self._tag_cache[tag_name]
        
        # Try to find existing tag
        tag_id = self._find_tag(tag_name)
        if tag_id:
            self._tag_cache[tag_name] = tag_id
            return tag_id
        
        # Create new tag
        tag_id = self._create_tag(tag_name)
        if tag_id:
            self._tag_cache[tag_name] = tag_id
        
        return tag_id
    
    def _find_category(self, category_name):
        """Find category by name"""
        try:
            params = {"search": category_name}
            response = self.session.get(f"{self.base_url}/categories", params=params)
            response.raise_for_status()
            
            categories = response.json()
            if categories:
                # Return first exact match
                for cat in categories:
                    if cat["name"].lower() == category_name.lower():
                        logger.info(f"Category found: {cat['id']}")
                        return cat["id"]
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding category: {e}")
            return None
    
    def _create_category(self, category_name):
        """Create new category"""
        try:
            data = {"name": category_name}
            response = self.session.post(f"{self.base_url}/categories", json=data)
            response.raise_for_status()
            
            cat_data = response.json()
            category_id = cat_data.get("id")
            logger.info(f"Category created: {category_id}")
            return category_id
            
        except Exception as e:
            logger.error(f"Error creating category: {e}")
            return None
    
    def _find_tag(self, tag_name):
        """Find tag by name"""
        try:
            params = {"search": tag_name}
            response = self.session.get(f"{self.base_url}/tags", params=params)
            response.raise_for_status()
            
            tags = response.json()
            if tags:
                # Return first exact match
                for tag in tags:
                    if tag["name"].lower() == tag_name.lower():
                        logger.info(f"Tag found: {tag['id']}")
                        return tag["id"]
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding tag: {e}")
            return None
    
    def _create_tag(self, tag_name):
        """Create new tag"""
        try:
            data = {"name": tag_name}
            response = self.session.post(f"{self.base_url}/tags", json=data)
            response.raise_for_status()
            
            tag_data = response.json()
            tag_id = tag_data.get("id")
            logger.info(f"Tag created: {tag_id}")
            return tag_id
            
        except Exception as e:
            logger.error(f"Error creating tag: {e}")
            return None
    
    def get_all_categories(self):
        """Get all categories from WordPress"""
        try:
            response = self.session.get(f"{self.base_url}/categories?per_page=100")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            return []
    
    def get_all_tags(self):
        """Get all tags from WordPress"""
        try:
            response = self.session.get(f"{self.base_url}/tags?per_page=100")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting tags: {e}")
            return []
