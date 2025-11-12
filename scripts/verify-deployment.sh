#!/bin/bash

# =============================================================================
# BAHR Platform - Deployment Verification Script
# =============================================================================
# This script verifies that frontend and backend are properly configured
# and can communicate with each other.
#
# Usage:
#   ./scripts/verify-deployment.sh <backend-url> <frontend-url>
#
# Example:
#   ./scripts/verify-deployment.sh \
#     https://bahr-backend.railway.app \
#     https://bahr-frontend.railway.app
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
BACKEND_URL="${1:-http://localhost:8000}"
FRONTEND_URL="${2:-http://localhost:3000}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}BAHR Platform Deployment Verification${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Backend URL:  ${YELLOW}${BACKEND_URL}${NC}"
echo -e "Frontend URL: ${YELLOW}${FRONTEND_URL}${NC}"
echo ""

# Test counter
PASSED=0
FAILED=0

# =============================================================================
# Test 1: Backend Health Check
# =============================================================================
echo -e "${BLUE}[Test 1/6]${NC} Checking backend health..."

if curl -sf "${BACKEND_URL}/health" > /dev/null; then
    RESPONSE=$(curl -s "${BACKEND_URL}/health")
    STATUS=$(echo "$RESPONSE" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

    if [ "$STATUS" = "healthy" ]; then
        echo -e "${GREEN}✓ PASSED${NC} - Backend is healthy"
        echo "  Response: $RESPONSE"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} - Backend status is not healthy"
        echo "  Response: $RESPONSE"
        ((FAILED++))
    fi
else
    echo -e "${RED}✗ FAILED${NC} - Cannot reach backend health endpoint"
    echo "  URL: ${BACKEND_URL}/health"
    echo "  Possible issues:"
    echo "    - Backend not deployed"
    echo "    - Wrong URL"
    echo "    - Backend crashed"
    ((FAILED++))
fi
echo ""

# =============================================================================
# Test 2: Backend API Documentation
# =============================================================================
echo -e "${BLUE}[Test 2/6]${NC} Checking backend API documentation..."

if curl -sf "${BACKEND_URL}/docs" > /dev/null; then
    echo -e "${GREEN}✓ PASSED${NC} - API documentation is accessible"
    echo "  URL: ${BACKEND_URL}/docs"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} - Cannot reach API documentation"
    ((FAILED++))
fi
echo ""

# =============================================================================
# Test 3: CORS Configuration
# =============================================================================
echo -e "${BLUE}[Test 3/6]${NC} Checking CORS configuration..."

CORS_RESPONSE=$(curl -sI -X OPTIONS "${BACKEND_URL}/api/v1/analyze/" \
    -H "Origin: ${FRONTEND_URL}" \
    -H "Access-Control-Request-Method: POST" \
    -H "Access-Control-Request-Headers: Content-Type")

CORS_ALLOW_ORIGIN=$(echo "$CORS_RESPONSE" | grep -i "access-control-allow-origin" | tr -d '\r' | cut -d' ' -f2)

if [ -n "$CORS_ALLOW_ORIGIN" ]; then
    if [[ "$CORS_ALLOW_ORIGIN" == *"$FRONTEND_URL"* ]] || [[ "$CORS_ALLOW_ORIGIN" == "*" ]]; then
        echo -e "${GREEN}✓ PASSED${NC} - CORS is properly configured"
        echo "  Allowed Origin: $CORS_ALLOW_ORIGIN"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠ WARNING${NC} - CORS origin doesn't match frontend URL"
        echo "  Expected: ${FRONTEND_URL}"
        echo "  Got: ${CORS_ALLOW_ORIGIN}"
        ((FAILED++))
    fi
else
    echo -e "${RED}✗ FAILED${NC} - No CORS headers found"
    echo "  Backend may not be configured to allow frontend origin"
    echo "  Check CORS_ORIGINS environment variable in backend"
    ((FAILED++))
fi
echo ""

# =============================================================================
# Test 4: Backend Analysis Endpoint
# =============================================================================
echo -e "${BLUE}[Test 4/6]${NC} Testing analysis endpoint..."

ANALYSIS_RESPONSE=$(curl -s -X POST "${BACKEND_URL}/api/v1/analyze/" \
    -H "Content-Type: application/json" \
    -H "Origin: ${FRONTEND_URL}" \
    -d '{
        "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
        "detect_bahr": true,
        "suggest_corrections": false
    }')

if echo "$ANALYSIS_RESPONSE" | grep -q "taqti3"; then
    echo -e "${GREEN}✓ PASSED${NC} - Analysis endpoint is working"

    # Extract key fields
    BAHR_NAME=$(echo "$ANALYSIS_RESPONSE" | grep -o '"name_ar":"[^"]*"' | head -1 | cut -d'"' -f4)
    CONFIDENCE=$(echo "$ANALYSIS_RESPONSE" | grep -o '"confidence":[0-9.]*' | head -1 | cut -d':' -f2)

    if [ -n "$BAHR_NAME" ]; then
        echo "  Detected meter: $BAHR_NAME (confidence: $CONFIDENCE)"
    fi
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} - Analysis endpoint error"
    echo "  Response: $ANALYSIS_RESPONSE"
    ((FAILED++))
fi
echo ""

# =============================================================================
# Test 5: BAHR v2.0 Enhanced Endpoint
# =============================================================================
echo -e "${BLUE}[Test 5/6]${NC} Testing BAHR v2.0 enhanced endpoint..."

V2_RESPONSE=$(curl -s -X POST "${BACKEND_URL}/api/v1/analyze-v2/" \
    -H "Content-Type: application/json" \
    -H "Origin: ${FRONTEND_URL}" \
    -d '{
        "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
        "detect_bahr": true,
        "suggest_corrections": true
    }')

if echo "$V2_RESPONSE" | grep -q "transformations"; then
    echo -e "${GREEN}✓ PASSED${NC} - BAHR v2.0 endpoint is working"

    # Extract explainability fields
    MATCH_QUALITY=$(echo "$V2_RESPONSE" | grep -o '"match_quality":"[^"]*"' | head -1 | cut -d'"' -f4)

    if [ -n "$MATCH_QUALITY" ]; then
        echo "  Match quality: $MATCH_QUALITY"
        echo "  ✓ Zihafat Rules Engine operational"
    fi
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ WARNING${NC} - BAHR v2.0 endpoint may not be fully configured"
    echo "  Response doesn't include explainability fields"
    echo "  This is not critical - v1 endpoint still works"
    ((FAILED++))
fi
echo ""

# =============================================================================
# Test 6: Frontend Accessibility
# =============================================================================
echo -e "${BLUE}[Test 6/6]${NC} Checking frontend accessibility..."

if curl -sf "${FRONTEND_URL}" > /dev/null; then
    echo -e "${GREEN}✓ PASSED${NC} - Frontend is accessible"
    echo "  URL: ${FRONTEND_URL}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} - Cannot reach frontend"
    echo "  Possible issues:"
    echo "    - Frontend not deployed"
    echo "    - Wrong URL"
    echo "    - Frontend crashed"
    ((FAILED++))
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Verification Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Tests Passed: ${GREEN}${PASSED}/6${NC}"
echo -e "Tests Failed: ${RED}${FAILED}/6${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓✓✓ ALL TESTS PASSED ✓✓✓${NC}"
    echo ""
    echo "Your BAHR platform is properly configured!"
    echo ""
    echo "Next steps:"
    echo "  1. Open frontend: ${FRONTEND_URL}/analyze"
    echo "  2. Test verse analysis with sample verse"
    echo "  3. Monitor logs for any errors"
    echo ""
    exit 0
else
    echo -e "${RED}✗✗✗ SOME TESTS FAILED ✗✗✗${NC}"
    echo ""
    echo "Configuration issues detected. Please review:"
    echo ""

    if curl -sf "${BACKEND_URL}/health" > /dev/null; then
        echo "Backend status: ${GREEN}OK${NC}"
    else
        echo "Backend status: ${RED}FAILED${NC}"
        echo "  → Check backend deployment in Railway"
        echo "  → Verify backend URL is correct"
    fi

    if [ -n "$CORS_ALLOW_ORIGIN" ]; then
        echo "CORS status: ${GREEN}Configured${NC}"
    else
        echo "CORS status: ${RED}NOT CONFIGURED${NC}"
        echo "  → Set CORS_ORIGINS in backend environment variables"
        echo "  → Value should be: ${FRONTEND_URL}"
    fi

    if curl -sf "${FRONTEND_URL}" > /dev/null; then
        echo "Frontend status: ${GREEN}OK${NC}"
    else
        echo "Frontend status: ${RED}FAILED${NC}"
        echo "  → Check frontend deployment in Railway"
        echo "  → Verify frontend URL is correct"
    fi

    echo ""
    echo "See RAILWAY_DEPLOYMENT_GUIDE.md for detailed troubleshooting"
    echo ""
    exit 1
fi
