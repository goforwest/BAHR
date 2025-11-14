#!/bin/bash
set -e

echo "Handling duplicate files (archiving)..."

# Create archive directory for duplicates
mkdir -p archive/duplicates

# Handle optimized_feature_indices.npy duplicate
if [[ -f "ml_pipeline/results/optimized_feature_indices.npy" ]]; then
    git mv ml_pipeline/results/optimized_feature_indices.npy archive/duplicates/
    echo "  Archived: ml_pipeline/results/optimized_feature_indices.npy"
fi

# Handle .backup file
if [[ -f "dataset/evaluation/golden_set_v0_80_complete.backup.jsonl" ]]; then
    git mv dataset/evaluation/golden_set_v0_80_complete.backup.jsonl archive/duplicates/
    echo "  Archived: dataset/evaluation/golden_set_v0_80_complete.backup.jsonl"
fi

# Handle alembic duplicates in database/migrations
if [[ -f "backend/database/migrations/script.py.mako" ]]; then
    git mv backend/database/migrations/script.py.mako archive/duplicates/
    echo "  Archived: backend/database/migrations/script.py.mako"
fi

if [[ -f "backend/database/migrations/README" ]]; then
    git mv backend/database/migrations/README archive/duplicates/
    echo "  Archived: backend/database/migrations/README"
fi

# Handle empty files - review and remove
echo "  Reviewing empty files..."

# Create directory for empty files
mkdir -p archive/duplicates/empty_files

EMPTY_FILES=(
    "backend/requirements/minimal-production.txt"
    "backend/tests/core/prosody/__init__.py"
    "docs/devops/DOCKER_IMAGE_SIZE_OPTIMIZATION.md"
)

for file in "${EMPTY_FILES[@]}"; do
    if [[ -f "$file" ]] && [[ ! -s "$file" ]]; then
        git mv "$file" archive/duplicates/empty_files/
        echo "  Archived empty: $file"
    fi
done

# Handle tawil duplicate batches in ml_dataset expansion_staging
echo "  Checking for duplicates in ml_dataset/expansion_staging..."

# Compare verified/ vs by_meter/ for tawil batches
if [[ -d "ml_dataset/expansion_staging/verified" ]] && [[ -d "ml_dataset/expansion_staging/by_meter/الطويل" ]]; then
    for batch in ml_dataset/expansion_staging/verified/tawil_batch*.jsonl; do
        if [[ -f "$batch" ]]; then
            filename=$(basename "$batch")
            meter_batch="ml_dataset/expansion_staging/by_meter/الطويل/${filename/tawil_batch/batch}"
            
            if [[ -f "$meter_batch" ]]; then
                # Keep in verified/, archive from by_meter/
                mkdir -p archive/duplicates/ml_dataset_tawil/
                git mv "$meter_batch" archive/duplicates/ml_dataset_tawil/
                echo "  Archived duplicate: $meter_batch"
            fi
        fi
    done
fi

echo "✓ Duplicates archived"
