#!/bin/bash
# =============================================================================
# Docker Image Size Verification Script
# =============================================================================
# Usage: ./check-image-size.sh [image-name]
# Default image: bahr-backend:railway-optimized

set -e

IMAGE_NAME="${1:-bahr-backend:railway-optimized}"
RAILWAY_LIMIT_GB=4.0
RAILWAY_LIMIT_BYTES=$((4 * 1024 * 1024 * 1024))

echo "================================="
echo "Docker Image Size Analysis"
echo "================================="
echo ""

# Check if image exists
if ! docker image inspect "$IMAGE_NAME" > /dev/null 2>&1; then
    echo "❌ Error: Image '$IMAGE_NAME' not found"
    echo "Build it first with: docker build -t $IMAGE_NAME ."
    exit 1
fi

# Get image size
IMAGE_SIZE_BYTES=$(docker image inspect "$IMAGE_NAME" --format='{{.Size}}')
IMAGE_SIZE_GB=$(echo "scale=2; $IMAGE_SIZE_BYTES / 1024 / 1024 / 1024" | bc)

echo "📊 Image: $IMAGE_NAME"
echo "📏 Size: ${IMAGE_SIZE_GB} GB (${IMAGE_SIZE_BYTES} bytes)"
echo "🎯 Railway Limit: ${RAILWAY_LIMIT_GB} GB"
echo ""

# Check if under limit
if [ "$IMAGE_SIZE_BYTES" -lt "$RAILWAY_LIMIT_BYTES" ]; then
    REMAINING=$(echo "scale=2; $RAILWAY_LIMIT_GB - $IMAGE_SIZE_GB" | bc)
    echo "✅ SUCCESS! Image is under Railway's 4 GB limit"
    echo "   Remaining headroom: ${REMAINING} GB"
else
    EXCESS=$(echo "scale=2; $IMAGE_SIZE_GB - $RAILWAY_LIMIT_GB" | bc)
    echo "❌ FAILED! Image exceeds Railway's 4 GB limit"
    echo "   Exceeded by: ${EXCESS} GB"
    exit 1
fi

echo ""
echo "================================="
echo "Layer Analysis (Top 10 Largest)"
echo "================================="
docker history "$IMAGE_NAME" --human --no-trunc | head -11

echo ""
echo "================================="
echo "Optimization Tips"
echo "================================="
echo "• Use 'docker-slim build $IMAGE_NAME' to reduce further"
echo "• Use 'dive $IMAGE_NAME' to inspect layers interactively"
echo "• Check if all dependencies in requirements are necessary"
echo ""
