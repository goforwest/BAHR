"""
Tests for pattern similarity and fuzzy matching.

Tests the fuzzy pattern matching algorithm that enables detection of meters
even when verse patterns don't exactly match theoretical patterns.
"""

import pytest
from app.core.prosody.pattern_similarity import (
    PatternSimilarity,
    PatternNormalizer,
    calculate_pattern_similarity,
    find_best_meter_matches,
)


class TestPatternSimilarity:
    """Test similarity calculation between prosodic patterns."""

    def test_identical_patterns_perfect_score(self):
        """Identical patterns should get similarity score of 1.0."""
        pattern = "//o/o//o/o/o"
        similarity = PatternSimilarity.calculate_similarity(pattern, pattern)
        assert similarity == 1.0

    def test_completely_different_patterns_low_score(self):
        """Completely different patterns should get low similarity."""
        pattern1 = "////////"
        pattern2 = "oooooooo"
        similarity = PatternSimilarity.calculate_similarity(pattern1, pattern2)
        assert similarity < 0.5  # Should be quite different

    def test_single_character_difference_high_score(self):
        """Patterns differing by one character should still be similar."""
        pattern1 = "//o/o"
        pattern2 = "//o//o"  # One extra /
        similarity = PatternSimilarity.calculate_similarity(pattern1, pattern2)
        assert similarity > 0.7  # Should be quite similar

    def test_empty_patterns_zero_similarity(self):
        """Empty patterns should return 0.0 similarity."""
        assert PatternSimilarity.calculate_similarity("", "//o/o") == 0.0
        assert PatternSimilarity.calculate_similarity("//o/o", "") == 0.0
        assert PatternSimilarity.calculate_similarity("", "") == 0.0

    def test_length_difference_affects_similarity(self):
        """Longer length differences should reduce similarity."""
        pattern1 = "//o/o"
        pattern2_short = "//o/oo"  # 1 char longer
        pattern2_long = "//o/oooooo"  # Much longer

        sim_short = PatternSimilarity.calculate_similarity(pattern1, pattern2_short)
        sim_long = PatternSimilarity.calculate_similarity(pattern1, pattern2_long)

        assert sim_short > sim_long  # Shorter diff should be more similar

    def test_substitution_vs_insertion(self):
        """Test that substitutions are weighted differently from insertions."""
        base = "//o/o"
        substituted = "/oo/o"  # Changed / → o
        inserted = "//o//o"     # Inserted /

        sim_sub = PatternSimilarity.calculate_similarity(base, substituted)
        sim_ins = PatternSimilarity.calculate_similarity(base, inserted)

        # Both should be similar but may have different costs
        assert 0.5 < sim_sub < 1.0
        assert 0.5 < sim_ins < 1.0

    def test_real_verse_vs_theoretical_pattern(self):
        """Test real verse pattern vs theoretical meter pattern."""
        # Real verse from golden dataset
        verse_pattern = "//o/o//o///o//o/o//o//"

        # Theoretical الطويل pattern
        al_tawil_pattern = "//o/o//o/o/o//o/o//o/o/o"

        similarity = PatternSimilarity.calculate_similarity(
            verse_pattern,
            al_tawil_pattern
        )

        # Should be reasonably similar (same meter, some variations)
        assert similarity > 0.6
        assert similarity < 1.0

    def test_symmetry(self):
        """Similarity should be symmetric: sim(A,B) == sim(B,A)."""
        pattern1 = "//o/o//o"
        pattern2 = "/o/o///o"

        sim_forward = PatternSimilarity.calculate_similarity(pattern1, pattern2)
        sim_backward = PatternSimilarity.calculate_similarity(pattern2, pattern1)

        assert abs(sim_forward - sim_backward) < 0.001  # Should be equal (within floating point error)


class TestWeightedEditDistance:
    """Test the weighted edit distance algorithm."""

    def test_zero_distance_for_identical(self):
        """Identical patterns should have zero edit distance."""
        pattern = "//o/o"
        distance = PatternSimilarity._weighted_edit_distance(pattern, pattern)
        assert distance == 0.0

    def test_single_substitution_cost(self):
        """Test cost of single character substitution."""
        pattern1 = "//o/o"
        pattern2 = "/oo/o"  # One substitution: / → o
        distance = PatternSimilarity._weighted_edit_distance(pattern1, pattern2)

        # Should be approximately equal to substitution weight
        expected_cost = PatternSimilarity.WEIGHTS['substitute_weight']
        assert abs(distance - expected_cost) < 0.1

    def test_single_insertion_cost(self):
        """Test cost of single character insertion."""
        pattern1 = "//o/o"
        pattern2 = "//o//o"  # One insertion: /
        distance = PatternSimilarity._weighted_edit_distance(pattern1, pattern2)

        # Should include insert cost + length penalty
        expected_cost = PatternSimilarity.WEIGHTS['insert_delete'] + PatternSimilarity.WEIGHTS['length_penalty']
        assert abs(distance - expected_cost) < 0.1

    def test_single_deletion_cost(self):
        """Test cost of single character deletion."""
        pattern1 = "//o//o"
        pattern2 = "//o/o"  # One deletion: /
        distance = PatternSimilarity._weighted_edit_distance(pattern1, pattern2)

        # Should include delete cost + length penalty
        expected_cost = PatternSimilarity.WEIGHTS['insert_delete'] + PatternSimilarity.WEIGHTS['length_penalty']
        assert abs(distance - expected_cost) < 0.1


class TestFindBestMatches:
    """Test finding best matching meters from candidates."""

    def test_find_exact_match_first(self):
        """Exact match should be returned first with score 1.0."""
        input_pattern = "//o/o//o/o/o"
        candidates = [
            ("الكامل", "///o//o///o//o"),
            ("الطويل", "//o/o//o/o/o"),  # Exact match
            ("البسيط", "/o/o//o/o//o"),
        ]

        matches = PatternSimilarity.find_best_matches(input_pattern, candidates, top_k=3)

        assert len(matches) == 3
        assert matches[0][0] == "الطويل"  # Should be first
        assert matches[0][2] == 1.0        # Perfect score

    def test_top_k_limiting(self):
        """Should return at most top_k matches."""
        input_pattern = "//o/o"
        candidates = [
            (f"meter_{i}", "//o/o" + "o" * i)
            for i in range(10)
        ]

        matches = PatternSimilarity.find_best_matches(input_pattern, candidates, top_k=3)
        assert len(matches) <= 3

    def test_min_similarity_threshold(self):
        """Should only return matches above min_similarity."""
        input_pattern = "////////"  # All light syllables
        candidates = [
            ("similar", "///////o"),    # Very similar
            ("different", "oooooooo"),  # Very different
        ]

        matches = PatternSimilarity.find_best_matches(
            input_pattern,
            candidates,
            min_similarity=0.7,  # High threshold
            top_k=10
        )

        # Should only include the similar one
        assert len(matches) == 1
        assert matches[0][0] == "similar"

    def test_sorted_by_similarity(self):
        """Matches should be sorted by similarity (highest first)."""
        input_pattern = "//o/o"
        candidates = [
            ("low", "oo/oo"),          # Low similarity (but above default min)
            ("high", "//o/o"),         # High similarity (exact)
            ("medium", "//o//o"),      # Medium similarity
        ]

        matches = PatternSimilarity.find_best_matches(
            input_pattern,
            candidates,
            min_similarity=0.3,  # Lower threshold to include "low"
            top_k=3
        )

        # Check ordering
        assert matches[0][0] == "high"
        assert matches[1][0] == "medium"
        # "low" might not be included if similarity is too low, so check length
        if len(matches) == 3:
            assert matches[2][0] == "low"

        # Check scores are descending
        assert matches[0][2] >= matches[1][2]
        if len(matches) == 3:
            assert matches[1][2] >= matches[2][2]

    def test_empty_candidates_returns_empty(self):
        """Empty candidate list should return empty results."""
        matches = PatternSimilarity.find_best_matches("//o/o", [], top_k=5)
        assert matches == []

    def test_empty_input_pattern_returns_empty(self):
        """Empty input pattern should return empty results."""
        candidates = [("meter1", "//o/o")]
        matches = PatternSimilarity.find_best_matches("", candidates, top_k=5)
        assert matches == []


class TestCalculateConfidence:
    """Test confidence score calculation."""

    def test_high_similarity_high_confidence(self):
        """High similarity should give high confidence."""
        confidence = PatternSimilarity.calculate_confidence(0.9, 20)
        assert confidence > 0.85

    def test_low_similarity_low_confidence(self):
        """Low similarity should give low confidence."""
        confidence = PatternSimilarity.calculate_confidence(0.5, 20)
        assert confidence < 0.7

    def test_longer_patterns_boost_confidence(self):
        """Longer patterns should get confidence boost."""
        conf_short = PatternSimilarity.calculate_confidence(0.8, 5)   # Short pattern
        conf_long = PatternSimilarity.calculate_confidence(0.8, 25)   # Long pattern

        assert conf_long > conf_short  # Longer should be more confident

    def test_confidence_capped_at_one(self):
        """Confidence should never exceed 1.0."""
        confidence = PatternSimilarity.calculate_confidence(0.99, 100)
        assert confidence <= 1.0

    def test_confidence_never_negative(self):
        """Confidence should never be negative."""
        confidence = PatternSimilarity.calculate_confidence(0.0, 10)
        assert confidence >= 0.0


class TestPatternNormalizer:
    """Test pattern normalization utilities."""

    def test_is_valid_pattern_accepts_valid(self):
        """Valid patterns (only / and o) should be accepted."""
        assert PatternNormalizer.is_valid_pattern("//o/o") is True
        assert PatternNormalizer.is_valid_pattern("/") is True
        assert PatternNormalizer.is_valid_pattern("o") is True
        assert PatternNormalizer.is_valid_pattern("//oooo//") is True

    def test_is_valid_pattern_rejects_invalid(self):
        """Invalid patterns should be rejected."""
        assert PatternNormalizer.is_valid_pattern("abc") is False
        assert PatternNormalizer.is_valid_pattern("//x/o") is False
        assert PatternNormalizer.is_valid_pattern("123") is False
        assert PatternNormalizer.is_valid_pattern("") is False

    def test_normalize_returns_pattern(self):
        """Normalize should return a valid pattern."""
        pattern = "//o/o"
        normalized = PatternNormalizer.normalize(pattern)
        assert PatternNormalizer.is_valid_pattern(normalized)
        # Currently returns as-is
        assert normalized == pattern


class TestConvenienceFunctions:
    """Test convenience wrapper functions."""

    def test_calculate_pattern_similarity_wrapper(self):
        """Test convenience wrapper for similarity calculation."""
        similarity = calculate_pattern_similarity("//o/o", "//o/o")
        assert similarity == 1.0

    def test_find_best_meter_matches_wrapper(self):
        """Test convenience wrapper for finding matches."""
        verse_pattern = "//o/o"
        meter_patterns = [
            ("الطويل", "//o/o//o/o/o"),
            ("الكامل", "///o//o///o//o"),
        ]

        matches = find_best_meter_matches(verse_pattern, meter_patterns, top_k=2)

        assert len(matches) <= 2
        assert all(len(match) == 3 for match in matches)  # (name, pattern, score)
        assert all(isinstance(match[2], float) for match in matches)  # Score is float


class TestRealWorldScenarios:
    """Test with real-world examples from golden dataset."""

    def test_golden_dataset_verse_001(self):
        """Test with actual verse from golden dataset."""
        # Verse #001: قِفا نَبْكِ مِن ذِكرى حَبيبٍ ومَنْزِلِ
        verse_pattern = "//o/o//o///o//o/o//o//"

        # Expected meter: الطويل
        al_tawil_base = "//o/o//o/o/o//o/o//o/o/o"

        similarity = calculate_pattern_similarity(verse_pattern, al_tawil_base)

        # Should be reasonably similar despite differences
        assert similarity > 0.6  # Should recognize as الطويل
        assert similarity < 1.0  # But not perfect match

    def test_multiple_meter_candidates(self):
        """Test matching against multiple meter candidates."""
        # Simplified verse pattern
        verse_pattern = "//o/o//o/o"

        candidates = [
            ("الطويل", "//o/o//o/o/o//o/o//o/o/o"),
            ("الكامل", "///o//o///o//o///o//o"),
            ("البسيط", "/o/o//o/o//o/o/o//o/o//o"),
            ("الوافر", "//o///o//o///o/o/o"),
        ]

        matches = find_best_meter_matches(
            verse_pattern,
            candidates,
            min_similarity=0.5,
            top_k=3
        )

        # Should find at least some matches
        assert len(matches) > 0

        # All matches should meet min_similarity
        assert all(score >= 0.5 for _, _, score in matches)

        # Should be sorted by similarity
        scores = [score for _, _, score in matches]
        assert scores == sorted(scores, reverse=True)

    def test_hemistich_vs_full_verse(self):
        """Test that hemistich can match against full verse pattern."""
        # Hemistich pattern (4 tafāʿīl)
        hemistich = "//o/o//o/o/o//o/o//o/o/o"[:12]  # First half

        # Full verse pattern (8 tafāʿīl)
        full_verse = "//o/o//o/o/o//o/o//o/o/o"

        similarity = calculate_pattern_similarity(hemistich, full_verse)

        # Should have some similarity (shares initial pattern)
        assert similarity > 0.3  # Not completely different
        assert similarity < 0.9  # But not very close (different lengths)
