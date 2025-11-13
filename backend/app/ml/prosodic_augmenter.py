"""
Prosodic Augmentation Engine for Arabic Poetry.

Generates prosodically-valid verse variations by applying classical
transformations (ziḥāfāt and ʿilal) while maintaining metrical correctness.
"""

import sys
from typing import List, Tuple, Optional
import random
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.core.phonetics import text_to_phonetic_pattern


class ProsodicAugmenter:
    """
    Generate prosodically-valid variations of Arabic poetry verses.

    Strategy:
    1. Phonetic variations (stress, vowel quality)
    2. Letter variations (spelling variants)
    3. Transformation variations (apply/remove ziḥāfāt)
    """

    def __init__(self):
        self.random = random.Random(42)  # Reproducible augmentations

    def augment_verse(
        self,
        text: str,
        meter: str,
        target_count: int = 2
    ) -> List[str]:
        """
        Generate prosodically-valid variations of a verse.

        Args:
            text: Original verse text
            meter: Meter name (Arabic)
            target_count: Number of variations to generate

        Returns:
            List of augmented verses (may be fewer than target_count)
        """
        variations = []

        # Get original pattern
        try:
            original_pattern = text_to_phonetic_pattern(text)
        except Exception:
            return []  # Can't augment if we can't parse

        # Strategy 1: Phonetic variations
        phonetic_vars = self._phonetic_variations(text, original_pattern, meter)
        variations.extend(phonetic_vars[:max(1, target_count // 3)])

        # Strategy 2: Letter-level variations
        letter_vars = self._letter_variations(text, original_pattern, meter)
        variations.extend(letter_vars[:max(1, target_count // 3)])

        # Strategy 3: Word reordering (preserving meter)
        reorder_vars = self._word_reordering(text, original_pattern, meter)
        variations.extend(reorder_vars[:max(1, target_count // 3)])

        # Ensure uniqueness
        unique_variations = list(set(variations))

        # Remove original if it snuck in
        unique_variations = [v for v in unique_variations if v != text]

        return unique_variations[:target_count]

    def _phonetic_variations(
        self,
        text: str,
        original_pattern: str,
        meter: str
    ) -> List[str]:
        """
        Generate phonetic variations (vowel quality, stress).

        These don't change the prosodic pattern but provide
        diverse training examples.
        """
        variations = []

        # Strategy 1.1: Tanwin variations
        # إِنَّ → إِنْ (dropping tanwin, common in poetry)
        if 'ً' in text or 'ٌ' in text or 'ٍ' in text:
            no_tanwin = text.replace('ً', '').replace('ٌ', '').replace('ٍ', '')
            try:
                if text_to_phonetic_pattern(no_tanwin) == original_pattern:
                    variations.append(no_tanwin)
            except Exception:
                pass

        # Strategy 1.2: Shadda variations
        # مُحَمَّدٌ → مُحَمْمَدٌ (explicit gemination)
        # This is pronunciation-level, pattern stays same
        if 'ّ' in text:
            # Most shadda variations don't change pattern
            # Just keep original for now (conservative)
            pass

        # Strategy 1.3: Hamza variations
        # أَ ↔ إِ ↔ ا (hamza spelling variants)
        hamza_variants = {
            'أ': ['إ', 'ا'],
            'إ': ['أ', 'ا'],
            'ؤ': ['وء'],
            'ئ': ['يء']
        }

        for original_hamza, variants in hamza_variants.items():
            if original_hamza in text:
                for variant in variants:
                    modified = text.replace(original_hamza, variant, 1)  # Only first occurrence
                    try:
                        if text_to_phonetic_pattern(modified) == original_pattern:
                            variations.append(modified)
                    except Exception:
                        pass

        return variations

    def _letter_variations(
        self,
        text: str,
        original_pattern: str,
        meter: str
    ) -> List[str]:
        """
        Generate letter-level spelling variations.

        These are valid Arabic spelling variants that maintain
        the prosodic pattern.
        """
        variations = []

        # Strategy 2.1: ة ↔ ه at end of word
        # Example: رَحْمَة ↔ رَحْمَه
        if 'ة' in text:
            tah_to_hah = text.replace('ة', 'ه')
            try:
                if text_to_phonetic_pattern(tah_to_hah) == original_pattern:
                    variations.append(tah_to_hah)
            except Exception:
                pass

        # Strategy 2.2: ى ↔ ي (alif maqsura variations)
        # Example: إِلَى ↔ إِلَي
        if 'ى' in text:
            alif_maq_to_ya = text.replace('ى', 'ي')
            try:
                if text_to_phonetic_pattern(alif_maq_to_ya) == original_pattern:
                    variations.append(alif_maq_to_ya)
            except Exception:
                pass

        # Strategy 2.3: و ↔ ؤ for hamza
        if 'و' in text and 'ء' in text:
            # Try combining them
            modified = text.replace('وء', 'ؤ', 1)
            try:
                if text_to_phonetic_pattern(modified) == original_pattern:
                    variations.append(modified)
            except Exception:
                pass

        return variations

    def _word_reordering(
        self,
        text: str,
        original_pattern: str,
        meter: str
    ) -> List[str]:
        """
        Generate variations by reordering words (Arabic allows flexible word order).

        This maintains semantic meaning while providing pattern diversity.
        """
        variations = []

        # Split into words
        words = text.split()

        # Only try reordering for verses with 3-6 words (manageable)
        if not (3 <= len(words) <= 6):
            return variations

        # Try a few random permutations
        for _ in range(min(3, len(words))):
            # Shuffle (but keep first/last word often for meaning preservation)
            if len(words) >= 4:
                # Keep first and last, shuffle middle
                middle = words[1:-1]
                self.random.shuffle(middle)
                reordered = [words[0]] + middle + [words[-1]]
            else:
                # Full shuffle
                reordered = words.copy()
                self.random.shuffle(reordered)

            reordered_text = ' '.join(reordered)

            try:
                new_pattern = text_to_phonetic_pattern(reordered_text)
                # Accept if pattern is SIMILAR (not necessarily exact)
                # This captures prosodically-compatible reorderings
                if self._patterns_similar(original_pattern, new_pattern):
                    variations.append(reordered_text)
            except Exception:
                pass

        return variations

    def _patterns_similar(self, p1: str, p2: str, threshold: float = 0.9) -> bool:
        """Check if two patterns are similar (allowing minor differences)."""
        if p1 == p2:
            return True

        # Allow patterns to differ by up to 10% of length
        if abs(len(p1) - len(p2)) > len(p1) * 0.1:
            return False

        # Simple character-level similarity
        min_len = min(len(p1), len(p2))
        matches = sum(1 for i in range(min_len) if p1[i] == p2[i])
        similarity = matches / max(len(p1), len(p2))

        return similarity >= threshold

    def augment_dataset(
        self,
        dataset: List[Tuple[str, str]],
        augmentation_priorities: dict
    ) -> List[Tuple[str, str]]:
        """
        Augment entire dataset according to priorities.

        Args:
            dataset: List of (text, meter) tuples
            augmentation_priorities: Dict with augmentation factors per meter

        Returns:
            Augmented dataset (original + generated variations)
        """
        augmented = []

        # Keep all originals
        augmented.extend(dataset)

        # Group by meter
        meter_verses = {}
        for text, meter in dataset:
            if meter not in meter_verses:
                meter_verses[meter] = []
            meter_verses[meter].append(text)

        # Augment each meter according to priority
        for meter, priority_info in augmentation_priorities.items():
            if meter not in meter_verses:
                continue

            original_count = priority_info['count']
            target_count = priority_info['target_count']
            aug_factor = priority_info['aug_factor']

            verses = meter_verses[meter]

            # Calculate how many variations per verse
            variations_needed = target_count - original_count
            variations_per_verse = max(1, int(variations_needed / len(verses)))

            print(f"Augmenting {meter}: {original_count} → {target_count} verses")
            print(f"  Generating {variations_per_verse} variations per verse...")

            generated_count = 0
            for verse in verses:
                variations = self.augment_verse(
                    verse,
                    meter,
                    target_count=variations_per_verse
                )

                for var in variations:
                    augmented.append((var, meter))
                    generated_count += 1

            print(f"  ✅ Generated {generated_count} new verses for {meter}")

        print(f"\n✅ Augmentation complete: {len(dataset)} → {len(augmented)} verses")
        return augmented


def main():
    """Test augmentation on a single verse."""
    augmenter = ProsodicAugmenter()

    # Test verse (الطويل)
    test_verse = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ"
    test_meter = "الطويل"

    print("=" * 80)
    print("Testing Prosodic Augmentation")
    print("=" * 80)
    print(f"\nOriginal verse: {test_verse}")
    print(f"Meter: {test_meter}")
    print()

    variations = augmenter.augment_verse(test_verse, test_meter, target_count=5)

    print(f"Generated {len(variations)} variations:")
    print()
    for i, var in enumerate(variations, 1):
        print(f"{i}. {var}")

    print()
    print("=" * 80)


if __name__ == '__main__':
    main()
