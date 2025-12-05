import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class FactChecker:
    """Verifica hechos usando heurísticas básicas y detección de inconsistencias"""
    
    def __init__(self):
        self.common_red_flags = [
            r'always\s+\w+',
            r'never\s+\w+',
            r'everyone\s+knows',
            r'obviously',
            r'clearly',
            r'definitely',
        ]
        self.date_pattern = r'\b(?:\d{1,2}[/-]?\d{1,2}[/-]?\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})\b'
    
    def check(self, text):
        """
        Check text for factual red flags and inconsistencies
        
        Args:
            text: Input text to check
        
        Returns:
            Dict with risk indicators and warnings
        """
        logger.info("Starting fact-checking process")
        
        results = {
            "red_flags": self._detect_red_flags(text),
            "date_consistency": self._check_dates(text),
            "numerical_consistency": self._check_numbers(text),
            "citation_count": self._count_citations(text),
            "risk_score": 0.0,
            "warnings": []
        }
        
        # Calculate risk score
        results["risk_score"] = self._calculate_risk(results)
        
        logger.info(f"Fact-checking completed. Risk score: {results['risk_score']}")
        return results
    
    def _detect_red_flags(self, text):
        """Detect language patterns that indicate unreliable claims"""
        flags = []
        
        for pattern in self.common_red_flags:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                flags.append({
                    "type": "absolute_claim",
                    "text": match.group(),
                    "position": match.start()
                })
        
        # Check for excessive exclamation marks
        exc_count = text.count('!')
        if exc_count > 5:
            flags.append({
                "type": "excessive_punctuation",
                "count": exc_count
            })
        
        # Check for ALL CAPS sentences
        all_caps_sentences = re.findall(r'\b[A-Z]{3,}\b', text)
        if len(all_caps_sentences) > 3:
            flags.append({
                "type": "excessive_caps",
                "count": len(all_caps_sentences)
            })
        
        return flags
    
    def _check_dates(self, text):
        """Check for date inconsistencies"""
        dates = re.findall(self.date_pattern, text)
        
        consistency = {
            "dates_found": dates,
            "is_future_date": False,
            "warnings": []
        }
        
        # Check if any date is in the future
        for date_str in dates:
            # Simple check for 4-digit years
            year_match = re.search(r'\d{4}', date_str)
            if year_match:
                year = int(year_match.group())
                if year > datetime.now().year + 1:
                    consistency["is_future_date"] = True
                    consistency["warnings"].append(f"Future date detected: {date_str}")
        
        return consistency
    
    def _check_numbers(self, text):
        """Check for numerical consistency"""
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        
        consistency = {
            "numbers_found": len(numbers),
            "large_numbers": [],
            "repeated_numbers": []
        }
        
        # Find large numbers (possible data quality issues)
        for num_str in numbers:
            num = float(num_str)
            if num > 1000000:
                consistency["large_numbers"].append(num)
        
        # Find repeated numbers
        from collections import Counter
        num_counts = Counter(numbers)
        for num, count in num_counts.items():
            if count > 2:
                consistency["repeated_numbers"].append({"number": num, "count": count})
        
        return consistency
    
    def _count_citations(self, text):
        """Count citation markers"""
        citations = len(re.findall(r'\[[\w\s]+\]', text))
        return citations
    
    def _calculate_risk(self, results):
        """Calculate overall risk score (0-1)"""
        risk = 0.0
        
        # Red flags increase risk
        risk += len(results["red_flags"]) * 0.15
        
        # Future dates increase risk significantly
        if results["date_consistency"]["is_future_date"]:
            risk += 0.3
        
        # Lack of citations increases risk
        if results["citation_count"] == 0:
            risk += 0.2
        
        # Cap at 1.0
        return min(risk, 1.0)
