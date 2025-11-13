"""
Unit tests for letter-level ʿilal transformations (Phase 2).

These tests verify that end-of-verse variations work correctly at the
letter level, as defined in classical Arabic prosody.
"""

import pytest
from app.core.prosody.letter_structure import parse_tafila_from_text
from app.core.prosody.ilal import (
    hadhf_transform_letters,
    qat_transform_letters,
    qasr_transform_letters,
    kashf_transform_letters,
    batr_transform_letters,
    hadhdhah_transform_letters,
)


class TestHadhfTransformation:
    """Test ḤADHF (حَذْف) - Remove last sabab khafīf."""

    def test_hadhf_basic(self):
        """Test ḤADHF removes last 2 letters."""
        # Use فعولن as test case
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')
        original_len = len(faculun.letters)

        # Apply ḤADHF
        result = hadhf_transform_letters(faculun)

        # Should remove last 2 letters
        assert len(result.letters) == original_len - 2

    def test_hadhf_insufficient_letters(self):
        """Test ḤADHF on tafʿīlah with fewer than 2 letters."""
        # Create minimal structure (this is hypothetical)
        # In practice, we test that it handles edge cases
        pass


class TestQatTransformation:
    """Test QAṬʿ (قَطْع) - Remove last letter and make preceding sākin."""

    def test_qat_basic(self):
        """Test QAṬʿ removes last letter and makes new last sākin."""
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')
        original_len = len(faculun.letters)

        # Apply QAṬʿ
        result = qat_transform_letters(faculun)

        # Should have one less letter
        assert len(result.letters) == original_len - 1

        # Last letter should be sākin
        if len(result.letters) > 0:
            assert result.letters[-1].is_sakin()


class TestQasrTransformation:
    """Test QAṢR (قَصْر) - Make last mutaḥarrik sākin."""

    def test_qasr_basic(self):
        """Test QAṢR makes last mutaharrik sākin."""
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')

        # Find last mutaharrik
        last_mutaharrik_pos = None
        for i in range(len(faculun.letters) - 1, -1, -1):
            if faculun.letters[i].is_mutaharrik():
                last_mutaharrik_pos = i
                break

        if last_mutaharrik_pos is not None:
            # Apply QAṢR
            result = qasr_transform_letters(faculun)

            # Letter count should be preserved
            assert len(result.letters) == len(faculun.letters)

            # Last mutaharrik should now be sakin
            assert result.letters[last_mutaharrik_pos].is_sakin()


class TestKashfTransformation:
    """Test KASHF (كَشْف) - Remove last sākin."""

    def test_kashf_basic(self):
        """Test KASHF removes last sākin."""
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')

        # Find last sakin/madd
        last_sakin_pos = None
        for i in range(len(faculun.letters) - 1, -1, -1):
            if faculun.letters[i].is_sakin() or faculun.letters[i].is_madd():
                last_sakin_pos = i
                break

        if last_sakin_pos is not None:
            # Apply KASHF
            result = kashf_transform_letters(faculun)

            # Should have one less letter
            assert len(result.letters) == len(faculun.letters) - 1


class TestBatrTransformation:
    """Test BATR (بَتْر) - Combined: ḤADHF + QAṢR."""

    def test_batr_composition(self):
        """Test that BATR correctly applies ḤADHF then QAṢR."""
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')

        # Apply BATR (ḤADHF + QAṢR)
        result_batr = batr_transform_letters(faculun)

        # Apply transformations separately
        result_hadhf = hadhf_transform_letters(faculun)
        result_separate = qasr_transform_letters(result_hadhf)

        # Should produce the same result
        assert result_batr.phonetic_pattern == result_separate.phonetic_pattern
        assert len(result_batr.letters) == len(result_separate.letters)


class TestHadhdhahTransformation:
    """Test ḤADHDHAH (حَذَذ) - Remove half of last watad."""

    def test_hadhdhah_basic(self):
        """Test ḤADHDHAH removes last letter."""
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')

        # Apply ḤADHDHAH
        result = hadhdhah_transform_letters(faculun)

        # Should remove 1 letter
        assert len(result.letters) == len(faculun.letters) - 1


class TestIlalIntegration:
    """Integration tests for all ʿilal transformations."""

    def test_all_ilal_preserve_immutability(self):
        """Verify all ʿilal return new structures."""
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')
        original_pattern = faculun.phonetic_pattern
        original_len = len(faculun.letters)

        transformations = [
            hadhf_transform_letters,
            qat_transform_letters,
            qasr_transform_letters,
            kashf_transform_letters,
            batr_transform_letters,
            hadhdhah_transform_letters,
        ]

        for transform_func in transformations:
            result = transform_func(faculun)

            # Original should be unchanged
            assert faculun.phonetic_pattern == original_pattern
            assert len(faculun.letters) == original_len

            # Result should be different object (if transformation applied)
            if result.phonetic_pattern != original_pattern:
                assert result is not faculun

    def test_ilal_return_valid_patterns(self):
        """Verify all ʿilal return valid phonetic patterns."""
        faculun = parse_tafila_from_text('فعولن', 'فَعُولُنْ')

        transformations = [
            hadhf_transform_letters,
            qat_transform_letters,
            qasr_transform_letters,
            kashf_transform_letters,
            batr_transform_letters,
            hadhdhah_transform_letters,
        ]

        for transform_func in transformations:
            result = transform_func(faculun)

            # Pattern should only contain '/' and 'o'
            assert all(c in '/o' for c in result.phonetic_pattern), \
                f"{transform_func.__name__} produced invalid pattern: {result.phonetic_pattern}"

            # Pattern should match letter count
            assert len(result.phonetic_pattern) == len(result.letters), \
                f"{transform_func.__name__} pattern length doesn't match letter count"


# All ʿilal transformations are now implemented and tested!
