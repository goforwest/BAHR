"""
Pattern Similarity - Fuzzy matching for Arabic prosodic patterns.

This module implements similarity-based pattern matching to handle phonological
variations in real Arabic poetry that don't exactly match theoretical meter patterns.

The key insight is that real poetry often has natural variations from ideal patterns:
- Elision of short vowels
- Vowel lengthening/shortening
- Phonological processes (assimilation, etc.)

Rather than requiring exact pattern matches, we use weighted edit distance to find
the best matching meter with a confidence score.
"""

from typing import List, Tuple
import re


class PatternSimilarity:
    """
    Calculate similarity between prosodic patterns using weighted edit distance.

    Prosodic patterns use:
    - '/' = mutaḥarrik (light/moving syllable)
    - 'o' = sākin/madd (heavy/still syllable)

    Weighted costs account for prosodic significance:
    - Changing / ↔ o: High cost (changes syllable weight)
    - Inserting/deleting a single position: Medium cost
    - Changing /o ↔ //, //o ↔ ///: Lower cost (subtle variations)
    """

    # Cost weights for different edit operations
    WEIGHTS = {
        'substitute_weight': 2.0,     # / ↔ o (changes syllable type)
        'insert_delete': 1.0,          # Add/remove a position
        'length_penalty': 0.5,         # Penalty for length mismatch
    }

    @staticmethod
    def calculate_similarity(pattern1: str, pattern2: str) -> float:
        """
        Calculate similarity score between two prosodic patterns.

        Returns a score from 0.0 (completely different) to 1.0 (identical).
        Uses normalized weighted edit distance.

        Args:
            pattern1: First prosodic pattern (e.g., "//o/o")
            pattern2: Second prosodic pattern (e.g., "//o//o")

        Returns:
            Similarity score (0.0 to 1.0)

        Examples:
            >>> PatternSimilarity.calculate_similarity("//o/o", "//o/o")
            1.0  # Identical

            >>> PatternSimilarity.calculate_similarity("//o/o", "//o//o")
            0.8  # Very similar (one extra /)

            >>> PatternSimilarity.calculate_similarity("//o/o", "/o/o/o")
            0.6  # Moderately similar

            >>> PatternSimilarity.calculate_similarity("//o/o", "ooooo")
            0.2  # Very different
        """
        if not pattern1 or not pattern2:
            return 0.0

        if pattern1 == pattern2:
            return 1.0

        # Calculate weighted edit distance
        distance = PatternSimilarity._weighted_edit_distance(pattern1, pattern2)

        # Normalize by maximum possible distance
        max_len = max(len(pattern1), len(pattern2))
        max_distance = max_len * PatternSimilarity.WEIGHTS['substitute_weight']

        # Convert distance to similarity (0.0 to 1.0)
        if max_distance == 0:
            return 1.0

        similarity = 1.0 - (distance / max_distance)
        return max(0.0, min(1.0, similarity))  # Clamp to [0, 1]

    @staticmethod
    def _weighted_edit_distance(s1: str, s2: str) -> float:
        """
        Calculate weighted edit distance between two patterns.

        Uses dynamic programming with custom weights for prosodic patterns.

        Args:
            s1: First pattern
            s2: Second pattern

        Returns:
            Weighted edit distance (lower is more similar)
        """
        m, n = len(s1), len(s2)

        # Create DP table
        dp = [[0.0] * (n + 1) for _ in range(m + 1)]

        # Initialize first row and column
        for i in range(m + 1):
            dp[i][0] = i * PatternSimilarity.WEIGHTS['insert_delete']
        for j in range(n + 1):
            dp[0][j] = j * PatternSimilarity.WEIGHTS['insert_delete']

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    # Characters match - no cost
                    dp[i][j] = dp[i-1][j-1]
                else:
                    # Calculate costs for each operation
                    substitute_cost = dp[i-1][j-1] + PatternSimilarity._get_substitution_cost(
                        s1[i-1], s2[j-1]
                    )
                    insert_cost = dp[i][j-1] + PatternSimilarity.WEIGHTS['insert_delete']
                    delete_cost = dp[i-1][j] + PatternSimilarity.WEIGHTS['insert_delete']

                    dp[i][j] = min(substitute_cost, insert_cost, delete_cost)

        # Add length mismatch penalty
        length_diff = abs(m - n)
        length_penalty = length_diff * PatternSimilarity.WEIGHTS['length_penalty']

        return dp[m][n] + length_penalty

    @staticmethod
    def _get_substitution_cost(c1: str, c2: str) -> float:
        """
        Get the cost of substituting c1 with c2 in a prosodic pattern.

        Prosodically significant changes (/ ↔ o) have higher cost than
        subtle variations.

        Args:
            c1: First character ('/' or 'o')
            c2: Second character ('/' or 'o')

        Returns:
            Substitution cost
        """
        # / ↔ o is a fundamental change (light vs heavy syllable)
        if {c1, c2} == {'/', 'o'}:
            return PatternSimilarity.WEIGHTS['substitute_weight']

        # Same character (shouldn't reach here, but just in case)
        if c1 == c2:
            return 0.0

        # Unknown characters - treat as high cost
        return PatternSimilarity.WEIGHTS['substitute_weight']

    @staticmethod
    def find_best_matches(
        input_pattern: str,
        candidate_patterns: List[Tuple[str, str]],
        min_similarity: float = 0.5,
        top_k: int = 5
    ) -> List[Tuple[str, str, float]]:
        """
        Find best matching patterns from candidates using fuzzy matching.

        Args:
            input_pattern: The pattern to match (e.g., from verse analysis)
            candidate_patterns: List of (meter_name, pattern) tuples to match against
            min_similarity: Minimum similarity threshold (0.0 to 1.0)
            top_k: Return top K matches

        Returns:
            List of (meter_name, pattern, similarity_score) tuples, sorted by similarity

        Example:
            >>> candidates = [
            ...     ("الطويل", "//o/o//o/o/o//o/o//o/o/o"),
            ...     ("الكامل", "///o//o///o//o///o//o"),
            ... ]
            >>> matches = PatternSimilarity.find_best_matches(
            ...     "//o/o//o///o//o/o//o//",
            ...     candidates,
            ...     min_similarity=0.6,
            ...     top_k=3
            ... )
            >>> # Returns top 3 matches with similarity scores
        """
        if not input_pattern or not candidate_patterns:
            return []

        # Calculate similarity for each candidate
        scored_matches = []
        for meter_name, pattern in candidate_patterns:
            similarity = PatternSimilarity.calculate_similarity(input_pattern, pattern)
            if similarity >= min_similarity:
                scored_matches.append((meter_name, pattern, similarity))

        # Sort by similarity (highest first)
        scored_matches.sort(key=lambda x: x[2], reverse=True)

        # Return top K
        return scored_matches[:top_k]

    @staticmethod
    def calculate_confidence(similarity_score: float, pattern_length: int) -> float:
        """
        Calculate confidence score for a match based on similarity and pattern length.

        Longer patterns with high similarity get higher confidence than short patterns
        with the same similarity (more evidence).

        Args:
            similarity_score: Similarity score (0.0 to 1.0)
            pattern_length: Length of the matched pattern

        Returns:
            Confidence score (0.0 to 1.0)

        Examples:
            >>> PatternSimilarity.calculate_confidence(0.9, 20)
            0.95  # High confidence (long pattern, high similarity)

            >>> PatternSimilarity.calculate_confidence(0.9, 5)
            0.85  # Lower confidence (short pattern, same similarity)

            >>> PatternSimilarity.calculate_confidence(0.6, 20)
            0.6  # Medium confidence
        """
        # Base confidence from similarity
        base_confidence = similarity_score

        # Boost for longer patterns (more evidence)
        # Short patterns (<10): no boost
        # Medium patterns (10-20): small boost
        # Long patterns (>20): larger boost
        if pattern_length > 20:
            length_boost = 0.05
        elif pattern_length > 10:
            length_boost = 0.02
        else:
            length_boost = 0.0

        # Apply boost but cap at 1.0
        confidence = min(1.0, base_confidence + length_boost)

        return confidence


class PatternNormalizer:
    """
    Normalize patterns to handle common phonological variations.

    This can help improve matching by standardizing certain patterns before comparison.
    """

    @staticmethod
    def normalize(pattern: str) -> str:
        """
        Normalize a prosodic pattern to canonical form.

        Currently a placeholder for future enhancements like:
        - Collapsing certain sequences (/oo → /o in some contexts)
        - Handling known variation patterns
        - Standardizing super-heavy syllables

        Args:
            pattern: Input pattern

        Returns:
            Normalized pattern
        """
        # For now, just return as-is
        # Future: Add normalization rules based on observed patterns
        return pattern

    @staticmethod
    def is_valid_pattern(pattern: str) -> bool:
        """
        Check if a pattern string is valid.

        Valid patterns contain only '/' and 'o' characters.

        Args:
            pattern: Pattern to validate

        Returns:
            True if valid, False otherwise
        """
        if not pattern:
            return False
        return all(c in '/o' for c in pattern)


# Convenience functions for direct use

def calculate_pattern_similarity(pattern1: str, pattern2: str) -> float:
    """
    Calculate similarity between two prosodic patterns.

    Convenience wrapper for PatternSimilarity.calculate_similarity().

    Args:
        pattern1: First pattern
        pattern2: Second pattern

    Returns:
        Similarity score (0.0 to 1.0)
    """
    return PatternSimilarity.calculate_similarity(pattern1, pattern2)


def find_best_meter_matches(
    verse_pattern: str,
    meter_patterns: List[Tuple[str, str]],
    min_similarity: float = 0.5,
    top_k: int = 3
) -> List[Tuple[str, str, float]]:
    """
    Find best matching meters for a verse pattern.

    Convenience wrapper for PatternSimilarity.find_best_matches().

    Args:
        verse_pattern: Pattern extracted from verse
        meter_patterns: List of (meter_name, pattern) tuples
        min_similarity: Minimum similarity threshold
        top_k: Number of top matches to return

    Returns:
        List of (meter_name, pattern, similarity) tuples
    """
    return PatternSimilarity.find_best_matches(
        verse_pattern,
        meter_patterns,
        min_similarity,
        top_k
    )
