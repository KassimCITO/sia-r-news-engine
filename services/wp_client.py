import requests
import logging
from config import WP_BASE_URL, WP_USERNAME, WP_PASSWORD, WP_API_ENDPOINT
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)

class WordPressClient:
    """Cliente para interactuar con WordPress via REST API"""
    
    def __init__(self):
        self.base_url = WP_API_ENDPOINT
        self.auth = HTTPBasicAuth(WP_USERNAME, WP_PASSWORD)
        self.session = requests.Session()
        self.session.auth = self.auth
    
    def create_post(self, title, content, categories=None, tags=None, 
                   featured_image_id=None, status="draft"):
        """
        Create a new WordPress post
        
        Args:
            title: Post title
            content: Post content (HTML)
            categories: List of category IDs
            tags: List of tag IDs
            featured_image_id: Featured image ID
            status: post status (draft, publish, pending)
        
        Returns:
            Post ID or None if failed
        """
        logger.info(f"Creating WordPress post: {title}")
        
        data = {
            "title": title,
            "content": content,
            "status": status,
        }
        
        if categories:
            data["categories"] = categories
        if tags:
            data["tags"] = tags
        if featured_image_id:
            data["featured_media"] = featured_image_id
        
        try:
            response = self.session.post(f"{self.base_url}/posts", json=data)
            response.raise_for_status()
            
            post_data = response.json()
            post_id = post_data.get("id")
            logger.info(f"Post created successfully. ID: {post_id}")
            return post_id
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating post: {e}")
            return None
    
    def update_post(self, post_id, title=None, content=None, 
                   categories=None, tags=None, status=None):
        """
        Update an existing WordPress post
        
        Args:
            post_id: Post ID to update
            title: New title
            content: New content
            categories: New categories
            tags: New tags
            status: New status
        
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Updating WordPress post: {post_id}")
        
        data = {}
        if title:
            data["title"] = title
        if content:
            data["content"] = content
        if categories:
            data["categories"] = categories
        if tags:
            data["tags"] = tags
        if status:
            data["status"] = status
        
        try:
            response = self.session.post(f"{self.base_url}/posts/{post_id}", json=data)
            response.raise_for_status()
            logger.info(f"Post {post_id} updated successfully")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error updating post: {e}")
            return False
    
    def upload_image(self, file_path):
        """
        Upload image to WordPress media library
        
        Args:
            file_path: Path to image file
        
        Returns:
            Media ID or None if failed
        """
        logger.info(f"Uploading image: {file_path}")
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = self.session.post(f"{self.base_url}/media", files=files)
                response.raise_for_status()
            
            media_data = response.json()
            media_id = media_data.get("id")
            logger.info(f"Image uploaded successfully. ID: {media_id}")
            return media_id
            
        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            return None
    
    def set_featured_image(self, post_id, image_id):
        """
        Set featured image for a post
        
        Args:
            post_id: Post ID
            image_id: Media ID of the image
        
        Returns:
            True if successful
        """
        return self.update_post(post_id, featured_image_id=image_id)
    
    def get_post(self, post_id):
        """
        Get post data
        
        Args:
            post_id: Post ID
        
        Returns:
            Post data dict or None
        """
        try:
            response = self.session.get(f"{self.base_url}/posts/{post_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting post: {e}")
            return None
