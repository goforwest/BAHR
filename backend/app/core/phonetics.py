"""
Arabic phonetic analysis for prosody.

This module provides functions to convert Arabic text into phonetic representations
suitable for prosodic analysis. It handles diacritics, long vowels, and shadda.
"""

from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Phoneme:
    """
    Represents a phonetic unit in Arabic text.
    
    A phoneme consists of a consonant, a vowel (or absence thereof), and optionally
    a shadda (gemination marker).
    
    Attributes:
        consonant: The consonant character
        vowel: The vowel type. Can be:
            - 'a', 'u', 'i': short vowels (fatha, damma, kasra)
            - 'aa', 'uu', 'ii': long vowels (madd)
            - '': sukun (no vowel)
        has_shadda: Whether the consonant has shadda (gemination)
    
    Example:
        >>> p = Phoneme('ك', 'a', False)
        >>> str(p)
        'كa'
    """
    consonant: str
    vowel: str  # 'a', 'u', 'i', 'aa', 'uu', 'ii', '' (sukun)
    has_shadda: bool = False

    def __str__(self):
        """Return string representation of phoneme."""
        shadda_mark = "ّ" if self.has_shadda else ""
        return f"{self.consonant}{shadda_mark}{self.vowel}"

    def is_long_vowel(self) -> bool:
        """
        Check if phoneme has a long vowel (madd).
        
        Returns:
            True if vowel is 'aa', 'uu', or 'ii', False otherwise
        
        Example:
            >>> Phoneme('ك', 'aa').is_long_vowel()
            True
            >>> Phoneme('ك', 'a').is_long_vowel()
            False
        """
        return self.vowel in ['aa', 'uu', 'ii']

    def is_sukun(self) -> bool:
        """
        Check if phoneme has sukun (no vowel).
        
        Returns:
            True if vowel is empty string, False otherwise
        
        Example:
            >>> Phoneme('ك', '').is_sukun()
            True
            >>> Phoneme('ك', 'a').is_sukun()
            False
        """
        return self.vowel == ''


def extract_phonemes(text: str, has_tashkeel: bool = False) -> List[Phoneme]:
    """
    Extract phonemes from Arabic text.
    
    This function parses Arabic text and converts it into a list of phonemes,
    which represent the phonetic units needed for prosodic analysis.
    
    Args:
        text: Arabic text (should be normalized)
        has_tashkeel: Whether the text contains diacritical marks (tashkeel).
                     If False, vowels will be inferred using heuristics.
    
    Returns:
        List of Phoneme objects representing the phonetic structure
    
    Example:
        >>> extract_phonemes("كَتَبَ", has_tashkeel=True)
        [Phoneme('ك', 'a'), Phoneme('ت', 'a'), Phoneme('ب', 'a')]
        
        >>> extract_phonemes("كِتَاب", has_tashkeel=True)
        [Phoneme('ك', 'i'), Phoneme('ت', 'aa'), Phoneme('ب', 'a')]
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
    
    This converts a list of phonemes into the classical Arabic prosody notation:
    - '/' represents haraka (moving syllable): consonant + short vowel
    - 'o' represents sukun (still syllable): consonant without vowel or with long vowel
    
    Pattern rules:
    - Short vowel (a, u, i) → '/'
    - Long vowel (aa, uu, ii) → '/o' (haraka + sukun)
    - Sukun (no vowel) → 'o'
    
    Args:
        phonemes: List of Phoneme objects
    
    Returns:
        Pattern string like "/o//o/o"
    
    Example:
        >>> phonemes = [Phoneme('k', 'a'), Phoneme('t', 'a'), Phoneme('b', '')]
        >>> phonemes_to_pattern(phonemes)
        "//o"
        
        >>> phonemes = [Phoneme('k', 'aa'), Phoneme('t', 'a')]
        >>> phonemes_to_pattern(phonemes)
        "/o/"
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
    
    This is a convenience function that combines phoneme extraction and pattern
    conversion in a single call. It automatically detects whether the text has
    tashkeel if not specified.
    
    Args:
        text: Normalized Arabic text
        has_tashkeel: Whether text has diacritical marks. If None, will auto-detect.
    
    Returns:
        Phonetic pattern string
    
    Example:
        >>> text_to_phonetic_pattern("كَتَبَ")
        "///"
        
        >>> text_to_phonetic_pattern("كِتَاب")
        "/o//"
    """
    from app.core.normalization import has_diacritics

    if has_tashkeel is None:
        has_tashkeel = has_diacritics(text)

    phonemes = extract_phonemes(text, has_tashkeel)
    return phonemes_to_pattern(phonemes)
