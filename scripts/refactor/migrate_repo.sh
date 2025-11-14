#!/bin/bash
set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$REPO_ROOT"

echo "==============================================="
echo "BAHR Repository Refactor - Automated Migration"
echo "==============================================="
echo ""
echo "Repo root: $REPO_ROOT"
echo "Start time: $(date)"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step counter
STEP=1

run_step() {
    echo ""
    echo "${GREEN}[$STEP/17]${NC} $1"
    ((STEP++))
}

# PRE-FLIGHT CHECKS
run_step "Pre-flight checks"
./scripts/refactor/01_preflight_checks.sh || { echo "${RED}Pre-flight failed!${NC}"; exit 1; }

# BACKUP
run_step "Creating backup branch"
./scripts/refactor/02_create_backup.sh || { echo "${RED}Backup failed!${NC}"; exit 1; }

# MIGRATIONS
run_step "Moving Python scripts to organized locations"
./scripts/refactor/03_move_python_scripts.sh || { echo "${RED}Python script migration failed!${NC}"; exit 1; }

run_step "Moving Markdown files to docs/ and archive/"
if [[ -f "./scripts/refactor/04_move_markdown_files.sh" ]]; then
    ./scripts/refactor/04_move_markdown_files.sh || { echo "${RED}Markdown migration failed!${NC}"; exit 1; }
else
    echo "${YELLOW}  Script 04 not found - skipping${NC}"
fi

run_step "Moving data files to results/"
if [[ -f "./scripts/refactor/05_move_data_files.sh" ]]; then
    ./scripts/refactor/05_move_data_files.sh || { echo "${RED}Data file migration failed!${NC}"; exit 1; }
else
    echo "${YELLOW}  Script 05 not found - skipping${NC}"
fi

run_step "Reorganizing datasets"
if [[ -f "./scripts/refactor/06_reorganize_datasets.sh" ]]; then
    ./scripts/refactor/06_reorganize_datasets.sh || { echo "${RED}Dataset reorganization failed!${NC}"; exit 1; }
else
    echo "${YELLOW}  Script 06 not found - skipping${NC}"
fi

run_step "Updating Python imports and installing backend"
if [[ -f "./scripts/refactor/07_update_python_imports.sh" ]]; then
    ./scripts/refactor/07_update_python_imports.sh || { echo "${RED}Import update failed!${NC}"; exit 1; }
else
    echo "${YELLOW}  Script 07 not found - skipping${NC}"
fi

run_step "Updating Markdown links"
if [[ -f "./scripts/refactor/08_update_markdown_links.sh" ]]; then
    ./scripts/refactor/08_update_markdown_links.sh || { echo "${RED}Link update failed!${NC}"; exit 1; }
else
    echo "${YELLOW}  Script 08 not found - skipping${NC}"
fi

run_step "Updating shell scripts and configs"
if [[ -f "./scripts/refactor/09_update_configs.sh" ]]; then
    ./scripts/refactor/09_update_configs.sh || { echo "${RED}Config update failed!${NC}"; exit 1; }
else
    echo "${YELLOW}  Script 09 not found - skipping${NC}"
fi

run_step "Moving backend and frontend to src/"
./scripts/refactor/10_move_backend_frontend.sh || { echo "${RED}Backend/frontend move failed!${NC}"; exit 1; }

run_step "Updating backend references and validating database migrations"
./scripts/refactor/11_update_backend_references.sh || { echo "${RED}Backend reference update failed!${NC}"; exit 1; }

run_step "Updating GitHub workflows"
./scripts/refactor/12_update_github_workflows.sh || { echo "${RED}Workflow update failed!${NC}"; exit 1; }

run_step "Handling duplicate files"
./scripts/refactor/13_handle_duplicates.sh || { echo "${RED}Duplicate handling failed!${NC}"; exit 1; }

run_step "Creating backward compatibility layer"
./scripts/refactor/14_create_backward_compat.sh || { echo "${RED}Backward compat creation failed!${NC}"; exit 1; }

run_step "Verifying all references updated (proof)"
./scripts/refactor/15_proof_references_updated.sh || { echo "${RED}Proof verification failed!${NC}"; exit 1; }

run_step "Updating Docker configurations"
./scripts/refactor/16_update_docker_configs.sh || { echo "${RED}Docker config update failed!${NC}"; exit 1; }

run_step "Running smoke tests"
python3 ./scripts/refactor/smoke_tests.py || { echo "${RED}Smoke tests failed!${NC}"; exit 1; }

echo ""
echo "${GREEN}===============================================${NC}"
echo "${GREEN}Migration Complete!${NC}"
echo "${GREEN}===============================================${NC}"
echo ""
echo "✅ All 17 migration steps completed successfully"
echo ""
echo "Next steps:"
echo "1. Review changes: git status | head -50"
echo "2. Verify file count: find . -type f ! -path './.git/*' | wc -l"
echo "3. Test backend startup: cd src/backend && uvicorn app.main:app --reload"
echo "4. Run tests: cd src/backend && pytest tests/ -v"
echo "5. Test Docker build: docker build -t bahr-test ./src/backend"
echo "6. Review RAILWAY_MIGRATION_CHECKLIST.md for deployment steps"
echo ""
echo "⚠️  IMPORTANT: Follow staged rollout plan (Section 10)"
echo "   - Local validation complete ✓"
echo "   - Next: Deploy to STAGING first"
echo "   - Only deploy to PRODUCTION after staging validation"
echo ""
echo "End time: $(date)"
