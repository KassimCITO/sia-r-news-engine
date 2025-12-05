import json
import logging
from datetime import datetime
from storage.database import SessionLocal
from storage.models import PipelineLog, TaxonomyStats

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Recopila métricas del pipeline, éxitos/fallos y tráfico"""
    
    @staticmethod
    def log_pipeline_execution(user_id, input_text, output_json, status, 
                              execution_time, model_used, error_message=None, wp_post_id=None):
        """
        Log pipeline execution
        
        Args:
            user_id: User ID
            input_text: Input text
            output_json: Output JSON
            status: "success", "failed", "processing"
            execution_time: Time in seconds
            model_used: Model name (e.g., "gpt-4")
            error_message: Error message if failed
            wp_post_id: WordPress post ID if published
        
        Returns:
            Log ID
        """
        logger.info(f"Logging pipeline execution for user {user_id}")
        
        db = SessionLocal()
        try:
            log = PipelineLog(
                user_id=user_id,
                input_text=input_text[:1000],  # Store first 1000 chars
                output_json=output_json,
                status=status,
                error_message=error_message,
                execution_time=execution_time,
                model_used=model_used,
                wp_post_id=wp_post_id
            )
            db.add(log)
            db.commit()
            
            log_id = log.id
            logger.info(f"Pipeline log created: {log_id}")
            return log_id
            
        except Exception as e:
            logger.error(f"Error logging pipeline: {e}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def record_category_usage(category_name, traffic_score=1.0, relevance_score=0.5):
        """
        Record category usage and traffic
        
        Args:
            category_name: Category name
            traffic_score: Traffic indicator (0-1 or higher)
            relevance_score: Relevance score (0-1)
        """
        logger.info(f"Recording category usage: {category_name}")
        
        db = SessionLocal()
        try:
            # Find or create category stats
            stat = db.query(TaxonomyStats).filter(
                TaxonomyStats.category_name == category_name
            ).first()
            
            if stat:
                stat.usage_count += 1
                stat.traffic_score += traffic_score
                stat.relevance_score = (stat.relevance_score + relevance_score) / 2
            else:
                stat = TaxonomyStats(
                    category_name=category_name,
                    usage_count=1,
                    traffic_score=traffic_score,
                    relevance_score=relevance_score
                )
                db.add(stat)
            
            db.commit()
            logger.info(f"Category usage recorded: {category_name}")
            
        except Exception as e:
            logger.error(f"Error recording category usage: {e}")
        finally:
            db.close()
    
    @staticmethod
    def get_pipeline_stats(days=30):
        """
        Get pipeline statistics
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Dict with statistics
        """
        from datetime import timedelta
        
        db = SessionLocal()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Get all logs in period
            logs = db.query(PipelineLog).filter(
                PipelineLog.created_at >= cutoff_date
            ).all()
            
            total = len(logs)
            successful = sum(1 for log in logs if log.status == "success")
            failed = sum(1 for log in logs if log.status == "failed")
            avg_time = sum(log.execution_time for log in logs) / max(total, 1)
            
            stats = {
                "total_runs": total,
                "successful": successful,
                "failed": failed,
                "success_rate": successful / max(total, 1),
                "avg_execution_time": round(avg_time, 2),
                "period_days": days
            }
            
            return stats
            
        finally:
            db.close()
    
    @staticmethod
    def get_category_performance(limit=10):
        """
        Get top performing categories
        
        Args:
            limit: Number of top categories
        
        Returns:
            List of categories sorted by traffic score
        """
        db = SessionLocal()
        try:
            categories = db.query(TaxonomyStats).order_by(
                TaxonomyStats.traffic_score.desc()
            ).limit(limit).all()
            
            result = []
            for cat in categories:
                result.append({
                    "name": cat.category_name,
                    "usage_count": cat.usage_count,
                    "traffic_score": cat.traffic_score,
                    "relevance_score": cat.relevance_score
                })
            
            return result
            
        finally:
            db.close()
