"""
Pattern Generator - Generate all valid phonetic patterns for meters.

This module generates all theoretically valid phonetic patterns for each meter
by applying combinations of allowed Zihafat and 'Ilal according to the rules.
"""

from itertools import product
from typing import List, Optional, Set, Tuple

from .ilal import Ilah
from .meters import Meter
from .tafila import Tafila
from .zihafat import Zahaf


class PatternGenerator:
    """
    Generates all valid phonetic patterns for a meter.

    Uses combinatorial generation to apply all possible combinations
    of allowed zihafat and 'ilal according to meter rules.
    """

    def __init__(self, meter: Meter):
        """
        Initialize pattern generator for a specific meter.

        Args:
            meter: Meter to generate patterns for
        """
        self.meter = meter
        self._cache: Optional[Set[str]] = None

    def generate_all_patterns(self) -> Set[str]:
        """
        Generate all valid phonetic patterns for this meter.

        Returns:
            Set of all valid phonetic pattern strings

        Example:
            >>> from app.core.prosody.meters import AL_TAWIL
            >>> gen = PatternGenerator(AL_TAWIL)
            >>> patterns = gen.generate_all_patterns()
            >>> len(patterns)
            72  # All valid variations of الطويل
        """
        if self._cache is not None:
            return self._cache

        patterns = set()

        # Get all possible variations for each position
        position_variations = self._generate_position_variations()

        # Generate all combinations
        for combo in product(*position_variations):
            # Concatenate phonetic patterns
            pattern = "".join(tafila.phonetic for tafila in combo)
            patterns.add(pattern)

        self._cache = patterns
        return patterns

    def _generate_position_variations(self) -> List[List[Tafila]]:
        """
        Generate all possible tafila variations for each position.

        Returns:
            List of lists, where each inner list contains all possible
            tafa'il for that position (base + with zihafat/ilal applied)
        """
        variations = []

        for position in range(1, self.meter.tafail_count + 1):
            base_tafila = self.meter.get_tafila_at_position(position)
            position_vars = [base_tafila]  # Start with base form

            # Apply zihafat
            allowed_zihafat = self.meter.get_allowed_zihafat(position)
            for zahaf in allowed_zihafat:
                try:
                    modified = zahaf.apply(base_tafila)
                    position_vars.append(modified)
                except Exception:
                    # Skip if transformation fails
                    pass

            # Apply 'ilal (final position only)
            if self.meter.is_final_position(position):
                allowed_ilal = self.meter.get_allowed_ilal(position)

                # Apply 'ilal to base form
                for ilah in allowed_ilal:
                    try:
                        modified = ilah.apply(base_tafila)
                        position_vars.append(modified)
                    except Exception:
                        pass

                # Apply 'ilal to zahaf-modified forms (combinations)
                for zahaf in allowed_zihafat:
                    try:
                        zahaf_modified = zahaf.apply(base_tafila)
                        for ilah in allowed_ilal:
                            try:
                                combo_modified = ilah.apply(zahaf_modified)
                                position_vars.append(combo_modified)
                            except Exception:
                                pass
                    except Exception:
                        pass

            # Remove duplicates (same phonetic pattern)
            unique_vars = self._deduplicate_tafail(position_vars)
            variations.append(unique_vars)

        return variations

    def _deduplicate_tafail(self, tafail: List[Tafila]) -> List[Tafila]:
        """
        Remove duplicate tafa'il based on phonetic pattern.

        Args:
            tafail: List of tafa'il (may have duplicates)

        Returns:
            List of unique tafa'il
        """
        seen = set()
        unique = []

        for tafila in tafail:
            if tafila.phonetic not in seen:
                seen.add(tafila.phonetic)
                unique.append(tafila)

        return unique

    def generate_with_tracking(self) -> List[Tuple[str, List[str]]]:
        """
        Generate patterns with transformation tracking.

        Returns:
            List of (pattern, transformations_applied) tuples

        Example:
            >>> gen = PatternGenerator(AL_TAWIL)
            >>> patterns = gen.generate_with_tracking()
            >>> patterns[0]
            ('/o//o//o/o/o/o//o//o/o/o', ['base', 'base', 'base', 'base'])
            >>> patterns[1]
            ('/o////o/o/o/o//o//o/o/o', ['قبض at pos 1', 'base', 'base', 'base'])
        """
        results = []
        position_variations = self._generate_position_variations_with_names()

        for combo in product(*position_variations):
            tafail_list = [t[0] for t in combo]
            names_list = [t[1] for t in combo]

            pattern = "".join(tafila.phonetic for tafila in tafail_list)
            results.append((pattern, names_list))

        return results

    def _generate_position_variations_with_names(
        self,
    ) -> List[List[Tuple[Tafila, str]]]:
        """
        Generate position variations with transformation names.

        Returns:
            List of lists of (Tafila, transformation_name) tuples
        """
        variations = []

        for position in range(1, self.meter.tafail_count + 1):
            base_tafila = self.meter.get_tafila_at_position(position)
            position_vars = [(base_tafila, "base")]

            allowed_zihafat = self.meter.get_allowed_zihafat(position)
            for zahaf in allowed_zihafat:
                try:
                    modified = zahaf.apply(base_tafila)
                    position_vars.append((modified, f"{zahaf.name_ar}"))
                except Exception:
                    pass

            if self.meter.is_final_position(position):
                allowed_ilal = self.meter.get_allowed_ilal(position)

                for ilah in allowed_ilal:
                    try:
                        modified = ilah.apply(base_tafila)
                        position_vars.append((modified, f"{ilah.name_ar}"))
                    except Exception:
                        pass

                for zahaf in allowed_zihafat:
                    try:
                        zahaf_modified = zahaf.apply(base_tafila)
                        for ilah in allowed_ilal:
                            try:
                                combo_modified = ilah.apply(zahaf_modified)
                                position_vars.append(
                                    (combo_modified, f"{zahaf.name_ar}+{ilah.name_ar}")
                                )
                            except Exception:
                                pass
                    except Exception:
                        pass

            # Deduplicate
            unique_vars = self._deduplicate_with_names(position_vars)
            variations.append(unique_vars)

        return variations

    def _deduplicate_with_names(
        self, tafail: List[Tuple[Tafila, str]]
    ) -> List[Tuple[Tafila, str]]:
        """Deduplicate tafa'il with names."""
        seen = set()
        unique = []

        for tafila, name in tafail:
            if tafila.phonetic not in seen:
                seen.add(tafila.phonetic)
                unique.append((tafila, name))

        return unique

    def get_pattern_count(self) -> int:
        """
        Get total count of valid patterns without generating all.

        Returns:
            Number of valid patterns
        """
        position_variations = self._generate_position_variations()
        count = 1
        for variations in position_variations:
            count *= len(variations)
        return count

    def get_statistics(self) -> dict:
        """
        Get generation statistics.

        Returns:
            Dictionary with statistics
        """
        position_variations = self._generate_position_variations()

        return {
            "meter_id": self.meter.id,
            "meter_name": self.meter.name_ar,
            "tafail_count": self.meter.tafail_count,
            "variations_per_position": [len(v) for v in position_variations],
            "theoretical_patterns": self.get_pattern_count(),
            "base_pattern": self.meter.base_pattern,
        }


def generate_all_meter_patterns() -> dict:
    """
    Generate patterns for all defined meters.

    Returns:
        Dictionary mapping meter_id → set of patterns
    """
    from .meters import METERS_REGISTRY

    all_patterns = {}

    for meter_id, meter in METERS_REGISTRY.items():
        generator = PatternGenerator(meter)
        patterns = generator.generate_all_patterns()
        all_patterns[meter_id] = patterns

    return all_patterns


def get_total_pattern_count() -> int:
    """
    Get total count of patterns across all meters.

    Returns:
        Total number of valid patterns
    """
    from .meters import METERS_REGISTRY

    total = 0
    for meter in METERS_REGISTRY.values():
        generator = PatternGenerator(meter)
        total += generator.get_pattern_count()

    return total


def print_generation_report():
    """Print a report of pattern generation for all meters."""
    from .meters import METERS_REGISTRY

    print("=" * 80)
    print("PATTERN GENERATION REPORT - All 16 Classical Arabic Meters")
    print("=" * 80)
    print()

    total_patterns = 0

    for meter_id in sorted(METERS_REGISTRY.keys()):
        meter = METERS_REGISTRY[meter_id]
        generator = PatternGenerator(meter)
        stats = generator.get_statistics()

        print(f"{meter_id:2d}. {meter.name_ar:12s} ({meter.name_en})")
        print(f"    Tier: {meter.tier.value}, Rank: {meter.frequency_rank}")
        print(f"    Base: {stats['base_pattern']}")
        print(f"    Tafa'il: {stats['tafail_count']}")
        print(f"    Variations per position: {stats['variations_per_position']}")
        print(f"    Total valid patterns: {stats['theoretical_patterns']}")
        print()

        total_patterns += stats["theoretical_patterns"]

    print("=" * 80)
    print(f"TOTAL PATTERNS ACROSS ALL 16 METERS: {total_patterns}")
    print("=" * 80)


if __name__ == "__main__":
    # Run report when executed directly
    print_generation_report()
