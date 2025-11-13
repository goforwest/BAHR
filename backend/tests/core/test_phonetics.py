"""
Unit tests for phonetic analysis.

This module tests the phonetics.py module which handles conversion of Arabic
text to phonetic representations for prosodic analysis.
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
    """Test the Phoneme dataclass methods."""
    
    def test_long_vowel_detection_aa(self):
        """Test that 'aa' is correctly identified as a long vowel."""
        p = Phoneme('ك', 'aa')
        assert p.is_long_vowel() == True
    
    def test_long_vowel_detection_uu(self):
        """Test that 'uu' is correctly identified as a long vowel."""
        p = Phoneme('م', 'uu')
        assert p.is_long_vowel() == True
    
    def test_long_vowel_detection_ii(self):
        """Test that 'ii' is correctly identified as a long vowel."""
        p = Phoneme('ن', 'ii')
        assert p.is_long_vowel() == True

    def test_short_vowel_not_long(self):
        """Test that short vowels are not identified as long vowels."""
        p = Phoneme('ك', 'a')
        assert p.is_long_vowel() == False
        
        p = Phoneme('ك', 'u')
        assert p.is_long_vowel() == False
        
        p = Phoneme('ك', 'i')
        assert p.is_long_vowel() == False

    def test_sukun_detection(self):
        """Test that sukun (empty vowel) is correctly detected."""
        p = Phoneme('ك', '')
        assert p.is_sukun() == True

    def test_vowel_not_sukun(self):
        """Test that phonemes with vowels are not sukun."""
        p = Phoneme('ك', 'a')
        assert p.is_sukun() == False

    def test_diphthong_detection_aw(self):
        """Test that 'aw' is correctly identified as a diphthong."""
        p = Phoneme('و', 'aw')
        assert p.is_diphthong() == True

    def test_diphthong_detection_ay(self):
        """Test that 'ay' is correctly identified as a diphthong."""
        p = Phoneme('ي', 'ay')
        assert p.is_diphthong() == True

    def test_short_vowel_not_diphthong(self):
        """Test that short vowels are not identified as diphthongs."""
        p = Phoneme('ك', 'a')
        assert p.is_diphthong() == False

    def test_long_vowel_not_diphthong(self):
        """Test that long vowels are not identified as diphthongs."""
        p = Phoneme('ك', 'aa')
        assert p.is_diphthong() == False

    def test_str_representation(self):
        """Test string representation of phoneme."""
        p = Phoneme('ك', 'a')
        assert 'ك' in str(p)
        assert 'a' in str(p)


class TestExtractPhonemes:
    """Test phoneme extraction from Arabic text."""
    
    def test_simple_word_with_tashkeel(self):
        """Test extraction from كَتَبَ (kataba - he wrote)."""
        phonemes = extract_phonemes("كَتَبَ", has_tashkeel=True)
        assert len(phonemes) == 3
        assert all(p.vowel == 'a' for p in phonemes)
        assert phonemes[0].consonant == 'ك'
        assert phonemes[1].consonant == 'ت'
        assert phonemes[2].consonant == 'ب'

    def test_word_with_sukun(self):
        """Test extraction from كَتْبَ with sukun."""
        phonemes = extract_phonemes("كَتْبَ", has_tashkeel=True)
        assert len(phonemes) == 3
        assert phonemes[0].vowel == 'a'
        assert phonemes[1].vowel == ''  # sukun
        assert phonemes[2].vowel == 'a'

    def test_word_with_shadda(self):
        """Test extraction from مُحَمَّد (Muhammad) with shadda."""
        phonemes = extract_phonemes("مُحَمَّد", has_tashkeel=True)
        # Find the shadda phoneme (on م)
        shadda_phonemes = [p for p in phonemes if p.has_shadda]
        assert len(shadda_phonemes) >= 1
        # Verify we have phonemes
        assert len(phonemes) >= 3

    def test_word_with_long_vowel_aa(self):
        """Test extraction from كِتَاب (kitaab - book) with alef madd."""
        phonemes = extract_phonemes("كِتَاب", has_tashkeel=True)
        # Should detect 'aa' in تا
        long_vowels = [p for p in phonemes if p.is_long_vowel()]
        assert len(long_vowels) >= 1
        # Find the 'aa' specifically
        aa_vowels = [p for p in phonemes if p.vowel == 'aa']
        assert len(aa_vowels) >= 1

    def test_word_with_long_vowel_uu(self):
        """Test extraction with waw madd (uu)."""
        phonemes = extract_phonemes("نُور", has_tashkeel=True)
        # Should detect 'uu' in نو
        uu_vowels = [p for p in phonemes if p.vowel == 'uu']
        assert len(uu_vowels) >= 1

    def test_word_with_long_vowel_ii(self):
        """Test extraction with ya madd (ii)."""
        phonemes = extract_phonemes("كَرِيم", has_tashkeel=True)
        # Should detect 'ii' in ري
        ii_vowels = [p for p in phonemes if p.vowel == 'ii']
        assert len(ii_vowels) >= 1

    def test_word_without_tashkeel(self):
        """Test that vowels are inferred when no tashkeel is present."""
        phonemes = extract_phonemes("كتب", has_tashkeel=False)
        # Should have inferred vowels (heuristic: 'a')
        assert len(phonemes) >= 2
        # Most should have inferred vowel 'a'
        voweled = [p for p in phonemes if p.vowel != '']
        assert len(voweled) >= 1

    def test_word_with_tanween(self):
        """Test extraction with tanween marks."""
        phonemes = extract_phonemes("شُكْرًا", has_tashkeel=True)
        assert len(phonemes) >= 3
        # Check that tanween is handled
        vowels = [p.vowel for p in phonemes]
        assert 'an' in vowels or 'u' in vowels

    def test_word_with_damma(self):
        """Test extraction with damma (u)."""
        phonemes = extract_phonemes("كُتُب", has_tashkeel=True)
        u_vowels = [p for p in phonemes if p.vowel == 'u']
        assert len(u_vowels) >= 1

    def test_word_with_kasra(self):
        """Test extraction with kasra (i)."""
        phonemes = extract_phonemes("بِسْمِ", has_tashkeel=True)
        i_vowels = [p for p in phonemes if p.vowel == 'i']
        assert len(i_vowels) >= 1

    def test_word_with_diphthong_aw(self):
        """Test extraction from يَوْم (yawm - day) with 'aw' diphthong."""
        phonemes = extract_phonemes("يَوْم", has_tashkeel=True)
        # Should detect 'aw' diphthong: ي with fatha + و with sukun = يَوْ
        aw_diphthongs = [p for p in phonemes if p.vowel == 'aw']
        assert len(aw_diphthongs) == 1, f"Expected 1 'aw' diphthong, found {len(aw_diphthongs)}"

    def test_word_with_diphthong_ay(self):
        """Test extraction from بَيْت (bayt - house) with 'ay' diphthong."""
        phonemes = extract_phonemes("بَيْت", has_tashkeel=True)
        # Should detect 'ay' diphthong: ب with fatha + ي with sukun = بَيْ
        ay_diphthongs = [p for p in phonemes if p.vowel == 'ay']
        assert len(ay_diphthongs) == 1, f"Expected 1 'ay' diphthong, found {len(ay_diphthongs)}"

    def test_multiple_diphthongs(self):
        """Test extraction from عَيْنَوْن (hypothetical) with multiple diphthongs."""
        phonemes = extract_phonemes("عَيْنَوْن", has_tashkeel=True)
        # Should have both 'ay' and 'aw'
        diphthongs = [p for p in phonemes if p.is_diphthong()]
        assert len(diphthongs) >= 1

    def test_hamza_wasl_definite_article(self):
        """Test hamza waṣl detection in definite article ال."""
        phonemes = extract_phonemes("الكِتَاب", has_tashkeel=True)
        # First phoneme should be alef with hamza waṣl marker
        hamza_wasl_phonemes = [p for p in phonemes if p.is_hamza_wasl]
        assert len(hamza_wasl_phonemes) >= 1, "Expected hamza waṣl in الكتاب"
        assert phonemes[0].consonant == 'ا'
        assert phonemes[0].is_hamza_wasl == True

    def test_hamza_wasl_ibn(self):
        """Test hamza waṣl detection in ابن (ibn - son)."""
        phonemes = extract_phonemes("ابن", has_tashkeel=True)
        # First phoneme should be alef with hamza waṣl marker
        assert phonemes[0].consonant == 'ا'
        assert phonemes[0].is_hamza_wasl == True

    def test_hamza_wasl_ism(self):
        """Test hamza waṣl detection in اسم (ism - name)."""
        phonemes = extract_phonemes("اسم", has_tashkeel=True)
        # First phoneme should be alef with hamza waṣl marker
        assert phonemes[0].consonant == 'ا'
        assert phonemes[0].is_hamza_wasl == True

    def test_hamza_wasl_form_x_verb(self):
        """Test hamza waṣl detection in Form X verb استـ."""
        phonemes = extract_phonemes("استَمَعَ", has_tashkeel=True)
        # First phoneme should be alef with hamza waṣl marker
        hamza_wasl_phonemes = [p for p in phonemes if p.is_hamza_wasl]
        assert len(hamza_wasl_phonemes) >= 1, "Expected hamza waṣl in استمع"
        assert phonemes[0].consonant == 'ا'
        assert phonemes[0].is_hamza_wasl == True

    def test_hamza_qat_not_wasl(self):
        """Test that hamza qat' is NOT marked as hamza waṣl."""
        # أَكَلَ (akala - he ate) starts with hamza qat' (أ), not hamza waṣl
        phonemes = extract_phonemes("أَكَلَ", has_tashkeel=True)
        # Should not have any hamza waṣl markers
        hamza_wasl_phonemes = [p for p in phonemes if p.is_hamza_wasl]
        assert len(hamza_wasl_phonemes) == 0, "Hamza qat' should not be marked as waṣl"


class TestPhonemesToPattern:
    """Test conversion of phonemes to prosodic patterns."""
    
    def test_all_short_vowels(self):
        """Test pattern with all short vowels."""
        phonemes = [Phoneme('ك', 'a'), Phoneme('ت', 'a'), Phoneme('ب', 'a')]
        assert phonemes_to_pattern(phonemes) == "///"

    def test_with_sukun(self):
        """Test pattern with sukun."""
        phonemes = [Phoneme('ك', 'a'), Phoneme('ت', ''), Phoneme('ب', 'a')]
        assert phonemes_to_pattern(phonemes) == "/o/"

    def test_with_long_vowel(self):
        """Test pattern with long vowel."""
        phonemes = [Phoneme('ك', 'aa'), Phoneme('ت', 'a'), Phoneme('ب', 'a')]
        assert phonemes_to_pattern(phonemes) == "/o//"

    def test_mixed_pattern(self):
        """Test complex pattern with mixed vowel types."""
        phonemes = [
            Phoneme('ك', 'a'),   # /
            Phoneme('ت', 'aa'),  # /o
            Phoneme('ب', ''),    # o
            Phoneme('م', 'u'),   # /
        ]
        assert phonemes_to_pattern(phonemes) == "//oo/"

    def test_all_sukun(self):
        """Test pattern with all sukun."""
        phonemes = [Phoneme('ك', ''), Phoneme('ت', ''), Phoneme('ب', '')]
        assert phonemes_to_pattern(phonemes) == "ooo"

    def test_all_long_vowels(self):
        """Test pattern with all long vowels."""
        phonemes = [Phoneme('ك', 'aa'), Phoneme('م', 'uu'), Phoneme('ن', 'ii')]
        assert phonemes_to_pattern(phonemes) == "/o/o/o"

    def test_empty_phonemes_list(self):
        """Test pattern with empty phonemes list."""
        phonemes = []
        assert phonemes_to_pattern(phonemes) == ""

    def test_with_diphthong_aw(self):
        """Test pattern with 'aw' diphthong (heavy syllable)."""
        phonemes = [Phoneme('ي', 'aw'), Phoneme('م', '')]
        # Diphthong forms heavy syllable (/o) + sukun (o)
        assert phonemes_to_pattern(phonemes) == "/oo"

    def test_with_diphthong_ay(self):
        """Test pattern with 'ay' diphthong (heavy syllable)."""
        phonemes = [Phoneme('ب', 'ay'), Phoneme('ت', '')]
        # Diphthong forms heavy syllable (/o) + sukun (o)
        assert phonemes_to_pattern(phonemes) == "/oo"

    def test_mixed_with_diphthong(self):
        """Test pattern mixing diphthongs with other vowel types."""
        phonemes = [
            Phoneme('ك', 'a'),   # / (short vowel)
            Phoneme('ت', 'ay'),  # /o (diphthong)
            Phoneme('ب', 'aa'),  # /o (long vowel)
            Phoneme('م', ''),    # o (sukun)
        ]
        assert phonemes_to_pattern(phonemes) == "//o/oo"

    def test_super_heavy_cvvc(self):
        """Test super-heavy syllable CVVC (long vowel + consonant)."""
        # دَاب (daab) - long vowel + final consonant
        phonemes = [Phoneme('د', 'aa'), Phoneme('ب', '')]
        # CVVC = /o (long vowel) + o (sukun) = /oo
        assert phonemes_to_pattern(phonemes) == "/oo"

    def test_super_heavy_cvcc(self):
        """Test super-heavy syllable CVCC (short vowel + two consonants)."""
        # دَرْس (dars) - short vowel + sukun + consonant
        phonemes = [Phoneme('د', 'a'), Phoneme('ر', ''), Phoneme('س', '')]
        # CVCC = /o (CV+C combined) + o (final C) = /oo
        assert phonemes_to_pattern(phonemes) == "/oo"


class TestTextToPhoneticPattern:
    """Test end-to-end text to pattern conversion."""
    
    def test_simple_word_with_tashkeel(self):
        """Test كَتَبَ converts to correct pattern."""
        pattern = text_to_phonetic_pattern("كَتَبَ")
        assert '/' in pattern
        assert len(pattern) >= 3
        # All fatha should give "///"
        assert pattern == "///"

    def test_word_with_long_vowel(self):
        """Test كِتَاب converts to pattern with /o."""
        pattern = text_to_phonetic_pattern("كِتَاب")
        assert '/o' in pattern
        assert '/' in pattern

    def test_handles_no_tashkeel(self):
        """Test that vowels are inferred when no tashkeel."""
        pattern = text_to_phonetic_pattern("كتب", has_tashkeel=False)
        assert pattern != ""
        assert '/' in pattern or 'o' in pattern

    def test_auto_detect_tashkeel(self):
        """Test auto-detection of tashkeel."""
        # With tashkeel - should auto-detect
        pattern1 = text_to_phonetic_pattern("كَتَبَ")
        assert pattern1 != ""
        
        # Without tashkeel - should auto-detect
        pattern2 = text_to_phonetic_pattern("كتب")
        assert pattern2 != ""

    def test_word_with_sukun(self):
        """Test word with sukun produces 'o' in pattern."""
        pattern = text_to_phonetic_pattern("كَتْبَ")
        assert 'o' in pattern

    def test_verse_fragment(self):
        """Test a fragment of a verse."""
        # "إذا غامرت" - famous verse beginning
        pattern = text_to_phonetic_pattern("إِذَا غَامَرْتَ")
        assert pattern != ""
        assert '/' in pattern
        # Should have sukun from ت with sukun
        assert 'o' in pattern

    def test_word_with_tanween(self):
        """Test word with tanween."""
        pattern = text_to_phonetic_pattern("شُكْرًا")
        assert pattern != ""
        assert '/' in pattern or 'o' in pattern

    def test_multiple_words(self):
        """Test phrase with multiple words."""
        pattern = text_to_phonetic_pattern("كَتَبَ الشِّعْرَ")
        assert pattern != ""
        assert '/' in pattern

    def test_word_with_all_short_vowels(self):
        """Test word with fatha, damma, kasra."""
        pattern = text_to_phonetic_pattern("مَعَ الشَّمْسِ")
        assert '/' in pattern
        assert 'o' in pattern  # From sukun in شمس

    def test_word_with_diphthong_aw(self):
        """Test يَوْم (yawm - day) produces pattern with /o for diphthong."""
        pattern = text_to_phonetic_pattern("يَوْم")
        # يَوْ is a diphthong (/o), م is sukun (o)
        assert pattern == "/oo" or "/o" in pattern

    def test_word_with_diphthong_ay(self):
        """Test بَيْت (bayt - house) produces pattern with /o for diphthong."""
        pattern = text_to_phonetic_pattern("بَيْت")
        # بَيْ is a diphthong (/o), ت is sukun (o)
        assert pattern == "/oo" or "/o" in pattern

    def test_classical_word_with_diphthong(self):
        """Test classical word خَوْف (khawf - fear) with diphthong."""
        pattern = text_to_phonetic_pattern("خَوْف")
        # خَوْ is diphthong (/o), ف is likely sukun or short vowel
        assert "/o" in pattern

    def test_super_heavy_syllable_cvvc(self):
        """Test word with super-heavy CVVC syllable."""
        pattern = text_to_phonetic_pattern("دَاب")
        # دَا is long vowel (/o), ب is sukun (o) → /oo pattern
        assert "/oo" in pattern or pattern == "/oo"

    def test_super_heavy_syllable_cvcc(self):
        """Test word with super-heavy CVCC syllable."""
        pattern = text_to_phonetic_pattern("دَرْس")
        # دَرْ forms heavy syllable (/o), س is sukun (o) → /oo pattern
        assert pattern == "/oo" or "/o" in pattern
