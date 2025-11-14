#!/usr/bin/env python3
"""Count features by category."""

import sys
sys.path.insert(0, 'backend')

from app.ml.feature_extractor import BAHRFeatureExtractor

extractor = BAHRFeatureExtractor()
feature_names = extractor.get_feature_names()

print(f"Total feature names: {len(feature_names)}\n")

# Count by category
pattern_features = [f for f in feature_names if f in ['pattern_length', 'sakin_count', 'mutaharrik_count', 'sakin_ratio', 'pattern_complexity', 'consecutive_sakin_max', 'consecutive_mutaharrik_max', 'rhythm_alternation']]
similarity_features = [f for f in feature_names if f.startswith('similarity_to_meter_')]
discriminative_features = [f for f in feature_names if f in ['similarity_spread', 'similarity_ratio', 'similarity_std', 'similarity_mean', 'is_clear_winner']]
relative_similarity_features = [f for f in feature_names if f.startswith('relative_similarity_meter_')]
rule_features = [f for f in feature_names if f.startswith('rule_match_meter_')]
linguistic_features = [f for f in feature_names if f in ['word_count', 'avg_word_length', 'unique_letters', 'letter_diversity', 'has_tanween', 'has_shadda', 'vowel_density', 'long_vowel_count', 'verse_length_chars', 'hamza_count']]

print(f"Pattern features: {len(pattern_features)}")
print(f"Similarity features: {len(similarity_features)}")
print(f"Discriminative features: {len(discriminative_features)}")
for f in discriminative_features:
    print(f"  - {f}")
print(f"Relative similarity features: {len(relative_similarity_features)}")
print(f"  First 3: {relative_similarity_features[:3]}")
print(f"Rule features: {len(rule_features)}")
print(f"Linguistic features: {len(linguistic_features)}")
print()
print(f"Total: {len(pattern_features)} + {len(similarity_features)} + {len(discriminative_features)} + {len(relative_similarity_features)} + {len(rule_features)} + {len(linguistic_features)} = {len(pattern_features) + len(similarity_features) + len(discriminative_features) + len(relative_similarity_features) + len(rule_features) + len(linguistic_features)}")
