# Docker Image Optimization Issue - Summary

## Goal
Reduce Docker image from **7.1 GB to under 4 GB** for Railway deployment.

---

## Root Cause Identified
The `camel-tools==1.5.7` dependency pulls in massive ML libraries:
- **PyTorch with CUDA**: ~2.8 GB
- **Transformers with models**: ~1.2 GB
- **Package tests/docs**: ~1.2 GB
- **Total bloat**: ~6+ GB

---

## Optimization Strategy (Should Work)
1. Install all Python packages normally
2. Upgrade PyTorch from CUDA to CPU-only version (saves 1.5 GB)
3. Remove test files, docs, large model files (saves 2+ GB)
4. Multi-stage build to exclude build tools

**Expected result**: 3-3.5 GB image (under 4 GB limit)

---

## Current Blocker: Packages Not Installing

### Symptom
```
=== Final package directory ===
13M /usr/local/lib/python3.11/site-packages
```

Only **13 MB** in site-packages when it should be **500+ MB**. This means:
- ❌ Pip is running but packages aren't being installed
- ❌ Or packages are installing to a different location
- ❌ Production stage can't find uvicorn/fastapi/torch

### Error in Production Stage
```
ModuleNotFoundError: No module named 'uvicorn'
```

---

## What We've Tried (All Failed)

### Attempt 1: `--prefix=/install`
```dockerfile
pip install --prefix=/install -r requirements.txt
COPY --from=builder /install/lib/python3.11/site-packages /usr/local
```
**Result**: `/install` directory not created

### Attempt 2: `--target=/install`
```dockerfile
pip install --target=/install -r requirements.txt
COPY --from=builder /install /usr/local/lib/python3.11/site-packages
```
**Result**: `/install` directory empty (only `.` and `..`)

### Attempt 3: Install to default location
```dockerfile
pip install -r requirements.txt  # Installs to /usr/local
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
```
**Result**: Only 13 MB installed (packages missing)

### Attempt 4: CPU PyTorch first, then requirements
**Result**: Dependency conflicts, uvicorn not installed

### Attempt 5: Requirements first, then upgrade PyTorch
**Result**: Still only 13 MB installed

---

## Possible Root Causes

### 1. Railway's Docker Build Environment Issue
- Railway might be using a custom pip configuration
- Environment variables interfering with pip
- Build caching causing stale layers

### 2. Requirements File Problem
Check if `requirements/production.txt` is:
- Actually being copied correctly
- Has correct syntax
- References `requirements/base.txt` correctly

### 3. Pip Installation Location
Pip might be installing to:
- `/root/.local/lib/python3.11/site-packages` (user install)
- A virtual environment that's activated
- Different Python version's site-packages

### 4. Docker Layer Caching
Railway's cached layers might be:
- Using an old broken layer
- Not rebuilding when Dockerfile changes
- Corrupted cache

---

## Next Steps to Debug

### Step 1: Check Requirements Files
```bash
cat backend/requirements/base.txt | grep uvicorn
cat backend/requirements/production.txt
```

Verify uvicorn is actually in the requirements.

### Step 2: Add Debugging to Dockerfile
```dockerfile
RUN set -ex && \
    pip install --upgrade pip setuptools wheel && \
    echo "=== Installing requirements ===" && \
    pip install -r requirements/production.txt && \
    echo "=== Where did packages go? ===" && \
    find /usr -name "uvicorn*" 2>/dev/null && \
    pip list && \
    python -c "import site; print(site.getsitepackages())"
```

This will show:
- What's actually installed
- Where pip put the packages
- What Python thinks the site-packages location is

### Step 3: Try Single-Stage Build (Simpler)
```dockerfile
FROM python:3.11-slim-bookworm

RUN pip install -r requirements.txt && \
    pip install --upgrade --extra-index-url https://download.pytorch.org/whl/cpu torch==2.9.0+cpu
    # ... cleanup steps
```

Eliminates multi-stage complexity to isolate the issue.

### Step 4: Force Railway to Rebuild from Scratch
- Railway Settings → Deployments → "Clear Build Cache"
- Or add a dummy comment to Dockerfile to bust cache

### Step 5: Check if It Works Locally
```bash
cd backend
docker build -t test-build .
docker run --rm test-build python -c "import uvicorn; print('SUCCESS')"
```

If it works locally but not on Railway, it's a Railway environment issue.

---

## Alternative Approaches

### Option A: Accept Larger Image, Optimize Later
1. Remove all optimization attempts
2. Just install packages normally (with CUDA PyTorch)
3. Deploy ~5-6 GB image
4. Might still work if Railway's limit is flexible

### Option B: Use Pre-built Base Image
Create a custom base image with all dependencies:
```dockerfile
FROM pytorch/pytorch:2.9.0-cpu  # Pre-built CPU PyTorch
RUN pip install uvicorn fastapi camel-tools
```

### Option C: Separate PyTorch Requirements
Split into two requirement files:
- `requirements-ml.txt` (torch, transformers, camel-tools)
- `requirements-api.txt` (uvicorn, fastapi, etc.)

Install separately to avoid conflicts.

### Option D: Use Conda Instead of Pip
```dockerfile
FROM continuumio/miniconda3
RUN conda install pytorch-cpu -c pytorch
RUN pip install -r requirements.txt
```

Conda handles PyTorch dependencies better than pip.

---

## Quick Win: Test Locally First

Before debugging Railway, verify the Dockerfile works locally:

```bash
cd backend
docker build -t bahr-test .
docker images bahr-test  # Check size
docker run --rm bahr-test python -c "import uvicorn, fastapi, torch; print('All packages OK')"
```

If this works, the issue is Railway-specific. If this fails too, the issue is in the Dockerfile itself.

---

## Files Modified
- `backend/Dockerfile` - Multi-stage build with optimizations
- `backend/.dockerignore` - Exclude unnecessary files
- `railway.toml` - Use `python -m uvicorn` for startup
- `backend/check-image-size.sh` - Size validation script

---

## Contact for Help
If stuck, consider:
1. Railway Discord/Support - might be known issue
2. Docker forums - show minimal reproduction
3. PyTorch forums - CPU installation issues

---

## When You Come Back
1. Read "Next Steps to Debug" above
2. Start with Step 2 (add debugging output)
3. If packages still missing, try Step 3 (single-stage build)
4. Test locally before pushing to Railway

Good luck! 🚀
