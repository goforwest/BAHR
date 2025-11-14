#!/bin/bash
set -e

echo "=============================================="
echo "Automated Proof: References Updated"
echo "=============================================="
echo ""

ERRORS=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to check for old patterns
check_old_pattern() {
    local pattern="$1"
    local description="$2"
    local exclude_paths="$3"
    
    echo "Checking for: $description"
    
    # Build grep command with exclusions
    local grep_cmd="grep -r --include='*.py' --include='*.sh' --include='*.md' --include='*.yml' --include='*.yaml'"
    
    if [[ -n "$exclude_paths" ]]; then
        for path in $exclude_paths; do
            grep_cmd="$grep_cmd --exclude-dir='$path'"
        done
    fi
    
    grep_cmd="$grep_cmd '$pattern' . 2>/dev/null"
    
    # Execute and capture results
    if eval "$grep_cmd" | head -5; then
        echo -e "  ${RED}✗ FOUND old pattern${NC}"
        ((ERRORS++))
    else
        echo -e "  ${GREEN}✓ No old patterns found${NC}"
    fi
    echo ""
}

# Check for old backend/ references (should be src/backend/)
check_old_pattern \
    'Path.*parent.*"backend"' \
    "Old backend path in Python files" \
    ".git .venv node_modules archive"

# Check for old dataset/ references (should be data/processed/datasets/)
check_old_pattern \
    'dataset/evaluation/[^/]' \
    "Old dataset/ paths in code" \
    ".git .venv node_modules archive data/processed/datasets BACKWARD_COMPAT_NOTICE.md"

# Check for old ml_dataset/ references (should be data/raw/ml_dataset/)
check_old_pattern \
    'ml_dataset/[^/]' \
    "Old ml_dataset/ paths in code" \
    ".git .venv node_modules archive data/raw/ml_dataset BACKWARD_COMPAT_NOTICE.md"

# Check for root-level test scripts (should be in scripts/testing/)
echo "Checking for root-level test scripts..."
ROOT_TESTS=$(find . -maxdepth 1 -name "test_*.py" 2>/dev/null | wc -l | tr -d ' ')
if [[ $ROOT_TESTS -gt 0 ]]; then
    echo -e "  ${RED}✗ Found $ROOT_TESTS test files in root${NC}"
    find . -maxdepth 1 -name "test_*.py"
    ((ERRORS++))
else
    echo -e "  ${GREEN}✓ No root-level test scripts${NC}"
fi
echo ""

# Check for root-level train scripts (should be in scripts/ml/)
echo "Checking for root-level train scripts..."
ROOT_TRAINS=$(find . -maxdepth 1 -name "train_*.py" 2>/dev/null | wc -l | tr -d ' ')
if [[ $ROOT_TRAINS -gt 0 ]]; then
    echo -e "  ${RED}✗ Found $ROOT_TRAINS train files in root${NC}"
    find . -maxdepth 1 -name "train_*.py"
    ((ERRORS++))
else
    echo -e "  ${GREEN}✓ No root-level train scripts${NC}"
fi
echo ""

# Check for root-level markdown phase files (should be in archive/phases/)
echo "Checking for root-level PHASE_*.md files..."
ROOT_PHASES=$(find . -maxdepth 1 -name "PHASE_*.md" 2>/dev/null | wc -l | tr -d ' ')
if [[ $ROOT_PHASES -gt 0 ]]; then
    echo -e "  ${RED}✗ Found $ROOT_PHASES phase files in root${NC}"
    find . -maxdepth 1 -name "PHASE_*.md"
    ((ERRORS++))
else
    echo -e "  ${GREEN}✓ No root-level phase files${NC}"
fi
echo ""

# Verify new structure exists
echo "Verifying new directory structure..."
REQUIRED_DIRS=(
    "scripts/testing"
    "scripts/ml"
    "scripts/data_processing"
    "data/raw"
    "data/processed"
    "data/interim"
    "docs/api"
    "docs/deployment"
    "archive/phases"
    "results/evaluations"
)

ALL_DIRS_EXIST=true
for dir in "${REQUIRED_DIRS[@]}"; do
    if [[ -d "$dir" ]]; then
        echo -e "  ${GREEN}✓${NC} $dir"
    else
        echo -e "  ${RED}✗${NC} Missing: $dir"
        ALL_DIRS_EXIST=false
        ((ERRORS++))
    fi
done
echo ""

# Count files in new locations
echo "File counts in new locations:"
echo "  scripts/testing:        $(find scripts/testing -name '*.py' 2>/dev/null | wc -l | tr -d ' ') files"
echo "  scripts/ml:             $(find scripts/ml -name '*.py' 2>/dev/null | wc -l | tr -d ' ') files"
echo "  scripts/data_processing: $(find scripts/data_processing -name '*.py' 2>/dev/null | wc -l | tr -d ' ') files"
echo "  docs/api:               $(find docs/api -name '*.md' 2>/dev/null | wc -l | tr -d ' ') files"
echo "  archive/phases:         $(find archive/phases -name '*.md' 2>/dev/null | wc -l | tr -d ' ') files"
echo ""

# Summary
echo "=============================================="
if [[ $ERRORS -eq 0 ]]; then
    echo -e "${GREEN}✓ PROOF COMPLETE: All references updated correctly${NC}"
    echo ""
    echo "Migration validation successful!"
    echo "No old patterns detected."
    exit 0
else
    echo -e "${RED}✗ PROOF FAILED: Found $ERRORS issues${NC}"
    echo ""
    echo "⚠️  Some old references still exist."
    echo "Review errors above and update code."
    exit 1
fi
