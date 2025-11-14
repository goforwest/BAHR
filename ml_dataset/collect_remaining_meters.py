#!/usr/bin/env python3
"""
Collect all remaining meters systematically.
Completes the dataset to 2000+ verses across all 20 meters.
"""

import sys
sys.path.insert(0, '../')

from batch_collector import collect_batch
from prosody_validator import METERS

# Meters that need full collection (100 verses each)
METERS_TO_COLLECT = {
    3: ('البسيط', 95),  # Need 95 more (have 5)
    5: ('الرجز', 95),   # Need 95 more (have 5)
    6: ('الرمل', 95),   # Need 95 more (have 5)
    7: ('الخفيف', 95),  # Need 95 more (have 5)
    12: ('الهزج', 100),  # Need 100 (have 0)
    14: ('المقتضب', 100),  # Need 100 (have 0)
    15: ('المضارع', 100),  # Need 100 (have 0)
    17: ('الكامل (مجزوء)', 100),  # Need 100 (have 0)
    18: ('الهزج (مجزوء)', 100),  # Need 100 (have 0)
    19: ('الكامل (3 تفاعيل)', 100),  # Need 100 (have 0)
    20: ('السريع (مفعولات)', 100),  # Need 100 (have 0)
}

def collect_all_remaining():
    """Collect all remaining meters to complete the dataset."""
    total_needed = sum(count for _, count in METERS_TO_COLLECT.values())
    total_collected = 0
    failures = []
    
    print(f"=== COLLECTING REMAINING METERS ===")
    print(f"Total verses needed: {total_needed}")
    print(f"Total meters to process: {len(METERS_TO_COLLECT)}")
    print("=" * 50)
    
    for meter_id, (meter_name, verses_needed) in METERS_TO_COLLECT.items():
        print(f"\n📊 Meter {meter_id}: {meter_name}")
        print(f"   Target: {verses_needed} verses")
        
        # Calculate number of batches (20 verses per batch)
        num_batches = (verses_needed + 19) // 20  # Ceiling division
        
        meter_collected = 0
        meter_failures = 0
        
        # Determine starting batch number
        # For meters 3,5,6,7 we already have batch_001.jsonl with 5 verses
        # So we start from batch 2 for those
        start_batch = 2 if verses_needed == 95 else 1
        
        for batch_num in range(start_batch, start_batch + num_batches):
            print(f"   Batch {batch_num}... ", end='', flush=True)
            
            success = collect_batch(meter_id, batch_num)
            
            if success:
                # Each batch should collect ~20 verses
                batch_size = min(20, verses_needed - meter_collected)
                meter_collected += batch_size
                total_collected += batch_size
                print(f"✓ ({meter_collected}/{verses_needed})")
            else:
                meter_failures += 1
                print(f"✗ FAILED")
                failures.append((meter_id, meter_name, batch_num))
        
        print(f"   ✅ Completed: {meter_collected}/{verses_needed} verses")
        
        if meter_failures > 0:
            print(f"   ⚠️  Failures: {meter_failures} batches")
    
    # Final summary
    print("\n" + "=" * 50)
    print("=== COLLECTION COMPLETE ===")
    print(f"Total verses collected: {total_collected}/{total_needed}")
    print(f"Success rate: {(total_collected/total_needed)*100:.1f}%")
    
    if failures:
        print(f"\n⚠️  Failed batches ({len(failures)}):")
        for meter_id, meter_name, batch_num in failures:
            print(f"   - Meter {meter_id} ({meter_name}), Batch {batch_num}")
    else:
        print("\n🎉 ALL BATCHES COLLECTED SUCCESSFULLY!")
    
    return total_collected, failures

if __name__ == '__main__':
    collected, failures = collect_all_remaining()
    sys.exit(0 if not failures else 1)
