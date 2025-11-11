# Railway Build Configuration - Image Size Fix

## Problem
Image size of 8.2 GB exceeded Railway's 4 GB limit.

## Root Cause
Railway was likely building from repository root, including frontend/, docs/, dataset/, and other unnecessary directories.

## Solution

### 1. Configure Root Directory in Railway Dashboard

**CRITICAL:** Set the Root Directory to `backend` in Railway:

1. Go to your Railway project
2. Select your backend service
3. Go to **Settings** → **Service Settings**
4. Set **Root Directory** = `backend`
5. Click **Save**
6. Redeploy

### 2. Verify Build Context

The build should now:
- Start from `/backend` directory
- Use `backend/nixpacks.toml` configuration
- Use `backend/.dockerignore` to exclude unnecessary files
- Install only production dependencies from `requirements/production.txt`

### 3. Image Size Optimizations Applied

**Files Updated:**
- ✅ `backend/.dockerignore` - Excludes virtual environments, cache, tests, docs
- ✅ `backend/nixpacks.toml` - Uses `requirements/production.txt`, aggressive cleanup
- ✅ `.dockerignore` (root) - Safety net if building from root

**Size Reduction Steps:**
1. Exclude `.venv/`, `__pycache__/`, `.pytest_cache/`
2. Use production requirements only (no dev dependencies)
3. Remove pip cache after install
4. Remove Python bytecode files (`.pyc`, `.pyo`)
5. Remove test directories

### 4. Expected Image Size

With these optimizations:
- Base Python 3.11-slim: ~150 MB
- Production dependencies (FastAPI, SQLAlchemy, CAMeL Tools): ~500-800 MB
- Application code: ~2 MB
- **Total: ~1-1.2 GB** (well under 4 GB limit)

### 5. If Still Over Limit

If the image is still too large, CAMeL Tools data might be the culprit:

**Option A: Use CAMeL Tools Without Full Data**
```toml
# In backend/nixpacks.toml [phases.install]
"/opt/venv/bin/pip install camel-tools-lite"  # If available
```

**Option B: Upgrade Railway Plan**
- Pro plan: 10 GB image limit
- Enterprise: Unlimited

### 6. Monitoring Build Size

Add to `backend/nixpacks.toml` build phase:
```toml
"du -sh /opt/venv",  # Check venv size
"du -sh /opt/venv/lib/python3.11/site-packages/camel_tools"  # Check CAMeL size
```

## Verification Checklist

- [ ] Root Directory set to `backend` in Railway dashboard
- [ ] Build logs show "Starting from /backend"
- [ ] Build uses `nixpacks.toml` from backend directory
- [ ] Image size reported as < 4 GB
- [ ] Deployment successful

## Troubleshooting

### Build still uses wrong directory
- Delete and recreate the service
- Or use Railway CLI: `railway up --service backend`

### Image still too large
- Check build logs for what's being included
- Review `.dockerignore` files
- Consider removing CAMeL Tools or using a lighter NLP library

### Missing files at runtime
- Check if `.dockerignore` is too aggressive
- Ensure `app/`, `database/`, `scripts/` are included
