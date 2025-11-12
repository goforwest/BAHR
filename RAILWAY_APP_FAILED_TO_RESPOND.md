# Railway Application Failed to Respond - Diagnostic Guide

**Issue:** Application deployed but not responding to requests  
**Error:** "Application failed to respond"  
**Request ID:** JxRn-adAToixY7eN0_TJvA  
**Date:** November 11, 2025

---

## 🔍 What This Error Means

**Good News:** The build likely **succeeded** (no more testing stage error!)  
**Problem:** The application is **crashing during startup** or not listening on the correct port

---

## 🚨 Immediate Diagnostic Steps

### Step 1: Check Railway Logs (CRITICAL)

```bash
# If you have Railway CLI installed:
railway logs

# Or use Railway Dashboard:
# 1. Go to https://railway.app
# 2. Select your backend service
# 3. Click "Deployments"
# 4. Click latest deployment
# 5. View "Deploy Logs" AND "Application Logs"
```

### Step 2: Look for These Common Errors

#### Error A: Port Binding Issue

**Symptom in logs:**
```
Error: Application failed to bind to port
Error: Address already in use
```

**Cause:** App not using Railway's `$PORT` variable

**Fix:** Check that your start command uses `$PORT`:
```bash
# In Railway Settings → Deploy → Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

#### Error B: Redis Connection Failed

**Symptom in logs:**
```
✗ Redis connection failed: Connection refused
ConnectionRefusedError: [Errno 111] Connection refused
```

**Cause:** Redis not configured or URL incorrect

**Fix in Railway Dashboard:**
1. Add Redis service if missing (New → Database → Redis)
2. Link to backend service
3. Environment variable `REDIS_URL` should auto-populate
4. Redeploy

---

#### Error C: Database Connection Failed

**Symptom in logs:**
```
sqlalchemy.exc.OperationalError
connection to server failed
FATAL: password authentication failed
```

**Cause:** PostgreSQL not configured or credentials wrong

**Fix:**
1. Add PostgreSQL service if missing
2. Verify `DATABASE_URL` environment variable is set
3. Check if Alembic migrations need to run

---

#### Error D: Missing Environment Variables

**Symptom in logs:**
```
KeyError: 'SECRET_KEY'
RuntimeError: Missing required environment variable
```

**Cause:** Required env vars not set

**Fix:** Add these in Railway Variables:
```bash
SECRET_KEY=<generate-secure-key>
CORS_ORIGINS=https://your-frontend.railway.app
REDIS_URL=<auto-from-redis-service>
DATABASE_URL=<auto-from-postgres-service>
```

---

#### Error E: Import Errors (Still)

**Symptom in logs:**
```
ModuleNotFoundError: No module named 'app.core'
ImportError: cannot import name 'normalize_arabic_text'
```

**Cause:** Dependencies not installed or PYTHONPATH issue

**Fix:**
1. Check `requirements/base.txt` has all dependencies
2. Verify build logs show pip install succeeded
3. Check Dockerfile WORKDIR is `/app`

---

## 🔧 Quick Fixes by Priority

### Fix 1: Verify Start Command

**Railway Dashboard → Settings → Deploy:**

Ensure start command is:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4
```

**NOT:**
```bash
uvicorn app.main:app --port 8000  # ❌ Wrong - ignores $PORT
```

---

### Fix 2: Add Missing Services

Your app needs:
- ✅ **Backend** (current service)
- ⚠️ **Redis** (for caching)
- ⚠️ **PostgreSQL** (for analytics/data)

**To add:**
1. Railway Dashboard → New
2. Database → Redis
3. Database → PostgreSQL
4. Connect both to backend service

---

### Fix 3: Set Critical Environment Variables

**Minimum required:**
```bash
# In Railway Variables tab:
SECRET_KEY=your-secret-key-here-change-me
CORS_ORIGINS=*
LOG_LEVEL=DEBUG

# These should auto-populate when you add services:
REDIS_URL=redis://...
DATABASE_URL=postgresql://...
```

---

### Fix 4: Simplify Startup (Temporarily)

Test if app can start without external dependencies:

**Edit Railway Start Command to:**
```bash
python -c "from app.main import app; print('✓ App imports OK')" && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

This will:
1. Test if imports work
2. Start server if imports succeed

Check logs to see if import test passes.

---

## 📋 Step-by-Step Troubleshooting

### 1. Check Build Logs First

**Railway → Deployments → Latest → Build Logs**

Look for:
```
✅ Successfully built production stage
✅ ---> Running in <container-id>
✅ Successfully tagged railway:latest
```

If build failed, you'll see errors here.

---

### 2. Check Deploy Logs

**Railway → Deployments → Latest → Deploy Logs**

Look for startup sequence:
```
Starting Container
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:$PORT
```

If you see startup errors, that's your issue.

---

### 3. Check Application Logs

**Railway → Deployments → Latest → View Logs (or Application Logs)**

Look for runtime errors after startup:
```
✓ Redis connection initialized  # Good
✗ Redis connection failed        # Bad - needs fixing
```

---

## 🎯 Most Likely Causes (Ranked)

| Rank | Cause | Probability | Quick Test |
|------|-------|-------------|------------|
| 1 | Redis not configured | 90% | Check if Redis service exists |
| 2 | Wrong PORT binding | 75% | Check start command uses `$PORT` |
| 3 | Missing env vars | 60% | Check Variables tab |
| 4 | Database connection fail | 50% | Check if PostgreSQL added |
| 5 | Import/dependency error | 30% | Check build logs |

---

## 🔧 Emergency Fixes

### Option A: Disable Redis Temporarily

**Purpose:** See if Redis is the problem

**Steps:**
1. Go to `backend/app/main.py`
2. Comment out Redis startup:

```python
@app.on_event("startup")
async def startup_event():
    """Initialize Redis connection on startup."""
    try:
        pass  # Temporarily disabled
        # await get_redis()
        # print("✓ Redis connection initialized")
    except Exception as e:
        print(f"✗ Redis connection failed: {e}")
```

3. Commit and push:
```bash
git add backend/app/main.py
git commit -m "temp: disable Redis for debugging"
git push origin main
```

4. Check if app starts now
5. If yes, Redis is the issue - add Redis service

---

### Option B: Use Minimal Start Command

**Railway Settings → Deploy → Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level debug
```

Remove `--workers 4` temporarily to simplify.

---

### Option C: Add Debug Health Check

Add to `backend/app/main.py`:

```python
@app.get("/debug")
async def debug():
    import os
    return {
        "status": "alive",
        "port": os.getenv("PORT", "not set"),
        "redis_url": os.getenv("REDIS_URL", "not set")[:20] + "...",
        "database_url": os.getenv("DATABASE_URL", "not set")[:20] + "...",
    }
```

Then test: `https://your-app.railway.app/debug`

---

## 📞 Get Logs (Commands)

### Using Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs

# Stream live logs
railway logs --follow
```

### Using Railway Dashboard

1. https://railway.app
2. Your project → Backend service
3. Deployments → Latest deployment
4. Click "View Logs" button
5. Look for red error messages

---

## ✅ Success Checklist

- [ ] Build logs show production stage built successfully
- [ ] Deploy logs show no errors
- [ ] Application logs show "Application startup complete"
- [ ] Redis service added and connected (or disabled)
- [ ] PostgreSQL service added and connected (or migrations disabled)
- [ ] Start command uses `$PORT` variable
- [ ] Environment variables set (SECRET_KEY, CORS_ORIGINS, etc.)
- [ ] Health endpoint responds: `/health`

---

## 🆘 If Still Stuck

**Copy and share these logs:**

```bash
# Get full deployment logs
railway logs > deployment-logs.txt

# Check build stage
railway logs --build

# Check startup
railway logs | grep -A 20 "Starting Container"
```

**Then review:**
- `deployment-logs.txt` for specific error messages
- Look for first error in sequence (others may be cascading)
- Focus on errors between "Starting Container" and "Application startup complete"

---

## 📚 Related Docs

- **Railway Port Binding:** https://docs.railway.app/deploy/exposing-your-app
- **Environment Variables:** https://docs.railway.app/develop/variables
- **Common Errors:** https://docs.railway.app/troubleshoot/fixing-common-errors
- **BAHR Integration Report:** `docs/technical/INTEGRATION_DIAGNOSTIC_REPORT.md`

---

**Next Action:** Check Railway logs immediately to see the actual error message. The logs will tell you exactly what's failing.

**Created:** November 11, 2025  
**Priority:** URGENT  
**Estimated Fix Time:** 10-30 minutes (depending on root cause)
