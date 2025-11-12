#!/usr/bin/env python3
"""
Recommendation: How to properly fix the overfitting problem.

Instead of adding 18 more patterns, we should:
1. Keep ONLY representative patterns (5-8 per meter)
2. Implement Levenshtein distance for fuzzy matching
3. Set appropriate threshold (15-20% edit distance)
"""

import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.better_similarity import levenshtein_similarity

# Sample patterns for الطويل (just keep 5-6 representative ones)
AL_TAWIL_REPRESENTATIVE = [
    "//////o//o//oo//o///o/o",    # Standard form 1
    "//o///o//o//oo//o///o//",    # Standard form 2  
    "//o/o////o/////////////o",   # Variation 1
    "/o/o///o///o/o//o//o///o",   # Variation 2
    "//////o/o/o//o///o//",       # Short form
]

# Failed test verse
failed_pattern = "//o////o///o//o/o/////"  # Imru' al-Qais famous verse

print("=" * 80)
print("TESTING: Can fuzzy matching solve the overfitting?")
print("=" * 80)
print()

print(f"Testing pattern from Imru' al-Qais's mu'allaqah:")
print(f"  '{failed_pattern}'")
print()

print(f"Against ONLY 5 representative الطويل patterns (not 17):")
print()

best_sim = 0.0
best_pattern = None

for pattern in AL_TAWIL_REPRESENTATIVE:
    similarity, within_threshold = levenshtein_similarity(
        failed_pattern, 
        pattern,
        threshold=0.20  # Allow 20% edit distance
    )
    
    print(f"  Pattern: {pattern[:30]}...")
    print(f"    Similarity: {similarity:.3f}, Within 20% threshold: {within_threshold}")
    
    if similarity > best_sim:
        best_sim = similarity
        best_pattern = pattern

print()
print(f"✓ Best match: {best_sim:.3f}")
print()

if best_sim >= 0.70:
    print("✅ SUCCESS: Would correctly identify as الطويل with fuzzy matching!")
    print(f"   Even with ONLY 5 patterns (not 17)")
else:
    print(f"❌ FAILED: {best_sim:.3f} < 0.70 threshold")

print()
print("=" * 80)
print("CONCLUSION")
print("=" * 80)
print()
print("The right fix is NOT to add more patterns.")
print("The right fix is to implement proper fuzzy matching:")
print()
print("1. Replace SequenceMatcher with Levenshtein distance")
print("2. Keep only 5-8 representative patterns per meter")  
print("3. Set threshold to 0.70-0.75 with 20% edit distance allowed")
print("4. This will generalize to unseen verses")
print()
print("📝 Implementation file: backend/app/core/better_similarity.py (already created)")
print("🔧 Next step: Update BahrDetector to use Levenshtein instead of SequenceMatcher")
