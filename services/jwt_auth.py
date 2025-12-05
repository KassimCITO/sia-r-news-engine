import jwt
import logging
from datetime import datetime, timedelta
from config import JWT_SECRET, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRES

logger = logging.getLogger(__name__)

class JWTAuth:
    """Gestiona autenticación por JWT"""
    
    @staticmethod
    def create_token(user_id, email, expires_in=None):
        """
        Create JWT token
        
        Args:
            user_id: User ID
            email: User email
            expires_in: Seconds until expiration
        
        Returns:
            JWT token string
        """
        logger.info(f"Creating JWT token for user {user_id}")
        
        if expires_in is None:
            expires_in = JWT_ACCESS_TOKEN_EXPIRES
        
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": datetime.utcnow() + timedelta(seconds=expires_in),
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    
    @staticmethod
    def verify_token(token):
        """
        Verify JWT token
        
        Args:
            token: JWT token string
        
        Returns:
            (user_id, email) tuple, or (None, None) if invalid
        """
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_id = payload.get("user_id")
            email = payload.get("email")
            
            if not user_id or not email:
                logger.warning("Invalid token payload")
                return None, None
            
            logger.info(f"Token verified for user {user_id}")
            return user_id, email
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None, None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None, None
    
    @staticmethod
    def refresh_token(token):
        """
        Refresh JWT token
        
        Args:
            token: Current JWT token
        
        Returns:
            New JWT token or None if invalid
        """
        user_id, email = JWTAuth.verify_token(token)
        
        if not user_id or not email:
            return None
        
        return JWTAuth.create_token(user_id, email)
