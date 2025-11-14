#!/usr/bin/env python3
"""
BAHR ML Pipeline - Validation Script

Checks that all components are properly installed and configured.
Run this before executing the main pipeline.

Usage:
    python ml_pipeline/validate_setup.py
"""

import sys
import importlib
from pathlib import Path


class SetupValidator:
    """Validate ML pipeline setup."""
    
    def __init__(self):
        self.results = []
        self.errors = []
        
    def check_python_version(self):
        """Check Python version (requires 3.9+)."""
        print("Checking Python version...")
        major, minor = sys.version_info[:2]
        
        if major >= 3 and minor >= 9:
            self.results.append(f"✅ Python {major}.{minor} (OK)")
            return True
        else:
            self.errors.append(f"❌ Python {major}.{minor} (requires 3.9+)")
            return False
    
    def check_required_packages(self):
        """Check required Python packages."""
        print("\nChecking required packages...")
        
        required = [
            'numpy',
            'pandas',
            'sklearn',
            'matplotlib',
            'seaborn',
            'joblib',
            'shap'
        ]
        
        missing = []
        
        for package in required:
            try:
                importlib.import_module(package)
                self.results.append(f"✅ {package}")
            except ImportError:
                missing.append(package)
                self.errors.append(f"❌ {package} not found")
        
        if missing:
            print(f"\n⚠️  Missing packages: {', '.join(missing)}")
            print("Install with: pip install " + " ".join(missing))
            return False
        
        return True
    
    def check_optional_packages(self):
        """Check optional packages (XGBoost, LightGBM, PyTorch)."""
        print("\nChecking optional packages...")
        
        optional = {
            'xgboost': 'Gradient boosting (ensemble)',
            'lightgbm': 'Gradient boosting (ensemble)',
            'torch': 'Deep learning (BiLSTM-CRF)',
            'transformers': 'Transfer learning (AraBERT)'
        }
        
        for package, purpose in optional.items():
            try:
                importlib.import_module(package)
                self.results.append(f"✅ {package} ({purpose})")
            except ImportError:
                self.results.append(f"⚠️  {package} not installed ({purpose})")
    
    def check_directory_structure(self):
        """Check required directories exist."""
        print("\nChecking directory structure...")
        
        required_dirs = [
            'backend/app/ml',
            'ml_pipeline',
            'data/ml',
            'models',
            'dataset/evaluation'
        ]
        
        for dir_path in required_dirs:
            path = Path(dir_path)
            if path.exists():
                self.results.append(f"✅ {dir_path}/")
            else:
                self.errors.append(f"❌ {dir_path}/ not found")
                # Try to create it
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    self.results.append(f"  → Created {dir_path}/")
                except Exception as e:
                    self.errors.append(f"  → Failed to create: {e}")
    
    def check_required_files(self):
        """Check required files exist."""
        print("\nChecking required files...")
        
        required_files = [
            'backend/app/ml/feature_extractor.py',
            'ml_pipeline/feature_optimization.py',
            'ml_pipeline/hyperparameter_search.py',
            'ml_pipeline/ensemble_trainer.py',
            'ml_pipeline/evaluation_suite.py',
            'ml_pipeline/Makefile',
            'requirements/ml.txt'
        ]
        
        for file_path in required_files:
            path = Path(file_path)
            if path.exists():
                self.results.append(f"✅ {file_path}")
            else:
                self.errors.append(f"❌ {file_path} not found")
    
    def check_data_availability(self):
        """Check if training data is available."""
        print("\nChecking data availability...")
        
        golden_set = Path('dataset/evaluation/golden_set_v1_3_with_sari.jsonl')
        
        if golden_set.exists():
            self.results.append(f"✅ Golden dataset found")
            
            # Count verses
            try:
                with open(golden_set, 'r', encoding='utf-8') as f:
                    count = sum(1 for line in f if line.strip())
                self.results.append(f"  → {count} verses available")
            except Exception as e:
                self.errors.append(f"  → Failed to read: {e}")
        else:
            self.errors.append(f"❌ Golden dataset not found")
            self.errors.append(f"  → Expected: {golden_set}")
        
        # Check if features already extracted
        X_train = Path('data/ml/X_train.npy')
        y_train = Path('data/ml/y_train.npy')
        
        if X_train.exists() and y_train.exists():
            self.results.append(f"✅ Training features extracted")
        else:
            self.results.append(f"⚠️  Training features not yet extracted")
            self.results.append(f"  → Run: make extract-features")
    
    def run_all_checks(self):
        """Run all validation checks."""
        print("="*80)
        print("BAHR ML Pipeline - Setup Validation")
        print("="*80)
        
        checks = [
            self.check_python_version,
            self.check_required_packages,
            self.check_optional_packages,
            self.check_directory_structure,
            self.check_required_files,
            self.check_data_availability
        ]
        
        for check in checks:
            check()
        
        # Print summary
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        
        if not self.errors:
            print("\n✅ All checks passed! You're ready to run the pipeline.")
            print("\nQuick start:")
            print("  make phase5-quick")
            return True
        else:
            print(f"\n❌ Found {len(self.errors)} error(s):")
            for error in self.errors:
                print(f"  {error}")
            
            print("\nFix errors and run validation again.")
            return False


def main():
    validator = SetupValidator()
    success = validator.run_all_checks()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
