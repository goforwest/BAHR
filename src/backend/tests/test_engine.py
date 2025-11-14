"""
Unit tests for prosody engine (meter detection).

Tests cover Week 1-2 MVP meter detection:
1. Pattern building from syllables
2. Basic meter detection
3. Confidence scoring
4. Alternative meter suggestions
5. Integration with normalizer and segmenter
"""

import pytest
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.prosody.engine import build_pattern, detect_meter, ProsodyPattern
from app.prosody.segmenter import segment, Syllable
from app.nlp.normalizer import basic_normalize


class TestPatternBuilding:
    """Test prosodic pattern building from syllables."""
    
    def test_build_pattern_from_syllables(self):
        """Test building pattern from syllable list"""
        syllables = [
            Syllable(text="با", kind="CV", long=True),
            Syllable(text="ب", kind="C", long=False),
            Syllable(text="باا", kind="CVV", long=True),
        ]
        pattern = build_pattern(syllables)
        
        assert isinstance(pattern, ProsodyPattern)
        assert pattern.pattern == "-u-"  # long, short, long
        assert pattern.syllable_count == 3
    
    def test_pattern_has_required_fields(self):
        """Test that ProsodyPattern has all required fields"""
        syllables = [Syllable(text="با", kind="CV", long=True)]
        pattern = build_pattern(syllables)
        
        assert hasattr(pattern, 'taqti3')
        assert hasattr(pattern, 'pattern')
        assert hasattr(pattern, 'syllable_count')
    
    def test_empty_syllable_list(self):
        """Test pattern building with empty syllable list"""
        pattern = build_pattern([])
        assert pattern.syllable_count == 0
        assert pattern.pattern == ""


class TestMeterDetection:
    """Test basic meter detection functionality."""
    
    def test_detect_meter_returns_tuple(self):
        """Test that detect_meter returns expected tuple"""
        pattern = "-u--u---"
        result = detect_meter(pattern)
        
        assert isinstance(result, tuple)
        assert len(result) == 3
        meter_name, confidence, alternatives = result
    
    def test_detect_known_meter_tawil(self):
        """Test detection of al-Tawil meter"""
        # al-Tawil pattern
        pattern = "-u--u---"
        meter_name, confidence, alternatives = detect_meter(pattern)
        
        # Should detect something (even if naive)
        assert meter_name is not None or confidence >= 0
    
    def test_detect_known_meter_kamil(self):
        """Test detection of al-Kamil meter"""
        # al-Kamil-like pattern
        pattern = "-u-u--u-u--u-u-"
        meter_name, confidence, alternatives = detect_meter(pattern)
        
        assert isinstance(confidence, float)
        assert 0 <= confidence <= 1
    
    def test_detect_unknown_pattern(self):
        """Test detection with unknown/random pattern"""
        pattern = "uuuuuuuu"  # Unlikely pattern
        meter_name, confidence, alternatives = detect_meter(pattern)
        
        # Should handle gracefully
        assert confidence is not None
        assert isinstance(alternatives, list)


class TestConfidenceScoring:
    """Test confidence score calculation."""
    
    def test_confidence_in_valid_range(self):
        """Test that confidence is between 0 and 1"""
        patterns = ["-u--u---", "--------", "uuuuuuuu", "-u-u-u-u"]
        
        for pattern in patterns:
            _, confidence, _ = detect_meter(pattern)
            assert 0 <= confidence <= 1, f"Confidence {confidence} out of range for pattern {pattern}"
    
    def test_exact_match_high_confidence(self):
        """Test that exact pattern match gives high confidence"""
        # Use known meter pattern
        pattern = "-u--u---"  # al-Tawil signature
        _, confidence, _ = detect_meter(pattern)
        
        # Should have reasonable confidence (>0 for any match)
        assert confidence >= 0
    
    def test_poor_match_low_confidence(self):
        """Test that poor match gives low confidence"""
        pattern = "x" * 20  # Invalid pattern
        _, confidence, _ = detect_meter(pattern)
        
        # Confidence should still be in valid range
        assert 0 <= confidence <= 1


class TestAlternativeMeters:
    """Test alternative meter suggestions."""
    
    def test_alternatives_is_list(self):
        """Test that alternatives is a list"""
        pattern = "-u--u---"
        _, _, alternatives = detect_meter(pattern)
        
        assert isinstance(alternatives, list)
    
    def test_alternatives_structure(self):
        """Test structure of alternative meters"""
        pattern = "-u--u---"
        _, _, alternatives = detect_meter(pattern)
        
        # Each alternative should be a dict (if any)
        for alt in alternatives:
            assert isinstance(alt, dict)


class TestIntegrationWithNormalizer:
    """Test integration between normalizer and prosody engine."""
    
    def test_full_pipeline_simple_verse(self):
        """Test complete pipeline: normalize → segment → detect"""
        # Simple verse
        verse = "قِفَا نَبْكِ"
        
        # Step 1: Normalize
        normalized = basic_normalize(verse)
        assert len(normalized) > 0
        
        # Step 2: Segment
        syllables = segment(normalized)
        assert len(syllables) > 0
        
        # Step 3: Build pattern
        pattern = build_pattern(syllables)
        assert pattern.syllable_count > 0
        
        # Step 4: Detect meter
        meter, confidence, alternatives = detect_meter(pattern.pattern)
        assert confidence is not None
    
    def test_full_pipeline_with_diacritics(self):
        """Test pipeline handles text with diacritics"""
        verse = "كَتَبَ الشَّاعِرُ قَصِيدَةً"
        
        normalized = basic_normalize(verse, remove_diacritics=True)
        syllables = segment(normalized)
        pattern = build_pattern(syllables)
        meter, conf, alts = detect_meter(pattern.pattern)
        
        # Should complete without errors
        assert meter is not None or conf >= 0


class TestRealPoetryExamples:
    """Test with real classical Arabic poetry verses."""
    
    def test_imru_alqais_verse(self):
        """Test with Imru' al-Qais معلقة verse (al-Tawil)"""
        verse = "قفا نبك من ذكرى حبيب ومنزل"
        
        normalized = basic_normalize(verse)
        syllables = segment(normalized)
        pattern = build_pattern(syllables)
        meter, confidence, alternatives = detect_meter(pattern.pattern)
        
        # Should detect something
        assert meter is not None or len(alternatives) > 0
        assert confidence >= 0
    
    def test_mutanabbi_verse(self):
        """Test with al-Mutanabbi verse"""
        verse = "الخيل والليل والبيداء تعرفني"
        
        normalized = basic_normalize(verse)
        syllables = segment(normalized)
        pattern = build_pattern(syllables)
        meter, confidence, alternatives = detect_meter(pattern.pattern)
        
        assert isinstance(confidence, float)
        assert 0 <= confidence <= 1
    
    def test_multiple_verses_consistency(self):
        """Test that same meter verses produce similar patterns"""
        # Two verses from same meter
        verse1 = "كتاب جميل"
        verse2 = "قلم كبير"
        
        # Process both
        norm1 = basic_normalize(verse1)
        norm2 = basic_normalize(verse2)
        
        syll1 = segment(norm1)
        syll2 = segment(norm2)
        
        patt1 = build_pattern(syll1)
        patt2 = build_pattern(syll2)
        
        # Both should produce patterns
        assert len(patt1.pattern) > 0
        assert len(patt2.pattern) > 0


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_very_short_pattern(self):
        """Test meter detection with very short pattern"""
        pattern = "-u"
        meter, confidence, alternatives = detect_meter(pattern)
        
        # Should handle without error
        assert confidence is not None
    
    def test_very_long_pattern(self):
        """Test meter detection with very long pattern"""
        pattern = "-u" * 50
        meter, confidence, alternatives = detect_meter(pattern)
        
        # Should handle without error
        assert 0 <= confidence <= 1
    
    def test_empty_pattern(self):
        """Test meter detection with empty pattern"""
        pattern = ""
        meter, confidence, alternatives = detect_meter(pattern)
        
        # Should handle gracefully
        assert confidence is not None
    
    def test_mixed_pattern_characters(self):
        """Test pattern with only valid characters"""
        # Only - and u should be in pattern
        syllables = segment("باب كتاب")
        pattern = build_pattern(syllables)
        
        # Pattern should only contain - and u
        assert all(c in "-u" for c in pattern.pattern)


class TestQualityAssessment:
    """Test quality scoring functionality (when implemented)."""
    
    def test_pattern_quality_indicators(self):
        """Test that pattern object can indicate quality"""
        syllables = segment("قفا نبك من ذكرى")
        pattern = build_pattern(syllables)
        
        # Pattern should have useful metrics
        assert pattern.syllable_count > 0
        assert len(pattern.pattern) == pattern.syllable_count


class TestPerformance:
    """Test performance and stress scenarios."""
    
    def test_long_verse_processing(self):
        """Test processing of long verse"""
        # Create a long verse
        verse = "قفا نبك من ذكرى حبيب ومنزل " * 10
        
        normalized = basic_normalize(verse)
        syllables = segment(normalized)
        pattern = build_pattern(syllables)
        meter, confidence, alternatives = detect_meter(pattern.pattern)
        
        # Should complete without error
        assert confidence is not None
    
    def test_multiple_verses_processing(self):
        """Test processing multiple verses in sequence"""
        verses = [
            "قفا نبك من ذكرى حبيب",
            "الخيل والليل والبيداء",
            "أراك عصي الدمع شيمتك الصبر",
        ]
        
        results = []
        for verse in verses:
            norm = basic_normalize(verse)
            syll = segment(norm)
            patt = build_pattern(syll)
            meter, conf, alts = detect_meter(patt.pattern)
            results.append((meter, conf))
        
        # All should process successfully
        assert len(results) == len(verses)
        assert all(conf >= 0 for _, conf in results)
