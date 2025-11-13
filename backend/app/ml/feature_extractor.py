"""
BAHR Feature Extractor for Machine Learning.

Extracts comprehensive feature set (50 features) from Arabic poetry verses:
- 8 pattern features (length, counts, complexity, rhythm)
- 16 similarity features (distance to each meter's patterns)
- 16 rule features (transformation matches for each meter)
- 10 linguistic features (word count, letter distribution, structure)

Total: 50 features for ML training (XGBoost, Random Forest, etc.)
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from collections import Counter

from ..core.phonetics import text_to_phonetic_pattern
from ..core.prosody.pattern_similarity import PatternSimilarity
from ..core.prosody.meters import METERS_REGISTRY
from ..core.prosody.detector_v2_hybrid import EMPIRICAL_PATTERNS


class BAHRFeatureExtractor:
    """
    Extract comprehensive features from Arabic poetry verses for ML models.

    Features extracted:
    1. Pattern features (8): Basic phonetic pattern characteristics
    2. Similarity features (16): Distance to each meter's empirical patterns
    3. Rule features (16): Transformation rule matches for each meter
    4. Linguistic features (10): Word-level and letter-level statistics

    Total: 50 features
    """

    def __init__(self):
        """Initialize feature extractor with similarity calculator."""
        self.similarity_calc = PatternSimilarity()
        self.meter_ids = sorted(EMPIRICAL_PATTERNS.keys())

    def extract_features(self, verse_text: str, include_target: bool = False,
                        target_meter_id: Optional[int] = None) -> Dict[str, float]:
        """
        Extract all 50 features from a verse.

        Args:
            verse_text: Arabic verse text (with or without tashkeel)
            include_target: Whether to include target meter ID
            target_meter_id: True meter ID (for training data)

        Returns:
            Dictionary with 50 feature values + optional target
        """
        # Convert text to phonetic pattern
        try:
            pattern = text_to_phonetic_pattern(verse_text, has_tashkeel=True)
        except Exception:
            # Fallback for verses without tashkeel
            pattern = text_to_phonetic_pattern(verse_text, has_tashkeel=False)

        if not pattern:
            # Return zero features if pattern extraction fails
            return self._get_zero_features()

        # Extract all feature groups
        features = {}
        features.update(self._extract_pattern_features(pattern))
        features.update(self._extract_similarity_features(pattern))
        features.update(self._extract_rule_features(verse_text, pattern))
        features.update(self._extract_linguistic_features(verse_text))

        # Add target if requested
        if include_target and target_meter_id is not None:
            features['target_meter_id'] = target_meter_id

        return features

    def _extract_pattern_features(self, pattern: str) -> Dict[str, float]:
        """
        Extract 8 basic pattern features.

        Features:
        1. pattern_length: Total pattern length
        2. sakin_count: Number of sakin positions (o)
        3. mutaharrik_count: Number of mutaharrik positions (/)
        4. sakin_ratio: Ratio of sakin to total
        5. pattern_complexity: Entropy of pattern
        6. consecutive_sakin_max: Max consecutive sakin
        7. consecutive_mutaharrik_max: Max consecutive mutaharrik
        8. rhythm_alternation: How often pattern alternates /o
        """
        features = {}

        # Basic counts
        features['pattern_length'] = len(pattern)
        features['sakin_count'] = pattern.count('o')
        features['mutaharrik_count'] = pattern.count('/')

        # Ratios
        total = len(pattern)
        features['sakin_ratio'] = features['sakin_count'] / total if total > 0 else 0

        # Pattern complexity (entropy)
        if total > 0:
            sakin_prob = features['sakin_count'] / total
            mutaharrik_prob = features['mutaharrik_count'] / total
            entropy = 0
            if sakin_prob > 0:
                entropy -= sakin_prob * np.log2(sakin_prob)
            if mutaharrik_prob > 0:
                entropy -= mutaharrik_prob * np.log2(mutaharrik_prob)
            features['pattern_complexity'] = entropy
        else:
            features['pattern_complexity'] = 0

        # Consecutive patterns
        features['consecutive_sakin_max'] = self._max_consecutive(pattern, 'o')
        features['consecutive_mutaharrik_max'] = self._max_consecutive(pattern, '/')

        # Rhythm alternation (how often it switches between / and o)
        alternations = 0
        for i in range(len(pattern) - 1):
            if pattern[i] != pattern[i+1]:
                alternations += 1
        features['rhythm_alternation'] = alternations / (total - 1) if total > 1 else 0

        return features

    def _extract_similarity_features(self, pattern: str) -> Dict[str, float]:
        """
        Extract 16 similarity features (one per meter).

        For each meter, compute minimum weighted edit distance to its empirical patterns.
        Features: similarity_to_meter_1, similarity_to_meter_2, ..., similarity_to_meter_16
        """
        features = {}

        for meter_id in self.meter_ids:
            if meter_id not in EMPIRICAL_PATTERNS:
                features[f'similarity_to_meter_{meter_id}'] = 0.0
                continue

            meter_patterns = EMPIRICAL_PATTERNS[meter_id].get('patterns', [])
            if not meter_patterns:
                features[f'similarity_to_meter_{meter_id}'] = 0.0
                continue

            # Find best similarity to any pattern in this meter
            best_similarity = 0.0
            for meter_pattern in meter_patterns:
                similarity = self.similarity_calc.calculate_similarity(
                    pattern, meter_pattern
                )
                best_similarity = max(best_similarity, similarity)

            features[f'similarity_to_meter_{meter_id}'] = best_similarity

        return features

    def _extract_rule_features(self, verse_text: str, pattern: str) -> Dict[str, float]:
        """
        Extract 16 rule-based features (one per meter).

        For each meter, check if verse matches theoretical prosodic rules.
        Features: rule_match_meter_1, rule_match_meter_2, ..., rule_match_meter_16

        This is a simplified version - in full implementation, would check:
        - Taf'ilah structure matches
        - Valid ziḥāfāt transformations
        - Valid 'ilal endings
        - Hemistich structure
        """
        features = {}

        # For now, use pattern-based heuristics
        # TODO: Implement full theoretical rule checking
        for meter_id in self.meter_ids:
            # Simple heuristic: does pattern length match expected range for this meter?
            if meter_id in EMPIRICAL_PATTERNS:
                meter_patterns = EMPIRICAL_PATTERNS[meter_id].get('patterns', [])
                if meter_patterns:
                    # Check if pattern length is in range of this meter's patterns
                    pattern_lengths = [len(p) for p in meter_patterns]
                    min_len = min(pattern_lengths)
                    max_len = max(pattern_lengths)

                    # Score based on how close to expected range
                    if min_len <= len(pattern) <= max_len:
                        features[f'rule_match_meter_{meter_id}'] = 1.0
                    else:
                        # Penalize based on distance from range
                        if len(pattern) < min_len:
                            distance = min_len - len(pattern)
                        else:
                            distance = len(pattern) - max_len
                        features[f'rule_match_meter_{meter_id}'] = max(0, 1 - distance / 20)
                else:
                    features[f'rule_match_meter_{meter_id}'] = 0.0
            else:
                features[f'rule_match_meter_{meter_id}'] = 0.0

        return features

    def _extract_linguistic_features(self, verse_text: str) -> Dict[str, float]:
        """
        Extract 10 linguistic features from the verse text.

        Features:
        1. word_count: Number of words
        2. avg_word_length: Average word length in characters
        3. unique_letters: Number of unique letters
        4. letter_diversity: Ratio of unique to total letters
        5. has_tanween: Presence of tanween (doubled vowels)
        6. has_shadda: Presence of shadda (doubling)
        7. vowel_density: Ratio of vowel marks to consonants
        8. long_vowel_count: Count of long vowels (ا، و، ي)
        9. verse_length_chars: Total character count
        10. hamza_count: Count of hamza characters
        """
        features = {}

        # Remove non-Arabic characters for analysis
        text_clean = ''.join(c for c in verse_text if '\u0600' <= c <= '\u06FF')

        # Word-level features
        words = verse_text.split()
        features['word_count'] = len(words)
        features['avg_word_length'] = np.mean([len(w) for w in words]) if words else 0

        # Letter-level features
        letters = [c for c in text_clean if '\u0621' <= c <= '\u064A']
        features['unique_letters'] = len(set(letters))
        features['letter_diversity'] = len(set(letters)) / len(letters) if letters else 0

        # Diacritical marks
        features['has_tanween'] = 1.0 if any(c in text_clean for c in '\u064B\u064C\u064D') else 0.0
        features['has_shadda'] = 1.0 if '\u0651' in text_clean else 0.0

        # Vowel analysis
        consonants = [c for c in text_clean if '\u0621' <= c <= '\u063A' or '\u0641' <= c <= '\u064A']
        vowels = [c for c in text_clean if '\u064B' <= c <= '\u0652']
        features['vowel_density'] = len(vowels) / len(consonants) if consonants else 0

        # Long vowels
        long_vowels = ['ا', 'و', 'ي']
        features['long_vowel_count'] = sum(text_clean.count(v) for v in long_vowels)

        # Length
        features['verse_length_chars'] = len(text_clean)

        # Hamza
        hamza_chars = ['ء', 'أ', 'إ', 'آ', 'ؤ', 'ئ']
        features['hamza_count'] = sum(text_clean.count(h) for h in hamza_chars)

        return features

    def _max_consecutive(self, pattern: str, char: str) -> int:
        """Find maximum consecutive occurrences of a character."""
        max_count = 0
        current_count = 0

        for c in pattern:
            if c == char:
                current_count += 1
                max_count = max(max_count, current_count)
            else:
                current_count = 0

        return max_count

    def _get_zero_features(self) -> Dict[str, float]:
        """Return dictionary with all features set to zero (fallback)."""
        features = {}

        # Pattern features (8)
        for feat in ['pattern_length', 'sakin_count', 'mutaharrik_count', 'sakin_ratio',
                     'pattern_complexity', 'consecutive_sakin_max', 'consecutive_mutaharrik_max',
                     'rhythm_alternation']:
            features[feat] = 0.0

        # Similarity features (16)
        for meter_id in self.meter_ids:
            features[f'similarity_to_meter_{meter_id}'] = 0.0

        # Rule features (16)
        for meter_id in self.meter_ids:
            features[f'rule_match_meter_{meter_id}'] = 0.0

        # Linguistic features (10)
        for feat in ['word_count', 'avg_word_length', 'unique_letters', 'letter_diversity',
                     'has_tanween', 'has_shadda', 'vowel_density', 'long_vowel_count',
                     'verse_length_chars', 'hamza_count']:
            features[feat] = 0.0

        return features

    def extract_batch(self, verses: List[Tuple[str, Optional[int]]]) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Extract features from multiple verses efficiently.

        Args:
            verses: List of (verse_text, meter_id) tuples

        Returns:
            Tuple of (feature_matrix, target_array)
            - feature_matrix: Shape (n_verses, 50)
            - target_array: Shape (n_verses,) or None if no targets
        """
        feature_list = []
        target_list = []
        has_targets = any(meter_id is not None for _, meter_id in verses)

        for verse_text, meter_id in verses:
            features = self.extract_features(
                verse_text,
                include_target=has_targets,
                target_meter_id=meter_id
            )

            # Extract feature values in consistent order
            feature_values = []

            # Pattern features (8)
            for feat in ['pattern_length', 'sakin_count', 'mutaharrik_count', 'sakin_ratio',
                        'pattern_complexity', 'consecutive_sakin_max', 'consecutive_mutaharrik_max',
                        'rhythm_alternation']:
                feature_values.append(features[feat])

            # Similarity features (16)
            for meter_id_feat in self.meter_ids:
                feature_values.append(features[f'similarity_to_meter_{meter_id_feat}'])

            # Rule features (16)
            for meter_id_feat in self.meter_ids:
                feature_values.append(features[f'rule_match_meter_{meter_id_feat}'])

            # Linguistic features (10)
            for feat in ['word_count', 'avg_word_length', 'unique_letters', 'letter_diversity',
                        'has_tanween', 'has_shadda', 'vowel_density', 'long_vowel_count',
                        'verse_length_chars', 'hamza_count']:
                feature_values.append(features[feat])

            feature_list.append(feature_values)

            if has_targets and meter_id is not None:
                target_list.append(meter_id)

        feature_matrix = np.array(feature_list)
        target_array = np.array(target_list) if has_targets else None

        return feature_matrix, target_array

    def get_feature_names(self) -> List[str]:
        """Get ordered list of all 50 feature names."""
        feature_names = []

        # Pattern features (8)
        feature_names.extend([
            'pattern_length', 'sakin_count', 'mutaharrik_count', 'sakin_ratio',
            'pattern_complexity', 'consecutive_sakin_max', 'consecutive_mutaharrik_max',
            'rhythm_alternation'
        ])

        # Similarity features (16)
        for meter_id in self.meter_ids:
            feature_names.append(f'similarity_to_meter_{meter_id}')

        # Rule features (16)
        for meter_id in self.meter_ids:
            feature_names.append(f'rule_match_meter_{meter_id}')

        # Linguistic features (10)
        feature_names.extend([
            'word_count', 'avg_word_length', 'unique_letters', 'letter_diversity',
            'has_tanween', 'has_shadda', 'vowel_density', 'long_vowel_count',
            'verse_length_chars', 'hamza_count'
        ])

        return feature_names
