from pytrends.request import TrendReq
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TrendsService:
    """Service to fetch trends from Google Trends using pytrends.

    This is a simple wrapper. It returns a list of trend dicts with fields
    compatible with the frontend expectations. On error it raises an exception
    so callers can fallback to mock data.
    """

    @staticmethod
    def fetch_google_trends(limit=10, geo='global'):
        """Fetch latest trending searches (regional/global) and return structured data.

        Args:
            limit (int): maximum number of trends to return
            geo (str): geographical region code or 'global'
        Returns:
            list[dict]
        """
        try:
            pytrends = TrendReq(hl='es-ES', tz=0)

            # pytrends trending_searches supports 'paises' via 'pn' param (e.g., 'global', 'spain')
            pn = 'global' if geo == 'global' else geo
            df = pytrends.trending_searches(pn=pn)

            trends = []
            now = datetime.utcnow().isoformat() + 'Z'

            # df is a DataFrame with single column containing search terms
            for idx, row in enumerate(df[0].tolist()[:limit]):
                trends.append({
                    'id': idx + 1,
                    'title': row,
                    'source': 'Google Trends',
                    'category': 'General',
                    'score': max(50, 100 - idx * int(100/limit)),
                    'summary': f'Búsqueda en tendencia: {row}',
                    'timestamp': now
                })

            return trends
        except Exception as e:
            logger.error(f"Error fetching google trends: {e}")
            raise
