#!/bin/bash
set -e

echo "Moving Python scripts to organized locations..."

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# Create target directories
mkdir -p tests/integration
mkdir -p scripts/ml
mkdir -p scripts/data_processing

# Move integration tests to tests/integration/
TEST_FILES=(
    "test_detector_manual.py"
    "test_ml_integration.py"
    "test_golden_set_v2.py"
    "test_enhanced_features.py"
    "test_shamela_verses.py"
    "test_augmentation.py"
    "test_generalization.py"
    "test_feature_extractor.py"
    "test_feedback.py"
    "test_multi_candidate.py"
    "test_pattern_fix.py"
)

echo "  Moving integration tests..."
for file in "${TEST_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        git mv "$file" "tests/integration/"
        echo "    ✓ $file → tests/integration/"
    fi
done

# Move ML scripts to scripts/ml/
ML_SCRIPTS=(
    "train_baseline_models.py"
    "train_ensemble.py"
    "train_hyperparameter_tuning.py"
    "train_on_augmented_data.py"
    "validate_augmented_model.py"
    "validate_hybrid.py"
    "run_full_augmentation.py"
    "count_features.py"
    "diagnose_features.py"
)

echo "  Moving ML scripts..."
for file in "${ML_SCRIPTS[@]}"; do
    if [[ -f "$file" ]]; then
        git mv "$file" "scripts/ml/"
        echo "    ✓ $file → scripts/ml/"
    fi
done

# Move data processing scripts
DATA_SCRIPTS=(
    "analyze_dataset_distribution.py"
    "add_missing_patterns_and_validate.py"
    "extract_missing_patterns.py"
    "missing_meters_patterns.py"
)

echo "  Moving data processing scripts..."
for file in "${DATA_SCRIPTS[@]}"; do
    if [[ -f "$file" ]]; then
        git mv "$file" "scripts/data_processing/"
        echo "    ✓ $file → scripts/data_processing/"
    fi
done

echo ""
echo "✓ Python scripts moved (24 files)"
