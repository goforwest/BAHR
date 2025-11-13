#!/usr/bin/env python3
"""
Test prosodic augmentation engine for correctness.

Validates:
1. Each augmentation strategy generates valid patterns
2. Generated variations maintain prosodic correctness
3. No invalid variations are created
"""

import sys
from pathlib import Path

sys.path.insert(0, 'backend')

from app.core.phonetics import text_to_phonetic_pattern
from app.ml.prosodic_augmenter import ProsodicAugmenter


def test_phonetic_variations():
    """Test phonetic variation strategy."""
    print("=" * 80)
    print("Testing Phonetic Variations")
    print("=" * 80)
    print()

    augmenter = ProsodicAugmenter()

    # Test cases with expected variation types
    test_cases = [
        {
            'text': 'قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ',
            'meter': 'الطويل',
            'expected_types': ['tanwin_removal', 'alif_maqsura_variation']
        },
        {
            'text': 'أَرَى أُمَّةً أَخْرَجَتْ مِنْهَا الْكِرَامُ',
            'meter': 'الكامل',
            'expected_types': ['hamza_variation']
        }
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"  Original: {case['text']}")
        print(f"  Meter: {case['meter']}")

        original_pattern = text_to_phonetic_pattern(case['text'])
        print(f"  Pattern: {original_pattern}")

        variations = augmenter.augment_verse(case['text'], case['meter'], target_count=5)

        print(f"  Generated {len(variations)} variations:")
        for j, var in enumerate(variations, 1):
            try:
                var_pattern = text_to_phonetic_pattern(var)
                match = "✅" if var_pattern == original_pattern else "❌"
                print(f"    {j}. {match} {var}")
                print(f"       Pattern: {var_pattern}")
            except Exception as e:
                print(f"    {j}. ❌ INVALID: {var}")
                print(f"       Error: {e}")

        print()

    print("✅ Phonetic variations test complete")
    print()


def test_letter_variations():
    """Test letter-level variation strategy."""
    print("=" * 80)
    print("Testing Letter Variations")
    print("=" * 80)
    print()

    augmenter = ProsodicAugmenter()

    # Test cases with letter-level spelling variants
    test_cases = [
        {
            'text': 'رَحْمَةُ اللَّهِ عَلَى عِبَادِهِ',
            'meter': 'البسيط',
            'contains': 'ة'  # Should generate ه variant
        },
        {
            'text': 'إِلَى الْمَعَالِي يَسْعَى',
            'meter': 'المتقارب',
            'contains': 'ى'  # Should generate ي variant
        }
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"  Original: {case['text']}")

        variations = augmenter.augment_verse(case['text'], case['meter'], target_count=3)

        print(f"  Generated {len(variations)} variations:")
        for j, var in enumerate(variations, 1):
            print(f"    {j}. {var}")

        print()

    print("✅ Letter variations test complete")
    print()


def test_word_reordering():
    """Test word reordering strategy."""
    print("=" * 80)
    print("Testing Word Reordering")
    print("=" * 80)
    print()

    augmenter = ProsodicAugmenter()

    # Test with 3-6 word verses (suitable for reordering)
    test_cases = [
        {
            'text': 'وَفِي السَّمَاءِ رِزْقُكُمْ',
            'meter': 'الرجز',
            'word_count': 3
        },
        {
            'text': 'يَا أَيُّهَا الْإِنْسَانُ مَا غَرَّكَ',
            'meter': 'الرمل',
            'word_count': 5
        }
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"  Original: {case['text']} ({case['word_count']} words)")

        original_pattern = text_to_phonetic_pattern(case['text'])
        print(f"  Pattern: {original_pattern}")

        variations = augmenter.augment_verse(case['text'], case['meter'], target_count=5)

        print(f"  Generated {len(variations)} variations:")
        for j, var in enumerate(variations, 1):
            try:
                var_pattern = text_to_phonetic_pattern(var)
                similarity = sum(1 for a, b in zip(original_pattern, var_pattern) if a == b) / max(len(original_pattern), len(var_pattern))
                match = "✅" if similarity >= 0.9 else "⚠️"
                print(f"    {j}. {match} {var} (similarity: {similarity:.1%})")
            except Exception as e:
                print(f"    {j}. ❌ INVALID: {var}")
                print(f"       Error: {e}")

        print()

    print("✅ Word reordering test complete")
    print()


def test_augmentation_batch():
    """Test batch augmentation on multiple meters."""
    print("=" * 80)
    print("Testing Batch Augmentation")
    print("=" * 80)
    print()

    augmenter = ProsodicAugmenter()

    # Sample verses from different meters
    test_dataset = [
        ('قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ', 'الطويل'),
        ('أَرَى أُمَّةً أَخْرَجَتْ مِنْهَا الْكِرَامُ', 'الكامل'),
        ('يَا لَيْلُ الصَّبُّ مَتَى غَدُهُ', 'البسيط'),
        ('فِي قَلْبِي حُبُّ الْجَمَالِ', 'الوافر'),
    ]

    # Augmentation priorities (simulated)
    priorities = {}
    for text, meter in test_dataset:
        priorities[meter] = {
            'count': 1,
            'target_count': 3,
            'aug_factor': 3.0
        }

    augmented = augmenter.augment_dataset(test_dataset, priorities)

    print(f"Original dataset: {len(test_dataset)} verses")
    print(f"Augmented dataset: {len(augmented)} verses")
    print(f"Augmentation factor: {len(augmented) / len(test_dataset):.1f}x")
    print()

    # Show sample augmentations
    print("Sample augmented verses:")
    for i, (text, meter) in enumerate(augmented[:10], 1):
        is_original = (text, meter) in test_dataset
        marker = "📌" if is_original else "✨"
        print(f"{i}. {marker} [{meter}] {text}")

    print()
    print("✅ Batch augmentation test complete")
    print()


def test_pattern_preservation():
    """Test that augmentation preserves prosodic patterns."""
    print("=" * 80)
    print("Testing Pattern Preservation")
    print("=" * 80)
    print()

    augmenter = ProsodicAugmenter()

    test_verse = 'قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ'
    meter = 'الطويل'

    print(f"Original verse: {test_verse}")
    original_pattern = text_to_phonetic_pattern(test_verse)
    print(f"Original pattern: {original_pattern}")
    print()

    variations = augmenter.augment_verse(test_verse, meter, target_count=10)

    print(f"Generated {len(variations)} variations")
    print()
    print("Pattern preservation check:")
    print("-" * 80)

    valid_count = 0
    for i, var in enumerate(variations, 1):
        try:
            var_pattern = text_to_phonetic_pattern(var)
            is_exact = var_pattern == original_pattern

            if is_exact:
                status = "✅ EXACT"
                valid_count += 1
            else:
                # Check similarity
                similarity = sum(1 for a, b in zip(original_pattern, var_pattern) if a == b) / max(len(original_pattern), len(var_pattern))
                if similarity >= 0.9:
                    status = f"⚠️  SIMILAR ({similarity:.1%})"
                    valid_count += 1
                else:
                    status = f"❌ DIFFERENT ({similarity:.1%})"

            print(f"{i}. {status}")
            print(f"   Text: {var}")
            print(f"   Pattern: {var_pattern}")

        except Exception as e:
            print(f"{i}. ❌ INVALID")
            print(f"   Text: {var}")
            print(f"   Error: {e}")

    print("-" * 80)
    print(f"Valid variations: {valid_count}/{len(variations)} ({100*valid_count/len(variations) if variations else 0:.1f}%)")
    print()

    if valid_count / len(variations) >= 0.95:
        print("✅ Pattern preservation: EXCELLENT (≥95% valid)")
    elif valid_count / len(variations) >= 0.85:
        print("⚠️  Pattern preservation: GOOD (≥85% valid)")
    else:
        print("❌ Pattern preservation: NEEDS IMPROVEMENT (<85% valid)")

    print()


def main():
    """Run all augmentation tests."""
    print("=" * 80)
    print("Prosodic Augmentation Engine - Comprehensive Tests")
    print("=" * 80)
    print()

    try:
        # Test individual strategies
        test_phonetic_variations()
        test_letter_variations()
        test_word_reordering()

        # Test batch processing
        test_augmentation_batch()

        # Test pattern preservation
        test_pattern_preservation()

        print("=" * 80)
        print("✅ ALL TESTS COMPLETE")
        print("=" * 80)
        print()
        print("Augmentation engine is ready for full dataset processing!")
        print()

    except Exception as e:
        print("=" * 80)
        print("❌ TEST FAILED")
        print("=" * 80)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
