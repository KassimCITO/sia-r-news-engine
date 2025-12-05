from flask import Blueprint, jsonify, request
from pipeline.run_pipeline import Pipeline
from pipeline.schema import PipelineRunRequest, PipelineSimulateRequest
import logging

logger = logging.getLogger(__name__)

pipeline_bp = Blueprint('pipeline', __name__, url_prefix='/api/pipeline')

# Initialize pipeline
pipeline = Pipeline()

@pipeline_bp.route('/run', methods=['POST'])
def run():
    """
    Run complete pipeline
    
    Expected JSON:
    {
        "title": "Article Title",
        "content": "Article content...",
        "author": "Author name",
        "auto_publish": false
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        # Validate request
        req = PipelineRunRequest(**data)
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400
    
    # Extract user_id from auth header if available
    user_id = None
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            token = auth_header.split(' ')[1]
            from services.jwt_auth import JWTAuth
            user_id, _ = JWTAuth.verify_token(token)
        except:
            pass
    
    logger.info(f"Running pipeline for user {user_id}")
    
    # Execute pipeline
    result = pipeline.run(
        title=req.title,
        content=req.content,
        user_id=user_id,
        auto_publish=req.auto_publish
    )
    
    status_code = 200 if result.get("status") == "success" else 500
    return jsonify(result), status_code

@pipeline_bp.route('/simulate', methods=['POST'])
def simulate():
    """
    Simulate pipeline without publishing
    
    Expected JSON:
    {
        "title": "Article Title",
        "content": "Article content..."
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        req = PipelineSimulateRequest(**data)
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400
    
    logger.info("Simulating pipeline")
    
    # Run with auto_publish disabled
    result = pipeline.run(
        title=req.title,
        content=req.content,
        auto_publish=False
    )
    
    status_code = 200 if result.get("status") == "success" else 500
    return jsonify(result), status_code

@pipeline_bp.route('/status', methods=['GET'])
def status():
    """Get pipeline status"""
    return jsonify({
        "status": "operational",
        "message": "Pipeline is ready"
    }), 200
