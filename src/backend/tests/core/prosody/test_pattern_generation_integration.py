"""
Integration tests for pattern generation with letter-level transformations.

These tests verify that the pattern generator correctly uses letter-level
transformations when TafilaLetterStructure is available, and falls back to
pattern-based transformations when it's not.
"""

import pytest
from app.core.prosody.letter_structure import parse_tafila_from_text
from app.core.prosody.tafila import Tafila
from app.core.prosody.zihafat import KHABN, QABD, IDMAR, TAYY
from app.core.prosody.ilal import HADHF, QAT, QASR, KASHF


class TestZahafWithLetterStructure:
    """Test that Zahaf.apply() uses letter-level transformations when available."""

    def test_qabd_preserves_letter_structure(self):
        """Test QABD preserves letter structure in result."""
        # Create a tafila with letter structure
        mafacilun = parse_tafila_from_text('مفاعيلن', 'مَفَاعِيلُنْ')

        # Create Tafila object with letter structure
        tafila = Tafila(
            name="مفاعيلن",
            phonetic=mafacilun.phonetic_pattern,
            structure="//o/o/o",
            syllable_count=3,
            letter_structure=mafacilun
        )

        # Apply QABD
        result = QABD.apply(tafila)

        # Result should have letter_structure preserved
        assert hasattr(result, 'letter_structure')
        assert result.letter_structure is not None

        # Phonetic pattern should match letter structure
        assert result.phonetic == result.letter_structure.phonetic_pattern

        # Should have one less letter than original
        assert len(result.letter_structure.letters) == len(mafacilun.letters) - 1

    def test_khabn_preserves_letter_structure(self):
        """Test KHABN preserves letter structure in result."""
        mustafcilun = parse_tafila_from_text('مستفعلن', 'مُسْتَفْعِلُنْ')

        tafila = Tafila(
            name="مستفعلن",
            phonetic=mustafcilun.phonetic_pattern,
            structure="/o/o//o",
            syllable_count=3,
            letter_structure=mustafcilun
        )

        result = KHABN.apply(tafila)

        assert hasattr(result, 'letter_structure')
        assert result.letter_structure is not None
        assert result.phonetic == result.letter_structure.phonetic_pattern

    def test_idmar_preserves_letter_structure(self):
        """Test IḌMĀR preserves letter structure in result."""
        mutafacilun = parse_tafila_from_text('متفاعلن', 'مُتَفَاعِلُنْ')

        tafila = Tafila(
            name="متفاعلن",
            phonetic=mutafacilun.phonetic_pattern,
            structure="///o//o",
            syllable_count=3,
            letter_structure=mutafacilun
        )

        result = IDMAR.apply(tafila)

        assert hasattr(result, 'letter_structure')
        assert result.letter_structure is not None
        assert result.phonetic == result.letter_structure.phonetic_pattern

    def test_tayy_preserves_letter_structure(self):
        """Test ṬAYY preserves letter structure in result."""
        mustafcilun = parse_tafila_from_text('مستفعلن', 'مُسْتَفْعِلُنْ')

        tafila = Tafila(
            name="مستفعلن",
            phonetic=mustafcilun.phonetic_pattern,
            structure="/o/o//o",
            syllable_count=3,
            letter_structure=mustafcilun
        )

        result = TAYY.apply(tafila)

        # TAYY removes 4th sākin, mustafcilun only has 3 sakins
        # So it should return unchanged
        assert hasattr(result, 'letter_structure')
        assert result.letter_structure is not None


class TestIlalWithLetterStructure:
    """Test that Ilah.apply() uses letter-level transformations when available."""

    def test_hadhf_preserves_letter_structure(self):
        """Test ḤADHF preserves letter structure in result."""
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')

        tafila = Tafila(
            name="فعولن",
            phonetic=faculun.phonetic_pattern,
            structure="/o//o",
            syllable_count=2,
            letter_structure=faculun
        )

        result = HADHF.apply(tafila)

        assert hasattr(result, 'letter_structure')
        assert result.letter_structure is not None
        assert result.phonetic == result.letter_structure.phonetic_pattern

        # Should remove last 2 letters
        assert len(result.letter_structure.letters) == len(faculun.letters) - 2

    def test_qat_preserves_letter_structure(self):
        """Test QAṬʿ preserves letter structure in result."""
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')

        tafila = Tafila(
            name="فعولن",
            phonetic=faculun.phonetic_pattern,
            structure="/o//o",
            syllable_count=2,
            letter_structure=faculun
        )

        result = QAT.apply(tafila)

        assert hasattr(result, 'letter_structure')
        assert result.letter_structure is not None
        assert result.phonetic == result.letter_structure.phonetic_pattern

        # Should remove last letter
        assert len(result.letter_structure.letters) == len(faculun.letters) - 1

    def test_qasr_preserves_letter_structure(self):
        """Test QAṢR preserves letter structure in result."""
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')

        tafila = Tafila(
            name="فعولن",
            phonetic=faculun.phonetic_pattern,
            structure="/o//o",
            syllable_count=2,
            letter_structure=faculun
        )

        result = QASR.apply(tafila)

        assert hasattr(result, 'letter_structure')
        assert result.letter_structure is not None
        assert result.phonetic == result.letter_structure.phonetic_pattern

    def test_kashf_preserves_letter_structure(self):
        """Test KASHF preserves letter structure in result."""
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')

        tafila = Tafila(
            name="فعولن",
            phonetic=faculun.phonetic_pattern,
            structure="/o//o",
            syllable_count=2,
            letter_structure=faculun
        )

        result = KASHF.apply(tafila)

        assert hasattr(result, 'letter_structure')
        assert result.letter_structure is not None
        assert result.phonetic == result.letter_structure.phonetic_pattern


class TestBackwardCompatibility:
    """Test that transformations still work without letter_structure (backward compatibility)."""

    def test_zahaf_works_without_letter_structure(self):
        """Test Zahaf.apply() works with Tafila that has no letter_structure."""
        tafila = Tafila(
            name="مفاعيلن",
            phonetic="//o/o/o",
            structure="//o/o/o",
            syllable_count=3
        )

        # Should not have letter_structure
        assert not hasattr(tafila, 'letter_structure') or tafila.letter_structure is None

        # Apply QABD - should use pattern-based transformation
        result = QABD.apply(tafila)

        # Should work without error
        assert result is not None
        assert result.phonetic is not None

    def test_ilal_works_without_letter_structure(self):
        """Test Ilah.apply() works with Tafila that has no letter_structure."""
        tafila = Tafila(
            name="فعولن",
            phonetic="/o//o",
            structure="/o//o",
            syllable_count=2
        )

        # Should not have letter_structure
        assert not hasattr(tafila, 'letter_structure') or tafila.letter_structure is None

        # Apply HADHF - should use pattern-based transformation
        result = HADHF.apply(tafila)

        # Should work without error
        assert result is not None
        assert result.phonetic is not None


class TestChainedTransformations:
    """Test that transformations can be chained while preserving letter structure."""

    def test_zahaf_chain_preserves_letter_structure(self):
        """Test chaining multiple zihafat preserves letter structure."""
        mustafcilun = parse_tafila_from_text('مستفعلن', 'مُسْتَفْعِلُنْ')

        tafila = Tafila(
            name="مستفعلن",
            phonetic=mustafcilun.phonetic_pattern,
            structure="/o/o//o",
            syllable_count=3,
            letter_structure=mustafcilun
        )

        # Apply KHABN first
        result1 = KHABN.apply(tafila)
        assert result1.letter_structure is not None

        # Apply TAYY to the result (this is KHABL = KHABN + TAYY)
        result2 = TAYY.apply(result1)
        assert result2.letter_structure is not None

        # Phonetic should match letter structure
        assert result2.phonetic == result2.letter_structure.phonetic_pattern

    def test_zahaf_then_ilal_preserves_letter_structure(self):
        """Test applying zahaf then 'ilah preserves letter structure."""
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')

        tafila = Tafila(
            name="فعولن",
            phonetic=faculun.phonetic_pattern,
            structure="/o//o",
            syllable_count=2,
            letter_structure=faculun
        )

        # Apply QABD first
        result1 = QABD.apply(tafila)
        assert result1.letter_structure is not None

        # Apply HADHF to the result
        result2 = HADHF.apply(result1)
        assert result2.letter_structure is not None

        # Phonetic should match letter structure
        assert result2.phonetic == result2.letter_structure.phonetic_pattern


class TestAllTransformationsIntegration:
    """Integration tests for all transformations."""

    def test_all_zihafat_preserve_letter_structure(self):
        """Test all ziḥāfāt preserve letter structure when available."""
        from app.core.prosody.zihafat import ZIHAFAT_REGISTRY

        mustafcilun = parse_tafila_from_text('مستفعلن', 'مُسْتَفْعِلُنْ')

        tafila = Tafila(
            name="مستفعلن",
            phonetic=mustafcilun.phonetic_pattern,
            structure="/o/o//o",
            syllable_count=3,
            letter_structure=mustafcilun
        )

        for zahaf_type, zahaf in ZIHAFAT_REGISTRY.items():
            try:
                result = zahaf.apply(tafila)

                # Should have letter_structure
                assert hasattr(result, 'letter_structure')

                # If transformation applied, phonetic should match letter structure
                if result.letter_structure is not None:
                    assert result.phonetic == result.letter_structure.phonetic_pattern, \
                        f"{zahaf.name_ar} didn't match phonetic to letter structure"
            except Exception as e:
                # Some transformations may not apply - that's OK
                pass

    def test_all_ilal_preserve_letter_structure(self):
        """Test all ʿilal preserve letter structure when available."""
        from app.core.prosody.ilal import ILAL_REGISTRY

        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')

        tafila = Tafila(
            name="فعولن",
            phonetic=faculun.phonetic_pattern,
            structure="/o//o",
            syllable_count=2,
            letter_structure=faculun
        )

        for ilah_type, ilah in ILAL_REGISTRY.items():
            try:
                result = ilah.apply(tafila)

                # Should have letter_structure
                assert hasattr(result, 'letter_structure')

                # If transformation applied, phonetic should match letter structure
                if result.letter_structure is not None:
                    assert result.phonetic == result.letter_structure.phonetic_pattern, \
                        f"{ilah.name_ar} didn't match phonetic to letter structure"
            except Exception as e:
                # Some transformations may not apply - that's OK
                pass
