#!/bin/bash
set -e

echo "Deep cleaning root directory..."

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# Remove backward compatibility symlinks (transition complete)
echo "  Removing backward compatibility symlinks..."
if [[ -L "backend" ]]; then
    rm backend
    echo "    ✓ Removed backend symlink"
fi

if [[ -L "frontend" ]]; then
    rm frontend
    echo "    ✓ Removed frontend symlink"
fi

# Remove development artifacts
echo "  Removing development artifacts..."
if [[ -d ".pytest_cache" ]]; then
    rm -rf .pytest_cache
    echo "    ✓ Removed .pytest_cache/"
fi

if [[ -d ".coverage" ]]; then
    rm -rf .coverage
    echo "    ✓ Removed .coverage"
fi

# Move ml_pipeline to proper location
echo "  Moving ml_pipeline to scripts/..."
if [[ -d "ml_pipeline" ]]; then
    git mv ml_pipeline scripts/
    echo "    ✓ ml_pipeline/ → scripts/ml_pipeline/"
fi

# Move tools to scripts
echo "  Moving tools to scripts/..."
if [[ -d "tools" ]]; then
    git mv tools scripts/
    echo "    ✓ tools/ → scripts/tools/"
fi

# Move requirements to src/backend if it's ML requirements
echo "  Reorganizing requirements..."
if [[ -d "requirements" ]] && [[ -f "requirements/ml.txt" ]]; then
    mkdir -p scripts/ml_pipeline/requirements
    git mv requirements/ml.txt scripts/ml_pipeline/requirements/
    rmdir requirements 2>/dev/null || echo "    ℹ️  requirements/ has other files, keeping it"
    echo "    ✓ requirements/ml.txt → scripts/ml_pipeline/requirements/"
fi

# Move .bahr_aliases.sh to scripts/setup
echo "  Moving development utilities..."
if [[ -f ".bahr_aliases.sh" ]]; then
    git mv .bahr_aliases.sh scripts/setup/
    echo "    ✓ .bahr_aliases.sh → scripts/setup/"
fi

echo ""
echo "✓ Deep clean complete!"
echo ""
echo "Root directory now contains ONLY:"
echo "  - Essential configs (.env.example, .gitignore, railway.toml, etc.)"
echo "  - Core docs (README.md, CHANGELOG.md, CONTRIBUTING.md, LICENSE, QUICK_START.md)"
echo "  - Main directories (src/, tests/, scripts/, docs/, data/, results/, archive/, infrastructure/, models/)"
