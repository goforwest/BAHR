#!/bin/bash
# =============================================================================
# Railway Cache Clear & Redeploy Script
# =============================================================================
# This script helps clear Railway's build cache and trigger a fresh deployment
#
# Usage: ./scripts/deployment/clear-railway-cache.sh
#
# Prerequisites:
# - Railway CLI installed: npm install -g @railway/cli
# - Railway project linked: railway link
# - Logged in: railway login
# =============================================================================

set -e  # Exit on error

echo "🚂 Railway Cache Clear & Redeploy"
echo "=================================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found!"
    echo ""
    echo "Install it with:"
    echo "  npm install -g @railway/cli"
    echo ""
    echo "Or use the Railway dashboard:"
    echo "  1. Go to https://railway.app"
    echo "  2. Select your project"
    echo "  3. Go to Settings → Deploy"
    echo "  4. Click 'Clear Build Cache'"
    echo "  5. Trigger new deployment"
    exit 1
fi

echo "✓ Railway CLI found"
echo ""

# Check if we're in a Railway project
if ! railway status &> /dev/null; then
    echo "❌ Not in a Railway project!"
    echo ""
    echo "Link your project with:"
    echo "  railway link"
    exit 1
fi

echo "✓ Railway project linked"
echo ""

# Show current project
echo "📋 Current Project:"
railway status
echo ""

# Confirm with user
read -p "Clear build cache and redeploy? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 0
fi

echo ""
echo "🗑️  Clearing build cache..."
echo ""

# Method 1: Using Railway CLI (if supported)
# Note: As of 2025, Railway CLI might not have direct cache clear command
# In that case, we'll guide the user to use the dashboard

echo "⚠️  Railway CLI doesn't support direct cache clearing yet."
echo ""
echo "Please follow these steps:"
echo ""
echo "1. Go to: https://railway.app"
echo "2. Select your BAHR backend service"
echo "3. Navigate to: Settings → Deploy"
echo "4. Click: 'Clear Build Cache'"
echo "5. Then trigger a new deployment with:"
echo ""
echo "   git commit --allow-empty -m 'chore: trigger rebuild'"
echo "   git push origin main"
echo ""
echo "Or manually trigger redeploy in Railway dashboard"
echo ""

# Offer to create an empty commit for redeploy
read -p "Create empty commit to trigger redeploy? (y/N) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📝 Creating empty commit..."
    git commit --allow-empty -m "chore: trigger Railway rebuild after cache clear"
    
    echo ""
    read -p "Push to origin/main now? (y/N) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "🚀 Pushing to origin/main..."
        git push origin main
        
        echo ""
        echo "✅ Done! Monitor deployment at:"
        echo "   https://railway.app"
    else
        echo ""
        echo "⚠️  Remember to push when ready:"
        echo "   git push origin main"
    fi
fi

echo ""
echo "✅ All done!"
echo ""
echo "Monitor your deployment at: https://railway.app"
