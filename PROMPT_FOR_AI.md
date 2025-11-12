# Docker Image Optimization - AI Prompt

Copy and paste this prompt to any AI assistant:

---

I need help fixing a Docker multi-stage build issue. My Railway deployment is failing because packages aren't being installed correctly.

## Problem
My Dockerfile (see `backend/Dockerfile`) installs Python packages in the builder stage, but when I check the installation, only **13 MB** is in `/usr/local/lib/python3.11/site-packages` when it should be **500+ MB**. The production stage then fails with `ModuleNotFoundError: No module named 'uvicorn'`.

## Current Build Output
```
=== Final package directory ===
13M /usr/local/lib/python3.11/site-packages
```

Then in production stage:
```
ModuleNotFoundError: No module named 'uvicorn'
```

## Current Dockerfile Approach (Failing)
```dockerfile
# Builder stage
RUN pip install -r requirements/production.txt && \
    pip install --upgrade --extra-index-url https://download.pytorch.org/whl/cpu torch==2.9.0+cpu && \
    # cleanup steps...
    du -sh /usr/local/lib/python3.11/site-packages  # Shows only 13M

# Production stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
```

## Requirements
- `requirements/base.txt` includes: uvicorn==0.30.6, fastapi==0.115.0, camel-tools==1.5.7
- `requirements/production.txt` includes base.txt plus production dependencies
- Must use CPU-only PyTorch to save space (saves 1.5 GB vs CUDA)
- Must work on Railway's build environment

## What I've Tried (All Failed)
1. `pip install --prefix=/install` - directory not created
2. `pip install --target=/install` - directory empty
3. Installing to default `/usr/local` - only 13 MB installed
4. Different installation orders (torch first vs requirements first)

## Task
Fix the Dockerfile so that:
1. All packages from `requirements/production.txt` are installed correctly
2. PyTorch uses CPU-only version (not CUDA - saves 1.5 GB)
3. Packages are successfully copied to production stage
4. Final image is under 4 GB (currently would be 7.1 GB with CUDA PyTorch)

## Files to Check
- `backend/Dockerfile` - the multi-stage build
- `backend/requirements/base.txt` - base dependencies
- `backend/requirements/production.txt` - production dependencies
- `backend/.dockerignore` - build context exclusions

## Success Criteria
Build should show:
- 500+ MB in site-packages after installation
- uvicorn, fastapi, and torch importable in production stage
- Final image size: 3-4 GB (not 7.1 GB)

Please provide a working Dockerfile with explanations of what was wrong and why your solution works.
