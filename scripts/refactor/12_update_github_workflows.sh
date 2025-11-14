#!/bin/bash
set -e

echo "Updating GitHub Actions workflows..."

if [[ ! -d ".github/workflows" ]]; then
    echo "  No workflows directory found, skipping"
    exit 0
fi

# Update all workflow files
for workflow in .github/workflows/*.yml .github/workflows/*.yaml; do
    if [[ ! -f "$workflow" ]]; then
        continue
    fi
    
    echo "  Processing: $workflow"
    
    # Backup
    cp "$workflow" "${workflow}.bak"
    
    # Update backend paths
    sed -i '' 's|backend/|src/backend/|g' "$workflow"
    
    # Update frontend paths
    sed -i '' 's|frontend/|src/frontend/|g' "$workflow"
    
    # Update dataset paths
    sed -i '' 's|dataset/|data/processed/datasets/|g' "$workflow"
    sed -i '' 's|ml_dataset/|data/raw/ml_dataset/|g' "$workflow"
    
    # Update working directory references
    sed -i '' 's|working-directory: backend|working-directory: src/backend|g' "$workflow"
    sed -i '' 's|working-directory: frontend|working-directory: src/frontend|g' "$workflow"
    
    # Clean up backup
    rm "${workflow}.bak"
    
    echo "    ✓ Updated"
done

echo "✓ GitHub workflows updated"
