import json
import os
import logging

logger = logging.getLogger(__name__)

class SettingsManager:
    """Gestiona configuración de auto-publicación y roles"""
    
    SETTINGS_FILE = "app_settings.json"
    
    DEFAULT_SETTINGS = {
        "auto_publish": {
            "enabled": False,
            "min_quality_score": 0.75,
            "max_risk_score": 0.4,
            "allowed_categories": [],
            "require_editor_for_sensitive": True
        },
        "roles": {
            "editor": {
                "can_review": True,
                "can_approve": True,
                "can_reject": True,
                "can_edit_settings": False
            },
            "admin": {
                "can_review": True,
                "can_approve": True,
                "can_reject": True,
                "can_edit_settings": True
            }
        },
        "notification": {
            "email_on_publish": True,
            "email_on_error": True,
            "slack_webhook": ""
        }
    }
    
    @classmethod
    def get_settings(cls):
        """Get all settings"""
        if os.path.exists(cls.SETTINGS_FILE):
            try:
                with open(cls.SETTINGS_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading settings: {e}")
        
        return cls.DEFAULT_SETTINGS
    
    @classmethod
    def get_auto_publish_config(cls):
        """Get auto-publish configuration"""
        settings = cls.get_settings()
        return settings.get("auto_publish", cls.DEFAULT_SETTINGS["auto_publish"])
    
    @classmethod
    def update_settings(cls, new_settings):
        """Update settings"""
        try:
            with open(cls.SETTINGS_FILE, 'w') as f:
                json.dump(new_settings, f, indent=2)
            logger.info("Settings updated")
            return True
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False
    
    @classmethod
    def should_auto_publish(cls, quality_score, risk_score, category=None):
        """Determine if article should auto-publish"""
        config = cls.get_auto_publish_config()
        
        if not config.get("enabled"):
            return False
        
        # Check quality and risk thresholds
        if quality_score < config.get("min_quality_score", 0.75):
            return False
        
        if risk_score > config.get("max_risk_score", 0.4):
            return False
        
        # Check category whitelist
        allowed = config.get("allowed_categories", [])
        if allowed and category not in allowed:
            return False
        
        return True
    
    @classmethod
    def get_user_role(cls, user_id):
        """Get user role (simplified - in production use DB)"""
        # This is simplified - in real system, store in DB
        # For now, return 'editor' by default
        return "editor"
    
    @classmethod
    def can_user_action(cls, user_id, action):
        """Check if user can perform action"""
        role = cls.get_user_role(user_id)
        settings = cls.get_settings()
        
        role_perms = settings.get("roles", {}).get(role, {})
        return role_perms.get(action, False)
