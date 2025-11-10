"""
Arabic phonetic analysis for prosody.

This module provides functions to convert Arabic text into phonetic representations
suitable for prosodic analysis. It handles diacritics, long vowels, and shadda.
"""

from typing import List, Tuple
from dataclasses import dataclass
import unicodedata


def normalize_unicode(text: str) -> str:
    """Normalize Unicode text to NFC form."""
    return unicodedata.normalize('NFC', text)


def normalize_alef_maksura_ar(text: str) -> str:
    """Normalize alef maksura (ى) to yeh (ي)."""
    return text.replace('ى', 'ي')


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
    # Normalize using CAMeL Tools
    try:
        text = normalize_unicode(text)
    except:
        pass  # Fallback to original text if CAMeL Tools fails
    
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
        'ى': 'aa',  # Alef maqsurah (also forms aa after fatha)
    }
    
    # Special madd letters that can extend vowels
    MADD_LETTERS = {'ا', 'و', 'ي', 'ى'}

    i = 0
    pending_vowel = None  # Track vowel waiting for next consonant
    
    while i < len(text):
        char = text[i]

        # Skip whitespace
        if char.isspace():
            i += 1
            continue

        # Check if Arabic letter (consonants and madd letters)
        if '\u0621' <= char <= '\u064A':
            # Look ahead for diacritics on this character
            j = i + 1
            vowel_on_this_char = None  # None = no diacritic, '' = explicit sukun
            has_shadda = False
            
            while j < len(text) and (text[j] in VOWEL_MAP.keys() or text[j] == '\u0651'):
                if text[j] == '\u0651':  # Shadda
                    has_shadda = True
                else:
                    vowel_on_this_char = VOWEL_MAP[text[j]]
                j += 1

            # CRITICAL: Check if this is a madd letter used for vowel extension
            # A madd letter is used for extension if:
            # 1. It's one of the madd letters (ا و ي ى)
            # 2. It has NO diacritic mark on it (vowel_on_this_char is None, not '')
            # 3. There's a previous phoneme to extend
            if char in MADD_LETTERS and vowel_on_this_char is None and not has_shadda and phonemes:
                last_phoneme = phonemes[-1]
                
                # Check vowel compatibility for madd
                extended = False
                if char in ['ا', 'ى']:
                    # Alef and alef maqsurah extend fatha (a) to aa
                    if last_phoneme.vowel in ['a', 'an']:
                        last_phoneme.vowel = 'aa'
                        extended = True
                elif char == 'و':
                    # Waw extends damma (u) to uu
                    if last_phoneme.vowel in ['u', 'un']:
                        last_phoneme.vowel = 'uu'
                        extended = True
                elif char == 'ي':
                    # Ya extends kasra (i) to ii
                    if last_phoneme.vowel in ['i', 'in']:
                        last_phoneme.vowel = 'ii'
                        extended = True
                
                if extended:
                    i = j
                    continue
                # If not extended, fall through and treat as consonant
            
            # This is a regular consonant (or a madd letter being used as consonant)
            consonant = char
            vowel = vowel_on_this_char if vowel_on_this_char is not None else ''  # Convert None to ''

            # Handle shadda: consonant gemination (doubling)
            # Shadda means the consonant is pronounced twice
            # First occurrence has sukun, second has the vowel
            if has_shadda:
                # Handle tanween with shadda (rare but possible)
                if vowel in ['an', 'un', 'in']:
                    base_vowel = vowel[0]  # 'a', 'u', or 'i'
                    # First consonant (with sukun - geminated part)
                    phonemes.append(Phoneme(consonant, '', False))
                    # Second consonant (with short vowel)
                    phonemes.append(Phoneme(consonant, base_vowel, False))
                    # Add separate phoneme for 'n' (noon sakinah from tanween)
                    phonemes.append(Phoneme('ن', '', False))
                else:
                    # First consonant (with sukun - geminated part)
                    phonemes.append(Phoneme(consonant, '', False))
                    # Second consonant (with the vowel or sukun)
                    phonemes.append(Phoneme(consonant, vowel, False))
                i = j
                continue
            
            # Handle tanween: creates an extra 'n' phoneme
            if vowel in ['an', 'un', 'in']:
                # Add phoneme with short vowel
                base_vowel = vowel[0]  # 'a', 'u', or 'i'
                phonemes.append(Phoneme(consonant, base_vowel, False))
                # Add separate phoneme for 'n' (noon sakinah)
                phonemes.append(Phoneme('ن', '', False))
                i = j
                continue

            # CRITICAL FIX: Infer vowels for consonants without explicit diacritics  
            # vowel is None = no diacritic found, '' = explicit sukun
            # Only apply heuristics if vowel is None (no marking)
            if vowel == '' and vowel_on_this_char is None:  # Explicitly check: was there no diacritic?
                # HEURISTIC 1: Check if next character is a madd letter
                if j < len(text) and text[j] in MADD_LETTERS:
                    # Infer compatible short vowel before madd letter
                    if text[j] in ['ا', 'ى']:
                        vowel = 'a'  # Will be extended to 'aa' by madd letter
                    elif text[j] == 'و':
                        vowel = 'u'  # Will be extended to 'uu' by madd letter  
                    elif text[j] == 'ي':
                        vowel = 'i'  # Will be extended to 'ii' by madd letter
                # HEURISTIC 2: Check if this is end of word (followed by space or end of text)
                elif j >= len(text) or text[j].isspace():
                    # End of word - likely has sukun (leave as '')
                    pass
                # HEURISTIC 3: Check if next char is a consonant with vowel
                # (meaning this consonant is in middle of word)
                elif j < len(text):
                    # Look ahead to see if next char has a vowel or is a consonant
                    next_char = text[j]
                    # If next is Arabic letter (not madd), assume this has fatha
                    if '\u0621' <= next_char <= '\u064A' and next_char not in MADD_LETTERS:
                        vowel = 'a'  # Default to fatha for mid-word consonants
                    # If next is a diacritic on next consonant, current one likely has sukun
                    # (but this is already handled - vowel stays '')
                # else: leave as '' (sukun)

            phonemes.append(Phoneme(consonant, vowel, False))
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
    
    CRITICAL: In Arabic prosody, syllables are the unit of measurement, not phonemes.
    A syllable ending with a sakin (sukun or long vowel continuation) forms a "heavy" syllable.
    
    Syllable types:
    - Light (open): CV = consonant + short vowel = `/` 
    - Heavy (closed): CVC = consonant + short vowel + sakin consonant = `/o`
    - Heavy (long): CVV = consonant + long vowel = `/o`
    
    Pattern rules:
    - Short vowel followed by sakin → `/o` (combine into one heavy syllable)
    - Short vowel followed by vowel → `/` (light syllable)
    - Long vowel → `/o` (heavy syllable)
    - Sakin alone → `o` (continuation of previous syllable)
    
    Args:
        phonemes: List of Phoneme objects
    
    Returns:
        Pattern string like "/o//o/o"
    
    Example:
        >>> phonemes = [Phoneme('م', 'a'), Phoneme('ر', ''), Phoneme('ت', 'a')]
        >>> phonemes_to_pattern(phonemes)
        "/o/"  # مَرْتَ = heavy + light
        
        >>> phonemes = [Phoneme('ك', 'aa'), Phoneme('ت', 'a')]
        >>> phonemes_to_pattern(phonemes)
        "/o/"  # كَاتَ = heavy + light
    """
    pattern = ""
    i = 0
    
    while i < len(phonemes):
        phoneme = phonemes[i]
        
        if phoneme.is_long_vowel():
            # Long vowel = heavy syllable
            pattern += "/o"
            i += 1
        elif phoneme.is_sukun():
            # Sakin alone (shouldn't happen at start, but handle it)
            pattern += "o"
            i += 1
        else:
            # Short vowel - check if next phoneme is sakin
            if i + 1 < len(phonemes) and phonemes[i + 1].is_sukun():
                # Short vowel + sakin = heavy syllable (closed)
                pattern += "/o"
                i += 2  # Skip the sakin phoneme since we consumed it
            else:
                # Short vowel alone = light syllable (open)
                pattern += "/"
                i += 1

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
