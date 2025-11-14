#!/bin/bash
# =============================================================================
# Docker Build Context Analyzer
# Verifies what files will be sent to Docker daemon
# =============================================================================

set -e

BACKEND_DIR="/Users/hamoudi/Desktop/Personal/BAHR/backend"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 Docker Build Context Analysis"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$BACKEND_DIR"

# Check .dockerignore exists
if [ ! -f .dockerignore ]; then
    echo "❌ ERROR: .dockerignore not found in $BACKEND_DIR"
    exit 1
fi

echo "✅ .dockerignore found"
echo ""

# Calculate build context size
echo "📦 Calculating build context size..."
CONTEXT_SIZE=$(tar --exclude='.git' -czf - . 2>/dev/null | wc -c | awk '{printf "%.2f MB", $1/1024/1024}')
echo "   Build context size: $CONTEXT_SIZE"
echo ""

# Expected size after optimization
echo "📊 Expected sizes:"
echo "   ✅ Good:      < 10 MB"
echo "   ⚠️  Warning:  10-50 MB"
echo "   ❌ Bad:      > 50 MB (likely including .venv or node_modules)"
echo ""

# List large files that would be included
echo "🔍 Large files in build context (>1MB):"
find . -type f -size +1M 2>/dev/null | while read file; do
    SIZE=$(du -h "$file" | cut -f1)
    echo "   $SIZE  $file"
done

echo ""
echo "🗂️  Checking for problematic directories:"

check_dir() {
    DIR=$1
    if [ -d "$DIR" ]; then
        SIZE=$(du -sh "$DIR" 2>/dev/null | cut -f1)
        echo "   ❌ FOUND: $DIR ($SIZE) - Should be in .dockerignore!"
        return 1
    else
        echo "   ✅ OK: $DIR not present in build context"
        return 0
    fi
}

ALL_GOOD=true

check_dir ".venv" || ALL_GOOD=false
check_dir "venv" || ALL_GOOD=false
check_dir "node_modules" || ALL_GOOD=false
check_dir ".pytest_cache" || ALL_GOOD=false
check_dir "__pycache__" || ALL_GOOD=false

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$ALL_GOOD" = true ]; then
    echo "✅ BUILD CONTEXT IS CLEAN - Ready to build!"
    echo ""
    echo "Next steps:"
    echo "  1. docker build -f Dockerfile.railway-optimized -t bahr-backend:test ."
    echo "  2. docker images bahr-backend:test"
    echo "  3. Should see image size < 2 GB"
else
    echo "❌ BUILD CONTEXT HAS ISSUES - Fix .dockerignore first!"
    echo ""
    echo "Action required:"
    echo "  1. Ensure .venv/, venv/, node_modules/ are in .dockerignore"
    echo "  2. Run this script again to verify"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
