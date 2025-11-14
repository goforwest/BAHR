#!/usr/bin/env python3
"""
Poet Distribution Checker

Ensures no single poet exceeds 5% representation in any meter.
Validates poet diversity across the dataset.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import poetry_sources


def check_poet_distribution(meter: str, max_percentage: float = 5.0) -> Dict:
    """
    Check poet distribution for a specific meter.
    
    Args:
        meter: Meter name
        max_percentage: Maximum allowed percentage per poet (default: 5%)
    
    Returns:
        Dict with analysis results
    """
    verses = poetry_sources.get_verses_by_meter(meter)
    total = len(verses)
    
    if total == 0:
        return {
            'meter': meter,
            'total_verses': 0,
            'total_poets': 0,
            'violations': [],
            'distribution': {}
        }
    
    # Count verses per poet
    poet_counts = defaultdict(int)
    for verse in verses:
        poet = verse.get('poet', 'Unknown')
        poet_counts[poet] += 1
    
    # Calculate percentages and find violations
    violations = []
    distribution = {}
    
    for poet, count in poet_counts.items():
        percentage = (count / total) * 100
        distribution[poet] = {
            'count': count,
            'percentage': percentage
        }
        
        if percentage > max_percentage:
            violations.append({
                'poet': poet,
                'count': count,
                'percentage': percentage,
                'excess': percentage - max_percentage,
                'verses_to_remove': count - int(total * max_percentage / 100)
            })
    
    # Sort violations by severity
    violations.sort(key=lambda x: x['percentage'], reverse=True)
    
    return {
        'meter': meter,
        'total_verses': total,
        'total_poets': len(poet_counts),
        'violations': violations,
        'distribution': distribution
    }


def check_all_meters(max_percentage: float = 5.0) -> Dict:
    """Check poet distribution across all meters."""
    meters = poetry_sources.list_available_meters()
    results = {
        'max_percentage': max_percentage,
        'total_meters': len(meters),
        'meters_with_violations': 0,
        'total_violations': 0,
        'meters': {}
    }
    
    for meter in meters:
        meter_result = check_poet_distribution(meter, max_percentage)
        results['meters'][meter] = meter_result
        
        if meter_result['violations']:
            results['meters_with_violations'] += 1
            results['total_violations'] += len(meter_result['violations'])
    
    return results


def print_meter_report(result: Dict):
    """Print report for a single meter."""
    print(f'\n{"="*70}')
    print(f'Meter: {result["meter"]}')
    print(f'{"="*70}')
    print(f'Total verses: {result["total_verses"]}')
    print(f'Total poets:  {result["total_poets"]}')
    print(f'Violations:   {len(result["violations"])}')
    
    if result['violations']:
        print(f'\n⚠️  Poet Balance Violations:')
        print(f'{"-"*70}')
        for v in result['violations']:
            print(f'  ❌ {v["poet"]:30s}: {v["count"]:3d} verses ({v["percentage"]:.1f}%)')
            print(f'      Exceeds threshold by {v["excess"]:.1f}% ({v["verses_to_remove"]} verses)')
    else:
        print(f'\n✅ No violations - poet distribution is balanced')
    
    # Show top 10 poets
    print(f'\nTop 10 Poets:')
    print(f'{"-"*70}')
    sorted_poets = sorted(result['distribution'].items(), 
                         key=lambda x: x[1]['count'], reverse=True)
    
    for i, (poet, data) in enumerate(sorted_poets[:10], 1):
        status = '⚠️' if data['percentage'] > result.get('max_percentage', 5.0) else '✅'
        print(f'{i:2d}. {status} {poet:30s}: {data["count"]:3d} verses ({data["percentage"]:.1f}%)')
    
    print(f'{"="*70}\n')


def print_summary_report(results: Dict):
    """Print summary report for all meters."""
    print(f'\n{"="*70}')
    print(f'POET DISTRIBUTION ANALYSIS - ALL METERS')
    print(f'{"="*70}')
    print(f'Maximum allowed per poet: {results["max_percentage"]}%')
    print(f'Total meters analyzed:    {results["total_meters"]}')
    print(f'Meters with violations:   {results["meters_with_violations"]}')
    print(f'Total violations:         {results["total_violations"]}')
    print(f'{"="*70}\n')
    
    if results['meters_with_violations'] > 0:
        print(f'Meters with Violations:')
        print(f'{"-"*70}')
        
        for meter, data in results['meters'].items():
            if data['violations']:
                print(f'\n{meter}:')
                for v in data['violations']:
                    print(f'  ❌ {v["poet"]:30s}: {v["count"]:3d} verses ({v["percentage"]:.1f}%) '
                          f'[excess: {v["verses_to_remove"]}]')
        
        print(f'\n{"="*70}')
        print(f'⚠️  Action Required: Remove or redistribute verses to balance poet representation')
    else:
        print(f'✅ All meters have balanced poet representation!')
    
    print(f'{"="*70}\n')


def export_report(results: Dict, output_file: str):
    """Export full report to JSON."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f'✅ Report exported to {output_file}')


def generate_recommendations(results: Dict) -> List[Dict]:
    """Generate actionable recommendations to fix violations."""
    recommendations = []
    
    for meter, data in results['meters'].items():
        if not data['violations']:
            continue
        
        for v in data['violations']:
            recommendations.append({
                'meter': meter,
                'poet': v['poet'],
                'current_count': v['count'],
                'current_percentage': v['percentage'],
                'target_percentage': results['max_percentage'],
                'verses_to_remove': v['verses_to_remove'],
                'action': f'Remove {v["verses_to_remove"]} verses by {v["poet"]} from {meter}',
                'priority': 'HIGH' if v['percentage'] > 10 else 'MEDIUM'
            })
    
    # Sort by priority and percentage
    recommendations.sort(key=lambda x: (x['priority'], -x['current_percentage']))
    
    return recommendations


def print_recommendations(recommendations: List[Dict]):
    """Print actionable recommendations."""
    if not recommendations:
        print('✅ No actions needed - all distributions are balanced\n')
        return
    
    print(f'\n{"="*70}')
    print(f'ACTIONABLE RECOMMENDATIONS')
    print(f'{"="*70}\n')
    
    high_priority = [r for r in recommendations if r['priority'] == 'HIGH']
    medium_priority = [r for r in recommendations if r['priority'] == 'MEDIUM']
    
    if high_priority:
        print(f'🔴 HIGH PRIORITY ({len(high_priority)} actions):')
        print(f'{"-"*70}')
        for i, rec in enumerate(high_priority, 1):
            print(f'{i}. {rec["action"]}')
            print(f'   Current: {rec["current_percentage"]:.1f}% → Target: ≤{rec["target_percentage"]:.1f}%')
        print()
    
    if medium_priority:
        print(f'🟡 MEDIUM PRIORITY ({len(medium_priority)} actions):')
        print(f'{"-"*70}')
        for i, rec in enumerate(medium_priority, 1):
            print(f'{i}. {rec["action"]}')
            print(f'   Current: {rec["current_percentage"]:.1f}% → Target: ≤{rec["target_percentage"]:.1f}%')
        print()
    
    print(f'{"="*70}\n')


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Check poet distribution balance')
    parser.add_argument('--meter', '-m', type=str, 
                       help='Check specific meter only')
    parser.add_argument('--max-percentage', '-p', type=float, default=5.0, 
                       help='Maximum allowed percentage per poet (default: 5.0)')
    parser.add_argument('--export', '-e', type=str, 
                       help='Export report to JSON file')
    parser.add_argument('--recommendations', '-r', action='store_true', 
                       help='Show actionable recommendations')
    
    args = parser.parse_args()
    
    if args.meter:
        # Check specific meter
        meters = poetry_sources.list_available_meters()
        if args.meter not in meters:
            print(f'❌ Error: Meter "{args.meter}" not found')
            sys.exit(1)
        
        result = check_poet_distribution(args.meter, args.max_percentage)
        print_meter_report(result)
        
        if args.recommendations and result['violations']:
            recs = generate_recommendations({
                'max_percentage': args.max_percentage,
                'meters': {args.meter: result}
            })
            print_recommendations(recs)
    
    else:
        # Check all meters
        results = check_all_meters(args.max_percentage)
        print_summary_report(results)
        
        if args.recommendations:
            recs = generate_recommendations(results)
            print_recommendations(recs)
        
        if args.export:
            export_report(results, args.export)
    
    # Exit code
    if args.meter:
        sys.exit(0 if not result['violations'] else 1)
    else:
        sys.exit(0 if results['total_violations'] == 0 else 1)


if __name__ == '__main__':
    main()
