#!/usr/bin/env python3
"""
Verse Collection Progress Tracker

Tracks the progress of poetry database expansion across all meters.
Shows current counts, targets, and remaining verses needed.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import poetry_sources


def get_current_counts() -> Dict[str, int]:
    """Get current verse counts for all meters."""
    meters = poetry_sources.list_available_meters()
    counts = {}
    
    for meter in meters:
        verses = poetry_sources.get_verses_by_meter(meter)
        counts[meter] = len(verses)
    
    return counts


def get_poet_distribution(meter: str) -> Dict[str, int]:
    """Get poet distribution for a specific meter."""
    verses = poetry_sources.get_verses_by_meter(meter)
    poet_counts = defaultdict(int)
    
    for verse in verses:
        poet = verse.get('poet', 'Unknown')
        poet_counts[poet] += 1
    
    return dict(poet_counts)


def calculate_progress(current: int, target: int = 100) -> float:
    """Calculate progress percentage."""
    return (current / target) * 100 if target > 0 else 0


def format_progress_bar(progress: float, width: int = 30) -> str:
    """Create a visual progress bar."""
    filled = int(width * progress / 100)
    bar = '█' * filled + '░' * (width - filled)
    return f'[{bar}] {progress:.1f}%'


def show_meter_summary(meter: str, target: int = 100):
    """Show detailed summary for a specific meter."""
    verses = poetry_sources.get_verses_by_meter(meter)
    current = len(verses)
    progress = calculate_progress(current, target)
    remaining = max(0, target - current)
    
    print(f'\n{"="*70}')
    print(f'Meter: {meter}')
    print(f'{"="*70}')
    print(f'Current verses: {current}')
    print(f'Target verses:  {target}')
    print(f'Remaining:      {remaining}')
    print(f'Progress:       {format_progress_bar(progress)}')
    
    # Poet distribution
    poet_dist = get_poet_distribution(meter)
    print(f'\nPoet Distribution ({len(poet_dist)} poets):')
    print(f'{"-"*70}')
    
    # Sort by count descending
    sorted_poets = sorted(poet_dist.items(), key=lambda x: x[1], reverse=True)
    
    for poet, count in sorted_poets[:10]:  # Show top 10
        percentage = (count / current) * 100 if current > 0 else 0
        status = '⚠️' if percentage > 5 else '✓'
        print(f'  {status} {poet:30s}: {count:3d} verses ({percentage:5.1f}%)')
    
    if len(sorted_poets) > 10:
        print(f'  ... and {len(sorted_poets) - 10} more poets')
    
    # Warnings
    print(f'\n{"Warnings":}')
    print(f'{"-"*70}')
    warnings = []
    
    for poet, count in sorted_poets:
        percentage = (count / current) * 100 if current > 0 else 0
        if percentage > 5:
            warnings.append(f'  ⚠️  {poet} exceeds 5% threshold ({percentage:.1f}%)')
    
    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print('  ✅ No poet balance issues detected')
    
    print(f'{"="*70}\n')


def show_overall_summary(target: int = 100):
    """Show summary for all meters."""
    counts = get_current_counts()
    total_current = sum(counts.values())
    total_target = len(counts) * target
    total_remaining = total_target - total_current
    overall_progress = calculate_progress(total_current, total_target)
    
    print(f'\n{"="*70}')
    print(f'POETRY DATABASE EXPANSION PROGRESS')
    print(f'{"="*70}')
    print(f'Total verses (current): {total_current}')
    print(f'Total verses (target):  {total_target}')
    print(f'Total remaining:        {total_remaining}')
    print(f'Overall progress:       {format_progress_bar(overall_progress)}')
    print(f'{"="*70}\n')
    
    # Sort meters by progress
    meter_progress = [(meter, count, calculate_progress(count, target)) 
                      for meter, count in counts.items()]
    meter_progress.sort(key=lambda x: x[2])  # Sort by progress ascending
    
    print(f'{"Meter":25s} {"Current":>8s} {"Target":>8s} {"Progress":>10s} {"Status":>10s}')
    print(f'{"-"*70}')
    
    for meter, current, progress in meter_progress:
        remaining = target - current
        status = '✅' if current >= target else f'Need {remaining}'
        print(f'{meter:25s} {current:8d} {target:8d} {progress:9.1f}% {status:>10s}')
    
    print(f'{"-"*70}')
    print(f'{"TOTAL":25s} {total_current:8d} {total_target:8d} {overall_progress:9.1f}%')
    print(f'{"="*70}\n')


def export_progress_json(output_file: str = 'expansion_progress.json', target: int = 100):
    """Export progress data as JSON."""
    counts = get_current_counts()
    
    progress_data = {
        'timestamp': str(Path(__file__).stat().st_mtime),
        'target_per_meter': target,
        'total_current': sum(counts.values()),
        'total_target': len(counts) * target,
        'total_remaining': (len(counts) * target) - sum(counts.values()),
        'overall_progress': calculate_progress(sum(counts.values()), len(counts) * target),
        'meters': {}
    }
    
    for meter, current in counts.items():
        progress_data['meters'][meter] = {
            'current': current,
            'target': target,
            'remaining': target - current,
            'progress': calculate_progress(current, target),
            'poet_count': len(get_poet_distribution(meter))
        }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)
    
    print(f'✅ Progress data exported to {output_file}')


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Track verse collection progress')
    parser.add_argument('--meter', '-m', type=str, help='Show detailed summary for specific meter')
    parser.add_argument('--target', '-t', type=int, default=100, help='Target verses per meter (default: 100)')
    parser.add_argument('--export', '-e', type=str, help='Export progress as JSON to file')
    parser.add_argument('--list-meters', '-l', action='store_true', help='List all available meters')
    
    args = parser.parse_args()
    
    if args.list_meters:
        meters = poetry_sources.list_available_meters()
        print(f'\nAvailable Meters ({len(meters)}):')
        print(f'{"-"*70}')
        for i, meter in enumerate(meters, 1):
            print(f'{i:2d}. {meter}')
        print()
        return
    
    if args.meter:
        # Show specific meter
        meters = poetry_sources.list_available_meters()
        if args.meter in meters:
            show_meter_summary(args.meter, args.target)
        else:
            print(f'❌ Error: Meter "{args.meter}" not found')
            print(f'Use --list-meters to see available meters')
            sys.exit(1)
    else:
        # Show overall summary
        show_overall_summary(args.target)
    
    if args.export:
        export_progress_json(args.export, args.target)


if __name__ == '__main__':
    main()
