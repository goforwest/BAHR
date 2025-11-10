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


# The 8 basic tafa'il
BASIC_TAFAIL = {
    "/o//o": "فعولن",      # fa'uulun
    "//o/o": "مفاعيلن",    # mafaa'iilun
    "///o": "مفاعلتن",     # mafaa'alatun
    "/o/o//o": "مستفعلن",  # mustaf'ilun
    "//o//o": "فاعلاتن",   # faa'ilaatun
    "/o/o/o": "فاعلن",     # faa'ilun
    "///": "فعلن",         # fa'lan
    "/o//": "مفعولات",     # maf'uulaatu
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

    while i < len(pattern):
        matched = False

        # Try to match longest pattern first (greedy)
        for length in range(min(8, len(pattern) - i), 0, -1):
            substring = pattern[i:i+length]

            if substring in BASIC_TAFAIL:
                tafail.append(BASIC_TAFAIL[substring])
                i += length
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
