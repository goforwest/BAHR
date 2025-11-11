#!/bin/bash
#
# Quick verification script for Redis caching
# Tests that the /api/v1/analyze endpoint is using Redis cache
#

set -e

API_URL="http://localhost:8000/api/v1/analyze"
TEST_VERSE='{"text": "إذا غامَرتَ في شَرَفٍ مَرومِ", "detect_bahr": true}'

echo "================================================"
echo "Redis Caching Verification Script"
echo "================================================"
echo ""

# Check server is running
echo "1. Checking if server is running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ✓ Server is running"
else
    echo "   ✗ Server is not running. Please start it:"
    echo "     cd backend && python -m uvicorn app.main:app --reload"
    exit 1
fi
echo ""

# Check Redis is running
echo "2. Checking if Redis is running..."
if docker ps --filter "name=redis" --format "{{.Status}}" | grep -q "Up"; then
    echo "   ✓ Redis is running"
else
    echo "   ✗ Redis is not running. Please start it:"
    echo "     docker-compose up -d redis"
    exit 1
fi
echo ""

# Clear any existing cache for this verse
echo "3. Clearing cache (if any)..."
NORMALIZED=$(echo "اذا غامرت في شرف مروم" | python3 -c "import sys, hashlib; text=sys.stdin.read().strip(); print(f'analysis:{hashlib.sha256(text.encode()).hexdigest()}')")
docker exec bahr_redis redis-cli DEL "$NORMALIZED" > /dev/null 2>&1 || true
echo "   ✓ Cache cleared"
echo ""

# First request (should be cache miss)
echo "4. First request (cache miss - performing analysis)..."
START1=$(python3 -c "import time; print(time.time())")
RESPONSE1=$(curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "$TEST_VERSE")
END1=$(python3 -c "import time; print(time.time())")
TIME1=$(python3 -c "print(f'{($END1 - $START1) * 1000:.2f}')" START1=$START1 END1=$END1)

echo "   Response time: ${TIME1}ms"

# Extract taqti3 if available
TAQTI3=$(echo "$RESPONSE1" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('taqti3', 'N/A'))" 2>/dev/null || echo "N/A")
echo "   Taqti3: $TAQTI3"
echo ""

# Wait a moment
sleep 1

# Second request (should be cache hit)
echo "5. Second request (cache hit - from Redis)..."
START2=$(python3 -c "import time; print(time.time())")
RESPONSE2=$(curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "$TEST_VERSE")
END2=$(python3 -c "import time; print(time.time())")
TIME2=$(python3 -c "print(f'{($END2 - $START2) * 1000:.2f}')" START2=$START2 END2=$END2)

echo "   Response time: ${TIME2}ms"
echo ""

# Calculate speedup
SPEEDUP=$(python3 <<EOF
time1 = float('$TIME1')
time2 = float('$TIME2')
if time2 > 0:
    print(f"{time1 / time2:.1f}x")
else:
    print("N/A")
EOF
)

# Display results
echo "================================================"
echo "RESULTS"
echo "================================================"
echo ""
echo "First request (analysis):  ${TIME1}ms"
echo "Second request (cached):   ${TIME2}ms"
echo "Speedup:                   ${SPEEDUP} faster"
echo ""

# Verify responses are identical
if [ "$RESPONSE1" = "$RESPONSE2" ]; then
    echo "✓ Responses are identical (caching working correctly)"
else
    echo "⚠ Responses differ (may be expected if response includes timestamps)"
fi
echo ""

# Check if caching provided benefit
python3 <<EOF
time1 = float('$TIME1')
time2 = float('$TIME2')

if time2 < 50 and time2 < time1:
    print("✓ Cache is working! Second request is fast (<50ms)")
    exit(0)
elif time2 < time1 * 0.5:
    print("✓ Cache is working! Second request is significantly faster")
    exit(0)
else:
    print("⚠ Cache may not be working optimally")
    print(f"  Expected: Second request <50ms or <50% of first request")
    print(f"  Actual: {time2:.2f}ms ({(time2/time1)*100:.1f}% of first request)")
    exit(1)
EOF

CACHE_STATUS=$?

echo ""
echo "================================================"
if [ $CACHE_STATUS -eq 0 ]; then
    echo "✓ VERIFICATION PASSED: Redis caching is working"
else
    echo "⚠ VERIFICATION FAILED: Check the implementation"
fi
echo "================================================"

exit $CACHE_STATUS
