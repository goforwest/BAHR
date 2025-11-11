"""
Comprehensive test suite for the Golden Dataset.
Tests all aspects of bahr detection, taqti3 accuracy, and confidence calibration
against manually verified classical Arabic poetry verses.
"""

import json
import pytest
from pathlib import Path
from typing import List, Dict

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Path to the golden dataset (expanded version with 80 verses)
GOLDEN_SET_PATH = PROJECT_ROOT / "dataset" / "evaluation" / "golden_set_v0_80_complete.jsonl"

import json
import os
import pytest
from pathlib import Path
from typing import List, Dict, Any

from app.core.normalization import normalize_arabic_text
from app.core.taqti3 import perform_taqti3
from app.core.bahr_detector import BahrDetector


# Constants
MIN_CONFIDENCE_THRESHOLD = 0.85  # Golden set should have high confidence
PERFECT_MATCH_THRESHOLD = 0.90  # For "perfect_match" edge cases


def load_golden_dataset() -> List[Dict[str, Any]]:
    """Load the golden dataset from JSONL file."""
    verses = []
    with open(GOLDEN_SET_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                verses.append(json.loads(line))
    return verses


# Load dataset once for all tests
GOLDEN_VERSES = load_golden_dataset()


@pytest.fixture(scope="module")
def analyzer():
    """Create a BahrDetector instance for testing."""
    return BahrDetector()


def analyze_verse(text: str, detector: BahrDetector):
    """
    Helper function to analyze a verse.
    
    Returns a dict with bahr, confidence, and taqti3.
    """
    # Normalize text
    normalized = normalize_arabic_text(
        text,
        remove_tashkeel=False,
        normalize_hamzas=True,
        normalize_alefs=True
    )
    
    # Detect bahr first
    bahr_info = detector.analyze_verse(normalized)
    
    # Perform taqti3 (scansion) using detected bahr for accurate theoretical pattern
    # If bahr is detected, pass bahr_id to get the standard tafail for that meter
    bahr_id = bahr_info.id if bahr_info else None
    taqti3_result = perform_taqti3(normalized, bahr_id=bahr_id)
    
    return {
        'bahr': bahr_info.name_ar if bahr_info else None,
        'confidence': bahr_info.confidence if bahr_info else 0.0,
        'taqti3': taqti3_result,
        'bahr_id': bahr_id
    }


# ============================================================================
# Test 1: Bahr Detection Accuracy
# ============================================================================

@pytest.mark.parametrize("verse", GOLDEN_VERSES, ids=lambda v: v['verse_id'])
def test_bahr_detection_accuracy(analyzer, verse):
    """
    Test that the analyzer correctly identifies the meter (bahr) for each golden verse.
    
    This is the core quality metric - the system should identify the correct meter
    for all manually verified classical poetry examples.
    """
    result = analyze_verse(verse['text'], analyzer)
    
    expected_meter = verse['meter']
    detected_meter = result['bahr']
    
    assert detected_meter == expected_meter, (
        f"Bahr mismatch for verse '{verse['verse_id']}' ({verse.get('poet', 'Unknown')})\n"
        f"Text: {verse['text']}\n"
        f"Expected: {expected_meter}\n"
        f"Got: {detected_meter}\n"
        f"Confidence: {result['confidence']}\n"
        f"Notes: {verse.get('notes', 'N/A')}"
    )


# ============================================================================
# Test 2: Confidence Levels
# ============================================================================

@pytest.mark.parametrize("verse", GOLDEN_VERSES, ids=lambda v: v['verse_id'])
def test_confidence_levels(analyzer, verse):
    """
    Test that confidence scores are appropriately high for golden verses.
    
    Manually verified classical poetry should produce high confidence scores.
    Lower confidence may indicate issues with the analyzer or edge cases.
    """
    result = analyze_verse(verse['text'], analyzer)
    
    # Adjust threshold based on edge case type
    edge_case = verse.get('edge_case_type', 'perfect_match')
    
    if edge_case == 'perfect_match':
        min_threshold = PERFECT_MATCH_THRESHOLD
    else:
        min_threshold = MIN_CONFIDENCE_THRESHOLD
    
    assert result['confidence'] >= min_threshold, (
        f"Low confidence for verse '{verse['verse_id']}'\n"
        f"Text: {verse['text']}\n"
        f"Expected meter: {verse['meter']}\n"
        f"Detected meter: {result['bahr']}\n"
        f"Confidence: {result['confidence']} (expected >= {min_threshold})\n"
        f"Edge case type: {edge_case}\n"
        f"Difficulty: {verse.get('difficulty_level', 'unknown')}\n"
        f"Notes: {verse.get('notes', 'N/A')}"
    )


# ============================================================================
# Test 3: Taqti3 Pattern Matching
# ============================================================================

@pytest.mark.parametrize("verse", GOLDEN_VERSES, ids=lambda v: v['verse_id'])
def test_taqti3_patterns(analyzer, verse):
    """
    Test that the analyzer produces correct taqti3 (scansion) patterns.
    
    Verifies that the syllabic analysis and prosodic patterns match
    the manually annotated tafail (feet) for each verse.
    """
    result = analyze_verse(verse['text'], analyzer)
    
    expected_tafail = verse.get('expected_tafail', [])
    detected_taqti3 = result['taqti3']
    
    # Skip if no expected tafail annotated
    if not expected_tafail:
        pytest.skip(f"No expected tafail annotated for verse '{verse['verse_id']}'")
    
    # Extract tafail from detected taqti3 string
    # The taqti3 string is like "فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِيلُنْ"
    detected_tafail = [t.strip() for t in detected_taqti3.split() if t.strip()]
    
    assert len(detected_tafail) == len(expected_tafail), (
        f"Tafail count mismatch for verse '{verse['verse_id']}'\n"
        f"Text: {verse['text']}\n"
        f"Expected tafail count: {len(expected_tafail)}\n"
        f"Detected tafail count: {len(detected_tafail)}\n"
        f"Expected: {' '.join(expected_tafail)}\n"
        f"Detected: {detected_taqti3}"
    )
    
    # Compare each tafila (foot)
    for i, (expected, detected) in enumerate(zip(expected_tafail, detected_tafail)):
        # Normalize for comparison (remove diacritics variations)
        expected_norm = expected.replace('ُ', '').replace('ْ', '').replace('َ', '').replace('ِ', '')
        detected_norm = detected.replace('ُ', '').replace('ْ', '').replace('َ', '').replace('ِ', '')
        
        assert expected_norm == detected_norm, (
            f"Tafila mismatch at position {i+1} for verse '{verse['verse_id']}'\n"
            f"Text: {verse['text']}\n"
            f"Expected tafila: {expected}\n"
            f"Detected tafila: {detected}\n"
            f"Full expected: {' '.join(expected_tafail)}\n"
            f"Full detected: {detected_taqti3}"
        )


# ============================================================================
# Test 4: Edge Cases - Diacritics
# ============================================================================

def test_diacritics_edge_cases(analyzer):
    """
    Test verses specifically marked as diacritics tests.
    
    These verses test the analyzer's ability to handle complex diacritical marks,
    shadda (gemination), tanwin, and other Arabic orthographic features.
    """
    diacritics_verses = [v for v in GOLDEN_VERSES if v.get('edge_case_type') == 'diacritics_test']
    
    assert len(diacritics_verses) > 0, "No diacritics test cases in golden set"
    
    results = []
    for verse in diacritics_verses:
        result = analyze_verse(verse['text'], analyzer)
        match = result['bahr'] == verse['meter']
        results.append({
            'verse_id': verse['verse_id'],
            'match': match,
            'confidence': result['confidence'],
            'expected': verse['meter'],
            'detected': result['bahr']
        })
    
    # Calculate accuracy
    matches = sum(1 for r in results if r['match'])
    accuracy = matches / len(results) if results else 0
    
    assert accuracy >= 0.85, (
        f"Diacritics edge cases accuracy too low: {accuracy:.2%}\n"
        f"Passed: {matches}/{len(results)}\n"
        f"Details: {json.dumps(results, ensure_ascii=False, indent=2)}"
    )


# ============================================================================
# Test 5: Edge Cases - Common Variations
# ============================================================================

def test_common_variations_edge_cases(analyzer):
    """
    Test verses with common prosodic variations (zihafs).
    
    These verses test the analyzer's ability to handle common variations
    like qabḍ, kaff, and other zihafs that modify the standard tafail.
    """
    variation_verses = [v for v in GOLDEN_VERSES if v.get('edge_case_type') == 'common_variations']
    
    if len(variation_verses) == 0:
        pytest.skip("No common variation test cases in golden set")
    
    results = []
    for verse in variation_verses:
        result = analyze_verse(verse['text'], analyzer)
        match = result['bahr'] == verse['meter']
        results.append({
            'verse_id': verse['verse_id'],
            'match': match,
            'confidence': result['confidence'],
            'expected': verse['meter'],
            'detected': result['bahr'],
            'notes': verse.get('notes', '')
        })
    
    # Calculate accuracy
    matches = sum(1 for r in results if r['match'])
    accuracy = matches / len(results) if results else 0
    
    assert accuracy >= 0.80, (
        f"Common variations accuracy too low: {accuracy:.2%}\n"
        f"Passed: {matches}/{len(results)}\n"
        f"Details: {json.dumps(results, ensure_ascii=False, indent=2)}"
    )


# ============================================================================
# Test 6: Difficulty Levels
# ============================================================================

@pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
def test_by_difficulty_level(analyzer, difficulty):
    """
    Test verses grouped by difficulty level.
    
    Easy verses should have near-perfect accuracy.
    Medium verses should have high accuracy.
    Hard verses may have lower accuracy but should still be reasonable.
    """
    difficulty_verses = [v for v in GOLDEN_VERSES if v.get('difficulty_level') == difficulty]
    
    if len(difficulty_verses) == 0:
        pytest.skip(f"No {difficulty} difficulty verses in golden set")
    
    results = []
    for verse in difficulty_verses:
        result = analyze_verse(verse['text'], analyzer)
        match = result['bahr'] == verse['meter']
        results.append({
            'verse_id': verse['verse_id'],
            'match': match,
            'confidence': result['confidence'],
            'expected': verse['meter'],
            'detected': result['bahr']
        })
    
    # Calculate accuracy
    matches = sum(1 for r in results if r['match'])
    accuracy = matches / len(results) if results else 0
    
    # Set thresholds based on difficulty
    thresholds = {
        'easy': 0.95,
        'medium': 0.85,
        'hard': 0.70
    }
    threshold = thresholds.get(difficulty, 0.80)
    
    assert accuracy >= threshold, (
        f"{difficulty.capitalize()} verses accuracy too low: {accuracy:.2%}\n"
        f"Expected >= {threshold:.0%}\n"
        f"Passed: {matches}/{len(results)}\n"
        f"Details: {json.dumps(results, ensure_ascii=False, indent=2)}"
    )


# ============================================================================
# Test 7: Meter Coverage
# ============================================================================

def test_meter_coverage(analyzer):
    """
    Test that we have coverage across multiple classical meters.
    
    Ensures the golden dataset and analyzer support a variety of
    Arabic prosodic meters (buhur).
    """
    meters_in_dataset = set(v['meter'] for v in GOLDEN_VERSES)
    
    # Major meters that should be covered
    major_meters = {
        'الطويل',
        'البسيط',
        'الكامل',
        'المتقارب',
        'الرمل',
        'الرجز'
    }
    
    covered_major_meters = major_meters & meters_in_dataset
    
    assert len(covered_major_meters) >= 5, (
        f"Insufficient major meter coverage in golden set\n"
        f"Covered: {covered_major_meters}\n"
        f"Missing: {major_meters - covered_major_meters}\n"
        f"All meters in dataset: {meters_in_dataset}"
    )


# ============================================================================
# Test 8: Overall Accuracy Summary
# ============================================================================

def test_overall_accuracy_summary(analyzer):
    """
    Calculate and report overall accuracy across the entire golden dataset.
    
    This is a summary test that provides aggregate statistics for monitoring
    system quality over time.
    """
    total_verses = len(GOLDEN_VERSES)
    correct_detections = 0
    confidence_scores = []
    
    failures = []
    
    for verse in GOLDEN_VERSES:
        result = analyze_verse(verse['text'], analyzer)
        confidence_scores.append(result['confidence'])
        
        if result['bahr'] == verse['meter']:
            correct_detections += 1
        else:
            failures.append({
                'verse_id': verse['verse_id'],
                'text': verse['text'],
                'expected': verse['meter'],
                'detected': result['bahr'],
                'confidence': result['confidence'],
                'poet': verse.get('poet', 'Unknown'),
                'notes': verse.get('notes', '')
            })
    
    accuracy = correct_detections / total_verses if total_verses > 0 else 0
    avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
    
    # Report statistics
    print(f"\n{'='*60}")
    print(f"GOLDEN DATASET ACCURACY REPORT")
    print(f"{'='*60}")
    print(f"Total verses: {total_verses}")
    print(f"Correct detections: {correct_detections}")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Average confidence: {avg_confidence:.3f}")
    print(f"{'='*60}")
    
    if failures:
        print(f"\nFAILURES ({len(failures)}):")
        print(json.dumps(failures, ensure_ascii=False, indent=2))
        print(f"{'='*60}")
    
    # Assert minimum accuracy threshold
    MIN_OVERALL_ACCURACY = 0.90  # 90% accuracy on golden set
    
    assert accuracy >= MIN_OVERALL_ACCURACY, (
        f"Overall accuracy too low: {accuracy:.2%} (expected >= {MIN_OVERALL_ACCURACY:.0%})\n"
        f"Passed: {correct_detections}/{total_verses}\n"
        f"Average confidence: {avg_confidence:.3f}\n"
        f"Failures: {len(failures)}"
    )


# ============================================================================
# Test 9: Specific Meter Accuracy
# ============================================================================

@pytest.mark.parametrize("meter", [
    'الطويل',
    'البسيط',
    'الكامل',
    'المتقارب',
    'الرمل',
    'الرجز',
    'الهزج',
    'الخفيف'
])
def test_specific_meter_accuracy(analyzer, meter):
    """
    Test accuracy for each specific meter.
    
    Ensures that the analyzer performs consistently well across
    all meters, not just on aggregate.
    """
    meter_verses = [v for v in GOLDEN_VERSES if v['meter'] == meter]
    
    if len(meter_verses) == 0:
        pytest.skip(f"No verses for meter '{meter}' in golden set")
    
    correct = 0
    confidences = []
    
    for verse in meter_verses:
        result = analyze_verse(verse['text'], analyzer)
        confidences.append(result['confidence'])
        
        if result['bahr'] == meter:
            correct += 1
    
    accuracy = correct / len(meter_verses)
    avg_confidence = sum(confidences) / len(confidences)
    
    # Require high accuracy for each meter
    assert accuracy >= 0.85, (
        f"Low accuracy for meter '{meter}': {accuracy:.2%}\n"
        f"Passed: {correct}/{len(meter_verses)}\n"
        f"Average confidence: {avg_confidence:.3f}"
    )


# ============================================================================
# Test 10: Famous Poets
# ============================================================================

def test_famous_poets_verses(analyzer):
    """
    Test verses from famous classical poets.
    
    Ensures the analyzer performs well on poetry from renowned poets
    like المتنبي, امرؤ القيس, أبو العلاء المعري.
    """
    famous_poets = ['المتنبي', 'امرؤ القيس', 'أبو العلاء المعري', 'جميل بثينة']
    
    poet_verses = [v for v in GOLDEN_VERSES if v.get('poet') in famous_poets]
    
    if len(poet_verses) == 0:
        pytest.skip("No verses from famous poets in golden set")
    
    results = []
    for verse in poet_verses:
        result = analyze_verse(verse['text'], analyzer)
        match = result['bahr'] == verse['meter']
        results.append({
            'verse_id': verse['verse_id'],
            'poet': verse.get('poet'),
            'match': match,
            'confidence': result['confidence'],
            'expected': verse['meter'],
            'detected': result['bahr']
        })
    
    matches = sum(1 for r in results if r['match'])
    accuracy = matches / len(results) if results else 0
    
    assert accuracy >= 0.90, (
        f"Famous poets verses accuracy too low: {accuracy:.2%}\n"
        f"Passed: {matches}/{len(results)}\n"
        f"Details: {json.dumps(results, ensure_ascii=False, indent=2)}"
    )
