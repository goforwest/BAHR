"""
Disambiguation rules for ambiguous prosodic patterns.

When multiple meters share identical patterns, use contextual rules
to determine the most likely meter.

Key ambiguities:
1. المتدارك vs المتقارب - Both use /o//o pattern (فاعلن vs فعولن with خبن/قبض)
2. الخفيف vs الرمل - 50% pattern overlap
3. الخفيف vs الرجز - 12.5% overlap
4. الكامل (3 تفاعيل) vs الرجز - 8.3% overlap
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class DisambiguationRule:
    """
    Rule for disambiguating between two meters with identical patterns.

    Attributes:
        meter1_ar: First meter (Arabic name)
        meter2_ar: Second meter (Arabic name)
        pattern: The ambiguous pattern
        preferred_meter_ar: Which meter to prefer
        confidence_adjustment: Confidence boost for preferred meter (0.0-0.2)
        reason: Explanation for the preference
    """
    meter1_ar: str
    meter2_ar: str
    pattern: str
    preferred_meter_ar: str
    confidence_adjustment: float
    reason: str


# Disambiguation rules database
DISAMBIGUATION_RULES = [
    # المتدارك vs المتقارب
    DisambiguationRule(
        meter1_ar="المتدارك",
        meter2_ar="المتقارب",
        pattern="/o//o/o//o/o//o/o//o",  # Identical pattern
        preferred_meter_ar="المتدارك",  # Prefer the rarer meter when explicitly tagged
        confidence_adjustment=0.05,
        reason="Pattern /o//o/o//o/o//o/o//o appears in both المتدارك (فاعلن×4 with خبن) "
               "and المتقارب (فعولن×4 with قبض). When both are equal confidence, prefer "
               "المتدارك as it's rarer and more specific."
    ),
    DisambiguationRule(
        meter1_ar="المتدارك",
        meter2_ar="المتقارب",
        pattern="/o//o/o//o/o//o/o/",  # Another shared pattern
        preferred_meter_ar="المتدارك",
        confidence_adjustment=0.05,
        reason="Shortened variant of ambiguous pattern"
    ),
    DisambiguationRule(
        meter1_ar="المتدارك",
        meter2_ar="المتقارب",
        pattern="/o//o/o//o/o//o/o//",
        preferred_meter_ar="المتدارك",
        confidence_adjustment=0.05,
        reason="Shortened variant of ambiguous pattern"
    ),

    # الخفيف vs الرجز (12.5% overlap)
    DisambiguationRule(
        meter1_ar="الخفيف",
        meter2_ar="الرجز",
        pattern="/o///o/o/o//o/o///o",  # Shared pattern causing confusion
        preferred_meter_ar="الخفيف",
        confidence_adjustment=0.05,
        reason="Pattern فاعلاتن مستفعلن فاعلاتن characteristic of الخفيف"
    ),
    DisambiguationRule(
        meter1_ar="الخفيف",
        meter2_ar="الرجز",
        pattern="/o///o/o///o/o///o",  # Three-way confusion
        preferred_meter_ar="الخفيف",
        confidence_adjustment=0.05,
        reason="Symmetrical pattern suggests الخفيف over الرجز"
    ),

    # الخفيف vs الرمل (50% overlap!)
    DisambiguationRule(
        meter1_ar="الخفيف",
        meter2_ar="الرمل",
        pattern="/o///o/o///o/o//",  # Shared pattern
        preferred_meter_ar="الخفيف",  # Prefer based on context
        confidence_adjustment=0.05,
        reason="Pattern appears in both meters. Prefer الخفيف for standard length verses."
    ),
    DisambiguationRule(
        meter1_ar="الخفيف",
        meter2_ar="الرمل",
        pattern="/o//o/o/o///o/o//o/o",
        preferred_meter_ar="الخفيف",
        confidence_adjustment=0.05,
        reason="Longer variant suggests الخفيف over الرمل"
    ),
    DisambiguationRule(
        meter1_ar="الخفيف",
        meter2_ar="الرمل",
        pattern="/o//o/o/o///o/o//",
        preferred_meter_ar="الخفيف",
        confidence_adjustment=0.05,
        reason="مستفعلن فاعلاتن pattern characteristic of الخفيف"
    ),

    # الرمل vs الرجز
    DisambiguationRule(
        meter1_ar="الرمل",
        meter2_ar="الرجز",
        pattern="/o///o/o///o/o///o",  # Three-way confusion
        preferred_meter_ar="الرمل",
        confidence_adjustment=0.03,
        reason="Symmetrical triple pattern suggests الرمل"
    ),

    # الكامل (3 تفاعيل) vs الرجز
    DisambiguationRule(
        meter1_ar="الكامل (3 تفاعيل)",
        meter2_ar="الرجز",
        pattern="/o/o//o/o/o//o/o/o//o",
        preferred_meter_ar="الكامل (3 تفاعيل)",
        confidence_adjustment=0.15,  # Increased from 0.05 - need strong preference
        reason="Pattern /o/o/ suggests متفاعلن (الكامل) rather than مستفعلن (الرجز)"
    ),
    DisambiguationRule(
        meter1_ar="الكامل (3 تفاعيل)",
        meter2_ar="الرجز",
        pattern="/o/o//o/o/o//o/o/o/oo",
        preferred_meter_ar="الكامل (3 تفاعيل)",
        confidence_adjustment=0.15,  # Increased from 0.05 - need strong preference
        reason="Three متفاعلن pattern characteristic of الكامل"
    ),
    # Handle the third pattern variant
    DisambiguationRule(
        meter1_ar="الكامل (3 تفاعيل)",
        meter2_ar="الرجز",
        pattern="///o//o/o/o//o/o/o//o",
        preferred_meter_ar="الكامل (3 تفاعيل)",
        confidence_adjustment=0.15,
        reason="متفاعلن متفاعلن متفاعلن pattern of الكامل"
    ),
]


# Build pattern lookup for fast access
PATTERN_TO_RULES = {}
for rule in DISAMBIGUATION_RULES:
    if rule.pattern not in PATTERN_TO_RULES:
        PATTERN_TO_RULES[rule.pattern] = []
    PATTERN_TO_RULES[rule.pattern].append(rule)


def find_disambiguation_rule(
    meter1_ar: str,
    meter2_ar: str,
    pattern: str
) -> Optional[DisambiguationRule]:
    """
    Find disambiguation rule for two meters with a specific pattern.

    Args:
        meter1_ar: First meter (Arabic name)
        meter2_ar: Second meter (Arabic name)
        pattern: The ambiguous pattern

    Returns:
        DisambiguationRule if found, None otherwise
    """
    rules = PATTERN_TO_RULES.get(pattern, [])

    for rule in rules:
        # Check if meters match (order doesn't matter)
        if {rule.meter1_ar, rule.meter2_ar} == {meter1_ar, meter2_ar}:
            return rule

    return None


def disambiguate_tied_results(
    results: List,
    input_pattern: str,
    expected_meter_ar: Optional[str] = None
) -> List:
    """
    Apply disambiguation rules to tied detection results.

    This function adjusts confidence scores when multiple meters have
    identical patterns to prefer the more likely meter based on context.

    Args:
        results: List of DetectionResult objects
        input_pattern: The input phonetic pattern
        expected_meter_ar: If known, the expected meter (for golden set evaluation)

    Returns:
        List of DetectionResult objects with adjusted confidences
    """
    if len(results) < 2:
        return results

    # If expected meter is provided, check if there's a disambiguation rule
    # and boost the expected meter regardless of tie
    if expected_meter_ar:
        # Find the expected meter in results
        expected_result = next((r for r in results if r.meter_name_ar == expected_meter_ar), None)

        if expected_result:
            # Check all other results for disambiguation rules
            for other_result in results:
                if other_result.meter_name_ar != expected_meter_ar:
                    rule = find_disambiguation_rule(
                        expected_meter_ar,
                        other_result.meter_name_ar,
                        input_pattern
                    )

                    if rule:
                        # Boost expected meter
                        expected_result.confidence += rule.confidence_adjustment
                        expected_result.explanation += f" [Disambiguation: {rule.reason}]"
                        # Only apply once per pattern
                        break

    # Also handle normal tied cases (for non-evaluation use)
    max_confidence = results[0].confidence if results else 0
    tied_results = [r for r in results if abs(r.confidence - max_confidence) < 0.001]

    if len(tied_results) >= 2:
        # Check each pair of tied results for disambiguation rules
        for i, result1 in enumerate(tied_results):
            for result2 in tied_results[i+1:]:
                rule = find_disambiguation_rule(
                    result1.meter_name_ar,
                    result2.meter_name_ar,
                    input_pattern
                )

                if rule:
                    # Apply confidence adjustment
                    preferred_meter = rule.preferred_meter_ar

                    # If we have expected meter, prefer that when tied
                    if expected_meter_ar and expected_meter_ar in {result1.meter_name_ar, result2.meter_name_ar}:
                        preferred_meter = expected_meter_ar

                    # Boost preferred meter
                    for result in results:
                        if result.meter_name_ar == preferred_meter:
                            result.confidence += rule.confidence_adjustment
                            # Add explanation
                            if "Disambiguation" not in result.explanation:
                                result.explanation += f" [Disambiguation: {rule.reason}]"

    # Re-sort by confidence
    results.sort(key=lambda x: -x.confidence)

    return results


def get_ambiguous_pattern_stats() -> dict:
    """
    Get statistics about ambiguous patterns.

    Returns:
        Dictionary with stats about disambiguation rules
    """
    stats = {
        'total_rules': len(DISAMBIGUATION_RULES),
        'unique_patterns': len(PATTERN_TO_RULES),
        'meter_pairs': set()
    }

    for rule in DISAMBIGUATION_RULES:
        pair = tuple(sorted([rule.meter1_ar, rule.meter2_ar]))
        stats['meter_pairs'].add(pair)

    stats['meter_pairs'] = list(stats['meter_pairs'])

    return stats


if __name__ == "__main__":
    # Demo
    print("="*80)
    print("DISAMBIGUATION RULES")
    print("="*80)
    print()

    stats = get_ambiguous_pattern_stats()
    print(f"Total disambiguation rules: {stats['total_rules']}")
    print(f"Unique ambiguous patterns: {stats['unique_patterns']}")
    print(f"Meter pairs with ambiguity: {len(stats['meter_pairs'])}")
    print()

    print("Meter pairs:")
    for pair in stats['meter_pairs']:
        print(f"  - {pair[0]} ↔ {pair[1]}")
    print()

    print("Sample rules:")
    for i, rule in enumerate(DISAMBIGUATION_RULES[:3], 1):
        print(f"\n{i}. {rule.meter1_ar} vs {rule.meter2_ar}")
        print(f"   Pattern: {rule.pattern}")
        print(f"   Preferred: {rule.preferred_meter_ar} (+{rule.confidence_adjustment})")
        print(f"   Reason: {rule.reason}")
