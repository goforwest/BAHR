#!/bin/bash
set -e

echo "Moving JSON/JSONL data files to results/..."

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# Create directories
mkdir -p results/ml
mkdir -p results/evaluations
mkdir -p results/phase4
mkdir -p results/phase5
mkdir -p results/diagnostics
mkdir -p results/data_processing

echo "  Moving ML results..."
[[ -f "augmentation_priorities.json" ]] && git mv "augmentation_priorities.json" "results/ml/" && echo "    ✓ augmentation_priorities.json"
[[ -f "augmented_training_results.json" ]] && git mv "augmented_training_results.json" "results/ml/" && echo "    ✓ augmented_training_results.json"

echo "  Moving evaluation results..."
[[ -f "generalization_test_results.json" ]] && git mv "generalization_test_results.json" "results/evaluations/" && echo "    ✓ generalization_test_results.json"
[[ -f "golden_dataset_validation_results.json" ]] && git mv "golden_dataset_validation_results.json" "results/evaluations/" && echo "    ✓ golden_dataset_validation_results.json"
[[ -f "golden_set_v2_evaluation_results.json" ]] && git mv "golden_set_v2_evaluation_results.json" "results/evaluations/" && echo "    ✓ golden_set_v2_evaluation_results.json"
[[ -f "hybrid_validation_results.json" ]] && git mv "hybrid_validation_results.json" "results/evaluations/" && echo "    ✓ hybrid_validation_results.json"
[[ -f "validation_results.json" ]] && git mv "validation_results.json" "results/evaluations/" && echo "    ✓ validation_results.json"

echo "  Moving phase results..."
[[ -f "phase4_evaluation_results_v1.json" ]] && git mv "phase4_evaluation_results_v1.json" "results/phase4/" && echo "    ✓ phase4_evaluation_results_v1.json"
[[ -f "phase4_improved_evaluation_output.txt" ]] && git mv "phase4_improved_evaluation_output.txt" "results/phase4/" && echo "    ✓ phase4_improved_evaluation_output.txt"
[[ -f "phase5_statistical_analysis.json" ]] && git mv "phase5_statistical_analysis.json" "results/phase5/" && echo "    ✓ phase5_statistical_analysis.json"

echo "  Moving diagnostics..."
[[ -f "problematic_meters_diagnosis.json" ]] && git mv "problematic_meters_diagnosis.json" "results/diagnostics/" && echo "    ✓ problematic_meters_diagnosis.json"

echo "  Moving data processing logs..."
[[ -f "removed_verses_log.json" ]] && git mv "removed_verses_log.json" "results/data_processing/" && echo "    ✓ removed_verses_log.json"

echo ""
echo "✓ Data files organized to results/"
