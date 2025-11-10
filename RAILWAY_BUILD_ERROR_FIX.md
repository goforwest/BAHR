# Railway Build Failure Fix - "Error creating build plan with Railpack"

## The Error You're Seeing

```
Deployment failed during the build process
Error creating build plan with Railpack
```

---

## Root Cause

Railway's build system (Railpack/Nixpacks) couldn't automatically detect how to build your project. This happens when:
1. **Root Directory is not set** (most common)
2. Missing or unclear project markers (requirements.txt, package.json in wrong location)
3. Railway trying to build from repository root instead of service subdirectory

---

## Solution: Step-by-Step Fix

### ✅ CRITICAL: Set Root Directory

**This is THE most important step!**

1. Go to Railway Dashboard
2. Click on your service (the one that failed)
3. Click **"Settings"** tab
4. Scroll down to find **"Root Directory"**
5. **For Backend Service:** Enter `backend`
6. **For Frontend Service:** Enter `frontend`
7. Click outside the field to save
8. Railway will automatically redeploy

**Visual:**
```
Settings Tab
├── Service Name: backend
├── ...
├── Root Directory:
│   ┌─────────────────────┐
│   │ backend            │  ← Type this!
│   └─────────────────────┘
└── ...
```

---

## Why This Happens

### Your Repository Structure:
```
/BAHR/
├── backend/
│   ├── requirements.txt  ← Python project markers
│   ├── Procfile
│   ├── nixpacks.toml
│   └── app/
├── frontend/
│   ├── package.json      ← Node.js project markers
│   └── src/
└── ...
```

### Without Root Directory:
- Railway looks in `/BAHR/` (root)
- Doesn't find `requirements.txt` or `package.json`
- Doesn't know if it's Python, Node, or something else
- ❌ Error: "Cannot create build plan"

### With Root Directory = "backend":
- Railway looks in `/BAHR/backend/`
- Finds `requirements.txt`
- Detects: "This is a Python project!"
- Uses `Procfile`, `nixpacks.toml`
- ✅ Build succeeds

---

## Complete Deployment Checklist

### Backend Service

- [ ] **Step 1:** Service created from GitHub repo
- [ ] **Step 2:** ⚠️ **ROOT DIRECTORY SET TO `backend`**
- [ ] **Step 3:** PostgreSQL database added
- [ ] **Step 4:** Redis database added
- [ ] **Step 5:** Environment variables configured:
  - `SECRET_KEY` (generate: `openssl rand -hex 32`)
  - `DATABASE_URL=${{Postgres.DATABASE_URL}}`
  - `REDIS_URL=${{Redis.REDIS_URL}}`
  - `CORS_ORIGINS=<your-urls>`
  - All other variables from RAILWAY_ENV_VARIABLES_GUIDE.md
- [ ] **Step 6:** Build should now succeed automatically

### Frontend Service

- [ ] **Step 1:** Service created from SAME GitHub repo
- [ ] **Step 2:** ⚠️ **ROOT DIRECTORY SET TO `frontend`**
- [ ] **Step 3:** Environment variables configured:
  - `NEXT_PUBLIC_API_URL=<backend-url>/api/v1`
  - `NODE_ENV=production`
- [ ] **Step 4:** Build should now succeed automatically

---

## How to Verify Root Directory is Set

1. Go to service in Railway Dashboard
2. Click **"Settings"**
3. Look for **"Root Directory"** section
4. Should show: `backend` or `frontend`
5. If empty or shows `/` → That's the problem!

---

## Additional Configuration Files Created

Your repository now has these files to help Railway:

### Backend:
- ✅ `backend/Procfile` - Defines how to run the app
- ✅ `backend/nixpacks.toml` - Build configuration
- ✅ `backend/runtime.txt` - Python version
- ✅ `backend/railway.json` - Railway-specific config
- ✅ `backend/requirements.txt` - Python dependencies

### Frontend:
- ✅ `frontend/package.json` - Node.js dependencies
- ✅ `frontend/railway.json` - Railway-specific config

These files help Railway understand your project structure.

---

## Testing After Fix

### 1. Check Build Logs

After setting Root Directory:
1. Go to service → **"Deployments"**
2. Click on latest deployment
3. Watch the build logs

**Should see:**
```
✅ Detected Python application (from requirements.txt)
✅ Installing dependencies...
✅ Running release command...
✅ Starting server...
```

### 2. Verify Deployment

**Backend:**
```bash
curl https://your-backend-url.railway.app/health
# Expected: {"status":"healthy"}
```

**Frontend:**
```bash
curl https://your-frontend-url.railway.app/
# Expected: HTML (status 200)
```

---

## If Build Still Fails After Setting Root Directory

### Check Build Logs for:

**1. Node.js Version Error (Frontend):**
```
You are using Node.js 18.x. For Next.js, Node.js version ">=20.9.0" is required.
```
**Fix:** 
- ✅ Already fixed in `frontend/nixpacks.toml` (specifies nodejs_20)
- Push latest code to GitHub
- Redeploy frontend service
- Verify in build logs: Should show "nodejs_20" in setup phase

**2. Python Package Compatibility Error:**
```
ERROR: Could not find a version that satisfies the requirement camel-tools==1.5.2
ERROR: Ignored the following versions that require a different python version
```
**Fix:** 
- ✅ Already fixed: `camel-tools` updated to 1.5.7 (supports Python 3.11)
- Some packages have Python version requirements
- Check PyPI for compatible versions
- Update version in `requirements.txt`

**3. Missing Dependencies:**
```
Error: Could not find module 'X'
```
**Fix:** Add to `requirements.txt` or `package.json`

**4. Wrong Python Version:**
```
Error: Python 3.11 required
```
**Fix:** Check `backend/runtime.txt` has `python-3.11.*`

**5. Database Connection Error:**
```
Error: Cannot connect to database
```
**Fix:** Verify `DATABASE_URL=${{Postgres.DATABASE_URL}}` in variables

**6. Port Binding Error:**
```
Error: Address already in use
```
**Fix:** Verify start command uses `--port $PORT` (Railway provides this variable)

**7. Build Timeout During "importing to docker":**
```
importing to docker: 1m 13s
Build timed out
```
**Fix:** 
- ✅ Already optimized: Added `.dockerignore` to exclude unnecessary files
- ✅ Enabled pip caching in `nixpacks.toml`
- ✅ Reduced dependencies (removed build-essential)
- Push latest code and retry deployment
- Build should complete faster now (30-60s instead of 1m+)

**8. Dockerfile Detected But Failing:**
```
ERROR: failed to compute cache key: "/tests": not found
Using Detected Dockerfile
```
**Fix:**
- ✅ Already fixed: Renamed `backend/Dockerfile` to `Dockerfile.dev`
- Railway will now use Nixpacks instead of Dockerfile
- Nixpacks is faster and better optimized for Railway
- Automatically detects Python via `requirements.txt`
- Uses `nixpacks.toml` and `Procfile` for configuration

**9. Pip Command Not Found with Nixpacks:**
```
/bin/bash: line 1: pip: command not found
RUN pip install --upgrade pip setuptools wheel
```
**Fix:**
- ✅ Already fixed: Use `python -m pip` instead of `pip`
- Nix-provided Python requires module invocation
- Updated `nixpacks.toml` to use `python -m pip install`
- This ensures pip uses the correct Python interpreter

---

## Alternative: Manual Configuration

If Root Directory setting doesn't work, try manually:

### Via Railway Dashboard:

1. **Settings → Build Command:**
   ```bash
   cd backend && pip install -r requirements.txt
   ```

2. **Settings → Start Command:**
   ```bash
   cd backend && alembic upgrade head && python scripts/seed_database.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

**Note:** This is less elegant than Root Directory but should work.

---

## Quick Reference

| Problem | Solution |
|---------|----------|
| "Error creating build plan" | Set Root Directory |
| Build looks in wrong folder | Set Root Directory |
| Can't find requirements.txt | Set Root Directory |
| Can't find package.json | Set Root Directory |
| Railway doesn't detect language | Set Root Directory |
| Build succeeds but wrong app | Set Root Directory |

**Pattern noticed? 😄 SET ROOT DIRECTORY!**

---

## Visual Guide

### Before (❌ Fails):
```
Railway Build Process:
1. Clone repo → /workspace/
2. Look for project files in /workspace/
3. No requirements.txt found
4. No package.json found
5. ❌ Cannot determine project type
6. ❌ Build fails
```

### After (✅ Succeeds):
```
Railway Build Process (Backend):
1. Clone repo → /workspace/
2. Root Directory set → Change to /workspace/backend/
3. Found requirements.txt ✅
4. Detected Python project ✅
5. Found Procfile ✅
6. Run build commands ✅
7. ✅ Build succeeds
```

---

## Summary

**The Fix (90% of cases):**
1. Go to service Settings
2. Set Root Directory = `backend` or `frontend`
3. Save
4. Watch build succeed ✅

**Files We Added to Help:**
- `backend/runtime.txt` (Python version)
- `backend/railway.json` (Railway config)
- `frontend/railway.json` (Railway config)
- Updated `backend/nixpacks.toml` (better build config)

**Next Steps:**
1. Set Root Directory (if not already done)
2. Redeploy
3. Watch build logs
4. Test endpoints
5. Celebrate! 🎉

---

## Need More Help?

- **Root Directory Guide:** See RAILWAY_VISUAL_SETUP_GUIDE.md
- **Full Deployment:** See RAILWAY_DEPLOYMENT_GUIDE.md
- **Environment Variables:** See RAILWAY_ENV_VARIABLES_GUIDE.md
- **Quick Checklist:** See RAILWAY_QUICK_START_CHECKLIST.md

---

**Remember:** The most common mistake is forgetting to set Root Directory.

**Set it to `backend` or `frontend` and 99% of build errors disappear!** ✨
