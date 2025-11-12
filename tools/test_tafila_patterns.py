#!/usr/bin/env python3
"""Test tafila pattern generation."""

import sys
sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.phonetics import extract_phonemes
from app.core.prosody_phonetics import phonemes_to_prosodic_pattern_v2


def test_tafila(diacritized_text, name, expected_pattern):
    """Test a single tafila."""
    print(f"\nTesting: {name} ({diacritized_text})")
    print(f"Expected pattern: {expected_pattern}")
    print()

    # Extract phonemes
    phonemes = extract_phonemes(diacritized_text, has_tashkeel=True)

    print(f"Phonemes ({len(phonemes)}):")
    for i, p in enumerate(phonemes, 1):
        vowel_display = f"'{p.vowel}'" if p.vowel else "'sukun'"
        shadda_display = " (shadda)" if p.has_shadda else ""
        long_display = " [LONG]" if p.is_long_vowel() else ""
        sukun_display = " [SUKUN]" if p.is_sukun() else ""
        print(f"  {i}. {p.consonant} + {vowel_display}{shadda_display}{long_display}{sukun_display}")

    # Generate pattern
    pattern = phonemes_to_prosodic_pattern_v2(phonemes)
    print(f"\nGenerated pattern: {pattern}")
    print(f"Match: {'✅' if pattern == expected_pattern else '❌'}")

    if pattern != expected_pattern:
        print(f"\nMismatch analysis:")
        print(f"  Generated: {pattern}")
        print(f"  Expected:  {expected_pattern}")
        print(f"  Positions: {''.join('✓' if i < len(expected_pattern) and pattern[i] == expected_pattern[i] else '✗' for i in range(max(len(pattern), len(expected_pattern))))}")


if __name__ == '__main__':
    print("="*80)
    print("TAFILA PATTERN TESTING")
    print("="*80)

    # Test key tafail
    test_tafila("فَعُولُنْ", "فعولن", "/o//o")
    test_tafila("مُفَاعَيلُنْ", "مفاعيلن", "//o/o/o")
    test_tafila("فَاعِلُنْ", "فاعلن", "/o//o")
    test_tafila("مُتَفَاعِلُنْ", "متفاعلن", "///o//o")
    test_tafila("مُسْتَفْعِلُنْ", "مستفعلن", "/o/o//o")
