# 🚀 Refactor Quick Start Guide

## Pre-Execution Checklist

```bash
# 1. Verify you're on main branch with clean state
git status
git branch --show-current

# 2. Review the plan
cat Repo_Refactor_Plan.md | less
cat REFACTOR_ENHANCEMENTS.md | less

# 3. Check all scripts are executable
ls -lah scripts/refactor/*.sh

# 4. Ensure virtual environment is active
source .venv/bin/activate

# 5. Record current file count
find . -type f ! -path "./.git/*" | wc -l
# Expected: ~823 files
```

## Execute Refactor

```bash
# Run the master migration script (15 automated steps)
./scripts/refactor/migrate_repo.sh

# Duration: 1-2 hours
# Supervision: Monitor progress, check for errors
```

## Post-Execution Validation

```bash
# Run comprehensive validation (9 checks)
./scripts/refactor/validate_migration.sh

# If validation fails, check errors and either:
# - Fix issues manually, or
# - Rollback: git reset --hard backup-before-refactor-YYYYMMDD-HHMMSS
```

## Commit & Deploy

```bash
# If validation passes:
git add -A
git commit -m "refactor: reorganize repository structure

- Move 24 Python scripts to scripts/
- Move 54 Markdown files to docs/ and archive/
- Move 12 data files to results/
- Reorganize datasets into data/ structure
- Move backend/ and frontend/ to src/
- Archive duplicate files
- Add 30-day backward compatibility symlinks
- Update all references (imports, links, configs, CI/CD)

See: Repo_Refactor_Plan.md for complete details"

# Push to remote
git push origin main

# Monitor CI/CD workflows
# Check deployment succeeds
```

## Transition Period (30 Days)

```bash
# Backward compatibility symlinks are active:
# - backend/ → src/backend/
# - frontend/ → src/frontend/
# - dataset/ → data/processed/datasets/
# - ml_dataset/ → data/raw/ml_dataset/

# Team should update their scripts to use new paths
# Deprecation warnings will remind them
```

## After 30 Days

```bash
# Remove backward compatibility layer
./scripts/refactor/remove_backward_compat.sh

git add -A
git commit -m "chore: remove backward compatibility symlinks"
git push origin main
```

## Emergency Rollback

```bash
# If critical issues arise:

# Find backup branch
git branch | grep backup-before-refactor

# Use the exact name (example):
BACKUP_BRANCH="backup-before-refactor-20251114-101500"

# Hard reset to backup
git reset --hard $BACKUP_BRANCH

# Force push (DANGEROUS - notify team first!)
git push origin main --force

# Or if deployed, rollback deployment:
railway rollback  # or your platform's rollback command
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `Repo_Refactor_Plan.md` | Complete refactor plan (1972 lines) |
| `REFACTOR_ENHANCEMENTS.md` | Enhancement details (gaps filled) |
| `REFACTOR_COMPLETION_SUMMARY.md` | Executive summary |
| `REFACTOR_QUICK_START.md` | This file - quick reference |
| `scripts/refactor/migrate_repo.sh` | Master orchestration script |
| `scripts/refactor/validate_migration.sh` | Validation suite |
| `scripts/refactor/15_proof_references_updated.sh` | Proof verification |

## Support

- Issues: Review error output from failed script
- Questions: See detailed plan in `Repo_Refactor_Plan.md`
- Rollback help: Section 7 in main plan

---

**Status:** ✅ Ready for Implementation  
**Risk Level:** Very Low  
**Expected Duration:** 1-2 hours  
**Reversible:** Yes (backup branch + rollback procedures)
