#!/usr/bin/env python3
"""Test and debug tafila segmenter."""

import sys
sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.phonetics import extract_phonemes
from app.core.prosody.tafila_segmenter import TafilaSegmenter


def main():
    print("="*80)
    print("TAFILA SEGMENTER DEBUG")
    print("="*80)
    print()

    segmenter = TafilaSegmenter()

    print(f"Tafila library: {len(segmenter.tafila_library)} unique patterns")
    print(f"Total tafila variations: {sum(len(v) for v in segmenter.tafila_library.values())}")
    print()

    # Show some patterns
    print("Sample tafila patterns in library:")
    for i, (pattern, tafail) in enumerate(list(segmenter.tafila_library.items())[:10]):
        print(f"  '{pattern}': {len(tafail)} variations")
        for tafila, variation in tafail[:2]:
            print(f"    - {tafila.name} ({variation})")
    print()

    # Test with a simple verse
    text = "قِفا نَبْكِ مِن ذِكرى حَبيبٍ ومَنْزِلِ"
    print(f"Test verse: {text}")
    print()

    # Extract phonemes
    phonemes = extract_phonemes(text, has_tashkeel=True)
    print(f"Phonemes ({len(phonemes)}):")
    for i, p in enumerate(phonemes[:10], 1):
        vowel_display = f"'{p.vowel}'" if p.vowel else "'sukun'"
        print(f"  {i}. {p.consonant} + {vowel_display}")
    print()

    # Try finding tafail at start
    print("Finding tafail at position 0:")
    matches = segmenter.find_tafila_matches(phonemes, 0)
    print(f"Found {len(matches)} possible tafail")
    for match in matches[:5]:
        print(f"  - {match.tafila.name}: '{match.tafila.phonetic}' (conf={match.confidence:.2f})")
    print()

    # Try segmentation
    print("Attempting full segmentation:")
    segmentations = segmenter.segment_verse(phonemes)
    print(f"Found {len(segmentations)} possible segmentations")
    if segmentations:
        print("First segmentation:")
        for tafila_match in segmentations[0]:
            print(f"  - {tafila_match.tafila.name}")
    print()

    # Try detection
    print("Attempting meter detection:")
    match = segmenter.detect_meter(text, has_tashkeel=True)
    if match:
        print(f"✅ Detected: {match.meter.name_ar}")
        print(f"   Confidence: {match.overall_confidence:.2%}")
        print(f"   Tafail: {' + '.join(t.tafila.name for t in match.tafail_sequence)}")
    else:
        print("❌ No detection")


if __name__ == '__main__':
    main()
