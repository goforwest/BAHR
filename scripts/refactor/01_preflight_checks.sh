#!/bin/bash
set -e

echo "Running pre-flight checks..."

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# Check clean git state
if [[ -n $(git status --porcelain) ]]; then
    echo "ERROR: Working directory is not clean. Commit or stash changes first."
    echo ""
    git status --short
    exit 1
fi

echo "  ✓ Git working directory clean"

# Check we're on correct branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" ]] && [[ "$CURRENT_BRANCH" != "develop" ]]; then
    echo "WARNING: Not on main or develop branch (current: $CURRENT_BRANCH)"
    read -p "Continue anyway? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "  ✓ Branch: $CURRENT_BRANCH"

# Count files for verification
FILE_COUNT=$(find . -type f ! -path "./.git/*" ! -path "./.venv/*" | wc -l | tr -d ' ')
echo "$FILE_COUNT" > /tmp/bahr_file_count_before.txt
echo "  ✓ File count recorded: $FILE_COUNT files"

# Verify critical directories exist
CRITICAL_DIRS=(
    "backend"
    "frontend"
    "dataset"
    "ml_dataset"
    "models"
    "docs"
    "scripts"
)

for dir in "${CRITICAL_DIRS[@]}"; do
    if [[ ! -d "$dir" ]]; then
        echo "ERROR: Critical directory missing: $dir"
        exit 1
    fi
done

echo "  ✓ All critical directories present"

# Check for required tools
command -v git >/dev/null 2>&1 || { echo "ERROR: git not installed"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not installed"; exit 1; }

echo "  ✓ Required tools available"

echo ""
echo "✓ Pre-flight checks passed"
echo "  Ready to proceed with migration"
