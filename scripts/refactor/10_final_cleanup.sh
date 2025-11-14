#!/bin/bash
set -e

echo "Final cleanup - organizing remaining root files..."

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# Move phase documentation to archive
echo "  Moving remaining phase documentation..."
if [[ -f "PHASE2_WEEK7_8_RESULTS.md" ]]; then
    git mv PHASE2_WEEK7_8_RESULTS.md archive/phases/
    echo "    ✓ PHASE2_WEEK7_8_RESULTS.md → archive/phases/"
fi

if [[ -f "PHASE2_WEEKS4_6_PHONEME_IMPROVEMENTS.md" ]]; then
    git mv PHASE2_WEEKS4_6_PHONEME_IMPROVEMENTS.md archive/phases/
    echo "    ✓ PHASE2_WEEKS4_6_PHONEME_IMPROVEMENTS.md → archive/phases/"
fi

# Move refactor documentation to docs/refactor
echo "  Moving refactor documentation..."
mkdir -p docs/refactor

if [[ -f "Repo_Refactor_Plan.md" ]]; then
    git mv Repo_Refactor_Plan.md docs/refactor/
    echo "    ✓ Repo_Refactor_Plan.md → docs/refactor/"
fi

if [[ -f "REFACTOR_COMPLETION_SUMMARY.md" ]]; then
    git mv REFACTOR_COMPLETION_SUMMARY.md docs/refactor/
    echo "    ✓ REFACTOR_COMPLETION_SUMMARY.md → docs/refactor/"
fi

if [[ -f "REFACTOR_ENHANCEMENTS.md" ]]; then
    git mv REFACTOR_ENHANCEMENTS.md docs/refactor/
    echo "    ✓ REFACTOR_ENHANCEMENTS.md → docs/refactor/"
fi

if [[ -f "REFACTOR_QUICK_START.md" ]]; then
    git mv REFACTOR_QUICK_START.md docs/refactor/
    echo "    ✓ REFACTOR_QUICK_START.md → docs/refactor/"
fi

if [[ -f "CRITICAL_FIXES_SUMMARY.md" ]]; then
    git mv CRITICAL_FIXES_SUMMARY.md docs/refactor/
    echo "    ✓ CRITICAL_FIXES_SUMMARY.md → docs/refactor/"
fi

if [[ -f "CRITICAL_FIXES_QUICK_REF.md" ]]; then
    git mv CRITICAL_FIXES_QUICK_REF.md docs/refactor/
    echo "    ✓ CRITICAL_FIXES_QUICK_REF.md → docs/refactor/"
fi

if [[ -f "BACKWARD_COMPAT_NOTICE.md" ]]; then
    git mv BACKWARD_COMPAT_NOTICE.md docs/refactor/
    echo "    ✓ BACKWARD_COMPAT_NOTICE.md → docs/refactor/"
fi

# Move release notes to docs/releases
echo "  Moving release notes..."
mkdir -p docs/releases

if [[ -f "RELEASE_NOTES_v1.0.md" ]]; then
    git mv RELEASE_NOTES_v1.0.md docs/releases/
    echo "    ✓ RELEASE_NOTES_v1.0.md → docs/releases/"
fi

# Move orphaned Python files to scripts
echo "  Moving orphaned Python scripts..."

for file in *.py; do
    if [[ -f "$file" ]]; then
        git mv "$file" scripts/analysis/
        echo "    ✓ $file → scripts/analysis/"
    fi
done

# Move phase3_materials to archive
echo "  Moving phase3_materials..."
if [[ -d "phase3_materials" ]]; then
    git mv phase3_materials archive/
    echo "    ✓ phase3_materials/ → archive/"
fi

echo ""
echo "✓ Final cleanup complete"
echo ""
echo "Root directory now contains only:"
echo "  - Essential config files (.gitignore, .env.example, etc.)"
echo "  - Key documentation (README.md, CHANGELOG.md, CONTRIBUTING.md, etc.)"
echo "  - Source directories (src/, tests/, scripts/, docs/, data/, etc.)"
