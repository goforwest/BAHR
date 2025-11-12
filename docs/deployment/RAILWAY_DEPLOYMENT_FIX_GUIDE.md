# Railway Deployment Fix Guide

**Issue:** Backend deployment failing during Docker build  
**Date:** November 11, 2025  
**Status:** ✅ FIXED

---

## Problem Summary

Railway was building the **testing** stage of the multi-stage Dockerfile instead of **production**, causing test failures during deployment.

### Error Details

```
ModuleNotFoundError: No module named 'backend'
Location: tests/test_envelope.py:7
```

**Root Cause:** The Dockerfile had `testing` as the last stage, so Railway defaulted to building that stage instead of `production`.

---

## Solution Applied

### ✅ Fix 1: Reordered Dockerfile Stages

**Changed:** Moved `production` stage to be the **last (default)** stage in Dockerfile  
**Result:** Railway now builds production stage by default

**Before:**
```dockerfile
FROM ... as production  # Stage 4
FROM ... as testing     # Stage 5 (LAST - was being built)
```

**After:**
```dockerfile
FROM ... as production  # Stage 4 (LAST - now default)
# Testing stage moved to separate file
```

### ✅ Fix 2: Created Separate Test Dockerfile

**File:** `backend/Dockerfile.test`  
**Purpose:** Run tests in CI/CD without affecting production builds

**Usage:**
```bash
# Local testing
docker build -f Dockerfile.test -t bahr-backend:test .
docker run bahr-backend:test

# CI/CD (GitHub Actions)
docker build -f Dockerfile.test -t test-image .
docker run test-image
```

### ✅ Fix 3: Enhanced Production Dockerfile

**Added:**
- `PYTHONPATH=/app` to testing stage (if needed later)
- Clear comments marking production as default
- Removed testing stage from main Dockerfile

---

## Deployment Steps

### 1. Commit and Push Changes

```bash
cd /Users/hamoudi/Desktop/Personal/BAHR

# Stage the changes
git add backend/Dockerfile
git add backend/Dockerfile.test
git add backend/.railway.json
git add backend/railway.toml

# Commit
git commit -m "fix(deploy): Make production stage default in Dockerfile

- Move production stage to be last (default) in Dockerfile
- Create separate Dockerfile.test for testing
- Fix Railway deployment build failures
- Add PYTHONPATH to testing environment

Fixes #<issue-number>"

# Push to trigger Railway deployment
git push origin main
```

### 2. Monitor Railway Deployment

1. Go to Railway dashboard: https://railway.app
2. Navigate to your backend service
3. Click on latest deployment
4. Watch build logs

**Expected Output:**
```
✅ Using Detected Dockerfile
✅ FROM python:3.11-slim as base
✅ FROM base as development
✅ FROM base as builder
✅ FROM python:3.11-slim as production  ← Building this one
✅ Build successful
✅ Deployment live
```

### 3. Verify Deployment

```bash
# Test health endpoint
curl https://your-backend.railway.app/health

# Expected response:
# {"status": "healthy", "timestamp": 1699707600, "version": "1.0.0"}

# Test analyze endpoint
curl -X POST https://your-backend.railway.app/api/v1/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
    "detect_bahr": true
  }'

# Expected: JSON response with taqti3 and bahr info
```

---

## Testing Locally

### Run Production Build

```bash
cd backend

# Build production image
docker build --target production -t bahr-backend:prod .

# Run container
docker run -p 8000:8000 \
  -e REDIS_URL=redis://host.docker.internal:6379/0 \
  -e DATABASE_URL=postgresql://user:pass@host.docker.internal:5432/bahr \
  bahr-backend:prod

# Test
curl http://localhost:8000/health
```

### Run Tests

```bash
cd backend

# Build test image
docker build -f Dockerfile.test -t bahr-backend:test .

# Run tests
docker run bahr-backend:test

# Expected: All tests pass with coverage report
```

---

## Configuration Files Added

### 1. `backend/railway.toml` (Optional)

Railway-specific configuration for build and deploy settings.

### 2. `backend/.railway.json` (Not used - for reference)

Railway doesn't support this yet, but kept for future compatibility.

### 3. `backend/Dockerfile.test`

Separate Dockerfile for running tests in CI/CD.

---

## Prevention for Future

### Multi-Stage Dockerfile Best Practices

1. **Always make production the last stage** when deploying to platforms that auto-detect stages
2. **Use explicit build targets** in CI/CD: `docker build --target production`
3. **Separate test Dockerfiles** for clarity and independence
4. **Document stage order** in Dockerfile comments

### Railway-Specific Tips

1. **Check build logs** to see which stage is being built
2. **Use Railway settings** to override Dockerfile if needed
3. **Set explicit start command** in Railway dashboard
4. **Monitor first deployment** after Dockerfile changes

---

## Rollback Plan (If Needed)

If deployment still fails:

```bash
# 1. Check Railway logs for specific error
# 2. Verify environment variables are set in Railway:
#    - REDIS_URL
#    - DATABASE_URL
#    - SECRET_KEY
#    - CORS_ORIGINS

# 3. Try manual build locally to debug:
cd backend
docker build --target production -t test .
docker run -p 8000:8000 test

# 4. If still failing, use nixpacks instead of Dockerfile:
# In Railway dashboard:
# Settings → Builder → Switch to Nixpacks
```

---

## Success Checklist

- [ ] Changes committed and pushed to `main` branch
- [ ] Railway deployment triggered automatically
- [ ] Build logs show production stage being built (not testing)
- [ ] Deployment completes successfully
- [ ] Health endpoint returns `{"status": "healthy"}`
- [ ] Analyze endpoint processes Arabic poetry correctly
- [ ] No import errors in logs
- [ ] Application running on correct port ($PORT)

---

## Related Documentation

- **Main diagnostic:** `docs/technical/INTEGRATION_DIAGNOSTIC_REPORT.md`
- **Architecture:** `docs/technical/ARCHITECTURE_OVERVIEW.md`
- **Deployment guide:** `archive/deployment/RAILWAY_DEPLOYMENT_GUIDE.md`
- **Quick start:** `docs/onboarding/QUICKSTART_NEW_PATHS.md`

---

## Contact & Support

If issues persist:

1. Check Railway logs: `railway logs`
2. Verify environment variables are set
3. Test locally with Docker first
4. Review this guide's troubleshooting section
5. Check Railway status page: https://status.railway.app

**Last Updated:** November 11, 2025  
**Status:** Active fix applied
