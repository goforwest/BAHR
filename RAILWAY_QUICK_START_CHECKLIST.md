# Railway Deployment - Quick Start Checklist

## ⚠️ READ THIS FIRST

**The #1 mistake that causes deployment to fail:**
- ❌ Not setting Root Directory for each service
- ✅ **You MUST set Root Directory = "backend" and "frontend"**

---

## Pre-Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Railway account created (railway.app)
- [ ] `openssl` available to generate secret key

---

## Backend Deployment (10 steps)

- [ ] **Step 1:** Create new project → Empty Project
- [ ] **Step 2:** Click "+ New" → GitHub Repo → Select BAHR
- [ ] **Step 3:** ⚠️ **CRITICAL** Settings → Root Directory → **"backend"**
- [ ] **Step 4:** Click "+ New" → Database → PostgreSQL
- [ ] **Step 5:** Click "+ New" → Database → Redis
- [ ] **Step 6:** Generate secret: `openssl rand -hex 32`
- [ ] **Step 7:** Backend Variables → Add all environment variables
- [ ] **Step 8:** Wait for deployment to complete
- [ ] **Step 9:** Settings → Networking → Generate Domain
- [ ] **Step 10:** Test: `curl <backend-url>/health`

---

## Frontend Deployment (6 steps)

- [ ] **Step 1:** Click "+ New" → GitHub Repo → Select BAHR (same repo)
- [ ] **Step 2:** ⚠️ **CRITICAL** Settings → Root Directory → **"frontend"**
- [ ] **Step 3:** Frontend Variables → Add NEXT_PUBLIC_API_URL
- [ ] **Step 4:** Wait for deployment to complete
- [ ] **Step 5:** Settings → Networking → Generate Domain
- [ ] **Step 6:** Test: Open frontend URL in browser

---

## Final Configuration (2 steps)

- [ ] **Step 1:** Update Backend CORS with both URLs
- [ ] **Step 2:** Run verification script

---

## Environment Variables Quick Reference

### Backend Service

```bash
PROJECT_NAME=BAHR API
API_VERSION=1.0.0
SECRET_KEY=<YOUR_GENERATED_KEY>
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
CORS_ORIGINS=<backend-url>,<frontend-url>
ENVIRONMENT=staging
LOG_LEVEL=INFO
CACHE_TTL=86400
DATABASE_ECHO=false
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600
MAINTENANCE_MODE=false
```

### Frontend Service

```bash
NEXT_PUBLIC_API_URL=<backend-url>/api/v1
NODE_ENV=production
```

---

## Verification

```bash
# Quick check
./scripts/health_check.sh <backend-url> <frontend-url>

# Full verification (10+ tests)
BACKEND_URL=<backend-url> FRONTEND_URL=<frontend-url> ./scripts/verify_deployment.sh
```

---

## Troubleshooting

### ❌ "Nixpacks was unable to generate a build plan"

**Fix:** You forgot Root Directory!
1. Click on service → Settings
2. Scroll to "Root Directory"
3. Enter: `backend` or `frontend`
4. Redeploy

### ❌ "Module not found" errors

**Fix:** Check Root Directory is set correctly
- Should be: `backend` (not `backend/` or `/backend`)

### ❌ "Can't connect to database"

**Fix:** Check DATABASE_URL variable
- Should be: `${{Postgres.DATABASE_URL}}`
- Not a hard-coded connection string

### ❌ CORS errors in browser

**Fix:** Update CORS_ORIGINS
- Include both backend and frontend URLs
- Format: `https://backend.railway.app,https://frontend.railway.app`
- No trailing slashes, comma-separated, no spaces

---

## Success Criteria

✅ Backend health check returns 200  
✅ Backend /docs page loads  
✅ Analysis endpoint works  
✅ Frontend homepage loads  
✅ Can analyze verse from frontend  
✅ Results display correctly  
✅ No CORS errors in browser console  

---

## Time Estimate

- Backend setup: 10-15 minutes
- Frontend setup: 5-10 minutes
- Verification: 5 minutes
- **Total: ~20-30 minutes**

---

## What Happens During Deployment

### Backend

```
1. Railway detects: Python (from requirements.txt)
2. Railway builds:
   - Installs dependencies
   - Runs: alembic upgrade head (migrations)
   - Runs: python scripts/seed_database.py (seed data)
3. Railway starts: uvicorn app.main:app
4. Result: 16 meters in database, API ready
```

### Frontend

```
1. Railway detects: Next.js (from package.json)
2. Railway builds:
   - Installs dependencies: npm ci
   - Builds: npm run build
3. Railway starts: npm start
4. Result: Production Next.js server running
```

---

## After Deployment

### Share with Team

```
Backend:
- URL: https://your-backend.railway.app
- API: https://your-backend.railway.app/docs
- Health: https://your-backend.railway.app/health

Frontend:
- URL: https://your-frontend.railway.app
- Analyze: https://your-frontend.railway.app/analyze
```

### Monitor

- Railway Dashboard → Service → Deployments → Logs
- Watch for errors
- Check response times
- Monitor database usage

---

## Cost

**Free Tier:** $5 credit/month  
**Staging Environment:** ~$10-15/month
- Backend: ~$5
- Frontend: ~$5  
- PostgreSQL: ~$5
- Redis: ~$5

---

## Help & Documentation

- **If deployment fails:** `RAILWAY_FIX_ROOT_DIRECTORY.md`
- **Visual guide:** `RAILWAY_VISUAL_SETUP_GUIDE.md`
- **Complete guide:** `RAILWAY_DEPLOYMENT_GUIDE.md`
- **Environment variables:** `RAILWAY_ENV_VARIABLES_GUIDE.md`

---

## Ready to Deploy?

1. ✅ Read the checklist
2. ✅ Understand Root Directory requirement
3. ✅ Have all commands ready
4. ✅ Go to railway.app
5. ✅ Follow the steps above
6. ✅ Deploy! 🚀

**Remember:** Set Root Directory = "backend" and "frontend"

That's the most important step!
