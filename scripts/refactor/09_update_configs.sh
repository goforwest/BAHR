#!/bin/bash
set -e

echo "Updating shell scripts and configs..."

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

echo "  Checking .bahr_aliases.sh..."
if grep -q "data/processed/datasets" .bahr_aliases.sh 2>/dev/null; then
    echo "    ✓ Already updated for data/ structure"
else
    echo "    ℹ️  May need updates for data/ paths"
fi

echo "  Checking scripts/setup/*.sh..."
for script in scripts/setup/*.sh; do
    if [[ -f "$script" ]]; then
        # Check if it references old paths
        if grep -q "backend/app" "$script" 2>/dev/null; then
            echo "    ⚠️  $(basename $script) may need path updates"
        else
            echo "    ✓ $(basename $script)"
        fi
    fi
done

echo ""
echo "✓ Configuration check complete"
echo ""
echo "⚠️  Review and update manually if needed:"
echo "    - .bahr_aliases.sh (dataset paths)"
echo "    - scripts/setup/*.sh (backend paths)"
echo "    - Any custom shell scripts"
