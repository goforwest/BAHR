# Railway Deployment - Step-by-Step Visual Guide

## The Problem You Encountered

```
❌ Railway tried to build from repository root:
   /BAHR/
   ├── backend/      ← Python project
   ├── frontend/     ← Node.js project
   └── ...
   
   Result: "Nixpacks was unable to generate a build plan"
   (It doesn't know which one to build!)
```

---

## The Solution: Two Services, Two Root Directories

```
✅ Create TWO separate services from SAME repository:

Service 1: Backend
├── Root Directory: "backend"
├── Railway builds from: /BAHR/backend/
├── Detects: Python (from requirements.txt)
└── Uses: backend/Procfile

Service 2: Frontend  
├── Root Directory: "frontend"
├── Railway builds from: /BAHR/frontend/
├── Detects: Node.js (from package.json)
└── Auto-configures: Next.js
```

---

## Step-by-Step Setup

### Step 1: Create Empty Project

```
Railway Dashboard → New Project → Empty Project
Name: "BAHR Staging"
```

### Step 2: Add Backend Service

```
1. Click "+ New" → GitHub Repo → Select BAHR repository

2. Configure the service:
   ┌─────────────────────────────────┐
   │ Settings                        │
   ├─────────────────────────────────┤
   │ Service Name: backend          │
   │                                 │
   │ Root Directory:                 │
   │ ┌─────────────────────────────┐ │
   │ │ backend                     │ │  ← CRITICAL!
   │ └─────────────────────────────┘ │
   │                                 │
   │ ✅ Auto-detected: Python       │
   └─────────────────────────────────┘

3. Railway will use:
   - backend/requirements.txt → Install dependencies
   - backend/Procfile → Build & start commands
```

### Step 3: Add Database Services

```
1. PostgreSQL:
   Click "+ New" → Database → PostgreSQL
   Result: DATABASE_URL automatically created

2. Redis:
   Click "+ New" → Database → Redis
   Result: REDIS_URL automatically created
```

### Step 4: Set Backend Variables

```
Backend Service → Variables → Add:

┌────────────────────────────────────────────┐
│ PROJECT_NAME          = BAHR API           │
│ SECRET_KEY            = <generate>         │
│ DATABASE_URL          = ${{Postgres.DB}}   │
│ REDIS_URL             = ${{Redis.URL}}     │
│ CORS_ORIGINS          = <backend-url>      │
│ LOG_LEVEL             = INFO               │
│ ENVIRONMENT           = staging            │
└────────────────────────────────────────────┘

Generate SECRET_KEY:
$ openssl rand -hex 32
```

### Step 5: Deploy Backend

```
After adding variables:

Deployment Process:
┌─────────────────────────────────────┐
│ 1. Installing dependencies...       │
│    ✅ pip install -r requirements   │
│                                     │
│ 2. Running release command...       │
│    ✅ alembic upgrade head          │
│    ✅ python scripts/seed_db.py     │
│                                     │
│ 3. Starting server...               │
│    ✅ uvicorn app.main:app          │
│                                     │
│ 🎉 Deployment successful!           │
└─────────────────────────────────────┘

Backend URL: https://bahr-backend-xxx.up.railway.app
```

### Step 6: Add Frontend Service

```
1. Click "+ New" → GitHub Repo → Select BAHR (same repo!)

2. Configure the service:
   ┌─────────────────────────────────┐
   │ Settings                        │
   ├─────────────────────────────────┤
   │ Service Name: frontend         │
   │                                 │
   │ Root Directory:                 │
   │ ┌─────────────────────────────┐ │
   │ │ frontend                    │ │  ← CRITICAL!
   │ └─────────────────────────────┘ │
   │                                 │
   │ ✅ Auto-detected: Next.js      │
   └─────────────────────────────────┘

3. Railway will use:
   - frontend/package.json → Install dependencies
   - Auto-runs: npm ci && npm run build && npm start
```

### Step 7: Set Frontend Variables

```
Frontend Service → Variables → Add:

┌────────────────────────────────────────────────────┐
│ NEXT_PUBLIC_API_URL = <backend-url>/api/v1        │
│ NODE_ENV            = production                   │
└────────────────────────────────────────────────────┘

Use backend URL from Step 5
```

### Step 8: Update Backend CORS

```
Backend Service → Variables → Update:

┌────────────────────────────────────────────────────┐
│ CORS_ORIGINS = <backend-url>,<frontend-url>       │
└────────────────────────────────────────────────────┘

Include both URLs (comma-separated, no spaces)
```

---

## Final Architecture

```
┌──────────────────────────────────────────────────────┐
│                  Railway Project                      │
│                   "BAHR Staging"                      │
├──────────────────────────────────────────────────────┤
│                                                       │
│  ┌────────────────┐      ┌─────────────────┐        │
│  │ Backend Service│◄─────┤   PostgreSQL    │        │
│  │                │      └─────────────────┘        │
│  │ Root: backend  │                                  │
│  │                │      ┌─────────────────┐        │
│  │ Python/FastAPI │◄─────┤     Redis       │        │
│  └────────┬───────┘      └─────────────────┘        │
│           │                                           │
│           │ CORS allows                               │
│           ▼                                           │
│  ┌────────────────┐                                  │
│  │Frontend Service│                                  │
│  │                │                                  │
│  │ Root: frontend │                                  │
│  │                │                                  │
│  │ Next.js        │                                  │
│  └────────────────┘                                  │
│                                                       │
└──────────────────────────────────────────────────────┘

User Request Flow:
1. User visits: https://bahr-frontend-xxx.railway.app
2. Frontend loads in browser
3. User analyzes verse
4. Frontend calls: https://bahr-backend-xxx.railway.app/api/v1/analyze
5. Backend processes request (checks Redis, runs analysis, caches result)
6. Backend returns JSON response
7. Frontend displays results
```

---

## Verification Checklist

```
Backend Service:
☐ Root Directory set to "backend"
☐ Python detected (check build logs)
☐ Procfile used (check deployment logs)
☐ DATABASE_URL linked to Postgres
☐ REDIS_URL linked to Redis
☐ SECRET_KEY generated and set
☐ CORS_ORIGINS includes both URLs
☐ Domain generated
☐ Health endpoint returns 200

Frontend Service:
☐ Root Directory set to "frontend"
☐ Next.js detected (check build logs)
☐ NEXT_PUBLIC_API_URL set correctly
☐ NODE_ENV=production
☐ Build succeeded (check logs)
☐ Domain generated
☐ Homepage loads in browser

Integration:
☐ Frontend can call backend API
☐ CORS allows requests
☐ Analysis endpoint works
☐ Results display in frontend
```

---

## Quick Test Commands

### After Deployment

```bash
# Set your URLs
BACKEND_URL="https://your-backend-url.railway.app"
FRONTEND_URL="https://your-frontend-url.railway.app"

# Test backend
curl $BACKEND_URL/health
# Expected: {"status":"healthy"}

# Test backend API
curl -X POST $BACKEND_URL/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "أَلا لَيتَ الشَبابَ يَعودُ يَوماً"}'
# Expected: JSON with bahr detection

# Test frontend
curl $FRONTEND_URL/
# Expected: HTML (status 200)

# Full verification
BACKEND_URL=$BACKEND_URL \
FRONTEND_URL=$FRONTEND_URL \
./scripts/verify_deployment.sh
```

---

## What Changed vs Original Error

### Before (❌ Failed)
```
Railway tried to build:
- From: /BAHR/ (repository root)
- Found: Multiple projects (backend/, frontend/)
- Result: Confusion → Build failed
```

### After (✅ Success)
```
Backend Service:
- From: /BAHR/backend/
- Found: requirements.txt, Procfile
- Result: Python project → Build succeeded

Frontend Service:
- From: /BAHR/frontend/
- Found: package.json, next.config.ts
- Result: Next.js project → Build succeeded
```

---

## Key Configuration File: Procfile

Located at: `backend/Procfile`

```procfile
web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
release: alembic upgrade head && python scripts/seed_database.py
```

Railway uses this to:
1. **release**: Run migrations and seed data (once before starting)
2. **web**: Start the FastAPI server

---

## Summary

### The Fix in 3 Steps:

1. **Create two services** from the same repository
2. **Set Root Directory** for each:
   - Backend → `backend`
   - Frontend → `frontend`
3. **Configure environment variables** for each service

Railway handles everything else automatically!

---

## Troubleshooting

### "Still can't detect project type"

**Check:**
```
Service Settings → Root Directory
Should show: "backend" or "frontend"
Not: "backend/" or "/backend"
```

### "Module not found errors"

**Solution:**
- Railway runs commands from Root Directory
- Imports work relative to that directory
- Example: `from app.core` works because Railway is in `backend/`

### "Can't connect to database"

**Check:**
```
Backend Variables → DATABASE_URL
Should be: ${{Postgres.DATABASE_URL}}
Not: Hard-coded connection string
```

---

**Need more help?**
- See: `RAILWAY_FIX_ROOT_DIRECTORY.md` (detailed fix guide)
- See: `RAILWAY_DEPLOYMENT_GUIDE.md` (complete deployment guide)
- See: `RAILWAY_ENV_VARIABLES_GUIDE.md` (environment variables)

**You got this! 🚀**
