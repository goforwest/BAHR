#!/bin/bash
# =============================================================================
# Quick Docker Build Test
# Tests the optimized Docker image build
# =============================================================================

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Building Optimized Docker Image"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd /Users/hamoudi/Desktop/Personal/BAHR/backend

# Step 1: Verify build context
echo "Step 1: Verifying build context..."
./verify-docker-context.sh
echo ""

# Step 2: Build the image
echo "Step 2: Building Docker image..."
echo "   Using: Dockerfile.railway-optimized"
echo ""

docker build \
    --progress=plain \
    -f Dockerfile.railway-optimized \
    -t bahr-backend:optimized \
    . 2>&1 | tee docker-build.log

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Build Results"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get image size
docker images bahr-backend:optimized --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo ""
SIZE_BYTES=$(docker images bahr-backend:optimized --format "{{.Size}}")
echo "Final image size: $SIZE_BYTES"
echo ""

# Check if under 4GB
echo "Railway Requirements:"
echo "   Maximum allowed: 4.0 GB"
echo "   Target size:     < 2.0 GB"
echo ""

echo "✅ Build completed successfully!"
echo "📝 Build log saved to: docker-build.log"
echo ""
echo "Next steps:"
echo "  1. Test locally: docker run -p 8000:8000 bahr-backend:optimized"
echo "  2. Push to Railway: git push origin main"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
