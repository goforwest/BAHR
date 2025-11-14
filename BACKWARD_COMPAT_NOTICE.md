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
