#!/usr/bin/env python3
"""
Smoke Tests for Post-Refactor Validation

Critical path validation to ensure core functionality works after repository refactoring.
Run immediately after migration to catch breaking changes.
"""

import sys
import json
from pathlib import Path
from typing import List, Tuple

# Color codes for output
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
NC = "\033[0m"  # No Color


def print_test(name: str, passed: bool, message: str = ""):
    """Print test result with color coding"""
    status = f"{GREEN}✓ PASS{NC}" if passed else f"{RED}✗ FAIL{NC}"
    print(f"  {status} - {name}")
    if message and not passed:
        print(f"    {message}")


def test_file_structure() -> bool:
    """Verify critical directories and files exist"""
    print("\n[1/6] Testing File Structure...")
    
    critical_paths = [
        "src/backend/app/main.py",
        "src/backend/app/core/prosody/detector_v2.py",
        "data/processed/datasets",
        "data/raw/ml_dataset",
        "scripts/ml",
        "scripts/data_processing",
        "tests/integration",
        "models",
        "docs",
    ]
    
    all_passed = True
    for path_str in critical_paths:
        path = Path(path_str)
        exists = path.exists()
        print_test(f"Path exists: {path_str}", exists, f"Missing: {path_str}")
        if not exists:
            all_passed = False
    
    return all_passed


def test_python_imports() -> bool:
    """Verify Python imports work correctly"""
    print("\n[2/6] Testing Python Imports...")
    
    # Test backend package can be imported
    try:
        sys.path.insert(0, str(Path("src/backend").resolve()))
        
        # Test critical imports
        from app.core.prosody.detector_v2 import BahrDetectorV2
        print_test("Import BahrDetectorV2", True)
        
        from app.ml.model_loader import ml_service
        print_test("Import ml_service", True)
        
        from app.config import settings
        print_test("Import settings", True)
        
        return True
        
    except ImportError as e:
        print_test("Backend imports", False, f"Import error: {e}")
        return False


def test_dataset_accessibility() -> bool:
    """Verify datasets are accessible at new locations"""
    print("\n[3/6] Testing Dataset Accessibility...")
    
    datasets = {
        "Golden Set": "data/processed/datasets/evaluation/golden_set_v0_80_complete.jsonl",
        "ML Dataset Dir": "data/raw/ml_dataset",
        "Interim Data": "data/interim",
    }
    
    all_passed = True
    for name, path_str in datasets.items():
        path = Path(path_str)
        exists = path.exists()
        
        if exists and path.is_file():
            # Verify file is readable
            try:
                with open(path) as f:
                    first_line = f.readline()
                    if first_line:
                        print_test(f"{name} readable", True)
                    else:
                        print_test(f"{name} readable", False, "File is empty")
                        all_passed = False
            except Exception as e:
                print_test(f"{name} readable", False, str(e))
                all_passed = False
        elif exists and path.is_dir():
            print_test(f"{name} exists", True)
        else:
            print_test(f"{name} exists", False, f"Not found: {path_str}")
            all_passed = False
    
    return all_passed


def test_configuration_files() -> bool:
    """Verify configuration files are in correct locations"""
    print("\n[4/6] Testing Configuration Files...")
    
    configs = [
        "railway.toml",  # Must stay in root
        "src/backend/.env.example",
        "src/backend/alembic.ini",
        "src/backend/requirements.txt",
    ]
    
    all_passed = True
    for config in configs:
        path = Path(config)
        exists = path.exists()
        print_test(f"Config: {config}", exists, f"Missing: {config}")
        if not exists:
            all_passed = False
    
    return all_passed


def test_backward_compatibility() -> bool:
    """Verify backward compatibility symlinks if they exist"""
    print("\n[5/6] Testing Backward Compatibility...")
    
    # Check if symlinks exist (they should during transition period)
    symlinks = {
        "backend": "src/backend",
        "frontend": "src/frontend",
        "dataset": "data/processed/datasets",
        "ml_dataset": "data/raw/ml_dataset",
    }
    
    symlink_count = 0
    for link_name, target in symlinks.items():
        link_path = Path(link_name)
        if link_path.exists() and link_path.is_symlink():
            actual_target = link_path.resolve()
            expected_target = Path(target).resolve()
            
            if actual_target == expected_target:
                print_test(f"Symlink {link_name} → {target}", True)
                symlink_count += 1
            else:
                print_test(
                    f"Symlink {link_name}", 
                    False, 
                    f"Points to {actual_target}, expected {expected_target}"
                )
    
    if symlink_count > 0:
        print(f"  ℹ️  Found {symlink_count} backward compatibility symlinks")
        return True
    else:
        print("  ℹ️  No backward compatibility symlinks (expected after transition)")
        return True


def test_integration_tests_discoverable() -> bool:
    """Verify integration tests can be discovered by pytest"""
    print("\n[6/6] Testing Integration Test Discovery...")
    
    test_dir = Path("tests/integration")
    
    if not test_dir.exists():
        print_test("Integration test directory", False, "tests/integration/ not found")
        return False
    
    # Find test files
    test_files = list(test_dir.glob("test_*.py"))
    
    if len(test_files) > 0:
        print_test(f"Found {len(test_files)} integration test files", True)
        
        # Verify a few expected tests
        expected_tests = [
            "test_detector_manual.py",
            "test_ml_integration.py",
            "test_golden_set_v2.py",
        ]
        
        for expected in expected_tests:
            found = any(t.name == expected for t in test_files)
            print_test(f"  Found {expected}", found)
        
        return True
    else:
        print_test("Integration tests", False, "No test_*.py files found")
        return False


def main():
    """Run all smoke tests"""
    print("=" * 60)
    print("BAHR Repository Refactor - Smoke Tests")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Python Imports", test_python_imports),
        ("Dataset Accessibility", test_dataset_accessibility),
        ("Configuration Files", test_configuration_files),
        ("Backward Compatibility", test_backward_compatibility),
        ("Integration Tests", test_integration_tests_discoverable),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"{RED}✗ EXCEPTION{NC} in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("SMOKE TEST SUMMARY")
    print("=" * 60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = f"{GREEN}✓{NC}" if passed else f"{RED}✗{NC}"
        print(f"  {status} {name}")
    
    print(f"\nResults: {passed_count}/{total_count} passed")
    
    if passed_count == total_count:
        print(f"{GREEN}✓ ALL SMOKE TESTS PASSED{NC}")
        print("\nNext steps:")
        print("  1. Run full test suite: pytest src/backend/tests/ tests/integration/")
        print("  2. Verify CI/CD pipelines")
        print("  3. Test deployment to staging")
        return 0
    else:
        print(f"{RED}✗ SOME SMOKE TESTS FAILED{NC}")
        print("\n⚠️  DO NOT PROCEED TO PRODUCTION")
        print("Fix the failed tests before continuing migration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
