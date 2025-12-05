import re
import logging
from services.llm_client import LLMClient

logger = logging.getLogger(__name__)

class Humanizer:
    """Humaniza el texto para evitar estilo robótico"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def humanize(self, text):
        """
        Make text more human-like and less robotic
        
        Args:
            text: Input text to humanize
        
        Returns:
            Humanized text
        """
        logger.info("Starting humanization process")
        
        # Apply local transformations first
        text = self._apply_local_humanization(text)
        
        # Use LLM for advanced humanization
        text = self._llm_humanize(text)
        
        logger.info("Humanization completed")
        return text
    
    def _apply_local_humanization(self, text):
        """Apply local humanization rules"""
        
        # Replace passive voice with active where possible
        replacements = {
            r'is\s+being\s+(\w+)': r'is \1',
            r'has\s+been\s+(\w+)': r'has \1',
            r'was\s+(\w+)ed\s+by': 'to'
        }
        
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Add contractions (common in human writing)
        contractions = {
            r'\bis\s+not\b': "isn't",
            r'\bwill\s+not\b': "won't",
            r'\bcannot\b': "can't",
            r'\bwould\s+not\b': "wouldn't",
        }
        
        for pattern, contraction in contractions.items():
            text = re.sub(pattern, contraction, text, flags=re.IGNORECASE)
        
        # Remove repetitive word structures
        text = self._reduce_word_repetition(text)
        
        return text
    
    def _reduce_word_repetition(self, text):
        """Reduce repetitive word usage"""
        words_to_vary = {
            'important': ['crucial', 'significant', 'vital', 'key'],
            'said': ['mentioned', 'noted', 'stated', 'explained'],
            'very': ['quite', 'really', 'extremely'],
        }
        
        # This is a simple approach - could be enhanced
        for word, alternatives in words_to_vary.items():
            pattern = r'\b' + word + r'\b'
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            
            if matches > 2:
                # Replace every other occurrence
                count = 0
                def replacer(match):
                    nonlocal count
                    count += 1
                    if count % 2 == 0 and alternatives:
                        import random
                        return random.choice(alternatives)
                    return match.group()
                
                text = re.sub(pattern, replacer, text, flags=re.IGNORECASE)
        
        return text
    
    def _llm_humanize(self, text):
        """Use LLM to improve text humanization"""
        system_prompt = """You are an expert writer. Rewrite the given text to be more natural and human-like.
        Focus on:
        - Using conversational tone
        - Varying sentence structure
        - Adding natural transitions
        - Removing robotic phrases
        - Maintaining journalistic professionalism
        
        Keep the same information, just make it sound more natural."""
        
        user_prompt = f"""Make this text more human and natural while maintaining journalistic quality:

{text[:1500]}

Provide only the rewritten text, no explanations."""
        
        try:
            humanized = self.llm.generate(user_prompt, system_prompt)
            return humanized if humanized else text
        except Exception as e:
            logger.error(f"Error in LLM humanization: {e}")
            return text
