from flask import Blueprint, jsonify, request
from services.wp_client import WordPressClient
from services.wp_taxonomy_manager import WordPressTaxonomyManager
from services.taxonomy_autolearn import TaxonomyAutolearn
from services.metrics_collector import MetricsCollector
import logging

logger = logging.getLogger(__name__)

wp_bp = Blueprint('wp', __name__, url_prefix='/api/wp')

# Initialize services
wp_client = WordPressClient()
wp_taxonomy_mgr = WordPressTaxonomyManager()
autolearn = TaxonomyAutolearn()

@wp_bp.route('/post', methods=['POST'])
def create_post():
    """
    Create a WordPress post
    
    Expected JSON:
    {
        "title": "Post Title",
        "content": "Post content...",
        "categories": ["Category1", "Category2"],
        "tags": ["tag1", "tag2"],
        "status": "draft"
    }
    """
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": "Missing title or content"}), 400
    
    try:
        title = data.get('title')
        content = data.get('content')
        categories = data.get('categories', [])
        tags = data.get('tags', [])
        status = data.get('status', 'draft')
        
        # Ensure categories exist in WP
        category_ids = []
        for cat in categories:
            cat_id = wp_taxonomy_mgr.ensure_category(cat)
            if cat_id:
                category_ids.append(cat_id)
                MetricsCollector.record_category_usage(cat)
        
        # Ensure tags exist in WP
        tag_ids = []
        for tag in tags:
            tag_id = wp_taxonomy_mgr.ensure_tag(tag)
            if tag_id:
                tag_ids.append(tag_id)
        
        # Create post
        post_id = wp_client.create_post(
            title=title,
            content=content,
            categories=category_ids,
            tags=tag_ids,
            status=status
        )
        
        if not post_id:
            return jsonify({"error": "Failed to create post"}), 500
        
        return jsonify({
            "status": "success",
            "post_id": post_id,
            "message": f"Post created successfully"
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        return jsonify({"error": str(e)}), 500

@wp_bp.route('/taxonomies', methods=['GET'])
def get_taxonomies():
    """
    Get all categories and tags from WordPress
    """
    try:
        categories = wp_taxonomy_mgr.get_all_categories()
        tags = wp_taxonomy_mgr.get_all_tags()
        
        return jsonify({
            "status": "success",
            "categories": [{"id": cat.get("id"), "name": cat.get("name")} for cat in categories],
            "tags": [{"id": tag.get("id"), "name": tag.get("name")} for tag in tags]
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting taxonomies: {e}")
        return jsonify({"error": str(e)}), 500

@wp_bp.route('/rebuild-taxonomy-profiles', methods=['POST'])
def rebuild_profiles():
    """
    Rebuild taxonomy auto-learn profiles
    """
    try:
        # Discover synonyms
        synonyms = autolearn.discover_synonyms()
        
        # Try to merge similar categories
        merges = autolearn.merge_similar_categories()
        
        # Get profile summary
        summary = autolearn.get_profile_summary()
        
        return jsonify({
            "status": "success",
            "message": "Taxonomy profiles rebuilt",
            "synonyms_discovered": len(synonyms),
            "categories_merged": len(merges),
            "summary": summary
        }), 200
        
    except Exception as e:
        logger.error(f"Error rebuilding profiles: {e}")
        return jsonify({"error": str(e)}), 500

@wp_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get WordPress publishing statistics
    """
    try:
        pipeline_stats = MetricsCollector.get_pipeline_stats(days=30)
        top_categories = MetricsCollector.get_category_performance(limit=10)
        
        return jsonify({
            "status": "success",
            "pipeline_stats": pipeline_stats,
            "top_categories": top_categories
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({"error": str(e)}), 500

@wp_bp.route('/update-post/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update a WordPress post
    
    Expected JSON:
    {
        "title": "New Title",
        "content": "New content",
        "status": "publish"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        success = wp_client.update_post(
            post_id=post_id,
            title=data.get('title'),
            content=data.get('content'),
            status=data.get('status')
        )
        
        if success:
            return jsonify({
                "status": "success",
                "message": f"Post {post_id} updated successfully"
            }), 200
        else:
            return jsonify({"error": "Failed to update post"}), 500
            
    except Exception as e:
        logger.error(f"Error updating post: {e}")
        return jsonify({"error": str(e)}), 500
