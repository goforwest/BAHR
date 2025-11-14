#!/usr/bin/env python3
"""
Production-ready batch collector for Arabic poetry dataset.

This module provides the main API for collecting verses in batches.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dataset_builder import DatasetOrchestrator
from prosody_validator import get_meter_info


def collect_batch(meter_id: int, batch_num: int = 1) -> bool:
    """
    Collect and export a batch of 20 verses for the specified meter.
    
    Args:
        meter_id: Meter ID (1-20)
        batch_num: Batch number (for sequential collection)
    
    Returns:
        True if successful, False otherwise
    """
    output_dir = Path(__file__).parent
    orchestrator = DatasetOrchestrator(output_dir)
    
    verses = orchestrator.collect_batch_for_meter(
        meter_id=meter_id,
        batch_num=batch_num,
        batch_size=20
    )
    
    return len(verses) > 0


def main():
    """Command-line interface for batch collection."""
    print("\n" + "="*80)
    print("ARABIC POETRY ML DATASET - BATCH COLLECTOR")
    print("="*80 + "\n")
    
    # Show meter list
    from prosody_validator import list_all_meters
    
    print("Available meters:")
    meters = list_all_meters()
    for m in meters:
        print(f"  {m['id']:2d}. {m['name_ar']:20s} ({m['name_en']})")
    
    print("\n" + "="*80)
    print("Which meter should I begin collecting?")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
