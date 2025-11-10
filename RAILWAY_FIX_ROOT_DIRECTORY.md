# Railway Deployment Fix - Root Directory Configuration

## Problem: "Nixpacks was unable to generate a build plan"

Railway failed because it tried to build from the repository root, which contains both `backend/` and `frontend/` directories. Railway's Nixpacks couldn't determine which one to build.

---

## Solution: Configure Root Directory for Each Service

Railway needs to deploy **two separate services** from the same repository, each with its own root directory.

---

## Step-by-Step Fix

### 1. Delete the Failed Service (if exists)

1. Go to Railway Dashboard
2. If you see a failed service, click on it
3. Settings → Danger → Delete Service

### 2. Create Backend Service

1. Click **"+ New"** in your Railway project
2. Select **"GitHub Repo"**
3. Choose your BAHR repository
4. Railway creates the service

**Configure Backend:**
1. Click on the new service
2. Go to **Settings**
3. Scroll to **Service Settings**
4. Find **Root Directory**
5. **Enter: `backend`** (without slashes)
6. Click outside to save

Railway will now:
- Build from `backend/` directory
- Detect Python automatically
- Use `backend/Procfile` for build/start commands

### 3. Add PostgreSQL

1. Click **"+ New"**
2. Select **Database → PostgreSQL**
3. Railway provisions database
4. `DATABASE_URL` variable auto-created

### 4. Add Redis

1. Click **"+ New"**
2. Select **Database → Redis**
3. Railway provisions Redis
4. `REDIS_URL` variable auto-created

### 5. Set Backend Environment Variables

Click on Backend Service → Variables → Add variables:

```bash
PROJECT_NAME=BAHR API
API_VERSION=1.0.0
SECRET_KEY=YOUR_GENERATED_SECRET_HERE
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
LOG_LEVEL=INFO
ENVIRONMENT=staging
CACHE_TTL=86400
DATABASE_ECHO=false
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600
MAINTENANCE_MODE=false
```

**Generate SECRET_KEY locally:**
```bash
openssl rand -hex 32
```

### 6. Deploy Backend

1. Backend will automatically deploy after setting variables
2. Watch the deployment logs
3. Should see:
   - ✅ Dependencies installed
   - ✅ Migrations run (`alembic upgrade head`)
   - ✅ Database seeded (`python scripts/seed_database.py`)
   - ✅ Server started

### 7. Get Backend URL

1. Backend Service → Settings → Networking
2. Click **"Generate Domain"**
3. Copy URL (e.g., `https://bahr-backend-production.up.railway.app`)
4. Save for next step

### 8. Update Backend CORS (First Pass)

1. Backend Service → Variables
2. Add/Update:
   ```
   CORS_ORIGINS=https://your-backend-url.railway.app
   ```
3. We'll add frontend URL after it's deployed

### 9. Create Frontend Service

1. Click **"+ New"** in Railway project
2. Select **"GitHub Repo"**
3. Choose the SAME BAHR repository
4. Railway creates another service

**Configure Frontend:**
1. Click on the new service
2. Rename it to "frontend" (Settings → Service Name)
3. Go to **Settings**
4. Scroll to **Service Settings**
5. Find **Root Directory**
6. **Enter: `frontend`** (without slashes)
7. Click outside to save

Railway will now:
- Build from `frontend/` directory
- Detect Next.js automatically
- Run `npm ci && npm run build && npm start`

### 10. Set Frontend Environment Variables

Click on Frontend Service → Variables → Add variables:

```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app/api/v1
NODE_ENV=production
```

Replace `your-backend-url` with the actual URL from Step 7.

### 11. Deploy Frontend

1. Frontend will automatically deploy
2. Watch deployment logs
3. Should see:
   - ✅ Dependencies installed
   - ✅ Next.js build succeeded
   - ✅ Server started

### 12. Get Frontend URL

1. Frontend Service → Settings → Networking
2. Click **"Generate Domain"**
3. Copy URL (e.g., `https://bahr-frontend-production.up.railway.app`)

### 13. Update Backend CORS (Final)

1. Go back to Backend Service → Variables
2. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-backend-url.railway.app,https://your-frontend-url.railway.app
   ```
3. Backend will redeploy automatically

---

## Verify Deployment

### Quick Health Check

**Backend:**
```bash
curl https://your-backend-url.railway.app/health
# Expected: {"status":"healthy"}
```

**Frontend:**
```bash
curl https://your-frontend-url.railway.app/
# Expected: HTML with status 200
```

### Full Verification

```bash
BACKEND_URL=https://your-backend-url.railway.app \
FRONTEND_URL=https://your-frontend-url.railway.app \
./scripts/verify_deployment.sh
```

---

## Visual Service Structure

After setup, your Railway project should have:

```
BAHR Project
├── Backend Service
│   ├── Root Directory: backend
│   ├── Variables: DATABASE_URL, REDIS_URL, SECRET_KEY, etc.
│   └── Domain: https://bahr-backend-xxx.up.railway.app
│
├── Frontend Service
│   ├── Root Directory: frontend
│   ├── Variables: NEXT_PUBLIC_API_URL, NODE_ENV
│   └── Domain: https://bahr-frontend-xxx.up.railway.app
│
├── PostgreSQL
│   └── DATABASE_URL → linked to Backend
│
└── Redis
    └── REDIS_URL → linked to Backend
```

---

## Common Issues After Fix

### Issue: Backend still won't build

**Check:**
1. Root Directory is exactly `backend` (no `/backend` or `backend/`)
2. Railway dashboard shows "Root Directory: backend"
3. Redeploy: Settings → Redeploy

### Issue: Module import errors

**Solution:**
- Railway runs from `backend/` directory
- Imports like `from app.core import` work correctly
- If errors persist, check `backend/requirements.txt`

### Issue: Migrations don't run

**Check deployment logs:**
- Should see: "Running release command: alembic upgrade head && python scripts/seed_database.py"
- If not, verify `backend/Procfile` exists with correct content

### Issue: Frontend can't reach backend

**Check:**
1. `NEXT_PUBLIC_API_URL` includes `/api/v1`
2. Backend URL is correct (test with curl)
3. CORS includes frontend URL
4. Both services are deployed and healthy

---

## Key Takeaway

**The root cause:** Railway needs explicit Root Directory configuration for monorepo projects.

**The fix:**
- Backend service → Root Directory = `backend`
- Frontend service → Root Directory = `frontend`

This tells Railway exactly which part of the repository to build for each service.

---

## Next Steps

After successful deployment:

1. ✅ Run verification script
2. ✅ Test analyze endpoint
3. ✅ Test frontend UI
4. ✅ Share URLs with team
5. ✅ Monitor logs for errors

---

## Need Help?

- **Deployment Guide**: See `RAILWAY_DEPLOYMENT_GUIDE.md`
- **Environment Variables**: See `RAILWAY_ENV_VARIABLES_GUIDE.md`
- **Quick Reference**: See `DEPLOYMENT_QUICK_REFERENCE.md`

---

**You're now ready to deploy! 🚀**

The key is setting the Root Directory for each service. Railway will handle the rest automatically.
