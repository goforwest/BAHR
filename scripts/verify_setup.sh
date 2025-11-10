#!/bin/bash

# =============================================================================
# BAHR Setup Verification Script
# Run this to verify that all required files are in place
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0
WARN=0

# Print header
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}BAHR Setup Verification${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check function
check_file() {
    local file=$1
    local required=$2

    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} Found: $file"
        ((PASS++))
        return 0
    else
        if [ "$required" = "required" ]; then
            echo -e "${RED}✗${NC} Missing (required): $file"
            ((FAIL++))
        else
            echo -e "${YELLOW}⚠${NC} Missing (optional): $file"
            ((WARN++))
        fi
        return 1
    fi
}

check_dir() {
    local dir=$1
    local required=$2

    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} Found directory: $dir"
        ((PASS++))
        return 0
    else
        if [ "$required" = "required" ]; then
            echo -e "${RED}✗${NC} Missing directory (required): $dir"
            ((FAIL++))
        else
            echo -e "${YELLOW}⚠${NC} Missing directory (optional): $dir"
            ((WARN++))
        fi
        return 1
    fi
}

# Check essential configuration files
echo -e "${BLUE}Checking Configuration Files...${NC}"
check_file ".gitignore" "required"
check_file "docker-compose.yml" "required"
check_file "backend/.env.example" "required"
check_file "backend/Dockerfile" "required"
check_file "CONTRIBUTING.md" "required"
echo ""

# Check documentation
echo -e "${BLUE}Checking Documentation...${NC}"
check_file "README.md" "optional"
check_file "docs/START_HERE.md" "required"
check_file "docs/technical/ARCHITECTURE_OVERVIEW.md" "required"
check_file "docs/technical/API_SPECIFICATION.yaml" "required"
check_file "docs/technical/DATABASE_SCHEMA.md" "required"
check_file "docs/PHASE_0_SETUP.md" "required"
check_file "CURRENT_STATE_ASSESSMENT.md" "required"
echo ""

# Check backend structure
echo -e "${BLUE}Checking Backend Structure...${NC}"
check_dir "backend" "required"
check_dir "backend/app" "required"
check_file "backend/requirements.txt" "required"
check_file "backend/app/main.py" "required"
check_file "backend/app/response_envelope.py" "required"
check_dir "backend/tests" "required"
check_file "backend/tests/test_envelope.py" "required"
echo ""

# Check if .env exists (should not be in git)
echo -e "${BLUE}Checking Environment Files...${NC}"
if [ -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠${NC} Found: backend/.env (remember: never commit this!)"
    ((WARN++))
else
    echo -e "${GREEN}✓${NC} backend/.env not found (good - create it from .env.example)"
    ((PASS++))
fi
echo ""

# Check Python version
echo -e "${BLUE}Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python version: $PYTHON_VERSION"
    ((PASS++))

    # Check if version is >= 3.11
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Python version >= 3.11 (required)"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} Python version < 3.11 (required: 3.11+)"
        ((FAIL++))
    fi
else
    echo -e "${RED}✗${NC} Python3 not found"
    ((FAIL++))
fi
echo ""

# Check Docker
echo -e "${BLUE}Checking Docker...${NC}"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version 2>&1 | awk '{print $3}' | sed 's/,//')
    echo -e "${GREEN}✓${NC} Docker version: $DOCKER_VERSION"
    ((PASS++))
else
    echo -e "${YELLOW}⚠${NC} Docker not found (optional but recommended)"
    ((WARN++))
fi

if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version 2>&1 | awk '{print $4}' | sed 's/,//')
    echo -e "${GREEN}✓${NC} Docker Compose version: $COMPOSE_VERSION"
    ((PASS++))
else
    echo -e "${YELLOW}⚠${NC} Docker Compose not found (optional but recommended)"
    ((WARN++))
fi
echo ""

# Check Git
echo -e "${BLUE}Checking Git...${NC}"
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version 2>&1 | awk '{print $3}')
    echo -e "${GREEN}✓${NC} Git version: $GIT_VERSION"
    ((PASS++))

    # Check if in git repo
    if git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Git repository initialized"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠${NC} Not a git repository (run: git init)"
        ((WARN++))
    fi
else
    echo -e "${RED}✗${NC} Git not found"
    ((FAIL++))
fi
echo ""

# Check Node.js (for future frontend)
echo -e "${BLUE}Checking Node.js (for frontend)...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version 2>&1)
    echo -e "${GREEN}✓${NC} Node.js version: $NODE_VERSION"
    ((PASS++))
else
    echo -e "${YELLOW}⚠${NC} Node.js not found (needed for frontend in Week 2)"
    ((WARN++))
fi
echo ""

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Passed:${NC}  $PASS"
echo -e "${YELLOW}Warnings:${NC} $WARN"
echo -e "${RED}Failed:${NC}  $FAIL"
echo ""

# Final verdict
if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Setup verification PASSED!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Copy backend/.env.example to backend/.env"
    echo "2. Edit backend/.env with your configuration"
    echo "3. Start Docker services: docker-compose up -d"
    echo "4. Follow docs/PHASE_0_SETUP.md for detailed setup"
    echo ""
    exit 0
else
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}✗ Setup verification FAILED${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Please address the failed checks above.${NC}"
    echo ""
    exit 1
fi
