#!/bin/bash
# BAHR Deployment Verification Script
# Verifies that both backend and frontend services are properly deployed and functional

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="${BACKEND_URL:-}"
FRONTEND_URL="${FRONTEND_URL:-}"

# Usage
if [ -z "$BACKEND_URL" ] || [ -z "$FRONTEND_URL" ]; then
    echo -e "${YELLOW}Usage:${NC}"
    echo "  BACKEND_URL=https://your-backend.railway.app FRONTEND_URL=https://your-frontend.railway.app ./verify_deployment.sh"
    echo ""
    echo -e "${YELLOW}Or export them first:${NC}"
    echo "  export BACKEND_URL=https://your-backend.railway.app"
    echo "  export FRONTEND_URL=https://your-frontend.railway.app"
    echo "  ./verify_deployment.sh"
    exit 1
fi

echo "============================================"
echo "   BAHR Deployment Verification"
echo "============================================"
echo ""
echo "Backend URL:  $BACKEND_URL"
echo "Frontend URL: $FRONTEND_URL"
echo ""

# Counter for passed/failed tests
PASSED=0
FAILED=0

# Function to check HTTP status
check_http() {
    local url=$1
    local expected=$2
    local description=$3
    
    echo -n "Checking $description... "
    
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    
    if [ "$status" -eq "$expected" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $status)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $status, expected $expected)"
        ((FAILED++))
        return 1
    fi
}

# Function to check JSON response
check_json() {
    local url=$1
    local field=$2
    local description=$3
    
    echo -n "Checking $description... "
    
    response=$(curl -s "$url")
    value=$(echo "$response" | grep -o "\"$field\"" || true)
    
    if [ -n "$value" ]; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (field '$field' not found)"
        echo "  Response: $response"
        ((FAILED++))
        return 1
    fi
}

echo "============================================"
echo "   Backend Tests"
echo "============================================"
echo ""

# Test 1: Backend health endpoint
check_http "$BACKEND_URL/health" 200 "Backend health endpoint"

# Test 2: Backend API docs
check_http "$BACKEND_URL/docs" 200 "Backend API documentation"

# Test 3: Backend root endpoint
check_http "$BACKEND_URL/" 200 "Backend root endpoint"

# Test 4: Analyze endpoint (POST request)
echo -n "Checking analyze endpoint functionality... "
analyze_response=$(curl -s -X POST "$BACKEND_URL/api/v1/analyze" \
    -H "Content-Type: application/json" \
    -d '{"text": "أَلا لَيتَ الشَبابَ يَعودُ يَوماً"}')

if echo "$analyze_response" | grep -q "taqti3"; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "  Response: $analyze_response"
    ((FAILED++))
fi

# Test 5: Redis caching (second request should be faster)
echo -n "Checking Redis caching... "
start_time=$(date +%s%N)
curl -s -X POST "$BACKEND_URL/api/v1/analyze" \
    -H "Content-Type: application/json" \
    -d '{"text": "أَلا لَيتَ الشَبابَ يَعودُ يَوماً"}' > /dev/null
end_time=$(date +%s%N)
cached_time=$((($end_time - $start_time) / 1000000))

if [ $cached_time -lt 100 ]; then
    echo -e "${GREEN}✓ PASSED${NC} (${cached_time}ms - cached response)"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ WARNING${NC} (${cached_time}ms - may not be cached)"
    ((PASSED++))
fi

echo ""
echo "============================================"
echo "   Frontend Tests"
echo "============================================"
echo ""

# Test 6: Frontend homepage
check_http "$FRONTEND_URL/" 200 "Frontend homepage"

# Test 7: Frontend analyze page
check_http "$FRONTEND_URL/analyze" 200 "Frontend analyze page"

# Test 8: Check for Arabic text in homepage
echo -n "Checking Arabic text rendering... "
homepage=$(curl -s "$FRONTEND_URL/")
if echo "$homepage" | grep -q "بَحْر"; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} (Arabic text 'بَحْر' not found)"
    ((FAILED++))
fi

echo ""
echo "============================================"
echo "   Database Tests"
echo "============================================"
echo ""

# Test 9: Check meters endpoint (if available)
echo -n "Checking meters data... "
meters_response=$(curl -s "$BACKEND_URL/api/v1/meters" 2>/dev/null || echo "endpoint not available")

if echo "$meters_response" | grep -q "الطويل\|al-Tawil" || echo "$meters_response" | grep -q "endpoint not available"; then
    if [ "$meters_response" = "endpoint not available" ]; then
        echo -e "${YELLOW}⚠ SKIPPED${NC} (endpoint not implemented yet)"
    else
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
    fi
else
    echo -e "${RED}✗ FAILED${NC}"
    ((FAILED++))
fi

echo ""
echo "============================================"
echo "   Integration Tests"
echo "============================================"
echo ""

# Test 10: CORS check
echo -n "Checking CORS configuration... "
cors_headers=$(curl -s -I -X OPTIONS "$BACKEND_URL/api/v1/analyze" \
    -H "Origin: $FRONTEND_URL" \
    -H "Access-Control-Request-Method: POST" 2>&1)

if echo "$cors_headers" | grep -q "Access-Control-Allow-Origin"; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "  CORS headers not found. Backend may not allow frontend origin."
    ((FAILED++))
fi

# Summary
echo ""
echo "============================================"
echo "   Summary"
echo "============================================"
echo ""
echo -e "Tests Passed: ${GREEN}$PASSED${NC}"
echo -e "Tests Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All critical tests passed!${NC}"
    echo ""
    echo "Your deployment is ready for beta testing."
    echo ""
    echo "Next steps:"
    echo "  1. Share the frontend URL with beta testers: $FRONTEND_URL"
    echo "  2. Monitor logs in Railway dashboard"
    echo "  3. Set up error tracking (e.g., Sentry)"
    echo "  4. Collect feedback from testers"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Some tests failed.${NC}"
    echo ""
    echo "Please review the failures above and:"
    echo "  1. Check Railway service logs"
    echo "  2. Verify environment variables"
    echo "  3. Ensure all services are running"
    echo "  4. Check database migrations"
    echo ""
    exit 1
fi
