# BAHR Platform - Quick Deployment Reference

## Railway Deployment Quick Start

### 1. Initial Setup (One-time)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project (or use dashboard)
railway init
```

### 2. Deploy Backend

**Via Railway Dashboard:**
1. New Project → Deploy from GitHub
2. Add PostgreSQL service
3. Add Redis service
4. Set root directory: `backend`
5. Add environment variables (see below)
6. Deploy!

**Environment Variables (Backend):**
```bash
PROJECT_NAME=BAHR API
API_VERSION=1.0.0
SECRET_KEY=<generate with: openssl rand -hex 32>
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
CORS_ORIGINS=<your-frontend-url>,<your-backend-url>
ENVIRONMENT=staging
LOG_LEVEL=INFO
CACHE_TTL=86400
```

### 3. Deploy Frontend

**Via Railway Dashboard:**
1. Add new service from same repo
2. Set root directory: `frontend`
3. Add environment variables (see below)
4. Deploy!

**Environment Variables (Frontend):**
```bash
NEXT_PUBLIC_API_URL=<your-backend-url>/api/v1
NODE_ENV=production
```

### 4. Verify Deployment

```bash
# Quick health check
./scripts/health_check.sh https://your-backend.railway.app https://your-frontend.railway.app

# Full verification
BACKEND_URL=https://your-backend.railway.app \
FRONTEND_URL=https://your-frontend.railway.app \
./scripts/verify_deployment.sh
```

### 5. Test the Platform

**Backend API:**
```bash
# Health check
curl https://your-backend.railway.app/health

# Test analysis
curl -X POST https://your-backend.railway.app/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "أَلا لَيتَ الشَبابَ يَعودُ يَوماً"}'
```

**Frontend:**
- Visit: `https://your-frontend.railway.app`
- Test: `https://your-frontend.railway.app/analyze`

---

## Files Created for Deployment

### Backend Files
- ✅ `backend/Procfile` - Process definition
- ✅ `backend/nixpacks.toml` - Build configuration
- ✅ `backend/.env.example` - Environment template

### Frontend Files
- ✅ `frontend/.env.production.example` - Production env template

### Configuration
- ✅ `railway.toml` - Railway project configuration

### Documentation
- ✅ `RAILWAY_DEPLOYMENT_GUIDE.md` - Complete deployment guide
- ✅ `DEPLOYMENT_QUICK_REFERENCE.md` - This file

### Scripts
- ✅ `scripts/verify_deployment.sh` - Full deployment verification
- ✅ `scripts/health_check.sh` - Quick health check

---

## Common Commands

### Railway CLI

```bash
# View logs
railway logs --service backend
railway logs --service frontend

# Run migrations
railway run --service backend alembic upgrade head

# Seed database
railway run --service backend python scripts/seed_database.py

# Connect to database
railway connect postgres

# View environment variables
railway variables --service backend
```

### Local Testing Before Deploy

```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev

# Run tests
cd backend
pytest tests/ -v
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] Code pushed to GitHub
- [ ] Tests passing locally
- [ ] Environment variables documented
- [ ] Database migrations created
- [ ] Seed data prepared

### Backend Deployment
- [ ] PostgreSQL service added
- [ ] Redis service added
- [ ] Environment variables configured
- [ ] CORS origins set correctly
- [ ] Backend deployed successfully
- [ ] Health check passing
- [ ] Database migrated
- [ ] Meters seeded (16 total)

### Frontend Deployment
- [ ] API URL configured
- [ ] Frontend built successfully
- [ ] Frontend deployed
- [ ] Can access homepage
- [ ] Can access /analyze page
- [ ] Arabic text displays correctly

### Post-Deployment
- [ ] Full verification script passed
- [ ] CORS working (frontend → backend)
- [ ] Analysis endpoint functional
- [ ] Caching working (Redis)
- [ ] Logs clean (no errors)
- [ ] URLs shared with team

---

## Troubleshooting Quick Fixes

### Backend won't start
```bash
# Check logs
railway logs --service backend

# Verify DATABASE_URL is set
railway variables --service backend | grep DATABASE_URL

# Manually run migrations
railway run --service backend alembic upgrade head
```

### Frontend can't connect to backend
```bash
# Check NEXT_PUBLIC_API_URL
railway variables --service frontend

# Update CORS on backend
railway variables --service backend
# Add frontend URL to CORS_ORIGINS

# Redeploy backend
railway up --service backend
```

### Database empty (no meters)
```bash
# Seed database
railway run --service backend python scripts/seed_database.py

# Verify
railway connect postgres
SELECT COUNT(*) FROM meters;
# Should return 16
```

### Redis not caching
```bash
# Check Redis URL
railway variables --service backend | grep REDIS_URL

# Check Redis service running
railway status

# Test connection
railway run --service backend python -c "import redis; r = redis.from_url('$REDIS_URL'); print(r.ping())"
```

---

## URLs Template

**Save your deployment URLs:**

```
Backend:
- URL: https://bahr-backend-production-xxxx.up.railway.app
- Health: https://bahr-backend-production-xxxx.up.railway.app/health
- Docs: https://bahr-backend-production-xxxx.up.railway.app/docs

Frontend:
- URL: https://bahr-frontend-production-xxxx.up.railway.app
- Analyze: https://bahr-frontend-production-xxxx.up.railway.app/analyze

Database:
- PostgreSQL: [connection string from Railway]
- Redis: [connection string from Railway]
```

---

## Next Steps After Deployment

1. **Test thoroughly** using verification script
2. **Share URLs** with beta testers
3. **Monitor logs** for errors
4. **Set up monitoring** (optional: Sentry, LogRocket)
5. **Collect feedback** from users
6. **Iterate** based on feedback
7. **Plan production** deployment

---

## Support Resources

- Railway Docs: https://docs.railway.app
- BAHR Full Guide: `RAILWAY_DEPLOYMENT_GUIDE.md`
- Deployment Scripts: `scripts/` directory
- GitHub Issues: [your-repo]/issues

---

**Quick Access:**
- Full Guide: `RAILWAY_DEPLOYMENT_GUIDE.md` (comprehensive)
- This Reference: `DEPLOYMENT_QUICK_REFERENCE.md` (quick commands)
- Verification: `scripts/verify_deployment.sh` (test deployment)
- Health Check: `scripts/health_check.sh` (simple status)
