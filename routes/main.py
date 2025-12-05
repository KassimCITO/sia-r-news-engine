from flask import Blueprint, jsonify
from datetime import datetime

main_bp = Blueprint('main', __name__, url_prefix='/api')

# Track start time for uptime calculation
start_time = datetime.now()

@main_bp.route('/status', methods=['GET'])
def status():
    """Get API status"""
    uptime = (datetime.now() - start_time).total_seconds()
    
    return jsonify({
        "status": "online",
        "message": "SIA-R News Engine API is running",
        "version": "1.0.0",
        "uptime_seconds": uptime,
        "timestamp": datetime.now().isoformat()
    }), 200

@main_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "healthy": True,
        "status": "operational"
    }), 200
