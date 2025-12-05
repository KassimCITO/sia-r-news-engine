import re
import logging

logger = logging.getLogger(__name__)

class Verifier:
    """Verifica coherencia final, duplicación y contradicciones"""
    
    def verify(self, text):
        """
        Verify final coherence and detect contradictions
        
        Args:
            text: Input text to verify
        
        Returns:
            Dict with verification results
        """
        logger.info("Starting verification process")
        
        results = {
            "coherence_score": 0.0,
            "contradiction_detected": False,
            "duplicate_ideas": [],
            "logical_issues": [],
            "sentence_flow": {},
            "overall_valid": True
        }
        
        results["coherence_score"] = self._calculate_coherence(text)
        results["duplicate_ideas"] = self._find_duplicate_ideas(text)
        results["contradiction_detected"] = self._detect_contradictions(text)
        results["logical_issues"] = self._find_logical_issues(text)
        results["sentence_flow"] = self._analyze_sentence_flow(text)
        
        # Determine if text is overall valid
        results["overall_valid"] = (
            results["coherence_score"] > 0.6 and
            not results["contradiction_detected"] and
            len(results["logical_issues"]) < 3
        )
        
        logger.info(f"Verification completed. Overall valid: {results['overall_valid']}")
        return results
    
    def _calculate_coherence(self, text):
        """Calculate text coherence score (0-1)"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return 0.5
        
        # Check for transitional phrases
        transitions = [
            'however', 'therefore', 'thus', 'furthermore', 'moreover',
            'in addition', 'on the other hand', 'consequently', 'meanwhile'
        ]
        
        transition_count = 0
        for sentence in sentences:
            for transition in transitions:
                if transition.lower() in sentence.lower():
                    transition_count += 1
                    break
        
        # Score based on transitions
        coherence = min(1.0, transition_count / max(len(sentences) - 1, 1))
        return coherence
    
    def _find_duplicate_ideas(self, text):
        """Find duplicate sentences or similar ideas"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        duplicates = []
        seen = set()
        
        for i, sent in enumerate(sentences):
            # Simple similarity check - normalize and compare
            sent_normalized = re.sub(r'\W+', '', sent).lower()
            
            for seen_sent in seen:
                if self._similarity(sent_normalized, seen_sent) > 0.8:
                    duplicates.append({
                        "original": sentences[i],
                        "duplicate": sent
                    })
            
            seen.add(sent_normalized)
        
        return duplicates
    
    def _detect_contradictions(self, text):
        """Detect logical contradictions"""
        # Look for patterns like "X is true" and "X is false"
        contradiction_patterns = [
            (r'is\s+not\s+(\w+)', r'is\s+\1'),
            (r'impossible', r'possible'),
            (r'never', r'always'),
        ]
        
        for neg_pattern, pos_pattern in contradiction_patterns:
            neg_matches = re.findall(neg_pattern, text)
            pos_matches = re.findall(pos_pattern, text)
            
            if neg_matches and pos_matches:
                return True
        
        return False
    
    def _find_logical_issues(self, text):
        """Find logical inconsistencies"""
        issues = []
        
        # Check for effect before cause
        if text.find('therefore') < text.find('because'):
            issues.append("Effect mentioned before cause")
        
        # Check for temporal inconsistencies
        past_tense = len(re.findall(r'was|were|had', text, re.IGNORECASE))
        present_tense = len(re.findall(r'is|are|has', text, re.IGNORECASE))
        future_tense = len(re.findall(r'will|shall|going', text, re.IGNORECASE))
        
        tense_shifts = sum([past_tense > 0, present_tense > 0, future_tense > 0])
        if tense_shifts > 2:
            issues.append("Multiple tense shifts detected")
        
        return issues
    
    def _analyze_sentence_flow(self, text):
        """Analyze sentence flow and readability"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        flow = {
            "total_sentences": len(sentences),
            "avg_length": sum(len(s.split()) for s in sentences) / max(len(sentences), 1),
            "too_short": sum(1 for s in sentences if len(s.split()) < 3),
            "too_long": sum(1 for s in sentences if len(s.split()) > 30),
        }
        
        return flow
    
    def _similarity(self, s1, s2):
        """Calculate similarity between two strings (0-1)"""
        if not s1 or not s2:
            return 0.0
        
        # Simple Jaccard similarity
        set1 = set(s1)
        set2 = set(s2)
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
