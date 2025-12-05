import logging
import os
from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import DEBUG, HOST, PORT, JWT_SECRET, LOG_LEVEL, FLASK_ENV
from storage.database import init_db
from routes.main import main_bp
from routes.auth import auth_bp
from routes.pipeline_routes import pipeline_bp
from routes.wp_routes import wp_bp
from routes.ui_routes import ui_bp

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['ENV'] = FLASK_ENV
app.config['DEBUG'] = DEBUG
app.config['JWT_SECRET_KEY'] = JWT_SECRET
app.config['JSON_SORT_KEYS'] = False

# Initialize JWT
jwt = JWTManager(app)

# Initialize CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Initialize database
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Error initializing database: {e}")

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(pipeline_bp)
app.register_blueprint(wp_bp)
app.register_blueprint(ui_bp)

logger.info(f"Registered blueprints: main, auth, pipeline, wp, ui")

# UI Routes - Serve HTML templates
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/review/view/<review_id>', methods=['GET'])
def review_page(review_id):
    return render_template('review.html')

@app.route('/pipeline/run', methods=['GET'])
def pipeline_page():
    return render_template('pipeline.html')

@app.route('/published', methods=['GET'])
def published_page():
    return render_template('published.html')

@app.route('/settings', methods=['GET'])
def settings_page():
    return render_template('settings.html')

@app.route('/logs', methods=['GET'])
def logs_page():
    return render_template('logs.html')

@app.route('/metrics', methods=['GET'])
def metrics_page():
    return render_template('metrics.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found", "message": "The requested resource was not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return {"error": "Internal server error", "message": "An unexpected error occurred"}, 500

@app.errorhandler(400)
def bad_request(error):
    return {"error": "Bad request", "message": "The request is invalid"}, 400

# Health check endpoint
@app.route('/', methods=['GET'])
def root():
    return {
        "message": "SIA-R News Engine API",
        "version": "1.0.0",
        "status": "online",
        "environment": FLASK_ENV
    }, 200

if __name__ == '__main__':
    logger.info(f"Starting SIA-R News Engine on {HOST}:{PORT}")
    logger.info(f"Environment: {FLASK_ENV}, Debug: {DEBUG}")
    app.run(host=HOST, port=PORT, debug=DEBUG)
