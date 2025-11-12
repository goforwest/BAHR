#!/usr/bin/env python3
"""
Complete workflow for golden set expansion.

This script guides you through the entire expansion process:
1. Review current meter gaps
2. Add new verses
3. Validate entries
4. Precompute patterns
5. Evaluate accuracy
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from collections import Counter

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
GOLDEN_SET_PATH = PROJECT_ROOT / "dataset/evaluation/golden_set_v1_0_with_patterns.jsonl"
EXPANSION_PATH = PROJECT_ROOT / "dataset/evaluation/golden_set_v1_1_expansion.jsonl"
MERGED_PATH = PROJECT_ROOT / "dataset/evaluation/golden_set_v1_1_merged.jsonl"


class Colors:
    """Terminal colors."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print section header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"{text}")
    print(f"{'='*70}{Colors.END}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓{Colors.END} {text}")


def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}✗{Colors.END} {text}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠{Colors.END}  {text}")


def print_info(text: str):
    """Print info message."""
    print(f"{Colors.CYAN}ℹ{Colors.END}  {text}")


def get_meter_statistics() -> dict:
    """Get comprehensive meter statistics."""
    golden_meters = []
    expansion_meters = []

    # Read golden set
    with open(GOLDEN_SET_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            verse = json.loads(line)
            golden_meters.append(verse['meter'])

    # Read expansion if exists
    if EXPANSION_PATH.exists():
        with open(EXPANSION_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                verse = json.loads(line)
                expansion_meters.append(verse['meter'])

    all_meters = golden_meters + expansion_meters
    counter = Counter(all_meters)

    return {
        'golden_count': len(golden_meters),
        'expansion_count': len(expansion_meters),
        'total_count': len(all_meters),
        'meter_distribution': counter,
        'sorted_meters': sorted(counter.items(), key=lambda x: x[1])
    }


def show_status():
    """Show current expansion status."""
    print_header("EXPANSION STATUS")

    stats = get_meter_statistics()

    print(f"Golden set (v1.0):  {stats['golden_count']} verses")
    print(f"Expansion added:    {stats['expansion_count']} verses")
    print(f"{Colors.BOLD}Total current:      {stats['total_count']} verses{Colors.END}")

    TARGET_MIN = 15
    priority_meters = [(m, c) for m, c in stats['sorted_meters'] if c < TARGET_MIN]
    verses_needed = sum(TARGET_MIN - c for _, c in priority_meters)

    print(f"\nMeters below target ({TARGET_MIN}): {len(priority_meters)}")
    print(f"Verses needed for balance: {verses_needed}")

    if EXPANSION_PATH.exists():
        print_success(f"Expansion file exists: {EXPANSION_PATH.name}")
    else:
        print_warning(f"Expansion file not created yet: {EXPANSION_PATH.name}")


def show_priority_meters():
    """Show meters that need more verses."""
    print_header("PRIORITY METERS")

    stats = get_meter_statistics()
    TARGET_MIN = 15

    print(f"Meters needing verses to reach minimum ({TARGET_MIN}):\n")
    print(f"{'Current':<8} {'Need':<6} {'Meter'}")
    print("-" * 60)

    total_needed = 0
    for meter, count in stats['sorted_meters']:
        if count < TARGET_MIN:
            need = TARGET_MIN - count
            total_needed += need
            print(f"{count:<8} {need:<6} {meter}")

    print("-" * 60)
    print(f"{'Total:':<8} {total_needed:<6}")


def validate_expansion():
    """Validate the expansion file."""
    print_header("VALIDATING EXPANSION")

    if not EXPANSION_PATH.exists():
        print_warning("No expansion file to validate")
        return False

    print_info(f"Validating: {EXPANSION_PATH}")

    result = subprocess.run([
        sys.executable,
        'tools/validate_expansion_verse.py',
        '--file',
        str(EXPANSION_PATH)
    ], cwd=PROJECT_ROOT)

    if result.returncode == 0:
        print_success("Validation passed")
        return True
    else:
        print_error("Validation failed - fix errors before proceeding")
        return False


def precompute_patterns():
    """Run pattern precomputation on expansion verses."""
    print_header("PRECOMPUTING PATTERNS")

    if not EXPANSION_PATH.exists():
        print_warning("No expansion file to process")
        return False

    print_info("Running pattern precomputation...")

    result = subprocess.run([
        sys.executable,
        'tools/precompute_golden_patterns.py',
        '--file',
        str(EXPANSION_PATH)
    ], cwd=PROJECT_ROOT)

    if result.returncode == 0:
        print_success("Pattern precomputation complete")
        return True
    else:
        print_error("Pattern precomputation failed")
        return False


def merge_files():
    """Merge golden set and expansion into unified file."""
    print_header("MERGING FILES")

    if not EXPANSION_PATH.exists():
        print_warning("No expansion file to merge")
        return False

    print_info("Merging golden set and expansion...")

    verses = []

    # Read golden set
    with open(GOLDEN_SET_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            verses.append(json.loads(line))

    golden_count = len(verses)

    # Read expansion
    with open(EXPANSION_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            verses.append(json.loads(line))

    expansion_count = len(verses) - golden_count

    # Write merged file
    with open(MERGED_PATH, 'w', encoding='utf-8') as f:
        for verse in verses:
            f.write(json.dumps(verse, ensure_ascii=False) + '\n')

    print_success(f"Merged {golden_count} + {expansion_count} = {len(verses)} verses")
    print_info(f"Saved to: {MERGED_PATH}")

    return True


def evaluate_accuracy():
    """Run accuracy evaluation on merged dataset."""
    print_header("EVALUATING ACCURACY")

    if not MERGED_PATH.exists():
        print_warning("No merged file to evaluate")
        return False

    print_info("Running detector evaluation...")

    result = subprocess.run([
        sys.executable,
        'tools/evaluate_detector_v1.py',
        '--file',
        str(MERGED_PATH)
    ], cwd=PROJECT_ROOT)

    if result.returncode == 0:
        print_success("Evaluation complete")
        return True
    else:
        print_warning("Evaluation completed with issues")
        return False


def show_menu():
    """Show main menu."""
    print_header("GOLDEN SET EXPANSION WORKFLOW")

    print("Commands:")
    print()
    print("  1. status        - Show current expansion status")
    print("  2. priority      - Show priority meters needing verses")
    print("  3. stats         - Show detailed meter statistics")
    print("  4. add           - Add new verse (interactive)")
    print("  5. validate      - Validate expansion file")
    print("  6. precompute    - Precompute prosody patterns")
    print("  7. merge         - Merge golden set + expansion")
    print("  8. evaluate      - Evaluate accuracy on merged set")
    print("  9. full-cycle    - Run complete workflow (validate→precompute→merge→evaluate)")
    print()
    print("  help             - Show this menu")
    print("  quit             - Exit")
    print()


def run_full_cycle():
    """Run complete workflow."""
    print_header("RUNNING FULL EXPANSION CYCLE")

    print_info("Step 1/4: Validating expansion...")
    if not validate_expansion():
        print_error("Validation failed - stopping workflow")
        return False

    print_info("Step 2/4: Precomputing patterns...")
    if not precompute_patterns():
        print_error("Precomputation failed - stopping workflow")
        return False

    print_info("Step 3/4: Merging files...")
    if not merge_files():
        print_error("Merge failed - stopping workflow")
        return False

    print_info("Step 4/4: Evaluating accuracy...")
    if not evaluate_accuracy():
        print_warning("Evaluation completed with warnings")

    print_success("Full cycle complete!")
    return True


def main():
    """Main interactive workflow."""
    if len(sys.argv) > 1:
        # Command-line mode
        command = sys.argv[1]

        if command == 'status':
            show_status()
        elif command == 'priority':
            show_priority_meters()
        elif command == 'stats':
            subprocess.run([sys.executable, 'tools/expansion_helper.py', 'stats'], cwd=PROJECT_ROOT)
        elif command == 'validate':
            validate_expansion()
        elif command == 'precompute':
            precompute_patterns()
        elif command == 'merge':
            merge_files()
        elif command == 'evaluate':
            evaluate_accuracy()
        elif command == 'full-cycle':
            run_full_cycle()
        elif command == 'add':
            subprocess.run([sys.executable, 'tools/expansion_helper.py', 'add'], cwd=PROJECT_ROOT)
        else:
            print(f"Unknown command: {command}")
            show_menu()
            sys.exit(1)
    else:
        # Interactive mode
        show_menu()

        while True:
            try:
                command = input(f"{Colors.CYAN}→{Colors.END} ").strip().lower()

                if not command:
                    continue

                if command in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break

                elif command in ['help', 'h', '?']:
                    show_menu()

                elif command in ['1', 'status']:
                    show_status()

                elif command in ['2', 'priority']:
                    show_priority_meters()

                elif command in ['3', 'stats']:
                    subprocess.run([sys.executable, 'tools/expansion_helper.py', 'stats'], cwd=PROJECT_ROOT)

                elif command in ['4', 'add']:
                    subprocess.run([sys.executable, 'tools/expansion_helper.py', 'add'], cwd=PROJECT_ROOT)

                elif command in ['5', 'validate']:
                    validate_expansion()

                elif command in ['6', 'precompute']:
                    precompute_patterns()

                elif command in ['7', 'merge']:
                    merge_files()

                elif command in ['8', 'evaluate']:
                    evaluate_accuracy()

                elif command in ['9', 'full-cycle']:
                    run_full_cycle()

                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands")

            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break


if __name__ == '__main__':
    main()
