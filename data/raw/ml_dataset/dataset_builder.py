#!/usr/bin/env python3
"""
Main orchestrator for Arabic Poetry ML Dataset Collection

This script coordinates the collection, validation, and export of
classical Arabic poetry according to the blueprint specifications.
"""

import sys
from pathlib import Path
from typing import List
import json

# Add ml_dataset to path
sys.path.insert(0, str(Path(__file__).parent))

from prosody_validator import (
    ProsodyValidator, 
    ArabicTextNormalizer, 
    get_meter_info,
    list_all_meters
)
from poetry_sources import get_verses_by_meter, list_available_meters
from collect_dataset import VerseData, ArabicPoetryCollector


class DatasetOrchestrator:
    """Main orchestrator for dataset collection."""
    
    def __init__(self, output_dir: Path = None):
        if output_dir is None:
            output_dir = Path(__file__).parent
        
        self.collector = ArabicPoetryCollector(output_dir)
        self.validator = ProsodyValidator()
        self.normalizer = ArabicTextNormalizer()
    
    def collect_batch_for_meter(
        self, 
        meter_id: int, 
        batch_num: int = 1,
        batch_size: int = 20
    ) -> List[VerseData]:
        """
        Collect a complete batch of verses for a specific meter.
        
        Args:
            meter_id: Meter ID (1-20)
            batch_num: Batch number for naming
            batch_size: Number of verses to collect
        
        Returns:
            List of validated VerseData objects
        """
        meter_info = get_meter_info(meter_id)
        if not meter_info:
            print(f"❌ Error: Invalid meter ID {meter_id}")
            return []
        
        print(f"\n{'='*80}")
        print(f"Collecting batch {batch_num} for meter: {meter_info.name_ar}")
        print(f"{'='*80}")
        
        # Get verses from curated sources
        raw_verses = get_verses_by_meter(meter_info.name_ar, limit=batch_size * 2)
        
        if not raw_verses:
            print(f"⚠️  No curated verses available for {meter_info.name_ar}")
            print(f"   Attempting web collection...")
            # Fallback to web collection would go here
            return []
        
        print(f"✓ Found {len(raw_verses)} candidate verses from curated sources")
        
        # Validate and annotate each verse
        validated_verses = []
        
        for i, raw_verse in enumerate(raw_verses, 1):
            if len(validated_verses) >= batch_size:
                break
            
            # Add source info
            raw_verse['source'] = raw_verse.get('source', 'Classical diwan')
            
            # Validate and annotate
            verse_data = self.collector.validate_and_annotate(raw_verse, meter_id)
            
            if verse_data:
                validated_verses.append(verse_data)
                print(f"   [{i:2d}] ✓ {verse_data.poet[:30]:30s} | {verse_data.text[:50]}")
            else:
                print(f"   [{i:2d}] ✗ Failed validation")
        
        print(f"\n{'='*80}")
        print(f"Batch complete: {len(validated_verses)}/{batch_size} verses validated")
        print(f"{'='*80}")
        
        # Export to JSONL
        if validated_verses:
            self.collector.export_to_jsonl(
                validated_verses, 
                meter_info.name_ar, 
                batch_num
            )
        
        return validated_verses
    
    def interactive_mode(self):
        """Interactive collection mode."""
        print("\n" + "="*80)
        print("Arabic Prosody ML Dataset Collection Tool")
        print("Interactive Mode")
        print("="*80)
        
        # List available meters
        print("\nAvailable meters:")
        meters = list_all_meters()
        
        for meter in meters:
            print(f"  {meter['id']:2d}. {meter['name_ar']:20s} ({meter['name_en']})")
        
        print("\n" + "="*80)
        
        return meters


def main():
    """Main entry point."""
    output_dir = Path(__file__).parent
    orchestrator = DatasetOrchestrator(output_dir)
    
    # Display meters
    meters = orchestrator.interactive_mode()
    
    print("\n📋 Ready to begin collection.")
    print("\nUsage:")
    print("  1. Choose a meter by ID")
    print("  2. Batches of 20 verses will be collected and exported to JSONL")
    print("  3. Each batch requires approval before continuing")
    print("\nTo begin, respond with the meter ID you want to start with.")
    

if __name__ == '__main__':
    main()
