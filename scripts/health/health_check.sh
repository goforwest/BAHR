#!/bin/bash
# Quick Health Check Script for BAHR Deployment
# Simple script to check if services are up and responding

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

BACKEND_URL="${1:-}"
FRONTEND_URL="${2:-}"

if [ -z "$BACKEND_URL" ]; then
    echo "Usage: ./health_check.sh <backend_url> [frontend_url]"
    echo "Example: ./health_check.sh https://bahr-backend.railway.app https://bahr-frontend.railway.app"
    exit 1
fi

echo "Checking BAHR Platform Health..."
echo ""

# Backend health
echo -n "Backend: "
backend_status=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health" 2>/dev/null || echo "000")
if [ "$backend_status" = "200" ]; then
    echo -e "${GREEN}✓ Healthy${NC} ($BACKEND_URL)"
else
    echo -e "${RED}✗ Down${NC} (HTTP $backend_status)"
    exit 1
fi

# Frontend health (if provided)
if [ -n "$FRONTEND_URL" ]; then
    echo -n "Frontend: "
    frontend_status=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL/" 2>/dev/null || echo "000")
    if [ "$frontend_status" = "200" ]; then
        echo -e "${GREEN}✓ Healthy${NC} ($FRONTEND_URL)"
    else
        echo -e "${RED}✗ Down${NC} (HTTP $frontend_status)"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}All services are healthy!${NC}"
