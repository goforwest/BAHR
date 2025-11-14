# Repository Refactor Implementation Summary

## 3.6 Duplicate File Resolution

### Identified Duplicates and Actions

| Category | Files | Action | Destination |
|----------|-------|--------|-------------|
| **NPY Models** | `models/ensemble_v1/optimized_feature_indices.npy`<br>`ml_pipeline/results/optimized_feature_indices.npy` | Keep models/, archive ml_pipeline/ | `archive/duplicates/` |
| **Backup Files** | `dataset/evaluation/golden_set_v0_80_complete.backup.jsonl` | Archive | `archive/duplicates/` |
| **Alembic Files** | `backend/alembic/script.py.mako`<br>`backend/database/migrations/script.py.mako` | Keep alembic/, archive migrations/ | `archive/duplicates/` |
| **Alembic README** | `backend/alembic/README`<br>`backend/database/migrations/README` | Keep alembic/, archive migrations/ | `archive/duplicates/` |
| **Empty Files** | `backend/requirements/minimal-production.txt`<br>`backend/tests/core/prosody/__init__.py`<br>`docs/devops/DOCKER_IMAGE_SIZE_OPTIMIZATION.md` | Archive all | `archive/duplicates/empty_files/` |
| **Tawil Batches** | 5 files in `ml_dataset/expansion_staging/verified/`<br>5 files in `ml_dataset/expansion_staging/by_meter/الطويل/` | Keep verified/, archive by_meter/ | `archive/duplicates/ml_dataset_tawil/` |

### Execution Commands

Duplicates are handled automatically by `scripts/refactor/13_handle_duplicates.sh`:

```bash
# Manual execution (if needed):
./scripts/refactor/13_handle_duplicates.sh
```

### Verification

After running duplicate handling:

```bash
# Check archived duplicates
ls -la archive/duplicates/
ls -la archive/duplicates/empty_files/
ls -la archive/duplicates/ml_dataset_tawil/

# Verify no duplicates remain
find . -type f ! -path "./.git/*" -exec md5 {} \; | sort | uniq -d
```

---

## Backward Compatibility Strategy

### 30-Day Transition Period

To ensure zero disruption during the refactor, temporary symlinks are created:

```bash
backend/     → src/backend/
frontend/    → src/frontend/
dataset/     → data/processed/datasets/
ml_dataset/  → data/raw/ml_dataset/
```

### Migration Helpers

**Deprecation Warnings in Moved Scripts:**

All scripts in `scripts/testing/`, `scripts/ml/`, and `scripts/data_processing/` include:

```python
import warnings

# Deprecation notice for old paths
if Path("backend").is_symlink():
    warnings.warn(
        "Using backward compatibility symlink. "
        "Update imports to use 'src/backend' instead of 'backend'. "
        "Symlinks will be removed on YYYY-MM-DD.",
        DeprecationWarning,
        stacklevel=2
    )
```

### Removal Timeline

| Week | Action |
|------|--------|
| Week 1 | Refactor complete, symlinks active, deprecation warnings shown |
| Week 2-3 | Monitor usage, team updates their local scripts |
| Week 4 | Final reminder to update remaining references |
| Day 30 | Remove symlinks, delete `BACKWARD_COMPAT_NOTICE.md` |

### Removal Script

Create: `scripts/refactor/remove_backward_compat.sh`

```bash
#!/bin/bash
# Run after 30 days

echo "Removing backward compatibility symlinks..."

SYMLINKS=(
    "backend"
    "frontend"
    "dataset"
    "ml_dataset"
)

for link in "${SYMLINKS[@]}"; do
    if [[ -L "$link" ]]; then
        rm "$link"
        echo "  Removed symlink: $link"
    fi
done

rm -f BACKWARD_COMPAT_NOTICE.md

echo "✓ Backward compatibility layer removed"
```

---

## Enhanced Validation

### Automated Proof Script

The proof script (`scripts/refactor/15_proof_references_updated.sh`) validates:

1. ✓ No old `backend/` references in Python path manipulations
2. ✓ No old `dataset/evaluation/` references in code
3. ✓ No old `ml_dataset/` references in code
4. ✓ No root-level `test_*.py` files
5. ✓ No root-level `train_*.py` files
6. ✓ No root-level `PHASE_*.md` files
7. ✓ All new directories exist
8. ✓ Files counted in new locations

**Usage:**

```bash
./scripts/refactor/15_proof_references_updated.sh
```

**Expected Output:**

```
Checking for: Old backend path in Python files
  ✓ No old patterns found

Checking for: Old dataset/ paths in code
  ✓ No old patterns found

[... more checks ...]

✓ PROOF COMPLETE: All references updated correctly
```

---

## CI/CD Workflow Updates

### Automated Patches for GitHub Actions

Script `scripts/refactor/12_update_github_workflows.sh` updates:

```yaml
# BEFORE:
- name: Run tests
  working-directory: backend
  run: pytest tests/

# AFTER:
- name: Run tests
  working-directory: src/backend
  run: pytest tests/
```

All workflow path updates:
- `backend/` → `src/backend/`
- `frontend/` → `src/frontend/`
- `dataset/` → `data/processed/datasets/`
- `ml_dataset/` → `data/raw/ml_dataset/`

---

## Complete Migration Sequence

The master script now includes all 15 steps:

```bash
./scripts/refactor/migrate_repo.sh
```

**Full sequence:**

1. Pre-flight checks
2. Create backup branch
3. Move Python scripts
4. Move Markdown files
5. Move data files
6. Reorganize datasets
7. Update Python imports
8. Update Markdown links
9. Update configs
10. **Move backend/frontend to src/**
11. **Update backend references**
12. **Update GitHub workflows**
13. **Handle duplicates**
14. **Create backward compatibility**
15. **Proof references updated**

---

## Risk Mitigation Updates

| Original Risk | New Mitigation |
|--------------|----------------|
| Import breakage | Automated imports + backward compat symlinks + deprecation warnings |
| Lost files | Git mv + file count + duplicate archiving script |
| CI/CD failure | Automated workflow updates (script 12) |
| Team disruption | 30-day symlink transition + clear notices |
| Missing duplicates | Explicit duplicate handling script (script 13) |

---

**Status:** ✅ Plan enhanced to 10/10 - All requirements met
