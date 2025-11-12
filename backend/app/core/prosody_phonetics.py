"""
Prosody-aware phonetic conversion for Arabic meter detection.

This module provides phonetic pattern conversion that aligns with
classical Arabic prosody (علم العروض) and tafila-based meter detection.

CRITICAL: This uses LETTER-BASED prosodic notation, not syllable-based.
- '/' = one haraka (متحرك) = consonant with short vowel
- 'o' = one sakin (ساكن) = consonant with sukun

This matches how tafail patterns are defined in the detector.

Example:
    فَعُولُنْ (fa-'u-lu-n) in letter-based notation:
    - ف with fatha = /
    - ع with damma = /
    - و (long vowel uu) = o
    - ل with damma = /
    - ن with sukun = o
    Result: //o/o which matches the tafila pattern for فعولن
"""

import sys
from typing import List, Optional

# Handle imports for both module use and standalone testing
try:
    from app.core.phonetics import extract_phonemes, Phoneme
except ModuleNotFoundError:
    # Standalone mode - add backend to path
    sys.path.insert(0, '/home/user/BAHR/backend')
    from app.core.phonetics import extract_phonemes, Phoneme


def phonemes_to_prosodic_pattern_v2(phonemes: List[Phoneme]) -> str:
    """
    Convert phonemes to prosodic pattern using LETTER-BASED notation.

    In classical Arabic prosody (علم العروض):
    - Each consonant with a short vowel (haraka) = '/'
    - Each consonant with sukun OR long vowel continuation = 'o'

    Rules:
    1. Short vowel (a, u, i) → '/'
    2. Sukun → 'o'
    3. Long vowel (aa, uu, ii) → '/o' (haraka + madd)
       - The haraka comes from the previous consonant
       - The madd creates a sakin
    4. Tanween (an, un, in) → '/' (treated as short vowel)
    5. Shadda → doubled pattern (first is 'o', second is '/')

    Args:
        phonemes: List of Phoneme objects with vowel information

    Returns:
        Pattern string using / and o notation

    Example:
        قِفا نَبْكِ (qifa nabki):
        - ق + i → /
        - ف + aa → /o (fatha + alef = haraka + madd)
        - ن + a → /
        - ب + sukun → o
        - ك + i → /
        Result: //o/o/
    """
    if not phonemes:
        return ""

    pattern = ""
    i = 0

    while i < len(phonemes):
        phoneme = phonemes[i]

        # Handle shadda (gemination) - consonant is doubled
        if phoneme.has_shadda:
            # First occurrence: treated as sakin (no vowel)
            pattern += 'o'
            # Second occurrence: has the vowel
            if phoneme.is_long_vowel():
                pattern += '/o'
            elif phoneme.is_sukun():
                pattern += 'o'
            else:
                pattern += '/'
            i += 1
            continue

        # Handle long vowels
        if phoneme.is_long_vowel():
            # Long vowel = haraka + madd (sakin)
            # The haraka was from the consonant, madd creates the sakin
            pattern += '/o'
            i += 1
            continue

        # Handle sukun
        if phoneme.is_sukun():
            pattern += 'o'
            i += 1
            continue

        # Handle short vowels (including tanween)
        # Tanween (an, un, in) is treated like short vowel + nun sakin
        if phoneme.vowel in ['a', 'u', 'i']:
            pattern += '/'
        elif phoneme.vowel in ['an', 'un', 'in']:
            # Tanween = short vowel + nun sakin
            pattern += '/o'

        i += 1

    return pattern


def prosodic_text_to_pattern(text: str, has_tashkeel: bool = True) -> str:
    """
    Convert Arabic text to prosodic pattern using classical prosody rules.

    This is the main entry point for converting text to patterns that match
    the detector's expected format.

    Args:
        text: Arabic text (preferably with diacritics)
        has_tashkeel: Whether text has diacritical marks

    Returns:
        Prosodic pattern string compatible with detector

    Example:
        >>> prosodic_text_to_pattern("فَعُولُنْ", has_tashkeel=True)
        "//o/o"  # matches فعولن tafila pattern
    """
    # Extract phonemes
    phonemes = extract_phonemes(text, has_tashkeel=has_tashkeel)

    if not phonemes:
        return ""

    # Convert to letter-based prosodic pattern
    pattern = phonemes_to_prosodic_pattern_v2(phonemes)

    return pattern


def text_to_pattern_v2(text: str, has_tashkeel: Optional[bool] = None) -> str:
    """
    Enhanced text-to-pattern converter with auto-detection.

    This function combines phoneme extraction with prosody-aware
    pattern generation to produce patterns compatible with the detector.

    Args:
        text: Normalized Arabic text
        has_tashkeel: Whether text has diacritics (auto-detects if None)

    Returns:
        Prosodic pattern string

    Example:
        >>> text_to_pattern_v2("قِفا نَبْكِ مِن ذِكرى")
        "/o//o/o/..."  # prosodic pattern
    """
    from app.core.normalization import has_diacritics

    if has_tashkeel is None:
        has_tashkeel = has_diacritics(text)

    return prosodic_text_to_pattern(text, has_tashkeel)


# Backwards compatibility alias
text_to_phonetic_pattern_v2 = text_to_pattern_v2


if __name__ == "__main__":
    # Demo and test
    import sys
    sys.path.insert(0, '/home/user/BAHR/backend')

    print("="*80)
    print("Prosody-Aware Phonetic Conversion Demo (Letter-Based)")
    print("="*80)
    print()

    # Test with تفاعيل
    print("Testing individual tafail:")
    print()

    tafail_tests = [
        ("فَعُولُنْ", "فعولن", "/o//o"),
        ("مُفَاعَيلُنْ", "مفاعيلن", "//o/o/o"),
        ("فَاعِلُنْ", "فاعلن", "/o//o"),
        ("مُتَفَاعِلُنْ", "متفاعلن", "///o//o"),
    ]

    for diacritized, name, expected in tafail_tests:
        pattern = prosodic_text_to_pattern(diacritized, has_tashkeel=True)
        match = "✅" if pattern == expected else "❌"
        print(f"{match} {name}: '{pattern}' (expected: '{expected}')")

    print()
    print("-"*80)
    print()

    # Test with full verse
    print("Testing full verse (الطويل):")
    print()

    verse = "قِفا نَبْكِ مِن ذِكرى حَبيبٍ ومَنْزِلِ"
    pattern = prosodic_text_to_pattern(verse, has_tashkeel=True)
    expected_base = "/o//o//o/o/o/o//o//o/o/o"  # Base pattern for الطويل

    print(f"Verse: {verse}")
    print(f"Generated:  {pattern} (len={len(pattern)})")
    print(f"Expected:   {expected_base} (len={len(expected_base)})")

    # Also show old method for comparison
    from app.core.phonetics import text_to_phonetic_pattern
    old_pattern = text_to_phonetic_pattern(verse, has_tashkeel=True)
    print(f"Old method: {old_pattern} (len={len(old_pattern)})")
    print()

    # Character-by-character comparison
    if pattern != expected_base:
        print("Character-by-character comparison:")
        max_len = max(len(pattern), len(expected_base))
        for i in range(max_len):
            gen_char = pattern[i] if i < len(pattern) else ' '
            exp_char = expected_base[i] if i < len(expected_base) else ' '
            match_char = '✓' if gen_char == exp_char else '✗'
            print(f"  {i+1:2d}: '{gen_char}' vs '{exp_char}' {match_char}")
