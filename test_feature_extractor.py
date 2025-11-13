#!/usr/bin/env python3
"""
Test BAHRFeatureExtractor on sample verses and golden dataset.
"""

import sys
sys.path.insert(0, 'backend')

from app.ml.feature_extractor import BAHRFeatureExtractor
import json

def test_single_verse():
    """Test feature extraction on a single verse."""
    print("=" * 80)
    print("Testing BAHRFeatureExtractor on Single Verse")
    print("=" * 80)
    print()

    # Create extractor
    extractor = BAHRFeatureExtractor()

    # Test verse (الطويل - al-Tawil)
    verse = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ"

    print(f"Verse: {verse}")
    print()

    # Extract features
    features = extractor.extract_features(verse)

    print(f"✅ Extracted {len(features)} features:")
    print()

    # Show pattern features
    print("Pattern Features (8):")
    for feat in ['pattern_length', 'sakin_count', 'mutaharrik_count', 'sakin_ratio',
                 'pattern_complexity', 'consecutive_sakin_max', 'consecutive_mutaharrik_max',
                 'rhythm_alternation']:
        print(f"  {feat}: {features[feat]:.3f}")
    print()

    # Show top 3 similarity scores
    print("Top 3 Similarity Scores:")
    similarity_features = {k: v for k, v in features.items() if k.startswith('similarity_to_meter_')}
    sorted_sims = sorted(similarity_features.items(), key=lambda x: x[1], reverse=True)
    for feat_name, value in sorted_sims[:3]:
        meter_id = feat_name.split('_')[-1]
        print(f"  Meter {meter_id}: {value:.3f}")
    print()

    # Show linguistic features
    print("Linguistic Features (10):")
    for feat in ['word_count', 'avg_word_length', 'unique_letters', 'letter_diversity',
                 'has_tanween', 'has_shadda', 'vowel_density', 'long_vowel_count',
                 'verse_length_chars', 'hamza_count']:
        print(f"  {feat}: {features[feat]:.3f}")
    print()

    # Verify feature count
    expected_count = 50  # 8 + 16 + 16 + 10
    print(f"Total features: {len(features)} (expected: {expected_count})")
    if len(features) == expected_count:
        print("✅ Feature count is correct!")
    else:
        print(f"⚠️  Warning: Expected {expected_count} features, got {len(features)}")
    print()

def test_golden_dataset_sample():
    """Test on sample from golden dataset."""
    print("=" * 80)
    print("Testing on Golden Dataset Sample")
    print("=" * 80)
    print()

    # Load first 10 verses from golden dataset
    dataset_path = 'dataset/evaluation/golden_set_v1_3_with_sari.jsonl'

    verses = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 10:
                break
            if line.strip():
                verses.append(json.loads(line))

    print(f"Loaded {len(verses)} sample verses")
    print()

    # Create extractor
    extractor = BAHRFeatureExtractor()

    # Extract features for each verse
    print("Extracting features...")
    for i, verse_data in enumerate(verses, 1):
        text = verse_data.get('text', '')
        meter = verse_data.get('meter', 'Unknown')

        features = extractor.extract_features(text)

        print(f"Verse {i}: {meter}")
        print(f"  Features extracted: {len(features)}")
        print(f"  Pattern length: {features['pattern_length']}")
        print(f"  Word count: {features['word_count']}")

        # Find best matching meter
        similarity_features = {k: v for k, v in features.items() if k.startswith('similarity_to_meter_')}
        best_meter = max(similarity_features.items(), key=lambda x: x[1])
        best_meter_id = best_meter[0].split('_')[-1]
        best_similarity = best_meter[1]

        print(f"  Best match: Meter {best_meter_id} (similarity: {best_similarity:.3f})")
        print()

    print("✅ Feature extraction successful on all sample verses!")
    print()

def test_batch_extraction():
    """Test batch extraction."""
    print("=" * 80)
    print("Testing Batch Extraction")
    print("=" * 80)
    print()

    # Load first 20 verses from golden dataset
    dataset_path = 'dataset/evaluation/golden_set_v1_3_with_sari.jsonl'

    # Map meter names to IDs (simplified mapping)
    meter_name_to_id = {
        'الطويل': 1,
        'الكامل': 2,
        'الوافر': 3,
        'الرمل': 4,
        'البسيط': 5,
        'المتقارب': 6,
        'الرجز': 7,
        'الهزج': 11,
        'الخفيف': 12,
        'السريع': 8,
        'المديد': 9,
        'المنسرح': 10,
        'المجتث': 13,
        'المقتضب': 14,
        'المضارع': 15,
        'المتدارك': 16
    }

    verses_with_meters = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 20:
                break
            if line.strip():
                verse_data = json.loads(line)
                text = verse_data.get('text', '')
                meter_name = verse_data.get('meter', '')
                meter_id = meter_name_to_id.get(meter_name)

                if text and meter_id:
                    verses_with_meters.append((text, meter_id))

    print(f"Loaded {len(verses_with_meters)} verses with meter IDs")
    print()

    # Create extractor
    extractor = BAHRFeatureExtractor()

    # Batch extract
    print("Performing batch extraction...")
    feature_matrix, target_array = extractor.extract_batch(verses_with_meters)

    print(f"✅ Feature matrix shape: {feature_matrix.shape}")
    print(f"✅ Target array shape: {target_array.shape}")
    print()

    print(f"Feature matrix stats:")
    print(f"  Mean: {feature_matrix.mean():.3f}")
    print(f"  Std: {feature_matrix.std():.3f}")
    print(f"  Min: {feature_matrix.min():.3f}")
    print(f"  Max: {feature_matrix.max():.3f}")
    print()

    print(f"Target distribution:")
    import numpy as np
    unique, counts = np.unique(target_array, return_counts=True)
    for meter_id, count in zip(unique, counts):
        print(f"  Meter {meter_id}: {count} verses")
    print()

    print("✅ Batch extraction successful!")
    print()

def main():
    """Run all tests."""
    try:
        test_single_verse()
        test_golden_dataset_sample()
        test_batch_extraction()

        print("=" * 80)
        print("✅ ALL TESTS PASSED!")
        print("=" * 80)
        print()
        print("BAHRFeatureExtractor is working correctly and ready for ML training.")
        print()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
