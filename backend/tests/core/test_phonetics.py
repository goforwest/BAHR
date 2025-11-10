"""
Unit tests for phonetic analysis.
"""

import pytest
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.phonetics import (
    Phoneme,
    extract_phonemes,
    phonemes_to_pattern,
    text_to_phonetic_pattern,
)


class TestPhoneme:
    def test_long_vowel_detection(self):
        p = Phoneme('ك', 'aa')
        assert p.is_long_vowel() == True

        p = Phoneme('ك', 'a')
        assert p.is_long_vowel() == False

    def test_sukun_detection(self):
        p = Phoneme('ك', '')
        assert p.is_sukun() == True

        p = Phoneme('ك', 'a')
        assert p.is_sukun() == False


class TestExtractPhonemes:
    def test_simple_word_with_tashkeel(self):
        phonemes = extract_phonemes("كَتَبَ", has_tashkeel=True)
        assert len(phonemes) == 3
        assert all(p.vowel == 'a' for p in phonemes)

    def test_word_with_sukun(self):
        phonemes = extract_phonemes("كَتْبَ", has_tashkeel=True)
        assert len(phonemes) == 3
        assert phonemes[0].vowel == 'a'
        assert phonemes[1].vowel == ''  # sukun
        assert phonemes[2].vowel == 'a'

    def test_word_with_shadda(self):
        phonemes = extract_phonemes("مُحَمَّد", has_tashkeel=True)
        # Find the shadda phoneme
        shadda_phonemes = [p for p in phonemes if p.has_shadda]
        assert len(shadda_phonemes) >= 1

    def test_word_with_long_vowel(self):
        # "كتاب" with tashkeel: "كِتَاب"
        phonemes = extract_phonemes("كِتَاب", has_tashkeel=True)
        # Should detect 'aa' in تا
        long_vowels = [p for p in phonemes if p.is_long_vowel()]
        assert len(long_vowels) >= 1


class TestPhonemesToPattern:
    def test_all_short_vowels(self):
        phonemes = [Phoneme('ك', 'a'), Phoneme('ت', 'a'), Phoneme('ب', 'a')]
        assert phonemes_to_pattern(phonemes) == "///"

    def test_with_sukun(self):
        phonemes = [Phoneme('ك', 'a'), Phoneme('ت', ''), Phoneme('ب', 'a')]
        assert phonemes_to_pattern(phonemes) == "/o/"

    def test_with_long_vowel(self):
        phonemes = [Phoneme('ك', 'aa'), Phoneme('ت', 'a'), Phoneme('ب', 'a')]
        assert phonemes_to_pattern(phonemes) == "/o//"


class TestTextToPhoneticPattern:
    def test_simple_verse(self):
        # Simple test (exact pattern depends on implementation details)
        pattern = text_to_phonetic_pattern("كَتَبَ")
        assert '/' in pattern
        assert len(pattern) >= 3

    def test_handles_no_tashkeel(self):
        # Should infer vowels
        pattern = text_to_phonetic_pattern("كتب", has_tashkeel=False)
        assert pattern != ""
