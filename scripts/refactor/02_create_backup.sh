#!/bin/bash
set -e

echo "Creating backup branch..."

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

BACKUP_BRANCH="backup-before-refactor-$(date +%Y%m%d-%H%M%S)"
CURRENT_BRANCH=$(git branch --show-current)

# Create backup branch
git checkout -b "$BACKUP_BRANCH"
echo "  ✓ Created backup branch: $BACKUP_BRANCH"

# Return to original branch
git checkout "$CURRENT_BRANCH"
echo "  ✓ Returned to: $CURRENT_BRANCH"

echo ""
echo "✓ Backup created successfully"
echo "  Rollback command: git reset --hard $BACKUP_BRANCH"
