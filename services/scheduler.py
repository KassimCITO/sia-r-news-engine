import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime

logger = logging.getLogger(__name__)

class SchedulerService:
    _scheduler = None
    
    @staticmethod
    def init_scheduler(app=None):
        """Initialize the scheduler"""
        if SchedulerService._scheduler:
            return
            
        SchedulerService._scheduler = BackgroundScheduler()
        
        # Add jobs
        
        # 1. Update trends every 3 hours
        SchedulerService._scheduler.add_job(
            func=SchedulerService.update_trends,
            trigger=IntervalTrigger(hours=3),
            id='update_trends',
            name='Update Trends',
            replace_existing=True
        )
        
        # 2. Generate articles every 10 minutes
        SchedulerService._scheduler.add_job(
            func=SchedulerService.generate_articles_job,
            trigger=IntervalTrigger(minutes=10),
            id='generate_articles',
            name='Generate Articles',
            replace_existing=True
        )
        
        # 3. Daily maintenance
        SchedulerService._scheduler.add_job(
            func=SchedulerService.daily_maintenance,
            trigger=IntervalTrigger(days=1),
            id='daily_maintenance',
            name='Daily Maintenance',
            replace_existing=True
        )
        
        SchedulerService._scheduler.start()
        logger.info("Scheduler started")
        
        # Do an initial run of trends update if needed
        # SchedulerService.update_trends()

    @staticmethod
    def update_trends():
        """Update trends from all sources"""
        try:
            from services.trend_harvester import TrendHarvester
            from storage.database import get_db_session
            from storage.models import Settings
            
            logger.info("Starting scheduled trend update...")
            
            # Get keywords from settings
            session = get_db_session()
            settings = session.query(Settings).first()
            keywords = settings.trend_keywords if settings else ""
            session.close()
            
            # Force refresh
            TrendHarvester.fetch_all_trends(force=True, keywords=keywords)
            logger.info("Scheduled trend update completed")
            
        except Exception as e:
            logger.error(f"Error in trend update job: {e}")

    @staticmethod
    def generate_articles_job():
        """Generate articles based on trends"""
        try:
            from services.trend_harvester import TrendHarvester
            from services.article_generator import ArticleGenerator
            from storage.database import get_db_session
            from storage.models import Settings, PipelineLog
            
            logger.info("Starting scheduled article generation...")
            
            # 1. Get Settings
            session = get_db_session()
            settings = session.query(Settings).first()
            if not settings:
                logger.warning("No settings found, skipping generation.")
                session.close()
                return
                
            keywords = settings.trend_keywords
            auto_publish = settings.auto_publish_enabled
            session.close()
            
            # 2. Get Trends
            trends = TrendHarvester.fetch_all_trends(limit=5, keywords=keywords)
            flat_trends = TrendHarvester.flatten_trends(trends, limit=5)
            
            if not flat_trends:
                logger.info("No trends found.")
                return

            # 3. Pick top trend not recently processed
            # (Simple logic: just pick top 1 for now, in real app check duplicates)
            top_trend = flat_trends[0]
            
            # 4. Generate Article
            generator = ArticleGenerator()
            result = generator.generate_from_trend(top_trend, auto_publish=auto_publish)
            
            if result.get('status') == 'success':
                logger.info(f"Article generated successfully: {top_trend.get('title')}")
            else:
                logger.warning(f"Article generation failed or blocked: {result}")
            
            logger.info("Scheduled article generation completed")
            
        except Exception as e:
            logger.error(f"Error in article generation job: {e}")

    @staticmethod
    def daily_maintenance():
        """Cleanup logs etc"""
        try:
            logger.info("Running daily maintenance...")
            # Cleanup old logs, etc.
            pass
        except Exception as e:
            logger.error(f"Error in maintenance job: {e}")

    @staticmethod
    def shutdown():
        """Shutdown scheduler"""
        if SchedulerService._scheduler:
            SchedulerService._scheduler.shutdown()
