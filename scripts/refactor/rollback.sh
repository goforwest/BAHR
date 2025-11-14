#!/bin/bash
set -e

echo "🚨 BAHR Repository Refactor - Emergency Rollback"
echo "================================================"
echo ""

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Detect latest backup branch
echo "Searching for backup branches..."
BACKUP_BRANCHES=$(git branch | grep "backup-before-refactor-" | sed 's/^[ *]*//' || echo "")

if [[ -z "$BACKUP_BRANCHES" ]]; then
    echo -e "${RED}❌ No backup branch found!${NC}"
    echo ""
    echo "Cannot proceed with rollback. No backup-before-refactor-* branch exists."
    echo "Check git branch list manually:"
    echo "  git branch -a"
    exit 1
fi

# Show available backups
echo -e "${GREEN}Found backup branches:${NC}"
echo "$BACKUP_BRANCHES" | nl
echo ""

# Get the most recent backup
LATEST_BACKUP=$(echo "$BACKUP_BRANCHES" | sort -r | head -1)
echo -e "Most recent backup: ${YELLOW}$LATEST_BACKUP${NC}"
echo ""

# Get current state
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"
echo ""

# Check for uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
    echo -e "${YELLOW}⚠️  WARNING: You have uncommitted changes${NC}"
    git status --short
    echo ""
    echo "These changes will be LOST during rollback."
    echo ""
    read -p "Continue anyway? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Rollback cancelled"
        exit 0
    fi
fi

# Confirm rollback
echo -e "${RED}⚠️  DANGER ZONE ⚠️${NC}"
echo ""
echo "This will:"
echo "  1. Reset repository to state in $LATEST_BACKUP"
echo "  2. Discard all changes made after backup"
echo "  3. Optionally force push to remote (production rollback)"
echo ""
read -p "Are you ABSOLUTELY SURE you want to rollback? [yes/NO] " -r
echo

if [[ ! $REPLY == "yes" ]]; then
    echo "Rollback cancelled (you must type 'yes' to confirm)"
    exit 0
fi

echo ""
echo "Initiating rollback..."

# Create safety checkpoint before rollback
CHECKPOINT_BRANCH="checkpoint-before-rollback-$(date +%Y%m%d-%H%M%S)"
git checkout -b "$CHECKPOINT_BRANCH"
echo -e "${GREEN}✓${NC} Created safety checkpoint: $CHECKPOINT_BRANCH"

# Switch back to main and reset
git checkout "$CURRENT_BRANCH"

# Hard reset to backup
echo "Resetting to $LATEST_BACKUP..."
git reset --hard "$LATEST_BACKUP"
echo -e "${GREEN}✓${NC} Repository reset to backup state"

echo ""
echo "=" * 60
echo "ROLLBACK COMPLETE (Local)"
echo "=" * 60
echo ""

# Offer to force push
read -p "Force push to remote origin/$CURRENT_BRANCH? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Force pushing to origin/$CURRENT_BRANCH..."
    git push origin "$CURRENT_BRANCH" --force
    echo -e "${GREEN}✓${NC} Pushed to remote"
    echo ""
    echo -e "${YELLOW}⚠️  Production rollback initiated${NC}"
    echo "Monitor deployment:"
    echo "  - Check CI/CD pipeline status"
    echo "  - Verify health endpoint: https://backend-production-c17c.up.railway.app/health"
    echo "  - Check error logs"
else
    echo "Local rollback only - not pushed to remote"
fi

echo ""
echo "=" * 60
echo "POST-ROLLBACK VALIDATION"
echo "=" * 60
echo ""

# Run validation checks
echo "Running validation checks..."

# Check 1: File count
FILE_COUNT=$(find . -type f ! -path "./.git/*" ! -path "./.venv/*" | wc -l | tr -d ' ')
echo "  File count: $FILE_COUNT"

# Check 2: Critical paths exist
CRITICAL_PATHS=(
    "backend/app/main.py"
    "frontend"
    "dataset"
    "ml_dataset"
)

echo "  Checking critical paths..."
ALL_EXIST=true
for path in "${CRITICAL_PATHS[@]}"; do
    if [[ -e "$path" ]]; then
        echo "    ✓ $path"
    else
        echo "    ✗ Missing: $path"
        ALL_EXIST=false
    fi
done

# Check 3: Test suite
echo ""
read -p "Run test suite to verify rollback? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running tests..."
    cd backend
    if pytest tests/ -v --tb=short -x; then
        echo -e "${GREEN}✓${NC} Tests passed"
    else
        echo -e "${RED}✗${NC} Tests failed - investigate issues"
    fi
    cd ..
fi

echo ""
echo "=" * 60
echo "ROLLBACK CHECKLIST"
echo "=" * 60
echo ""
echo "Verify the following manually:"
echo ""
echo "  [ ] API health check passes"
echo "      curl https://backend-production-c17c.up.railway.app/health"
echo ""
echo "  [ ] Frontend loads correctly"
echo "      https://frontend-production-6416.up.railway.app/"
echo ""
echo "  [ ] No 500 errors in production logs"
echo ""
echo "  [ ] Core meter detection works"
echo "      Test with sample Arabic verse"
echo ""
echo "  [ ] Redis connection stable"
echo ""
echo "  [ ] All CI/CD pipelines green"
echo ""

if [[ $ALL_EXIST == true ]]; then
    echo -e "${GREEN}✓ Rollback validation passed${NC}"
else
    echo -e "${YELLOW}⚠️  Some validation checks failed - review manually${NC}"
fi

echo ""
echo "Backup branches available:"
echo "  Current: $LATEST_BACKUP (restored)"
echo "  Checkpoint: $CHECKPOINT_BRANCH (state before rollback)"
echo ""
echo "To switch between states:"
echo "  git checkout $LATEST_BACKUP"
echo "  git checkout $CHECKPOINT_BRANCH"
echo ""
echo -e "${GREEN}Rollback complete${NC}"
