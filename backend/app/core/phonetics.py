"""
Arabic phonetic analysis for prosody.
"""

from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Phoneme:
    """Represents a phonetic unit."""
    consonant: str
    vowel: str  # 'a', 'u', 'i', 'aa', 'uu', 'ii', '' (sukun)
    has_shadda: bool = False

    def __str__(self):
        shadda_mark = "ّ" if self.has_shadda else ""
        return f"{self.consonant}{shadda_mark}{self.vowel}"

    def is_long_vowel(self) -> bool:
        """Check if phoneme has long vowel (madd)."""
        return self.vowel in ['aa', 'uu', 'ii']

    def is_sukun(self) -> bool:
        """Check if phoneme has sukun (no vowel)."""
        return self.vowel == ''


def extract_phonemes(text: str, has_tashkeel: bool = False) -> List[Phoneme]:
    """
    Extract phonemes from Arabic text.

    Args:
        text: Arabic text (normalized)
        has_tashkeel: Whether text has diacritics

    Returns:
        List of Phoneme objects

    Example:
        >>> extract_phonemes("كَتَبَ", has_tashkeel=True)
        [Phoneme('ك', 'a'), Phoneme('ت', 'a'), Phoneme('ب', 'a')]
    """
    phonemes = []

    # Diacritic mappings
    VOWEL_MAP = {
        '\u064E': 'a',   # Fatha
        '\u064F': 'u',   # Damma
        '\u0650': 'i',   # Kasra
        '\u0652': '',    # Sukun
        '\u064B': 'an',  # Tanween Fath
        '\u064C': 'un',  # Tanween Damm
        '\u064D': 'in',  # Tanween Kasr
    }

    LONG_VOWEL_MAP = {
        'ا': 'aa',  # Alef (after fatha)
        'و': 'uu',  # Waw (after damma)
        'ي': 'ii',  # Ya (after kasra)
    }

    i = 0
    while i < len(text):
        char = text[i]

        # Skip whitespace
        if char.isspace():
            i += 1
            continue

        # Check if Arabic letter
        if '\u0621' <= char <= '\u064A':
            consonant = char
            vowel = ''
            has_shadda = False

            # Look ahead for diacritics
            j = i + 1
            while j < len(text) and (text[j] in VOWEL_MAP.keys() or text[j] == '\u0651'):
                if text[j] == '\u0651':  # Shadda
                    has_shadda = True
                else:
                    vowel = VOWEL_MAP[text[j]]
                j += 1

            # Check for long vowel (madd letter after short vowel)
            if j < len(text) and text[j] in LONG_VOWEL_MAP:
                if vowel in ['a', 'u', 'i']:
                    vowel = LONG_VOWEL_MAP[text[j]]
                    j += 1

            # If no tashkeel, infer vowel (heuristic: assume 'a')
            if not has_tashkeel and vowel == '':
                # Simple heuristic: assume fatha unless it's end of word
                if i < len(text) - 1 and text[i+1] not in [' ', '.', '،']:
                    vowel = 'a'

            phonemes.append(Phoneme(consonant, vowel, has_shadda))
            i = j
        else:
            i += 1

    return phonemes


def phonemes_to_pattern(phonemes: List[Phoneme]) -> str:
    """
    Convert phonemes to prosodic pattern string.

    Pattern symbols:
    - / = haraka (moving, CV)
    - o = sukun (still, CVC or CVV)

    Args:
        phonemes: List of Phoneme objects

    Returns:
        Pattern string like "/o//o/o"

    Example:
        >>> phonemes = [Phoneme('k', 'a'), Phoneme('t', 'a'), Phoneme('b', '')]
        >>> phonemes_to_pattern(phonemes)
        "//o"
    """
    pattern = ""

    for phoneme in phonemes:
        if phoneme.is_sukun():
            pattern += "o"
        elif phoneme.is_long_vowel():
            pattern += "/o"  # Long vowel = haraka + sukun
        else:
            pattern += "/"   # Short vowel = haraka

    return pattern


def text_to_phonetic_pattern(text: str, has_tashkeel: bool = None) -> str:
    """
    Convert Arabic text directly to phonetic pattern.

    Args:
        text: Normalized Arabic text
        has_tashkeel: Auto-detect if None

    Returns:
        Phonetic pattern string

    Example:
        >>> text_to_phonetic_pattern("كَتَبَ")
        "///"
    """
    from app.core.normalization import has_diacritics

    if has_tashkeel is None:
        has_tashkeel = has_diacritics(text)

    phonemes = extract_phonemes(text, has_tashkeel)
    return phonemes_to_pattern(phonemes)
