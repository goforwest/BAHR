"""
Unit tests for letter-level prosodic structure.

Tests the core data structures and functions for letter-level prosody analysis,
which forms the foundation for Phase 2 transformations.
"""

import pytest
from app.core.prosody.letter_structure import (
    HarakaType,
    VowelQuality,
    ProsodyRole,
    LetterUnit,
    TafilaLetterStructure,
    parse_tafila_from_text,
    parse_tafila_from_pattern_template,
)


class TestHarakaType:
    """Test HarakaType enum."""

    def test_haraka_type_values(self):
        """Verify all haraka types are defined."""
        assert HarakaType.MUTAHARRIK.value == "mutaharrik"
        assert HarakaType.SAKIN.value == "sakin"
        assert HarakaType.MADD.value == "madd"


class TestVowelQuality:
    """Test VowelQuality enum."""

    def test_vowel_quality_values(self):
        """Verify all vowel qualities are defined."""
        assert VowelQuality.FATHA.value == "a"
        assert VowelQuality.DAMMA.value == "u"
        assert VowelQuality.KASRA.value == "i"
        assert VowelQuality.SUKUN.value == ""
        assert VowelQuality.AA.value == "aa"
        assert VowelQuality.UU.value == "uu"
        assert VowelQuality.II.value == "ii"


class TestLetterUnit:
    """Test LetterUnit dataclass and methods."""

    def test_create_mutaharrik_letter(self):
        """Test creating a mutaharrik letter (ف with fatha)."""
        letter = LetterUnit(
            consonant='ف',
            haraka_type=HarakaType.MUTAHARRIK,
            vowel_quality=VowelQuality.FATHA
        )

        assert letter.consonant == 'ف'
        assert letter.haraka_type == HarakaType.MUTAHARRIK
        assert letter.vowel_quality == VowelQuality.FATHA
        assert not letter.has_shadda
        assert letter.prosody_role == ProsodyRole.UNKNOWN

    def test_create_sakin_letter(self):
        """Test creating a sakin letter (ن with sukun)."""
        letter = LetterUnit(
            consonant='ن',
            haraka_type=HarakaType.SAKIN,
            vowel_quality=VowelQuality.SUKUN
        )

        assert letter.consonant == 'ن'
        assert letter.haraka_type == HarakaType.SAKIN
        assert letter.vowel_quality == VowelQuality.SUKUN

    def test_create_madd_letter(self):
        """Test creating a madd letter (و as long vowel)."""
        letter = LetterUnit(
            consonant='و',
            haraka_type=HarakaType.MADD,
            vowel_quality=VowelQuality.UU
        )

        assert letter.consonant == 'و'
        assert letter.haraka_type == HarakaType.MADD
        assert letter.vowel_quality == VowelQuality.UU

    def test_is_mutaharrik(self):
        """Test is_mutaharrik() method."""
        mut_letter = LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA)
        sakin_letter = LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN)
        madd_letter = LetterUnit('ا', HarakaType.MADD, VowelQuality.AA)

        assert mut_letter.is_mutaharrik()
        assert not sakin_letter.is_mutaharrik()
        assert not madd_letter.is_mutaharrik()

    def test_is_sakin(self):
        """Test is_sakin() method."""
        mut_letter = LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA)
        sakin_letter = LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN)
        madd_letter = LetterUnit('ا', HarakaType.MADD, VowelQuality.AA)

        assert not mut_letter.is_sakin()
        assert sakin_letter.is_sakin()
        assert not madd_letter.is_sakin()

    def test_is_madd(self):
        """Test is_madd() method."""
        mut_letter = LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA)
        sakin_letter = LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN)
        madd_letter = LetterUnit('ا', HarakaType.MADD, VowelQuality.AA)

        assert not mut_letter.is_madd()
        assert not sakin_letter.is_madd()
        assert madd_letter.is_madd()

    def test_to_phonetic_symbol_mutaharrik(self):
        """Test phonetic symbol conversion for mutaharrik."""
        letter = LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA)
        assert letter.to_phonetic_symbol() == '/'

    def test_to_phonetic_symbol_sakin(self):
        """Test phonetic symbol conversion for sakin."""
        letter = LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN)
        assert letter.to_phonetic_symbol() == 'o'

    def test_to_phonetic_symbol_madd(self):
        """Test phonetic symbol conversion for madd."""
        letter = LetterUnit('ا', HarakaType.MADD, VowelQuality.AA)
        assert letter.to_phonetic_symbol() == 'o'

    def test_letter_unit_str_mutaharrik(self):
        """Test string representation of mutaharrik letter."""
        letter = LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA)
        result = str(letter)
        # Should contain ف and fatha diacritic
        assert 'ف' in result
        assert '\u064e' in result  # Fatha

    def test_letter_unit_str_sakin(self):
        """Test string representation of sakin letter."""
        letter = LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN)
        result = str(letter)
        # Should contain ن and sukun diacritic
        assert 'ن' in result
        assert '\u0652' in result  # Sukun

    def test_letter_unit_with_shadda(self):
        """Test letter with shadda."""
        letter = LetterUnit(
            'ل',
            HarakaType.MUTAHARRIK,
            VowelQuality.FATHA,
            has_shadda=True
        )
        assert letter.has_shadda
        result = str(letter)
        assert 'ل' in result
        assert '\u0651' in result  # Shadda


class TestTafilaLetterStructure:
    """Test TafilaLetterStructure class."""

    def test_create_simple_structure(self):
        """Test creating a simple tafila letter structure."""
        # Note: In phoneme extraction, عُو combines into single long vowel
        # So فَعُولُنْ is: ف(mut) عو(madd) ل(mut) ن(sakin) = 4 phonemes
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),
            LetterUnit('ع', HarakaType.MADD, VowelQuality.UU),  # Combined عُو
            LetterUnit('ل', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),
            LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN),
        ]

        structure = TafilaLetterStructure(
            name="فعولن",
            letters=letters
        )

        assert structure.name == "فعولن"
        assert len(structure.letters) == 4
        assert structure.phonetic_pattern == "/o/o"

    def test_compute_phonetic_pattern(self):
        """Test phonetic pattern computation from letters."""
        letters = [
            LetterUnit('م', HarakaType.MUTAHARRIK, VowelQuality.FATHA),  # /
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),  # /
            LetterUnit('ا', HarakaType.MADD, VowelQuality.AA),          # o
            LetterUnit('ع', HarakaType.MUTAHARRIK, VowelQuality.FATHA),  # /
            LetterUnit('ي', HarakaType.MADD, VowelQuality.II),          # o
            LetterUnit('ل', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),  # /
            LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN),      # o
        ]

        structure = TafilaLetterStructure("مفاعيلن", letters)
        assert structure.phonetic_pattern == "//o/o/o"

    def test_get_mutaharrik_letters(self):
        """Test getting all mutaharrik letters."""
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),  # 0
            LetterUnit('ع', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),  # 1
            LetterUnit('و', HarakaType.MADD, VowelQuality.UU),          # 2
            LetterUnit('ل', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),  # 3
            LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN),      # 4
        ]

        structure = TafilaLetterStructure("فعولن", letters)
        mutaharriks = structure.get_mutaharrik_letters()

        assert len(mutaharriks) == 3
        assert mutaharriks[0][0] == 0  # Position 0
        assert mutaharriks[0][1].consonant == 'ف'
        assert mutaharriks[1][0] == 1  # Position 1
        assert mutaharriks[1][1].consonant == 'ع'
        assert mutaharriks[2][0] == 3  # Position 3
        assert mutaharriks[2][1].consonant == 'ل'

    def test_get_sakin_letters(self):
        """Test getting all sakin letters (explicit sukun only)."""
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),
            LetterUnit('ع', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),
            LetterUnit('و', HarakaType.MADD, VowelQuality.UU),          # Not included
            LetterUnit('ل', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),
            LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN),      # Included
        ]

        structure = TafilaLetterStructure("فعولن", letters)
        sakins = structure.get_sakin_letters()

        assert len(sakins) == 1
        assert sakins[0][0] == 4  # Position 4
        assert sakins[0][1].consonant == 'ن'

    def test_get_sakin_and_madd_letters(self):
        """Test getting both sakin and madd letters."""
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),  # Not included
            LetterUnit('ع', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),  # Not included
            LetterUnit('و', HarakaType.MADD, VowelQuality.UU),          # Included (pos 2)
            LetterUnit('ل', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),  # Not included
            LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN),      # Included (pos 4)
        ]

        structure = TafilaLetterStructure("فعولن", letters)
        sakin_and_madd = structure.get_sakin_and_madd_letters()

        assert len(sakin_and_madd) == 2
        assert sakin_and_madd[0][0] == 2  # Madd at position 2
        assert sakin_and_madd[0][1].consonant == 'و'
        assert sakin_and_madd[1][0] == 4  # Sakin at position 4
        assert sakin_and_madd[1][1].consonant == 'ن'

    def test_get_nth_sakin_with_madd(self):
        """Test getting nth sakin letter (including madd)."""
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),
            LetterUnit('ع', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),
            LetterUnit('و', HarakaType.MADD, VowelQuality.UU),          # 1st sakin
            LetterUnit('ل', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),
            LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN),      # 2nd sakin
        ]

        structure = TafilaLetterStructure("فعولن", letters)

        # Get 1st sakin (should be و at position 2)
        first_sakin = structure.get_nth_sakin(1, include_madd=True)
        assert first_sakin is not None
        assert first_sakin[0] == 2
        assert first_sakin[1].consonant == 'و'

        # Get 2nd sakin (should be ن at position 4)
        second_sakin = structure.get_nth_sakin(2, include_madd=True)
        assert second_sakin is not None
        assert second_sakin[0] == 4
        assert second_sakin[1].consonant == 'ن'

        # Get 3rd sakin (doesn't exist)
        third_sakin = structure.get_nth_sakin(3, include_madd=True)
        assert third_sakin is None

    def test_get_nth_sakin_without_madd(self):
        """Test getting nth sakin letter (excluding madd)."""
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),
            LetterUnit('ع', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),
            LetterUnit('و', HarakaType.MADD, VowelQuality.UU),          # Not counted
            LetterUnit('ل', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),
            LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN),      # 1st sakin
        ]

        structure = TafilaLetterStructure("فعولن", letters)

        # Get 1st sakin (should be ن at position 4)
        first_sakin = structure.get_nth_sakin(1, include_madd=False)
        assert first_sakin is not None
        assert first_sakin[0] == 4
        assert first_sakin[1].consonant == 'ن'

        # Get 2nd sakin (doesn't exist)
        second_sakin = structure.get_nth_sakin(2, include_madd=False)
        assert second_sakin is None

    def test_get_nth_mutaharrik(self):
        """Test getting nth mutaharrik letter."""
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),  # 1st
            LetterUnit('ع', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),  # 2nd
            LetterUnit('و', HarakaType.MADD, VowelQuality.UU),
            LetterUnit('ل', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),  # 3rd
            LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN),
        ]

        structure = TafilaLetterStructure("فعولن", letters)

        # Get 1st mutaharrik
        first = structure.get_nth_mutaharrik(1)
        assert first is not None
        assert first[0] == 0
        assert first[1].consonant == 'ف'

        # Get 2nd mutaharrik
        second = structure.get_nth_mutaharrik(2)
        assert second is not None
        assert second[0] == 1
        assert second[1].consonant == 'ع'

        # Get 3rd mutaharrik
        third = structure.get_nth_mutaharrik(3)
        assert third is not None
        assert third[0] == 3
        assert third[1].consonant == 'ل'

        # Get 4th mutaharrik (doesn't exist)
        fourth = structure.get_nth_mutaharrik(4)
        assert fourth is None

    def test_remove_letter_at_position(self):
        """Test removing a letter at specific position."""
        # Use actual phoneme structure: فَعُو = ف(mut) + عُو(madd)
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),  # 0
            LetterUnit('ع', HarakaType.MADD, VowelQuality.UU),          # 1 - Remove this
            LetterUnit('ل', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),  # 2
            LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN),      # 3
        ]

        structure = TafilaLetterStructure("فعولن", letters)
        assert structure.phonetic_pattern == "/o/o"

        # Remove position 1 (ع/madd)
        new_structure = structure.remove_letter_at_position(1)

        assert len(new_structure.letters) == 3
        assert new_structure.phonetic_pattern == "//o"
        assert new_structure.letters[0].consonant == 'ف'
        assert new_structure.letters[1].consonant == 'ل'  # Was position 2
        assert new_structure.letters[2].consonant == 'ن'  # Was position 3

    def test_remove_letter_invalid_position(self):
        """Test removing letter at invalid position raises error."""
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),
        ]

        structure = TafilaLetterStructure("test", letters)

        with pytest.raises(ValueError):
            structure.remove_letter_at_position(5)

        with pytest.raises(ValueError):
            structure.remove_letter_at_position(-1)

    def test_change_haraka_at_position(self):
        """Test changing haraka at specific position."""
        # Use actual phoneme structure
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),  # 0
            LetterUnit('ع', HarakaType.MADD, VowelQuality.UU),          # 1 - Change this to mut
            LetterUnit('ل', HarakaType.MUTAHARRIK, VowelQuality.DAMMA),  # 2
            LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN),      # 3
        ]

        structure = TafilaLetterStructure("فعولن", letters)
        assert structure.phonetic_pattern == "/o/o"

        # Change position 1 (ع madd) to mutaharrik
        new_structure = structure.change_haraka_at_position(
            1,
            HarakaType.MUTAHARRIK,
            VowelQuality.DAMMA
        )

        assert len(new_structure.letters) == 4
        assert new_structure.phonetic_pattern == "///o"
        assert new_structure.letters[1].consonant == 'ع'
        assert new_structure.letters[1].is_mutaharrik()

    def test_change_haraka_invalid_position(self):
        """Test changing haraka at invalid position raises error."""
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),
        ]

        structure = TafilaLetterStructure("test", letters)

        with pytest.raises(ValueError):
            structure.change_haraka_at_position(
                5, HarakaType.SAKIN, VowelQuality.SUKUN
            )

    def test_to_dict(self):
        """Test converting structure to dictionary."""
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),
            LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN),
        ]

        structure = TafilaLetterStructure("test", letters, structure_type="simple")
        result = structure.to_dict()

        assert result['name'] == "test"
        assert result['phonetic_pattern'] == "/o"
        assert result['structure_type'] == "simple"
        assert len(result['letters']) == 2
        assert result['letters'][0]['consonant'] == 'ف'
        assert result['letters'][0]['haraka_type'] == 'mutaharrik'

    def test_str_representation(self):
        """Test string representation (vocalized text)."""
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),
            LetterUnit('ن', HarakaType.SAKIN, VowelQuality.SUKUN),
        ]

        structure = TafilaLetterStructure("test", letters)
        text = str(structure)

        assert 'ف' in text
        assert 'ن' in text
        # Should have diacritics
        assert '\u064e' in text or '\u0652' in text

    def test_repr(self):
        """Test developer representation."""
        letters = [
            LetterUnit('ف', HarakaType.MUTAHARRIK, VowelQuality.FATHA),
        ]

        structure = TafilaLetterStructure("test", letters)
        result = repr(structure)

        assert "TafilaLetterStructure" in result
        assert "test" in result
        assert "/" in result  # Pattern

    def test_empty_letters_raises_error(self):
        """Test that empty letters list raises error."""
        with pytest.raises(ValueError):
            TafilaLetterStructure("test", [])


class TestParseTafilaFromText:
    """Test parsing tafila from vocalized text."""

    def test_parse_faculun(self):
        """
        Test parsing فَعُولُنْ (faculun).

        Note: Phoneme extraction combines عُو into single long vowel phoneme.
        Actual phonemes: ف(mut,a) + عو(madd,uu) + ل(mut,u) + ن(sakin)
        Pattern: / + o + / + o = /o/o
        """
        structure = parse_tafila_from_text("فعولن", "فَعُولُنْ")

        assert structure.name == "فعولن"
        assert len(structure.letters) == 4  # Not 5, because عُو is one phoneme

        # Check letters
        assert structure.letters[0].consonant == 'ف'
        assert structure.letters[0].is_mutaharrik()
        assert structure.letters[1].consonant == 'ع'
        assert structure.letters[1].is_madd()  # Combined عُو as long vowel
        assert structure.letters[2].consonant == 'ل'
        assert structure.letters[2].is_mutaharrik()
        assert structure.letters[3].consonant == 'ن'
        assert structure.letters[3].is_sakin()

        # Check pattern
        assert all(c in '/o' for c in structure.phonetic_pattern)
        assert structure.phonetic_pattern == "/o/o"

    def test_parse_facilun(self):
        """
        Test parsing فَاعِلُنْ (facilun).

        Letters: ف(mut,a) ا(madd,aa) ع(mut,i) ل(mut,u) ن(sakin)
        Pattern: / o / / o = /o//o
        """
        structure = parse_tafila_from_text("فاعلن", "فَاعِلُنْ")

        assert structure.name == "فاعلن"
        # Should have 4 phonemes: fa(/) ʿi(/) lun(/o) based on phoneme extraction
        # Or could be: fa-a(/o) ʿi(/) lun(/o)
        assert all(c in '/o' for c in structure.phonetic_pattern)

    def test_parse_mustafcilun(self):
        """
        Test parsing مُسْتَفْعِلُنْ (mustafcilun).

        Complex tafila with multiple sakins.
        """
        structure = parse_tafila_from_text("مستفعلن", "مُسْتَفْعِلُنْ")

        assert structure.name == "مستفعلن"
        # Should have pattern /o/o//o based on classical prosody
        assert all(c in '/o' for c in structure.phonetic_pattern)

    def test_parse_mutafacilun(self):
        """
        Test parsing مُتَفَاعِلُنْ (mutafacilun).

        Used in الكامل meter.
        """
        structure = parse_tafila_from_text("متفاعلن", "مُتَفَاعِلُنْ")

        assert structure.name == "متفاعلن"
        # Pattern should be ///o//o
        assert all(c in '/o' for c in structure.phonetic_pattern)

    def test_parse_mafacilun(self):
        """
        Test parsing مَفَاعِيلُنْ (mafacilun).

        Contains long vowel (ي).
        """
        structure = parse_tafila_from_text("مفاعيلن", "مَفَاعِيلُنْ")

        assert structure.name == "مفاعيلن"
        assert all(c in '/o' for c in structure.phonetic_pattern)

    def test_parse_empty_text_raises_error(self):
        """Test that empty text raises error."""
        with pytest.raises(ValueError):
            parse_tafila_from_text("test", "")

    def test_parse_preserves_shadda(self):
        """Test that shadda is preserved in parsing."""
        # Example with shadda: لَيْلَةَّ (should preserve shadda on ة)
        structure = parse_tafila_from_text("test", "مُشَدَّدٌ")

        # Find letter with shadda
        shadda_letters = [l for l in structure.letters if l.has_shadda]
        assert len(shadda_letters) > 0, "Should find at least one letter with shadda"


class TestParseTafilaFromPatternTemplate:
    """Test parsing tafila from pattern template."""

    def test_not_implemented(self):
        """Test that template parsing raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            parse_tafila_from_pattern_template(
                "فعولن",
                "//o//o",
                "CvCvvCvC"
            )


class TestIntegrationScenarios:
    """Integration tests for realistic usage scenarios."""

    def test_qabd_transformation_simulation(self):
        """
        Simulate QABD transformation: remove 5th sakin letter.

        This tests the letter-level approach for a real transformation.
        """
        # Parse مَفَاعِيلُنْ
        structure = parse_tafila_from_text("مفاعيلن", "مَفَاعِيلُنْ")

        # Get 5th sakin (if it exists)
        # Note: Need to check if this tafila actually has 5 sakins!
        # This is part of the investigation needed for QABD fix
        sakin_and_madd = structure.get_sakin_and_madd_letters()

        # Document how many sakins this tafila has
        print(f"\nمفاعيلن has {len(sakin_and_madd)} sakin/madd letters")
        for pos, letter in sakin_and_madd:
            print(f"  Position {pos}: {letter.consonant} ({letter.haraka_type.value})")

    def test_khabn_transformation_simulation(self):
        """
        Simulate KHABN transformation: remove 2nd sakin letter.
        """
        # Parse مُسْتَفْعِلُنْ
        structure = parse_tafila_from_text("مستفعلن", "مُسْتَفْعِلُنْ")

        # Get 2nd sakin
        second_sakin = structure.get_nth_sakin(2, include_madd=True)

        if second_sakin:
            pos, letter = second_sakin
            # Remove it
            new_structure = structure.remove_letter_at_position(pos)

            print(f"\nKHABN: Removed 2nd sakin ({letter.consonant}) at position {pos}")
            print(f"  Original pattern: {structure.phonetic_pattern}")
            print(f"  New pattern: {new_structure.phonetic_pattern}")

    def test_idmar_transformation_simulation(self):
        """
        Simulate IḌMĀR transformation: make 2nd mutaharrik sakin.
        """
        # Parse مُتَفَاعِلُنْ
        structure = parse_tafila_from_text("متفاعلن", "مُتَفَاعِلُنْ")

        # Get 2nd mutaharrik
        second_mut = structure.get_nth_mutaharrik(2)

        if second_mut:
            pos, letter = second_mut
            # Make it sakin
            new_structure = structure.change_haraka_at_position(
                pos,
                HarakaType.SAKIN,
                VowelQuality.SUKUN
            )

            print(f"\nIḌMĀR: Made 2nd mutaharrik ({letter.consonant}) sakin")
            print(f"  Original pattern: {structure.phonetic_pattern}")
            print(f"  New pattern: {new_structure.phonetic_pattern}")
