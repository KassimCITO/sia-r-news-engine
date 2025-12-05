import os
from dotenv import load_dotenv

load_dotenv()

# === OPENAI CONFIGURATION ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))

# === JWT CONFIGURATION ===
JWT_SECRET = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-change-me")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600"))

# === API KEY CONFIGURATION ===
API_KEY_MASTER = os.getenv("API_KEY_MASTER", "master-api-key-change-me")

# === WORDPRESS CONFIGURATION ===
WP_BASE_URL = os.getenv("WP_BASE_URL", "https://eldiademichoacan.com")
WP_USERNAME = os.getenv("WP_USERNAME", "")
WP_PASSWORD = os.getenv("WP_PASSWORD", "")
WP_API_ENDPOINT = f"{WP_BASE_URL}/wp-json/wp/v2"

# === DATABASE CONFIGURATION ===
DB_URL = os.getenv("DB_URL", "sqlite:///./sia_r.db")
SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False") == "True"

# === PIPELINE CONFIGURATION ===
PIPELINE_CONFIG = {
    "cleaning_enabled": True,
    "tagging_enabled": True,
    "auditing_enabled": True,
    "fact_checking_enabled": True,
    "verification_enabled": True,
    "humanizing_enabled": True,
    "seo_optimization_enabled": True,
    "planning_enabled": True,
    "taxonomy_normalization_enabled": True,
}

# === TAXONOMY AUTO-LEARN CONFIGURATION ===
TAXONOMY_AUTOLEARN_CONFIG = {
    "enabled": True,
    "learning_interval_hours": 24,
    "min_traffic_threshold": 10,
    "synonym_confidence_threshold": 0.75,
    "auto_merge_threshold": 0.85,
    "profile_file": "./taxonomy_profile.json",
}

# === LOGGING CONFIGURATION ===
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# === APPLICATION CONFIGURATION ===
FLASK_ENV = os.getenv("FLASK_ENV", "development")
DEBUG = FLASK_ENV == "development"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# === ADDITIONAL FEATURES ===
ENABLE_PDF_GENERATION = os.getenv("ENABLE_PDF_GENERATION", "True") == "True"
AUTO_PUBLISH_ENABLED = os.getenv("AUTO_PUBLISH_ENABLED", "False") == "True"
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID", "")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
