---
title: "Railway Deployment - Complete Guide"
type: "deployment-guide"
category: "operations"
stage: "production"
status: "active"
version: "2.0"
last_updated: "2025-11-10"
consolidates:
  - RAILWAY_DEPLOYMENT_GUIDE.md
  - RAILWAY_VISUAL_SETUP_GUIDE.md
  - RAILWAY_ENV_VARIABLES_GUIDE.md
  - RAILWAY_QUICK_START_CHECKLIST.md
  - RAILWAY_FIX_ROOT_DIRECTORY.md
  - RAILWAY_BUILD_ERROR_FIX.md
  - RAILWAY_NEXT_STEPS.md
---

# BAHR Platform - Railway Deployment Complete Guide

This comprehensive guide consolidates all Railway deployment documentation into one authoritative resource for deploying the BAHR platform to staging/production.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Deployment](#step-by-step-deployment)
4. [Environment Variables Reference](#environment-variables-reference)
5. [Troubleshooting](#troubleshooting)
6. [Post-Deployment](#post-deployment)
7. [Advanced Topics](#advanced-topics)

---

## Quick Start

**⚠️ MOST CRITICAL STEP:**
**You MUST set Root Directory = `backend` and `frontend` for each service.**

This is the #1 cause of deployment failures!

### 20-Minute Deployment Checklist

**Backend (10 steps - 10 minutes):**
- [ ] Step 1: Create Empty Project → "BAHR Staging"
- [ ] Step 2: "+ New" → GitHub Repo → Select BAHR
- [ ] Step 3: ⚠️ **Settings → Root Directory → `backend`**
- [ ] Step 4: "+ New" → Database → PostgreSQL
- [ ] Step 5: "+ New" → Database → Redis
- [ ] Step 6: Generate secret: `openssl rand -hex 32`
- [ ] Step 7: Backend → Variables → Add all environment variables
- [ ] Step 8: Wait for deployment to complete
- [ ] Step 9: Settings → Networking → Generate Domain
- [ ] Step 10: Test: `curl <backend-url>/health`

**Frontend (6 steps - 5 minutes):**
- [ ] Step 1: "+ New" → GitHub Repo → Select BAHR (same repo)
- [ ] Step 2: ⚠️ **Settings → Root Directory → `frontend`**
- [ ] Step 3: Frontend → Variables → Add `NEXT_PUBLIC_API_URL`
- [ ] Step 4: Wait for deployment to complete
- [ ] Step 5: Settings → Networking → Generate Domain
- [ ] Step 6: Test: Open frontend URL in browser

**Final Configuration (2 steps - 5 minutes):**
- [ ] Step 1: Update Backend CORS_ORIGINS with both URLs
- [ ] Step 2: Run verification: `./scripts/verify_deployment.sh`

**Total Time: ~20-30 minutes**

---

## Prerequisites

### Required Accounts & Tools
1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: BAHR code pushed to GitHub
3. **Railway CLI** (optional but recommended):
   ```bash
   npm install -g @railway/cli
   railway login
   ```

### Generate Secrets Locally
You'll need a secure SECRET_KEY for the backend:
```bash
openssl rand -hex 32
```
Save this output - you'll use it in environment variables.

---

## Step-by-Step Deployment

### Part 1: Backend Deployment

#### Step 1: Create Railway Project

1. Log in to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Select **"Empty Project"** (we'll add services manually)
4. Name your project: "BAHR Staging"

**Why Empty Project?** We need to deploy 2 services from the same repository with different root directories. Starting empty gives us full control.

---

#### Step 2: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database" → "PostgreSQL"**
3. Railway provisions a PostgreSQL instance
4. `DATABASE_URL` environment variable is automatically created

**What happens:** Railway creates a managed PostgreSQL database and makes the connection string available via `${{Postgres.DATABASE_URL}}` reference.

---

#### Step 3: Add Redis Cache

1. Click **"+ New"** again
2. Select **"Database" → "Redis"**
3. Railway provisions a Redis instance
4. `REDIS_URL` environment variable is automatically created

**What happens:** Railway creates a managed Redis instance for caching. You'll reference it via `${{Redis.REDIS_URL}}`.

---

#### Step 4: Add Backend Service

1. Click **"+ New"**
2. Select **"GitHub Repo"**
3. Choose your BAHR repository
4. Railway creates a service

**Visual Structure:**
```
BAHR Project
├── Postgres (DATABASE_URL)
├── Redis (REDIS_URL)
└── Backend Service ← Just created
```

---

#### Step 5: Configure Backend Root Directory

**⚠️ CRITICAL STEP - Don't skip this!**

1. Click on the backend service
2. Go to **"Settings"** tab
3. Scroll to **"Service Settings"**
4. Find **"Root Directory"**
5. **Enter: `backend`** (without slashes, no `/backend` or `backend/`)
6. Click outside to save

**What this does:**
```
Without Root Directory (❌):
Railway looks in: /BAHR/
Can't find requirements.txt
Doesn't know it's Python
Build fails

With Root Directory = backend (✅):
Railway looks in: /BAHR/backend/
Finds requirements.txt
Detects Python automatically
Uses Procfile for commands
Build succeeds
```

**Railway will now:**
- Build from `backend/` directory
- Detect Python automatically (from `requirements.txt`)
- Use `backend/Procfile` for build/start commands
- Use `backend/nixpacks.toml` for build configuration

---

#### Step 6: Set Backend Environment Variables

Click on Backend Service → **"Variables"** → Add these variables:

```bash
# Application Settings
PROJECT_NAME=BAHR API
API_VERSION=1.0.0
ANALYSIS_ENGINE_VERSION=1.0.0
ENVIRONMENT=staging
LOG_LEVEL=INFO

# Security - CRITICAL: Use your generated secret
SECRET_KEY=<paste-your-openssl-rand-hex-32-output>

# Database - Railway auto-links these
DATABASE_URL=${{Postgres.DATABASE_URL}}
DATABASE_ECHO=false

# Redis - Railway auto-links
REDIS_URL=${{Redis.REDIS_URL}}
CACHE_TTL=86400

# CORS - Update after frontend is deployed
CORS_ORIGINS=https://your-backend-url.railway.app

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600

# Maintenance
MAINTENANCE_MODE=false
```

**Important Notes:**
- `${{Postgres.DATABASE_URL}}` is a Railway reference, not a hardcoded string
- `SECRET_KEY` must be exactly 64 hex characters (from `openssl rand -hex 32`)
- `CORS_ORIGINS` will be updated in Step 13 with frontend URL

---

#### Step 7: Deploy Backend

After setting environment variables, Railway automatically deploys.

**Watch the deployment logs** (Deployments tab):
```
✅ Detected Python from requirements.txt
✅ Installing dependencies from requirements.txt
✅ Running migrations: alembic upgrade head
✅ Seeding database: python scripts/seed_database.py
✅ Starting server: uvicorn app.main:app
✅ Deployment successful
```

**What the Procfile does:**
```
web: /opt/venv/bin/alembic upgrade head && /opt/venv/bin/python scripts/seed_database.py && /opt/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

This runs migrations, seeds the database with 16 Arabic meters, then starts FastAPI.

---

#### Step 8: Generate Backend Domain

1. Backend Service → Settings → **"Networking"**
2. Click **"Generate Domain"**
3. Copy the URL (e.g., `https://backend-production-c17c.up.railway.app`)
4. **Save this URL** - you'll need it for:
   - Frontend's `NEXT_PUBLIC_API_URL`
   - Backend's `CORS_ORIGINS`

---

#### Step 9: Verify Backend Deployment

**Health Check:**
```bash
curl https://your-backend-url.railway.app/health

# Expected response:
{"status":"healthy"}
```

**API Documentation:**
```bash
open https://your-backend-url.railway.app/docs
# Should show Swagger UI
```

**Test Analyze Endpoint:**
```bash
curl -X POST https://your-backend-url.railway.app/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "أَلا لَيتَ الشَبابَ يَعودُ يَوماً"}'

# Expected: JSON with bahr detection results
```

---

### Part 2: Frontend Deployment

#### Step 10: Add Frontend Service

1. In the same Railway project, click **"+ New"**
2. Select **"GitHub Repo"**
3. Choose the **SAME BAHR repository**
4. Railway creates a new service

**Visual Structure:**
```
BAHR Project
├── Postgres
├── Redis
├── Backend Service
└── Frontend Service ← Just created
```

---

#### Step 11: Configure Frontend Root Directory

**⚠️ CRITICAL STEP - Don't skip this!**

1. Click on the frontend service
2. Rename it to "frontend" (Settings → Service Name)
3. Go to **"Settings"** tab
4. Scroll to **"Service Settings"**
5. Find **"Root Directory"**
6. **Enter: `frontend`** (without slashes)
7. Click outside to save

**Railway will now:**
- Build from `frontend/` directory
- Detect Next.js automatically (from `package.json`)
- Run `npm ci && npm run build && npm start`
- Use Node.js 20 (specified in `frontend/nixpacks.toml`)

---

#### Step 12: Set Frontend Environment Variables

Click on Frontend Service → **"Variables"** → Add these:

```bash
# Backend API URL - Use the URL from Step 8
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app/api/v1

# Node Environment
NODE_ENV=production
```

**Critical:** Don't forget the `/api/v1` at the end of the API URL!

---

#### Step 13: Deploy Frontend

Railway automatically deploys after setting variables.

**Watch the deployment logs:**
```
✅ Detected Next.js from package.json
✅ Using Node.js 20.x (from nixpacks.toml)
✅ Installing dependencies: npm ci
✅ Building Next.js: npm run build
✅ Starting server: npm start
✅ Deployment successful
```

---

#### Step 14: Generate Frontend Domain

1. Frontend Service → Settings → **"Networking"**
2. Click **"Generate Domain"**
3. Copy the URL (e.g., `https://frontend-production-6416.up.railway.app`)

---

#### Step 15: Update Backend CORS (Final)

Now that you have both URLs, update backend CORS:

1. Go back to Backend Service → **"Variables"**
2. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://backend-production-c17c.up.railway.app,https://frontend-production-6416.up.railway.app
   ```
   (Replace with your actual URLs)
3. Railway will automatically redeploy backend

**Format:**
- Comma-separated, no spaces
- HTTPS URLs (Railway provides SSL automatically)
- No trailing slashes
- Include both backend and frontend URLs

---

#### Step 16: Verify Frontend Deployment

**Open in browser:**
```
https://your-frontend-url.railway.app
```

**You should see:**
- ✅ Arabic text displayed correctly (RTL)
- ✅ BAHR logo and title
- ✅ Homepage loads without errors

**Test analyze functionality:**
1. Go to `/analyze` page
2. Enter a verse: `أَلا لَيتَ الشَبابَ يَعودُ يَوماً`
3. Click "حلّل"
4. Should see bahr detection results (meter, confidence, taqti3)

---

## Environment Variables Reference

### Backend Service - Complete List

| Variable | Value | Purpose |
|----------|-------|---------|
| `PROJECT_NAME` | `BAHR API` | Application name |
| `API_VERSION` | `1.0.0` | API version |
| `ANALYSIS_ENGINE_VERSION` | `1.0.0` | Engine version |
| `ENVIRONMENT` | `staging` or `production` | Environment identifier |
| `LOG_LEVEL` | `INFO` or `DEBUG` | Logging verbosity |
| `SECRET_KEY` | 64-char hex string | JWT signing key |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | PostgreSQL connection |
| `DATABASE_ECHO` | `false` | Log SQL queries |
| `REDIS_URL` | `${{Redis.REDIS_URL}}` | Redis connection |
| `CACHE_TTL` | `86400` | Cache TTL (seconds) |
| `CORS_ORIGINS` | Comma-separated URLs | Allowed origins |
| `RATE_LIMIT_REQUESTS` | `100` | Max requests/period |
| `RATE_LIMIT_PERIOD` | `3600` | Rate limit window (seconds) |
| `MAINTENANCE_MODE` | `false` | Enable maintenance mode |

### Frontend Service - Complete List

| Variable | Value | Purpose |
|----------|-------|---------|
| `NEXT_PUBLIC_API_URL` | `https://backend-url/api/v1` | Backend API endpoint |
| `NODE_ENV` | `production` | Node environment |

### Railway Auto-Provided Variables

Railway automatically provides these (don't set manually):
- `PORT` - Port your app should listen on
- `RAILWAY_ENVIRONMENT` - Environment name
- `RAILWAY_PUBLIC_DOMAIN` - Your service's public domain

---

## Troubleshooting

### Issue 1: "Nixpacks was unable to generate a build plan"

**Symptoms:**
```
Error creating build plan with Nixpacks
Build failed
```

**Root Cause:** Root Directory not set

**Fix:**
1. Click on service → Settings
2. Set **Root Directory** = `backend` or `frontend`
3. Save (click outside field)
4. Railway will automatically redeploy
5. Build should succeed

**Why this happens:**
Your repository has both `backend/` and `frontend/` directories. Without Root Directory, Railway doesn't know which one to build.

---

### Issue 2: Node.js Version Error (Frontend)

**Symptoms:**
```
You are using Node.js 18.x
Next.js requires Node.js >=20.9.0
Build failed
```

**Root Cause:** Railway defaulted to Node.js 18

**Fix:**
✅ Already fixed in `frontend/nixpacks.toml`:
```toml
[phases.setup]
nixPkgs = ["nodejs_20"]
```

If you still see this error:
1. Verify `frontend/nixpacks.toml` exists in your repository
2. Push latest code to GitHub
3. Redeploy frontend service
4. Build logs should show: "Using Node.js 20.x.x"

---

### Issue 3: Database Connection Failed

**Symptoms:**
```
sqlalchemy.exc.OperationalError: could not connect to server
Connection refused
```

**Root Cause:** DATABASE_URL not configured correctly

**Fix:**
1. Backend Service → Variables
2. Verify `DATABASE_URL=${{Postgres.DATABASE_URL}}`
3. Check PostgreSQL service is running (green status)
4. Ensure both services are in the same Railway project
5. Redeploy backend

---

### Issue 4: Redis Connection Timeout

**Symptoms:**
```
redis.exceptions.ConnectionError: Error connecting to Redis
```

**Root Cause:** REDIS_URL not configured correctly

**Fix:**
1. Backend Service → Variables
2. Verify `REDIS_URL=${{Redis.REDIS_URL}}`
3. Check Redis service is running (green status)
4. Ensure both services are in the same Railway project
5. Redeploy backend

---

### Issue 5: CORS Errors in Browser Console

**Symptoms:**
```
Access to fetch at '...' from origin '...' has been blocked by CORS policy
```

**Root Cause:** CORS_ORIGINS doesn't include frontend URL

**Fix:**
1. Backend Service → Variables
2. Update `CORS_ORIGINS` to include both URLs:
   ```
   CORS_ORIGINS=https://backend-url.railway.app,https://frontend-url.railway.app
   ```
3. Use HTTPS (Railway default)
4. No trailing slashes
5. Comma-separated, no spaces
6. Redeploy backend after updating

---

### Issue 6: Migrations Not Running

**Symptoms:**
```
sqlalchemy.exc.ProgrammingError: relation "meters" does not exist
```

**Root Cause:** Database migrations didn't run during deployment

**Fix:**
1. Check deployment logs for migration output
2. Verify `backend/Procfile` contains migration command:
   ```
   web: /opt/venv/bin/alembic upgrade head && ...
   ```
3. Manually run migrations via Railway CLI:
   ```bash
   railway run --service backend /opt/venv/bin/alembic upgrade head
   ```
4. Verify database has tables:
   ```bash
   railway connect postgres
   \dt
   ```

---

### Issue 7: Image Size Too Large (8.5 GB)

**Symptoms:**
```
Error: Docker image size 8.5 GB exceeds Railway's 4 GB limit
```

**Root Cause:** Large ML dependencies (PyTorch, CUDA) from old camel-tools version

**Fix:**
✅ Already fixed - camel-tools removed, implemented functions ourselves:
- Image size reduced from 8.5 GB → ~500 MB
- No functionality lost (we only used 2 simple text normalization functions)

If you still see this:
1. Check `backend/requirements.txt` doesn't have `camel-tools`
2. Verify `backend/app/core/phonetics.py` has custom normalization functions
3. Push latest code and redeploy

---

### Issue 8: Meters Not Seeded

**Symptoms:**
```
GET /api/v1/bahrs returns empty array
Database has 0 meters
```

**Root Cause:** Seed script didn't run or failed

**Fix:**
1. Check deployment logs for seed script output
2. Manually run seed:
   ```bash
   railway run --service backend /opt/venv/bin/python scripts/seed_database.py
   ```
3. Verify seeding:
   ```bash
   curl https://backend-url/api/v1/bahrs
   # Should return 16 meters
   ```

---

### Issue 9: Frontend Can't Reach Backend (404)

**Symptoms:**
```
GET /api/v1/analyze → 404 Not Found
Network errors in browser console
```

**Root Cause:** Wrong NEXT_PUBLIC_API_URL

**Fix:**
1. Frontend Service → Variables
2. Verify `NEXT_PUBLIC_API_URL` is correct:
   - Includes backend URL
   - Ends with `/api/v1`
   - Uses HTTPS
   - No trailing slash after `/v1`
3. Test backend directly:
   ```bash
   curl https://backend-url/api/v1/health
   ```
4. Redeploy frontend after fixing

---

## Post-Deployment

### Share with Beta Testers

**Send them the frontend URL:**
```
Frontend: https://your-frontend-url.railway.app
```

**Instructions for testers:**
1. Visit the URL
2. Click "تحليل الشعر" or go to `/analyze`
3. Enter an Arabic poetry verse
4. Click "حلّل" to analyze
5. View results (bahr, taqti3, confidence score)

### Monitor Service Health

**Via Railway Dashboard:**
1. Check service status (green = healthy)
2. View deployment logs (Deployments → Latest → Logs)
3. Monitor metrics (CPU, memory, requests)

**Via CLI:**
```bash
# Backend logs
railway logs --service backend

# Frontend logs
railway logs --service frontend

# Follow logs in real-time
railway logs --service backend --follow
```

### Set Up Monitoring

Consider integrating:
- **Error tracking**: Sentry
- **Analytics**: Plausible or Google Analytics
- **Uptime monitoring**: UptimeRobot
- **Performance**: Railway built-in metrics

---

## Advanced Topics

### Database Management

**Connect to PostgreSQL:**
```bash
# Via Railway CLI
railway connect postgres

# Or get connection string
railway variables --service postgres
```

**Run migrations manually:**
```bash
railway run --service backend /opt/venv/bin/alembic upgrade head
```

**Create new migration:**
```bash
railway run --service backend /opt/venv/bin/alembic revision --autogenerate -m "description"
```

### Scaling & Performance

**Auto-scaling:**
Railway automatically scales based on:
- CPU usage
- Memory usage
- Request volume

Configure in: **Settings → Resources**

**Cost estimates:**
- Free tier: $5 credit/month
- Staging: ~$10-20/month
  - Backend: ~$5
  - Frontend: ~$5
  - PostgreSQL: ~$5
  - Redis: ~$5

**Performance optimization:**
1. ✅ Redis caching (already implemented)
2. Enable compression (Next.js default)
3. Monitor response times in Railway metrics
4. Add database indexes if needed
5. Consider CDN for frontend (Cloudflare)

### Custom Domains

**Add custom domain:**
1. Service → Settings → Domains
2. Click "Custom Domain"
3. Enter your domain (e.g., `api.bahr.app`)
4. Update DNS:
   - Type: CNAME
   - Name: api
   - Value: (Railway provides)
5. SSL certificate auto-generated

### Environment Management

**Create production environment:**
1. Duplicate staging setup
2. Use separate Railway project
3. Update environment variables:
   - `ENVIRONMENT=production`
   - Different `SECRET_KEY`
   - Different domains
4. Set up CI/CD for auto-deployment

---

## Quick Reference Commands

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to project
railway link

# View all services
railway service

# View logs
railway logs --service backend
railway logs --service frontend

# Run commands in service context
railway run --service backend <command>

# View environment variables
railway variables --service backend

# Set variable via CLI
railway variables --service backend set KEY=value

# Deploy (if using CLI)
railway up

# Connect to database
railway connect postgres

# Shell access (if needed)
railway run --service backend bash
```

---

## Complete Verification Checklist

### Backend Verification

- [ ] Health check returns 200: `curl /health`
- [ ] API docs accessible: `open /docs`
- [ ] Analyze endpoint works: `POST /api/v1/analyze`
- [ ] Database has 16 meters: `SELECT COUNT(*) FROM meters;`
- [ ] Redis caching works (second request faster)
- [ ] CORS allows frontend origin
- [ ] Logs show no errors
- [ ] Migrations applied successfully
- [ ] Seed data loaded

### Frontend Verification

- [ ] Homepage loads correctly
- [ ] Arabic text displays RTL
- [ ] Fonts load (Cairo, Amiri)
- [ ] Analyze page accessible
- [ ] Can submit verse for analysis
- [ ] Results display correctly
- [ ] Loading states work
- [ ] Error handling works
- [ ] No console errors in browser
- [ ] Mobile responsive

### Integration Verification

- [ ] Frontend can call backend API
- [ ] CORS allows requests
- [ ] Analysis results display in frontend
- [ ] Cache improves response time
- [ ] Multiple verses can be analyzed
- [ ] Results are accurate
- [ ] No network errors
- [ ] End-to-end flow works

---

## Success Criteria

Your deployment is successful when:

✅ **Backend:**
- Health endpoint returns `{"status":"healthy"}`
- Swagger UI loads at `/docs`
- Can analyze Arabic verses
- Database has 16 meters seeded
- Redis caching working

✅ **Frontend:**
- Homepage loads with correct RTL
- Can navigate to `/analyze`
- Can submit and analyze verses
- Results display correctly
- No CORS errors

✅ **Integration:**
- Frontend successfully calls backend
- Analysis flow works end-to-end
- Performance is acceptable (<500ms cached)

---

## Support & Resources

**Official Documentation:**
- [Railway Docs](https://docs.railway.app)
- [Nixpacks Documentation](https://nixpacks.com)

**BAHR Project Docs:**
- [Architecture Overview](../technical/ARCHITECTURE_OVERVIEW.md)
- [Backend API](../technical/BACKEND_API.md)
- [Database Schema](../technical/DATABASE_SCHEMA.md)

**Get Help:**
1. Check deployment logs first
2. Review this troubleshooting section
3. Search Railway Discord community
4. Open GitHub issue in BAHR repo
5. Contact Railway support (paid plans)

---

## Summary

After following this guide, you'll have:

✅ **Backend deployed** on Railway with:
- FastAPI application running
- PostgreSQL database with migrations applied
- Redis for caching
- 16 classical Arabic meters seeded
- Health checks configured
- Public API available

✅ **Frontend deployed** on Railway with:
- Next.js application built and running
- Connected to backend API
- RTL Arabic support working
- Analysis interface functional
- Mobile responsive

✅ **Staging/Production environment** ready with:
- Public URLs for both services
- Environment variables configured
- Database and caching operational
- Monitoring and logs available
- SSL certificates auto-generated

**Next Steps:**
1. Share URLs with team/beta testers
2. Monitor performance and errors
3. Collect feedback
4. Iterate based on testing
5. Plan production deployment
6. Set up CI/CD for auto-deployments

---

**Congratulations! Your BAHR platform is now live on Railway! 🚀**

---

## Archived Troubleshooting Guides

For historical troubleshooting documentation, see:
- [archive/deployment/RAILWAY_BUILD_ERROR_FIX.md](../../archive/deployment/RAILWAY_BUILD_ERROR_FIX.md) - 14 historical build issues and fixes
- [archive/deployment/RAILWAY_FIX_ROOT_DIRECTORY.md](../../archive/deployment/RAILWAY_FIX_ROOT_DIRECTORY.md) - Root directory configuration details
- [archive/deployment/RAILWAY_NEXT_STEPS.md](../../archive/deployment/RAILWAY_NEXT_STEPS.md) - Original next steps guide

These files document specific issues encountered during initial deployment and their resolutions. Most issues are already fixed in the current codebase.
