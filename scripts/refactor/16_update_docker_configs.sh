#!/bin/bash
set -e

echo "Updating Docker configurations..."

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# Update docker-compose.yml
if [[ -f "infrastructure/docker/docker-compose.yml" ]]; then
    echo "  Updating docker-compose.yml build contexts..."
    
    # Backup original
    cp infrastructure/docker/docker-compose.yml infrastructure/docker/docker-compose.yml.backup
    
    # Update backend context
    sed -i.tmp 's|context: ../../backend|context: ../../src/backend|g' infrastructure/docker/docker-compose.yml
    sed -i.tmp 's|context: \./backend|context: ./src/backend|g' infrastructure/docker/docker-compose.yml
    
    # Update frontend context
    sed -i.tmp 's|context: ../../frontend|context: ../../src/frontend|g' infrastructure/docker/docker-compose.yml
    sed -i.tmp 's|context: \./frontend|context: ./src/frontend|g' infrastructure/docker/docker-compose.yml
    
    # Clean up temp files
    rm -f infrastructure/docker/docker-compose.yml.tmp
    
    echo "  ✓ docker-compose.yml updated"
fi

# Check backend Dockerfile
if [[ -f "src/backend/Dockerfile" ]]; then
    echo "  Verifying backend Dockerfile..."
    
    # Verify critical paths exist
    if grep -q "COPY app/" src/backend/Dockerfile; then
        echo "  ✓ Backend Dockerfile paths look correct (relative to src/backend/)"
    else
        echo "  ⚠️  Review backend Dockerfile COPY commands manually"
    fi
fi

# Check frontend Dockerfile
if [[ -f "src/frontend/Dockerfile" ]]; then
    echo "  Verifying frontend Dockerfile..."
    
    if grep -q "COPY" src/frontend/Dockerfile; then
        echo "  ✓ Frontend Dockerfile exists"
    else
        echo "  ⚠️  Review frontend Dockerfile manually"
    fi
fi

# Verify .dockerignore files
echo "  Checking .dockerignore files..."
[[ -f "src/backend/.dockerignore" ]] && echo "  ✓ Backend .dockerignore found"
[[ -f "src/frontend/.dockerignore" ]] && echo "  ✓ Frontend .dockerignore found"

# Create reminder for Railway configuration
cat > RAILWAY_MIGRATION_CHECKLIST.md << 'EOF'
# Railway Migration Checklist

## Before Deploying to Railway

- [ ] Verify `railway.toml` root detection settings
- [ ] Update Railway dashboard build settings if needed:
  - Backend root: `src/backend`
  - Frontend root: `src/frontend`
- [ ] Test build in Railway staging environment first
- [ ] Verify environment variables still load correctly
- [ ] Check Procfile paths if using custom start commands

## Build Context Verification

Run locally first:
```bash
docker build -t bahr-backend src/backend
docker build -t bahr-frontend src/frontend
```

## Rollback Plan

If Railway deployment fails:
1. Revert to backup branch
2. Force push to trigger rebuild
3. Monitor health endpoints

---
**Delete this file after successful Railway deployment**
EOF

echo "  ✓ Created RAILWAY_MIGRATION_CHECKLIST.md"

echo ""
echo "✓ Docker configurations updated"
echo ""
echo "⚠️  MANUAL VERIFICATION REQUIRED:"
echo "  1. Review src/backend/Dockerfile COPY paths"
echo "  2. Review src/frontend/Dockerfile COPY paths"
echo "  3. Test Docker builds locally before pushing"
echo "  4. Read RAILWAY_MIGRATION_CHECKLIST.md"
