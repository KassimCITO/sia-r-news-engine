from datetime import datetime
from storage.database import SessionLocal
from storage.models import PipelineLog
import logging

logger = logging.getLogger(__name__)

class ReviewManager:
    """Gestiona revisiones de artículos antes de publicar"""
    
    @staticmethod
    def get_pending_reviews(limit=20):
        """Get articles pending review"""
        db = SessionLocal()
        try:
            logs = db.query(PipelineLog).filter(
                PipelineLog.status == "pending"
            ).order_by(
                PipelineLog.created_at.desc()
            ).limit(limit).all()
            
            return [ReviewManager._format_log(log) for log in logs]
        finally:
            db.close()
    
    @staticmethod
    def get_review_by_id(log_id):
        """Get specific review"""
        db = SessionLocal()
        try:
            log = db.query(PipelineLog).filter(
                PipelineLog.id == log_id
            ).first()
            
            if log:
                return ReviewManager._format_log(log)
            return None
        finally:
            db.close()
    
    @staticmethod
    def approve_review(log_id, editor_id):
        """Approve article for publication"""
        db = SessionLocal()
        try:
            log = db.query(PipelineLog).filter(
                PipelineLog.id == log_id
            ).first()
            
            if log:
                log.status = "approved"
                log.editor_id = editor_id
                db.commit()
                logger.info(f"Review {log_id} approved by editor {editor_id}")
                return True
            return False
        finally:
            db.close()
    
    @staticmethod
    def reject_review(log_id, editor_id, reason=""):
        """Reject article"""
        db = SessionLocal()
        try:
            log = db.query(PipelineLog).filter(
                PipelineLog.id == log_id
            ).first()
            
            if log:
                log.status = "rejected"
                log.editor_id = editor_id
                log.rejection_reason = reason
                db.commit()
                logger.info(f"Review {log_id} rejected by editor {editor_id}")
                return True
            return False
        finally:
            db.close()
    
    @staticmethod
    def get_published_articles(limit=50):
        """Get published articles"""
        db = SessionLocal()
        try:
            logs = db.query(PipelineLog).filter(
                PipelineLog.status == "published",
                PipelineLog.wp_post_id.isnot(None)
            ).order_by(
                PipelineLog.created_at.desc()
            ).limit(limit).all()
            
            return [ReviewManager._format_log(log) for log in logs]
        finally:
            db.close()
    
    @staticmethod
    def _format_log(log):
        """Format log for API response"""
        return {
            "id": log.id,
            "user_id": log.user_id,
            "status": log.status,
            "quality_score": log.output_json.get("quality_score", 0) if log.output_json else 0,
            "created_at": log.created_at.isoformat() if log.created_at else None,
            "wp_post_id": log.wp_post_id,
            "execution_time": log.execution_time,
            "preview_text": log.input_text[:100] if log.input_text else ""
        }
