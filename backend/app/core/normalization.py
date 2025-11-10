"""
Normalization utilities for core phonetics module.
"""
import re

# Pattern to detect Arabic diacritics
DIACRITICS_PATTERN = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]")


def has_diacritics(text: str) -> bool:
    """
    Check if text contains Arabic diacritics (tashkeel).
    
    Args:
        text: Arabic text to check
        
    Returns:
        True if text contains diacritics, False otherwise
    """
    return bool(DIACRITICS_PATTERN.search(text))
