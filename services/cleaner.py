import re
import unicodedata
from bs4 import BeautifulSoup
from unidecode import unidecode
import logging

logger = logging.getLogger(__name__)

class TextCleaner:
    """Servicio de limpieza de texto"""
    
    @staticmethod
    def clean_html(html_text):
        """Remove HTML tags but preserve text structure"""
        soup = BeautifulSoup(html_text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        return text
    
    @staticmethod
    def normalize_unicode(text):
        """Normalize Unicode characters"""
        # Decompose accented characters
        text = unicodedata.normalize('NFKD', text)
        # Filter out combining marks if needed, but keep accents
        return ''.join(c for c in text if not unicodedata.combining(c))
    
    @staticmethod
    def remove_extra_whitespace(text):
        """Remove extra spaces and normalize whitespace"""
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        # Remove spaces before punctuation
        text = re.sub(r' ([,.;:!?])', r'\1', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text
    
    @staticmethod
    def remove_duplicates(text):
        """Remove duplicate sentences and paragraphs"""
        lines = text.split('\n')
        seen = set()
        unique_lines = []
        
        for line in lines:
            line_clean = line.strip()
            if line_clean and line_clean not in seen:
                seen.add(line_clean)
                unique_lines.append(line)
        
        return '\n'.join(unique_lines)
    
    @staticmethod
    def fix_style(text):
        """Apply basic style corrections"""
        # Fix double negatives
        text = re.sub(r'\bno\s+es\s+no\b', 'es', text, flags=re.IGNORECASE)
        
        # Fix common typos
        corrections = {
            r'\bteh\b': 'the',
            r'\brecieve\b': 'receive',
            r'\bdefinately\b': 'definitely',
        }
        
        for pattern, replacement in corrections.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Fix sentence case after periods
        text = re.sub(r'(?<=[.!?])\s+([a-z])', lambda m: ' ' + m.group(1).upper(), text)
        
        return text
    
    @staticmethod
    def remove_noise(text):
        """Remove common noise patterns"""
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        # Remove excessive punctuation
        text = re.sub(r'[!?]{2,}', '!', text)
        # Remove numbers at start of lines (list markers)
        text = re.sub(r'^\d+\.?\s*', '', text, flags=re.MULTILINE)
        return text
    
    def clean(self, text, remove_html=True, normalize=True, 
              remove_duplicates=True, fix_style=True, remove_noise=True):
        """
        Comprehensive text cleaning pipeline
        
        Args:
            text: Input text
            remove_html: Remove HTML tags
            normalize: Normalize Unicode
            remove_duplicates: Remove duplicate sentences
            fix_style: Apply style corrections
            remove_noise: Remove noise patterns
        
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        logger.info("Starting text cleaning pipeline")
        
        if remove_html:
            text = self.clean_html(text)
        
        if remove_noise:
            text = self.remove_noise(text)
        
        if normalize:
            text = self.normalize_unicode(text)
        
        text = self.remove_extra_whitespace(text)
        
        if remove_duplicates:
            text = self.remove_duplicates(text)
        
        if fix_style:
            text = self.fix_style(text)
        
        logger.info("Text cleaning completed")
        return text
