#!/bin/bash
# Test script for the analyze endpoint

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=========================================="
echo "BAHR Analyze Endpoint Test"
echo "=========================================="
echo ""

# Check if server is running
echo "Checking if server is running..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${RED}✗ Server is not running${NC}"
    echo "Start the server with: cd backend && uvicorn app.main:app --reload"
    exit 1
fi
echo -e "${GREEN}✓ Server is running${NC}"
echo ""

# Test 1: Valid verse analysis
echo "Test 1: Analyzing a valid verse..."
response=$(curl -s -X POST http://localhost:8000/api/v1/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
    "detect_bahr": true,
    "suggest_corrections": true
  }')

if echo "$response" | grep -q "taqti3"; then
    echo -e "${GREEN}✓ Analysis successful${NC}"
    echo "$response" | jq '.'
else
    echo -e "${RED}✗ Analysis failed${NC}"
    echo "$response"
fi
echo ""

# Test 2: Another verse
echo "Test 2: Analyzing another verse..."
response=$(curl -s -X POST http://localhost:8000/api/v1/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "أَلا لَيتَ الشَبابَ يَعودُ يَوماً",
    "detect_bahr": true
  }')

if echo "$response" | grep -q "taqti3"; then
    echo -e "${GREEN}✓ Analysis successful${NC}"
    echo "$response" | jq '.'
else
    echo -e "${RED}✗ Analysis failed${NC}"
    echo "$response"
fi
echo ""

# Test 3: Invalid input (no Arabic)
echo "Test 3: Testing with invalid input (no Arabic)..."
response=$(curl -s -X POST http://localhost:8000/api/v1/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is English text"
  }')

if echo "$response" | grep -q "error\|detail"; then
    echo -e "${GREEN}✓ Validation error caught correctly${NC}"
    echo "$response" | jq '.'
else
    echo -e "${RED}✗ Should have returned an error${NC}"
    echo "$response"
fi
echo ""

# Test 4: Cache test (same verse twice)
echo "Test 4: Testing cache (analyzing same verse twice)..."
echo "First request..."
start1=$(date +%s%N)
curl -s -X POST http://localhost:8000/api/v1/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "فَلا تَجزَع إِذا ما نابَ خَطبٌ",
    "detect_bahr": true
  }' > /dev/null
end1=$(date +%s%N)
time1=$((($end1 - $start1) / 1000000))

echo "Second request (should be cached)..."
start2=$(date +%s%N)
curl -s -X POST http://localhost:8000/api/v1/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "فَلا تَجزَع إِذا ما نابَ خَطبٌ",
    "detect_bahr": true
  }' > /dev/null
end2=$(date +%s%N)
time2=$((($end2 - $start2) / 1000000))

echo "First request time: ${time1}ms"
echo "Second request time: ${time2}ms (cached)"

if [ "$time2" -lt "$time1" ]; then
    echo -e "${GREEN}✓ Cache is working (second request faster)${NC}"
else
    echo -e "${RED}⚠ Cache may not be working (second request not faster)${NC}"
fi
echo ""

echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "Endpoint: POST /api/v1/analyze/"
echo "Server: http://localhost:8000"
echo "Documentation: http://localhost:8000/docs"
echo ""
echo "All basic tests completed!"
