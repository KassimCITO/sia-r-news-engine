import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from storage.database import SessionLocal
from storage.models import ApiKey

logger = logging.getLogger(__name__)

class APIKeyAuth:
    """Gestiona autenticación por API Key"""
    
    @staticmethod
    def generate_key(user_id, expires_days=90):
        """
        Generate new API key
        
        Args:
            user_id: User ID
            expires_days: Days until key expires
        
        Returns:
            Plain key (for display), key hash (for storage)
        """
        logger.info(f"Generating new API key for user {user_id}")
        
        # Generate random key
        plain_key = secrets.token_urlsafe(32)
        
        # Hash it for storage
        key_hash = hashlib.sha256(plain_key.encode()).hexdigest()
        
        # Extract prefix for identification (first 8 chars)
        key_prefix = plain_key[:8]
        
        # Calculate expiration
        expires_at = datetime.now() + timedelta(days=expires_days)
        
        # Store in database
        db = SessionLocal()
        try:
            api_key = ApiKey(
                user_id=user_id,
                key_hash=key_hash,
                key_prefix=key_prefix,
                expires_at=expires_at,
                is_active=True
            )
            db.add(api_key)
            db.commit()
            logger.info(f"API key created successfully")
        finally:
            db.close()
        
        return plain_key, key_hash
    
    @staticmethod
    def verify_key(plain_key):
        """
        Verify API key is valid
        
        Args:
            plain_key: Plain API key from request
        
        Returns:
            (user_id, valid) tuple, or (None, False) if invalid
        """
        if not plain_key:
            return None, False
        
        # Hash the provided key
        key_hash = hashlib.sha256(plain_key.encode()).hexdigest()
        
        db = SessionLocal()
        try:
            # Look up the key
            api_key = db.query(ApiKey).filter(
                ApiKey.key_hash == key_hash,
                ApiKey.is_active == True
            ).first()
            
            if not api_key:
                logger.warning("Invalid API key")
                return None, False
            
            # Check expiration
            if api_key.expires_at and api_key.expires_at < datetime.now():
                logger.warning("API key expired")
                return None, False
            
            # Update last used
            api_key.last_used = datetime.now()
            db.commit()
            
            logger.info(f"API key verified for user {api_key.user_id}")
            return api_key.user_id, True
            
        finally:
            db.close()
    
    @staticmethod
    def revoke_key(key_prefix):
        """Revoke an API key by prefix"""
        db = SessionLocal()
        try:
            api_key = db.query(ApiKey).filter(
                ApiKey.key_prefix == key_prefix
            ).first()
            
            if api_key:
                api_key.is_active = False
                db.commit()
                logger.info(f"API key {key_prefix} revoked")
                return True
            
            return False
        finally:
            db.close()
