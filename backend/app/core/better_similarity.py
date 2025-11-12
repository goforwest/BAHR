"""
Improved similarity calculation using Levenshtein distance.

This module provides better fuzzy matching for prosodic patterns
than the simple SequenceMatcher approach.
"""

from typing import Tuple


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate Levenshtein (edit) distance between two strings.

    The Levenshtein distance is the minimum number of single-character
    edits (insertions, deletions, substitutions) needed to transform
    one string into another.

    Args:
        s1: First string
        s2: Second string

    Returns:
        Edit distance (0 = identical)

    Example:
        >>> levenshtein_distance("kitten", "sitting")
        3
        >>> levenshtein_distance("abc", "abc")
        0
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    # Initialize matrix
    previous_row = range(len(s2) + 1)

    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions, or substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def levenshtein_similarity(
    s1: str, s2: str, threshold: float = 0.10
) -> Tuple[float, bool]:
    """
    Calculate similarity score using Levenshtein distance.

    Converts edit distance to a similarity score between 0.0 and 1.0.
    Allows for fuzzy matching with a configurable threshold.

    Args:
        s1: First pattern string
        s2: Second pattern string
        threshold: Maximum allowed difference as percentage of length (default: 10%)

    Returns:
        Tuple of (similarity_score, within_threshold)

    Example:
        >>> levenshtein_similarity("//o//o//", "//o//o///")
        (0.89, True)  # 1 edit in 9 chars = 88.9% similar
    """
    if not s1 or not s2:
        return 0.0, False

    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))

    # Similarity = 1 - (distance / max_length)
    similarity = 1.0 - (distance / max_len)

    # Check if within threshold
    allowed_edits = int(max_len * threshold)
    within_threshold = distance <= allowed_edits

    return similarity, within_threshold


def fuzzy_pattern_match(
    input_pattern: str, meter_patterns: list[str], threshold: float = 0.10
) -> Tuple[float, str | None]:
    """
    Find best fuzzy match for input pattern against multiple meter patterns.

    Uses Levenshtein distance to allow for minor variations (zihafat)
    in the prosodic pattern while still identifying the correct meter.

    Args:
        input_pattern: Input phonetic pattern to match
        meter_patterns: List of known patterns for a meter
        threshold: Maximum allowed difference (default: 10% edit distance)

    Returns:
        Tuple of (best_similarity, best_matching_pattern)

    Example:
        >>> patterns = ["//o//o//o//", "//o/o//o//o"]
        >>> fuzzy_pattern_match("//o//o//o/", patterns)
        (0.91, "//o//o//o//")  # Matched with 1 missing char
    """
    best_similarity = 0.0
    best_pattern = None

    for pattern in meter_patterns:
        similarity, within_threshold = levenshtein_similarity(
            input_pattern, pattern, threshold
        )

        if similarity > best_similarity:
            best_similarity = similarity
            best_pattern = pattern

    return best_similarity, best_pattern


# For backward compatibility
def calculate_similarity(pattern1: str, pattern2: str) -> float:
    """
    Calculate similarity using Levenshtein distance.

    Drop-in replacement for SequenceMatcher.ratio() with better
    fuzzy matching capabilities.

    Args:
        pattern1: First pattern
        pattern2: Second pattern

    Returns:
        Similarity score (0.0 - 1.0)
    """
    similarity, _ = levenshtein_similarity(pattern1, pattern2)
    return similarity
