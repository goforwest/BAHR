#!/bin/bash
set -e

echo "Creating backward compatibility symlinks..."

# Create symlinks for critical paths (temporary - 30 days)
# These allow old references to work during transition period

# Backend symlink
if [[ ! -e "backend" ]] && [[ -d "src/backend" ]]; then
    ln -s src/backend backend
    echo "  Created symlink: backend -> src/backend"
fi

# Frontend symlink
if [[ ! -e "frontend" ]] && [[ -d "src/frontend" ]]; then
    ln -s src/frontend frontend
    echo "  Created symlink: frontend -> src/frontend"
fi

# Dataset symlink
if [[ ! -e "dataset" ]] && [[ -d "data/processed/datasets" ]]; then
    ln -s data/processed/datasets dataset
    echo "  Created symlink: dataset -> data/processed/datasets"
fi

# ml_dataset symlink
if [[ ! -e "ml_dataset" ]] && [[ -d "data/raw/ml_dataset" ]]; then
    ln -s data/raw/ml_dataset ml_dataset
    echo "  Created symlink: ml_dataset -> data/raw/ml_dataset"
fi

# Create deprecation notice
cat > BACKWARD_COMPAT_NOTICE.md << 'EOF'
# Backward Compatibility Notice

**Created:** $(date +%Y-%m-%d)
**Expires:** $(date -v+30d +%Y-%m-%d)

## Temporary Symlinks

The following symlinks provide backward compatibility during the transition period:

- `backend/` → `src/backend/`
- `frontend/` → `src/frontend/`
- `dataset/` → `data/processed/datasets/`
- `ml_dataset/` → `data/raw/ml_dataset/`

## Migration Required

Please update your scripts and references to use the new paths:

```bash
# OLD (deprecated)
from backend.app import main
dataset/evaluation/golden_set.jsonl

# NEW (correct)
from src.backend.app import main
data/processed/datasets/evaluation/golden_set.jsonl
```

## Removal Date

These symlinks will be **removed on $(date -v+30d +%Y-%m-%d)**.

Update your code before this date to avoid breakage.

## Questions?

See: docs/migration/REFACTOR_GUIDE.md
EOF

echo "✓ Backward compatibility layer created (30-day expiration)"
echo "  ⚠️  Remember to remove symlinks after transition period"
