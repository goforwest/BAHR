#!/usr/bin/env python3
"""
Test the better similarity algorithm vs. the current approach.

This demonstrates why Levenshtein distance is superior to
hardcoding every pattern variation.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from difflib import SequenceMatcher
from app.core.better_similarity import (
    levenshtein_distance,
    levenshtein_similarity,
    fuzzy_pattern_match
)


def test_similarity_comparison():
    """Compare SequenceMatcher vs Levenshtein for prosodic patterns."""
    
    print("=" * 80)
    print("SIMILARITY ALGORITHM COMPARISON")
    print("=" * 80)
    print()
    
    # Test cases: (input_pattern, expected_pattern, meter_name)
    test_cases = [
        # الطويل variations
        ("///o//o///o/o///o//o/o///o", "//////o//o//oo//o///o/o", "الطويل"),
        ("/////oo///////o//o/", "//////o/o/o//o///o//", "الطويل"),
        
        # الكامل variations  
        ("//o/o//o///o/////", "///o//o///o//o/o/o//", "الكامل"),
        ("////////o/o////o////o", "//o/////o/o//o/o//o//", "الكامل"),
        
        # الرمل variations
        ("//////////o////o//ooo", "//////o//o//o////////o", "الرمل"),
        ("/o//o/////////o//o/o//o///o", "/o/////o/o///o///", "الرمل"),
    ]
    
    print("Testing pattern matching with variations:\n")
    
    for input_pat, expected_pat, meter in test_cases:
        # SequenceMatcher approach (current)
        seq_sim = SequenceMatcher(None, input_pat, expected_pat).ratio()
        
        # Levenshtein approach (better)
        lev_sim, within_threshold = levenshtein_similarity(input_pat, expected_pat, threshold=0.20)
        distance = levenshtein_distance(input_pat, expected_pat)
        
        print(f"Meter: {meter}")
        print(f"  Input:    {input_pat[:40]}...")
        print(f"  Expected: {expected_pat[:40]}...")
        print(f"  SequenceMatcher: {seq_sim:.3f}")
        print(f"  Levenshtein:     {lev_sim:.3f} (distance: {distance}, threshold: {within_threshold})")
        print()


def test_fuzzy_matching():
    """Test fuzzy matching with multiple patterns."""
    
    print("=" * 80)
    print("FUZZY PATTERN MATCHING TEST")
    print("=" * 80)
    print()
    
    # Simulated meter patterns (just 3 patterns instead of 11-17)
    meter_patterns = {
        "الطويل": [
            "//////o//o//oo//o///o/o",
            "//////o/o/o//o///o//",
            "//o///////o/////o//ooo",
        ],
        "الكامل": [
            "///o//o///o//o/o/o//",
            "//o/////o/o//o/o//o//",
            "//o///o/o//////o/o/o/////o",
        ],
        "الرمل": [
            "//////o//o//o////////o",
            "/o/////o/o///o///",
            "/o////o/o/o///o///",
        ],
    }
    
    # Test verses that previously failed
    test_verses = [
        ("///o//o///o/o///o//o/o///o", "الطويل", "golden_081"),
        ("/////oo///////o//o/", "الطويل", "golden_083"),
        ("//o/o//o///o/////", "الكامل", "golden_084"),
        ("//////////o////o//ooo", "الرمل", "golden_094"),
    ]
    
    print(f"Testing with ONLY 3 patterns per meter (not 11-17):\n")
    
    correct = 0
    total = len(test_verses)
    
    for input_pattern, expected_meter, verse_id in test_verses:
        best_meter = None
        best_score = 0.0
        
        # Try all meters
        for meter_name, patterns in meter_patterns.items():
            score, matched_pattern = fuzzy_pattern_match(
                input_pattern, 
                patterns,
                threshold=0.20  # Allow 20% variation
            )
            
            if score > best_score:
                best_score = score
                best_meter = meter_name
        
        is_correct = (best_meter == expected_meter)
        correct += is_correct
        status = "✓" if is_correct else "✗"
        
        print(f"{status} {verse_id}: Expected {expected_meter}, Got {best_meter} ({best_score:.3f})")
    
    print()
    print(f"Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
    print()
    print("🎯 Key Insight: With fuzzy matching, we can achieve high accuracy")
    print("   with FAR FEWER hardcoded patterns!")


if __name__ == "__main__":
    test_similarity_comparison()
    print()
    test_fuzzy_matching()
