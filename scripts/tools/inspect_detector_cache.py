#!/usr/bin/env python3
"""
Inspect the detector cache to understand its structure.
"""

import sys
sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.prosody.detector_v2 import BahrDetectorV2


def inspect_cache():
    """Inspect detector cache structure."""

    print(f"{'='*80}")
    print(f"DETECTOR CACHE INSPECTION")
    print(f"{'='*80}\n")

    detector = BahrDetectorV2()

    print(f"Cache type: {type(detector.pattern_cache)}")
    print(f"Cache keys: {list(detector.pattern_cache.keys())}\n")

    # Count patterns per meter
    total_patterns = 0
    for meter, patterns in detector.pattern_cache.items():
        count = len(patterns)
        total_patterns += count
        print(f"{meter}: {count} patterns")

        # Show first 3 patterns
        if count > 0:
            sample = list(patterns)[:3]
            for p in sample:
                print(f"   {p}")
        print()

    print(f"Total patterns: {total_patterns}")


if __name__ == '__main__':
    inspect_cache()
