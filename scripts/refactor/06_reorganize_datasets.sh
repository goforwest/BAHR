#!/bin/bash
set -e

echo "Reorganizing datasets into data/ structure..."

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# Create new data structure
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/interim

echo "  Moving ml_dataset to data/raw..."
if [[ -d "ml_dataset" ]]; then
    git mv ml_dataset data/raw/ml_dataset
    echo "    ✓ ml_dataset/ → data/raw/ml_dataset/ (158 files)"
fi

echo "  Moving dataset to data/processed..."
if [[ -d "dataset" ]]; then
    git mv dataset data/processed/datasets
    echo "    ✓ dataset/ → data/processed/datasets/"
fi

echo "  Moving interim data file..."
if [[ -f "mutadarik_verses_partial.jsonl" ]]; then
    git mv mutadarik_verses_partial.jsonl data/interim/
    echo "    ✓ mutadarik_verses_partial.jsonl → data/interim/"
fi

echo ""
echo "✓ Datasets reorganized to data/"
echo "  Structure:"
echo "  - data/raw/ml_dataset/       (original JSONL datasets)"
echo "  - data/processed/datasets/   (processed evaluation data)"
echo "  - data/interim/              (intermediate processing files)"
