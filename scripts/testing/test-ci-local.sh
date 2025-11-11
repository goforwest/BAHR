#!/bin/bash
# CI/CD Local Test Runner
# Run this script before pushing to verify all CI checks will pass

set -e  # Exit on first error

echo "════════════════════════════════════════════════════════════"
echo "   🧪 BAHR CI/CD Local Test Runner"
echo "════════════════════════════════════════════════════════════"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
BACKEND_PASSED=true
FRONTEND_PASSED=true

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Error: Run this script from the project root${NC}"
    exit 1
fi

echo "📋 This script will run the same checks as GitHub Actions CI"
echo ""

# ============================================================================
# BACKEND CHECKS
# ============================================================================

if git diff --cached --name-only | grep -q "^backend/" || [ "$1" == "--all" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🐍 BACKEND CHECKS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    cd backend
    
    # Check 1: Flake8 Linting
    echo ""
    echo "1️⃣  Running flake8 (syntax & style)..."
    if flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics; then
        echo -e "${GREEN}✅ Flake8 critical errors: PASSED${NC}"
    else
        echo -e "${RED}❌ Flake8 critical errors: FAILED${NC}"
        BACKEND_PASSED=false
    fi
    
    if flake8 app --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics > /dev/null; then
        echo -e "${GREEN}✅ Flake8 warnings: PASSED${NC}"
    else
        echo -e "${YELLOW}⚠️  Flake8 warnings present (non-blocking)${NC}"
    fi
    
    # Check 2: Black Formatting
    echo ""
    echo "2️⃣  Running black (code formatting)..."
    if black --check app 2>/dev/null; then
        echo -e "${GREEN}✅ Black formatting: PASSED${NC}"
    else
        echo -e "${RED}❌ Black formatting: FAILED${NC}"
        echo -e "${YELLOW}💡 Fix with: black app${NC}"
        BACKEND_PASSED=false
    fi
    
    # Check 3: isort
    echo ""
    echo "3️⃣  Running isort (import sorting)..."
    if isort --check-only app 2>/dev/null; then
        echo -e "${GREEN}✅ isort: PASSED${NC}"
    else
        echo -e "${RED}❌ isort: FAILED${NC}"
        echo -e "${YELLOW}💡 Fix with: isort app${NC}"
        BACKEND_PASSED=false
    fi
    
    # Check 4: mypy Type Checking
    echo ""
    echo "4️⃣  Running mypy (type checking)..."
    if mypy app --ignore-missing-imports 2>/dev/null; then
        echo -e "${GREEN}✅ mypy: PASSED${NC}"
    else
        echo -e "${YELLOW}⚠️  mypy warnings present (non-blocking)${NC}"
    fi
    
    # Check 5: pytest
    echo ""
    echo "5️⃣  Running pytest (test suite)..."
    if pytest tests/ -v --cov=app --cov-report=term-missing 2>/dev/null; then
        echo -e "${GREEN}✅ pytest: PASSED${NC}"
    else
        echo -e "${RED}❌ pytest: FAILED${NC}"
        BACKEND_PASSED=false
    fi
    
    cd ..
else
    echo "⏭️  Skipping backend checks (no backend changes)"
    echo "   Run with --all to test everything"
fi

# ============================================================================
# FRONTEND CHECKS
# ============================================================================

if git diff --cached --name-only | grep -q "^frontend/" || [ "$1" == "--all" ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚛️  FRONTEND CHECKS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    cd frontend
    
    # Check 1: ESLint
    echo ""
    echo "1️⃣  Running ESLint..."
    if npm run lint 2>/dev/null; then
        echo -e "${GREEN}✅ ESLint: PASSED${NC}"
    else
        echo -e "${RED}❌ ESLint: FAILED${NC}"
        echo -e "${YELLOW}💡 Fix with: npm run lint -- --fix${NC}"
        FRONTEND_PASSED=false
    fi
    
    # Check 2: TypeScript
    echo ""
    echo "2️⃣  Running TypeScript compiler..."
    if npx tsc --noEmit 2>/dev/null; then
        echo -e "${GREEN}✅ TypeScript: PASSED${NC}"
    else
        echo -e "${RED}❌ TypeScript: FAILED${NC}"
        FRONTEND_PASSED=false
    fi
    
    # Check 3: Prettier
    echo ""
    echo "3️⃣  Running Prettier (format check)..."
    if npx prettier --check "src/**/*.{ts,tsx,js,jsx,json,css,md}" 2>/dev/null; then
        echo -e "${GREEN}✅ Prettier: PASSED${NC}"
    else
        echo -e "${RED}❌ Prettier: FAILED${NC}"
        echo -e "${YELLOW}💡 Fix with: npx prettier --write 'src/**/*.{ts,tsx,js,jsx,json,css,md}'${NC}"
        FRONTEND_PASSED=false
    fi
    
    # Check 4: Build
    echo ""
    echo "4️⃣  Running Next.js build..."
    if npm run build 2>/dev/null; then
        echo -e "${GREEN}✅ Next.js build: PASSED${NC}"
    else
        echo -e "${RED}❌ Next.js build: FAILED${NC}"
        FRONTEND_PASSED=false
    fi
    
    # Check 5: Tests (if available)
    echo ""
    echo "5️⃣  Running tests..."
    if grep -q "\"test\"" package.json; then
        if npm test -- --passWithNoTests 2>/dev/null; then
            echo -e "${GREEN}✅ Tests: PASSED${NC}"
        else
            echo -e "${RED}❌ Tests: FAILED${NC}"
            FRONTEND_PASSED=false
        fi
    else
        echo -e "${YELLOW}⚠️  No tests configured${NC}"
    fi
    
    cd ..
else
    echo ""
    echo "⏭️  Skipping frontend checks (no frontend changes)"
    echo "   Run with --all to test everything"
fi

# ============================================================================
# SUMMARY
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if $BACKEND_PASSED && $FRONTEND_PASSED; then
    echo -e "${GREEN}"
    echo "  ✅ ALL CHECKS PASSED"
    echo ""
    echo "  Your code is ready to push!"
    echo "  CI pipeline will likely succeed."
    echo -e "${NC}"
    exit 0
else
    echo -e "${RED}"
    echo "  ❌ SOME CHECKS FAILED"
    echo ""
    echo "  Please fix the errors above before pushing."
    echo "  Your CI pipeline will fail otherwise."
    echo -e "${NC}"
    
    echo ""
    echo "Quick fixes:"
    if ! $BACKEND_PASSED; then
        echo "  • Backend: cd backend && black app && isort app && pytest tests/"
    fi
    if ! $FRONTEND_PASSED; then
        echo "  • Frontend: cd frontend && npm run lint -- --fix && npx prettier --write ."
    fi
    
    exit 1
fi
