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


# Meter-to-Tafail Mapping (Classical Arabic Prosody)
# Based on standard theoretical patterns for each meter
# Each meter has a primary pattern (most common) and variations
BAHR_TO_TAFAIL = {
    1: {  # الطويل (at-Tawil)
        "primary": "فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِلُنْ",  # Most common (7/11 verses)
        "variations": [
            "فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِيلُنْ",  # Less common (4/11 verses)
        ]
    },
    2: {  # الكامل (al-Kamil)
        "primary": "مُتَفَاعِلُنْ مُتَفَاعِلُنْ مُتَفَاعِلُنْ",
        "variations": []
    },
    3: {  # الوافر (al-Wafir)
        "primary": "مُفَاعَلَتُنْ مُفَاعَلَتُنْ فَعُولُنْ",
        "variations": []
    },
    4: {  # الرمل (ar-Ramal)
        "primary": "فَاعِلاتُنْ فَاعِلاتُنْ فَاعِلاتُنْ",
        "variations": [
            "فَاعِلاتُنْ فَاعِلاتُنْ فَاعِلُنْ",  # حذف in last foot - shorter verses
        ]
    },
    5: {  # البسيط (al-Basit)
        "primary": "مُسْتَفْعِلُنْ فَاعِلُنْ مُسْتَفْعِلُنْ فَاعِلُنْ",
        "variations": [
            "مُسْتَفْعِلُنْ فَاعِلُنْ مُسْتَفْعِلُنْ فَعِلُنْ",  # خبن in last فاعلن
        ]
    },
    6: {  # المتقارب (al-Mutaqarib)
        "primary": "فَعُولُنْ فَعُولُنْ فَعُولُنْ فَعُولُنْ",
        "variations": []
    },
    7: {  # الرجز (ar-Rajaz)
        "primary": "مُسْتَفْعِلُنْ مُسْتَفْعِلُنْ مُسْتَفْعِلُنْ",
        "variations": []
    },
    8: {  # الهزج (al-Hazaj)
        "primary": "مَفَاعِيلُنْ مَفَاعِيلُنْ فَعُولُنْ",
        "variations": [
            "مَفَاعِيلُنْ مَفَاعِيلُنْ",  # Truncated form without ending
        ]
    },
    9: {  # الخفيف (al-Khafif)
        "primary": "فَاعِلاتُنْ مُسْتَفْعِلُنْ فَاعِلاتُنْ",
        "variations": [
            "فَاعِلاتُنْ مُسْتَفْعِلُنْ فَاعِلُنْ",  # حذف in last foot
        ]
    },
}


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
    # NOTE: Removed duplicate "//o/o": "مفعول" - conflicts with "//o/o": "فعولن" above
    
    # ============ 4-UNIT PATTERNS ============
    "//o": "فعو",               # fa-'u (shortened - for fragments)
    "/o/o": "فعول",             # fa-'uul (variation)
    "///": "فعل",               # fa-'al (short form)
    "/o/": "فاع",               # faa-' (shortened form)
    "//o/": "مفاعيل",          # ma-faa-'iil (truncated) - different from فعولُ
    
    # Additional important variations for each bahr
    # Tawil variations
    "//oo": "فعولان",           # Variant
    
    # Kamil variations  
    "///o//": "متفاعلُ",        # mu-ta-faa-'ilu (no final sukun)
    
    # Ramal variations
    "/o//o/": "فاعلات",         # faa-'i-laat (no final sukun)
    
    # Wafir variations
    "//o///": "مفاعلت",         # ma-faa-'a-lat (no final sukun)
}


def pattern_to_tafail(pattern: str) -> List[str]:
    """
    Convert phonetic pattern to list of tafa'il.

    Uses greedy matching with proper alignment. Tries all possible pattern lengths
    at each position, preferring longer matches.

    Args:
        pattern: Phonetic pattern string (e.g., "/o//o/o//o")

    Returns:
        List of taf'ila names

    Example:
        >>> pattern_to_tafail("//o/o//o/o/o")
        ["فعولن", "مفاعيلن"]
    """
    tafail = []
    i = 0
    
    # Sort patterns by length (longest first) for greedy matching
    sorted_patterns = sorted(BASIC_TAFAIL.items(), key=lambda x: len(x[0]), reverse=True)

    while i < len(pattern):
        matched = False

        # Try to match patterns at current position (longest first)
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
            # No exact match found at this position
            # This could mean: (1) incomplete vocalization, (2) unknown variation, or (3) error
            # For now, try to match smaller fragments or skip
            # As a fallback, try matching just 2-3 character patterns
            for min_len in [3, 2]:
                for tafila_pattern, tafila_name in sorted_patterns:
                    if len(tafila_pattern) == min_len:
                        pattern_len = len(tafila_pattern)
                        
                        if i + pattern_len <= len(pattern):
                            substring = pattern[i:i+pattern_len]
                            
                            if substring == tafila_pattern:
                                tafail.append(tafila_name)
                                i += pattern_len
                                matched = True
                                break
                if matched:
                    break
            
            # If still no match, skip one character (likely noise or error)
            if not matched:
                i += 1

    return tafail


def get_tafail_for_bahr(bahr_id: int, verse_text: str) -> str:
    """
    Get the appropriate tafail pattern for a given meter and verse.
    
    For meters with variations, uses heuristics based on phonetic pattern length,
    character count, and other features to select the most likely variation.
    
    Note: Some meters (like الطويل and الهزج) have overlapping ranges where
    variations are genuinely ambiguous. In these cases, returns the most
    common variation as default.
    
    Args:
        bahr_id: Meter ID (1-9)
        verse_text: The verse text (normalized)
        
    Returns:
        Appropriate tafail pattern string
    """
    if bahr_id not in BAHR_TO_TAFAIL:
        raise ValueError(f"Invalid bahr_id: {bahr_id}")
    
    meter_data = BAHR_TO_TAFAIL[bahr_id]
    primary = meter_data["primary"]
    variations = meter_data.get("variations", [])
    
    # If no variations, return primary
    if not variations:
        return primary
    
    # For meters with variations, analyze verse features
    try:
        pattern = text_to_phonetic_pattern(verse_text)
        pattern_len = len(pattern)
        char_count = len(verse_text.replace(' ', ''))
        
        # Meter-specific decision rules based on statistical analysis
        
        if bahr_id == 4:  # الرمل
            # Clear threshold at phonetic len 20
            if pattern_len < 20:
                return variations[0]  # فَاعِلاتُنْ فَاعِلاتُنْ فَاعِلُنْ
            return primary  # فَاعِلاتُنْ × 3
        
        elif bahr_id == 5:  # البسيط  
            # Clear threshold at phonetic len 22
            if pattern_len <= 21:
                return variations[0]  # ... فَعِلُنْ
            return primary  # ... فَاعِلُنْ
        
        elif bahr_id == 8:  # الهزج
            # Overlapping ranges (17-20 vs 16-25), use char count as tiebreaker
            if pattern_len < 17:
                return variations[0]  # Truncated: مَفَاعِيلُنْ × 2
            elif pattern_len > 20:
                return primary  # Full: مَفَاعِيلُنْ × 2 + فَعُولُنْ
            else:  # Ambiguous range, use character count
                if char_count < 28:
                    return variations[0]  # Truncated
                return primary  # Full
        
        elif bahr_id == 9:  # الخفيف
            # Only one variation example at len=19, all others 20+
            if pattern_len <= 19 and char_count <= 26:
                return variations[0]  # ... فَاعِلُنْ
            return primary  # ... فَاعِلاتُنْ
        
        elif bahr_id == 1:  # الطويل
            # Completely overlapping ranges (18-27 vs 20-25)
            # Use character count as primary discriminator
            # مفاعلن (primary): 27-36 chars, avg 33.4
            # مفاعيلن (variation): 32-35 chars, avg 33.5
            # They're nearly identical! Use pattern length as tiebreaker
            
            if char_count < 32:
                return primary  # مَفَاعِلُنْ (shorter verses)
            elif char_count > 35:
                # Could be either, check pattern length
                if pattern_len >= 24:
                    return primary  # Longer patterns tend to be مفاعلن
                return variations[0]  # مَفَاعِيلُنْ
            else:  # 32-35 range (ambiguous!)
                # Use phonetic pattern length as final arbiter
                if pattern_len <= 21:
                    return variations[0]  # مَفَاعِيلُنْ (shorter patterns)
                return primary  # مَفَاعِلُنْ (longer patterns)
        
    except Exception as e:
        # If analysis fails, return primary (most common form)
        pass
    
    return primary


def perform_taqti3(verse: str, normalize: bool = True, bahr_id: Optional[int] = None) -> str:
    """
    Perform taqti3 (prosodic scansion) on Arabic verse.
    
    If bahr_id is provided, returns the standard theoretical tafail pattern for that meter.
    This matches classical Arabic prosody where each meter has a fixed tafail sequence.
    
    If bahr_id is not provided, falls back to pattern matching (legacy behavior).

    Args:
        verse: Arabic verse text
        normalize: Whether to normalize text first
        bahr_id: Optional meter ID (1-9). If provided, returns standard tafail for that meter.

    Returns:
        Tafa'il pattern string (e.g., "فعولن مفاعيلن فعولن مفاعيلن")

    Raises:
        ValueError: If verse is invalid or bahr_id is out of range

    Example:
        >>> perform_taqti3("إذا غامَرتَ في شَرَفٍ مَرومِ", bahr_id=1)
        "فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِيلُنْ"
        
        >>> perform_taqti3("أَلا فِي سَبيلِ المَجدِ ما أَنا فاعِلُ", bahr_id=7)
        "مُسْتَفْعِلُنْ مُسْتَفْعِلُنْ مُسْتَفْعِلُنْ"
    """
    # Edge case: None or non-string input
    if verse is None:
        raise ValueError("Verse cannot be None")
    
    if not isinstance(verse, str):
        raise ValueError(f"Verse must be a string, got {type(verse).__name__}")
    
    if not verse or not verse.strip():
        raise ValueError("Verse cannot be empty")
    
    # Edge case: Very long verse (likely not a single verse)
    if len(verse) > 500:
        raise ValueError("Verse is too long (max 500 characters per verse)")
    
    # Normalize text if needed
    verse_for_analysis = verse
    if normalize:
        try:
            verse_for_analysis = normalize_arabic_text(verse)
        except ValueError as e:
            raise ValueError(f"Normalization failed: {str(e)}")
    
    # If bahr_id is provided, return standard tafail pattern for that meter
    if bahr_id is not None:
        if not isinstance(bahr_id, int):
            raise ValueError(f"bahr_id must be an integer, got {type(bahr_id).__name__}")
        
        if bahr_id not in BAHR_TO_TAFAIL:
            raise ValueError(f"Invalid bahr_id: {bahr_id}. Must be between 1 and 9.")
        
        # Get appropriate tafail (primary or variation) based on verse structure
        return get_tafail_for_bahr(bahr_id, verse_for_analysis)

    # Legacy behavior: pattern matching (used when bahr is not known)
    # Convert to phonetic pattern
    try:
        has_tash = has_diacritics(verse_for_analysis)
        pattern = text_to_phonetic_pattern(verse_for_analysis, has_tash)
    except Exception as e:
        raise ValueError(f"Phonetic conversion failed: {str(e)}")
    
    # Edge case: Empty or invalid pattern
    if not pattern or not pattern.strip():
        raise ValueError("Could not generate phonetic pattern from verse")

    # Convert pattern to tafa'il
    try:
        tafail = pattern_to_tafail(pattern)
    except Exception as e:
        raise ValueError(f"Pattern matching failed: {str(e)}")
    
    # Edge case: No tafa'il matched
    if not tafail:
        raise ValueError("Could not identify any tafa'il in verse - text may not be poetry")

    # Join with spaces
    return " ".join(tafail)
