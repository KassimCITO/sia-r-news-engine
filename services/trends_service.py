from pytrends.request import TrendReq
from datetime import datetime
import logging
import time

logger = logging.getLogger(__name__)


class TrendsService:
    """Service to fetch trends from Google Trends using pytrends.

    This wrapper adds a small retry/backoff loop to tolerate transient
    network or Google-side errors. If all retries fail, it raises the
    last exception so callers can fallback to mock data.
    """

    @staticmethod
    def fetch_google_trends(limit=10, geo='global', retries=3, backoff=1.0):
        """Fetch latest trending searches (regional/global) with retries.

        Args:
            limit (int): maximum number of trends to return
            geo (str): geographical region code or 'global'
            retries (int): number of attempts
            backoff (float): initial backoff in seconds (exponential)
        Returns:
            list[dict]
        """
        last_exc = None
        for attempt in range(1, retries + 1):
            try:
                pytrends = TrendReq(hl='es-ES', tz=0)

                pn = 'global' if geo == 'global' else geo
                df = pytrends.trending_searches(pn=pn)

                trends = []
                now = datetime.utcnow().isoformat() + 'Z'

                for idx, row in enumerate(df[0].tolist()[:limit]):
                    trends.append({
                        'id': idx + 1,
                        'title': row,
                        'source': 'Google Trends',
                        'category': 'General',
                        'score': max(50, 100 - idx * int(100 / max(1, limit))),
                        'summary': f'Búsqueda en tendencia: {row}',
                        'timestamp': now
                    })

                return trends
            except Exception as e:
                last_exc = e
                logger.warning(f"Attempt {attempt}/{retries} failed fetching google trends: {e}")
                if attempt < retries:
                    sleep_time = backoff * (2 ** (attempt - 1))
                    time.sleep(sleep_time)
                else:
                    logger.error(f"Error fetching google trends after {retries} attempts: {e}")
        # If we reach here, all attempts failed
        raise last_exc
