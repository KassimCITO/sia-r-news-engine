from flask import Blueprint, jsonify, request
from services.jwt_auth import JWTAuth
from services.api_key_auth import APIKeyAuth
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint
    
    Expected JSON:
    {
        "email": "user@example.com",
        "password": "password"
    }
    """
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email or password"}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    # Simple demo authentication (in production use proper user DB)
    if email and password:
        # Extract user_id from email (simplified)
        user_id = hash(email) % 10000
        
        # Create JWT token
        token = JWTAuth.create_token(user_id, email)
        
        # Generate API key
        api_key, _ = APIKeyAuth.generate_key(user_id)
        
        return jsonify({
            "status": "success",
            "user_id": user_id,
            "email": email,
            "access_token": token,
            "api_key": api_key,
            "token_type": "Bearer"
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """
    Refresh JWT token
    
    Expected JSON:
    {
        "access_token": "jwt_token"
    }
    """
    data = request.get_json()
    
    if not data or not data.get('access_token'):
        return jsonify({"error": "Missing access_token"}), 400
    
    old_token = data.get('access_token')
    
    # Verify and refresh token
    new_token = JWTAuth.refresh_token(old_token)
    
    if not new_token:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    return jsonify({
        "status": "success",
        "access_token": new_token,
        "token_type": "Bearer"
    }), 200

@auth_bp.route('/verify', methods=['POST'])
def verify():
    """
    Verify JWT token
    
    Expected JSON:
    {
        "access_token": "jwt_token"
    }
    """
    data = request.get_json()
    
    if not data or not data.get('access_token'):
        return jsonify({"error": "Missing access_token"}), 400
    
    token = data.get('access_token')
    user_id, email = JWTAuth.verify_token(token)
    
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    
    return jsonify({
        "status": "valid",
        "user_id": user_id,
        "email": email
    }), 200
