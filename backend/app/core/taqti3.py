"""
Taqti3 (تقطيع) - Prosodic scansion for Arabic poetry.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from app.core.normalization import normalize_arabic_text, has_diacritics
from app.core.phonetics import text_to_phonetic_pattern


@dataclass
class Taf3ila:
    """Represents a taf'ila (prosodic foot)."""
    name: str
    pattern: str  # e.g., "/o//o" for فعولن

    def __str__(self):
        return self.name


# Comprehensive Tafa'il Dictionary with Zihafat (Prosodic Variations)
# Pattern notation: '/' = haraka (short vowel), 'o' = sakin (sukun or long vowel continuation)
# '/o' represents a long vowel (haraka + sakin)
#
# Strategy: Include only patterns >= 4 units to avoid over-matching
# Sorted by length (longest first) for proper greedy matching

BASIC_TAFAIL = {
    # ============ 8-UNIT PATTERNS ============
    "/o/o//o": "مستفعلن",       # mus-taf-'i-lun (Basit, Rajaz) - PRIMARY
    
    # ============ 7-UNIT PATTERNS ============
    "///o//o": "متفاعلن",       # mu-ta-faa-'i-lun (Kamil) *** CRITICAL ***
    "/o//o/o": "فاعلاتن",       # faa-'i-laa-tun (Ramal) - PRIMARY
    "//o///o": "مفاعلتن",       # ma-faa-'a-la-tun (Wafir) - PRIMARY
    "//o/o/o": "مفاعيلن",       # ma-faa-'ii-lun (Tawil) - PRIMARY
    
    # ============ 6-UNIT PATTERNS ============
    "//o/o": "فعولن",           # fa-'uu-lun (Tawil, Mutaqarib) - PRIMARY
    "///o/o": "مفاعلن",         # ma-faa-'i-lun (Wafir خبن variation)
    "/o///o": "فاعلتن",         # faa-'i-la-tun (variation)
    "//o//o": "مفعولن",         # maf-'uu-lun (variation)
    "/o/o//": "مستفعل",         # mus-taf-'il (مستفعلن with حذف)
    
    # ============ 5-UNIT PATTERNS ============
    "/o//o": "فاعلن",           # faa-'i-lun (Ramal ending, Mutaqarib) - IMPORTANT
    "///o": "فعلن",             # fa-'i-lun (common ending)
    "/o/o/o": "مستعلن",         # mus-ta-'i-lun (مستفعلن with طي)
    "//o//": "فعولُ",           # fa-'uu-lu (فعولن without final sukun)
    "/o//": "فاعل",             # faa-'il (فاعلن with حذف)
    "///o/": "متفاعل",          # mu-ta-faa-'il (Kamil without final sukun)
    "//o/o": "مفعول",           # maf-'uul (variation)
    
    # ============ 4-UNIT PATTERNS ============
    "//o": "فعو",               # fa-'u (shortened - for fragments)
    "/o/o": "فعول",             # fa-'uul (variation)
    "///": "فعل",               # fa-'al (short form)
    "/o/": "فاع",               # faa-' (shortened form)
    "//o/": "مفاعيل",          # ma-faa-'iil (truncated)
    "/o//": "فاعلُ",           # faa-'ilu (truncated)
    
    # Additional important variations for each bahr
    # Tawil variations
    "//o/": "فعولُ",            # fa-'uu-lu (no final sukun)
    "//oo": "فعولان",           # Variant
    
    # Kamil variations  
    "///o//": "متفاعلُ",        # mu-ta-faa-'ilu (no final sukun)
    "///o": "متفاع",            # mu-ta-faa-' (truncated)
    
    # Ramal variations
    "/o//o/": "فاعلات",         # faa-'i-laat (no final sukun)
    "/o/": "فاعُ",              # faa-'u (minimal)
    
    # Wafir variations
    "//o///": "مفاعلت",         # ma-faa-'a-lat (no final sukun)
    "///o/": "مفاعل",           # ma-faa-'il (truncated)
}


def pattern_to_tafail(pattern: str) -> List[str]:
    """
    Convert phonetic pattern to list of tafa'il.

    Uses greedy matching (longest match first).

    Args:
        pattern: Phonetic pattern string (e.g., "/o//o/o//o")

    Returns:
        List of taf'ila names

    Example:
        >>> pattern_to_tafail("/o//o/o//o")
        ["فعولن", "مفاعيلن"]  # (simplified)
    """
    tafail = []
    i = 0
    
    # Sort patterns by length (longest first) for greedy matching
    sorted_patterns = sorted(BASIC_TAFAIL.items(), key=lambda x: len(x[0]), reverse=True)

    while i < len(pattern):
        matched = False

        # Try to match longest pattern first (greedy)
        for tafila_pattern, tafila_name in sorted_patterns:
            pattern_len = len(tafila_pattern)
            
            if i + pattern_len <= len(pattern):
                substring = pattern[i:i+pattern_len]
                
                if substring == tafila_pattern:
                    tafail.append(tafila_name)
                    i += pattern_len
                    matched = True
                    break

        if not matched:
            # No match found, skip one character
            i += 1

    return tafail


def perform_taqti3(verse: str, normalize: bool = True) -> str:
    """
    Perform taqti3 (prosodic scansion) on Arabic verse.

    Args:
        verse: Arabic verse text
        normalize: Whether to normalize text first

    Returns:
        Tafa'il pattern string (e.g., "فعولن مفاعيلن فعولن مفاعيلن")

    Raises:
        ValueError: If verse is invalid

    Example:
        >>> perform_taqti3("إذا غامَرتَ في شَرَفٍ مَرومِ")
        "فعولن مفاعيلن فعولن مفاعيلن"
    """
    if not verse or not verse.strip():
        raise ValueError("Verse cannot be empty")

    # Normalize text
    if normalize:
        verse = normalize_arabic_text(verse)

    # Convert to phonetic pattern
    has_tash = has_diacritics(verse)
    pattern = text_to_phonetic_pattern(verse, has_tash)

    # Convert pattern to tafa'il
    tafail = pattern_to_tafail(pattern)

    # Join with spaces
    return " ".join(tafail)
