# BAHR Platform - Railway Deployment Guide

## Complete Step-by-Step Deployment to Railway Staging Environment

This guide provides detailed instructions for deploying the BAHR platform to Railway for beta testing.

---

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your BAHR code pushed to GitHub
3. **Railway CLI** (optional but recommended):
   ```bash
   npm install -g @railway/cli
   railway login
   ```

---

## Part 1: Backend Deployment

### Step 1: Create Railway Project

1. Log in to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Select **"Empty Project"** (not "Deploy from GitHub repo" - we'll add services manually)
4. Name your project: "BAHR Staging" or similar

### Step 2: Add PostgreSQL Database

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database" → "PostgreSQL"**
3. Railway will provision a PostgreSQL instance
4. The `DATABASE_URL` environment variable will be automatically added

### Step 3: Add Redis

1. Click **"+ New"** again
2. Select **"Database" → "Redis"**
3. Railway will provision a Redis instance
4. The `REDIS_URL` environment variable will be automatically added

### Step 4: Add Backend Service

1. In your Railway project, click **"+ New"**
2. Select **"GitHub Repo"**
3. Choose your BAHR repository
4. Railway will create a service

### Step 5: Configure Backend Service

1. Click on the backend service you just created
2. Go to **"Settings"** tab
3. **IMPORTANT:** Set **Root Directory** = `backend`
   - This tells Railway to build from the backend folder
4. Railway will auto-detect Python and use Nixpacks
5. The `Procfile` in `backend/` will be used automatically:
   - Build: Dependencies from `requirements.txt`
   - Release: `alembic upgrade head && python scripts/seed_database.py`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 6: Set Backend Environment Variables

Go to **"Variables"** tab and add:

```bash
# Application Settings
PROJECT_NAME=BAHR API
API_VERSION=1.0.0
ANALYSIS_ENGINE_VERSION=1.0.0
LOG_LEVEL=INFO
ENVIRONMENT=staging

# Security - Generate a secure secret key
SECRET_KEY=<run: openssl rand -hex 32>

# CORS - Will update after frontend is deployed
CORS_ORIGINS=https://your-backend-url.railway.app,https://your-frontend-url.railway.app

# Database (Auto-populated by Railway PostgreSQL)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (Auto-populated by Railway Redis)
REDIS_URL=${{Redis.REDIS_URL}}

# Cache Settings
CACHE_TTL=86400

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600

# Maintenance
MAINTENANCE_MODE=false
```

**To generate SECRET_KEY locally:**
```bash
openssl rand -hex 32
```

### Step 7: Deploy Backend

1. After setting environment variables, Railway will automatically deploy
2. Or click **"Deploy"** to manually trigger deployment
2. Railway will:
   - Build the backend
   - Run `alembic upgrade head` (create database schema)
   - Run `python scripts/seed_database.py` (seed 16 meters)
   - Start the FastAPI server

### Step 8: Get Backend URL

1. Go to **"Settings" → "Networking"**
2. Click **"Generate Domain"**
3. Copy the generated URL (e.g., `https://bahr-backend-production.up.railway.app`)
4. Save this for frontend configuration

### Step 9: Verify Backend Deployment

```bash
# Health check
curl https://your-backend-url.railway.app/health

# Expected response:
# {"status":"healthy"}

# API docs
curl https://your-backend-url.railway.app/docs
# Should return Swagger UI HTML

# Test analyze endpoint
curl -X POST https://your-backend-url.railway.app/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "أَلا لَيتَ الشَبابَ يَعودُ يَوماً"}'

# Expected: JSON response with bahr detection
```

---

## Part 2: Frontend Deployment

### Step 1: Create Frontend Service

1. In the same Railway project, click **"+ New"**
2. Select **"GitHub Repo"** and choose the same repository
3. Railway will create a new service

### Step 2: Configure Frontend Service

1. Click on the frontend service you just created
2. Go to **"Settings"** tab
3. **IMPORTANT:** Set **Root Directory** = `frontend`
   - This tells Railway to build from the frontend folder
4. Railway will auto-detect Next.js and configure automatically:
   - Build: `npm ci && npm run build`
   - Start: `npm start`

### Step 3: Set Frontend Environment Variables

Go to **"Variables"** tab and add:

```bash
# Backend API URL (use the URL from Backend Step 7)
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app/api/v1

# Node Environment
NODE_ENV=production
```

### Step 4: Deploy Frontend

1. Click **"Deploy"** or push changes
2. Railway will:
   - Install dependencies
   - Build Next.js app
   - Start the production server

### Step 5: Get Frontend URL

1. Go to **"Settings" → "Networking"**
2. Click **"Generate Domain"**
3. Copy the generated URL (e.g., `https://bahr-frontend-production.up.railway.app`)

### Step 6: Update Backend CORS

1. Go back to **Backend Service → Variables**
2. Update `CORS_ORIGINS` to include frontend URL:
   ```
   CORS_ORIGINS=https://your-backend-url.railway.app,https://your-frontend-url.railway.app
   ```
3. Redeploy backend if necessary

### Step 7: Verify Frontend Deployment

Visit in browser:
```
https://your-frontend-url.railway.app
```

You should see:
- Arabic text displayed correctly (RTL)
- BAHR logo and title
- "تحليل الشعر" button

Test the analyze functionality:
1. Go to `/analyze` page
2. Enter a verse: `أَلا لَيتَ الشَبابَ يَعودُ يَوماً`
3. Click "حلّل"
4. Should see bahr detection results

---

## Part 3: Database Management

### Running Migrations

If you need to run migrations manually:

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. Link to your project:
   ```bash
   railway link
   ```

3. Run migration:
   ```bash
   railway run --service backend alembic upgrade head
   ```

### Seeding Database

To re-seed the database:

```bash
railway run --service backend python scripts/seed_database.py
```

### Database Access

To access PostgreSQL directly:

```bash
railway connect postgres
```

Or get connection string:
```bash
railway variables --service postgres
```

---

## Part 4: Monitoring & Troubleshooting

### View Logs

**Via Dashboard:**
1. Click on service (backend or frontend)
2. Go to **"Deployments"** tab
3. Click on latest deployment
4. View real-time logs

**Via CLI:**
```bash
# Backend logs
railway logs --service backend

# Frontend logs
railway logs --service frontend
```

### Health Checks

**Backend Health Check:**
```bash
curl https://your-backend-url.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-10T12:00:00Z",
  "version": "1.0.0"
}
```

**Frontend Health Check:**
```bash
curl https://your-frontend-url.railway.app/
```

Should return HTML with status 200.

### Common Issues

#### Issue: Database connection failed
**Solution:**
- Verify `DATABASE_URL` is set correctly
- Check PostgreSQL service is running
- Check service linking in Railway dashboard

#### Issue: Redis connection timeout
**Solution:**
- Verify `REDIS_URL` is set correctly
- Check Redis service is running
- Ensure services are in the same Railway project

#### Issue: CORS errors in browser
**Solution:**
- Verify `CORS_ORIGINS` includes both frontend and backend URLs
- Use HTTPS URLs (Railway provides HTTPS by default)
- Redeploy backend after updating CORS settings

#### Issue: Migrations not running
**Solution:**
- Check start command includes `alembic upgrade head`
- View logs for migration errors
- Manually run migrations via Railway CLI

#### Issue: Meters not seeded
**Solution:**
- Check seed script output in logs
- Manually run: `railway run --service backend python scripts/seed_database.py`
- Verify database connection

---

## Part 5: Environment URLs & Credentials

### Staging Environment URLs

After deployment, you'll have:

**Backend:**
- URL: `https://bahr-backend-production.up.railway.app`
- API Docs: `https://bahr-backend-production.up.railway.app/docs`
- Health: `https://bahr-backend-production.up.railway.app/health`

**Frontend:**
- URL: `https://bahr-frontend-production.up.railway.app`
- Analyze: `https://bahr-frontend-production.up.railway.app/analyze`

**Database:**
- PostgreSQL: Managed by Railway (connection via `DATABASE_URL`)
- Redis: Managed by Railway (connection via `REDIS_URL`)

### Save These Credentials

Store in your password manager or team documentation:

```
# Backend Service
URL: https://your-backend-url.railway.app
SECRET_KEY: <your-generated-secret>

# Frontend Service  
URL: https://your-frontend-url.railway.app

# Database
PostgreSQL URL: <from Railway dashboard>
Redis URL: <from Railway dashboard>

# Railway Project
Project ID: <from Railway dashboard>
```

---

## Part 6: Testing Checklist

### Backend Tests

- [ ] Health check returns 200: `curl /health`
- [ ] API docs accessible: `curl /docs`
- [ ] Analyze endpoint works: `POST /api/v1/analyze`
- [ ] Database has 16 meters: Query `SELECT COUNT(*) FROM meters;`
- [ ] Redis caching works: Same verse analyzed twice (second faster)
- [ ] CORS allows frontend origin
- [ ] Logs show no errors

### Frontend Tests

- [ ] Homepage loads correctly
- [ ] Arabic text displays RTL
- [ ] Analyze page accessible
- [ ] Can submit verse for analysis
- [ ] Results display correctly
- [ ] Loading states work
- [ ] Error handling works (try invalid input)
- [ ] No console errors in browser

### Integration Tests

- [ ] Frontend can call backend API
- [ ] CORS allows requests
- [ ] Analysis results display in frontend
- [ ] Cache improves response time
- [ ] Multiple verses can be analyzed
- [ ] Results are accurate (test with known verses)

---

## Part 7: Post-Deployment

### Share with Beta Testers

Send them:

**Frontend URL:**
```
https://your-frontend-url.railway.app
```

**Instructions:**
1. Visit the URL
2. Click "تحليل الشعر" or go to `/analyze`
3. Enter an Arabic poetry verse
4. Click "حلّل" to analyze
5. View results (bahr, taqti3, confidence score)

### Collect Feedback

Set up:
- Error monitoring (consider Sentry)
- Analytics (consider Plausible or Google Analytics)
- Feedback form for beta testers
- Issue tracker (GitHub Issues)

### Monitoring

Check regularly:
- Railway dashboard for service health
- Logs for errors
- Database usage
- Redis memory usage
- API response times

---

## Part 8: Scaling & Optimization

### Auto-scaling

Railway automatically scales based on:
- CPU usage
- Memory usage
- Request volume

Configure in **Settings → Resources**

### Cost Optimization

- Free tier: $5 credit/month
- Staging environment: ~$10-20/month
  - Backend: ~$5
  - Frontend: ~$5
  - PostgreSQL: ~$5
  - Redis: ~$5

### Performance Tips

1. **Enable caching**: Already implemented with Redis
2. **Monitor response times**: Use Railway metrics
3. **Optimize database queries**: Add indexes if needed
4. **CDN for frontend**: Consider Cloudflare
5. **Compression**: Enable gzip (Next.js default)

---

## Quick Reference Commands

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

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

# Deploy (if using CLI)
railway up
```

---

## Support

If you encounter issues:

1. Check Railway [documentation](https://docs.railway.app)
2. Review deployment logs
3. Check BAHR project documentation
4. Contact Railway support (if plan includes it)
5. Open GitHub issue in BAHR repo

---

## Summary

You now have:

✅ **Backend deployed** on Railway with:
- FastAPI application running
- PostgreSQL database with migrations applied
- Redis for caching
- 16 classical Arabic meters seeded
- Health checks configured

✅ **Frontend deployed** on Railway with:
- Next.js application built and running
- Connected to backend API
- RTL Arabic support
- Analysis interface ready

✅ **Staging environment** ready for beta testing with:
- Public URLs for both services
- Environment variables configured
- Database and caching operational
- Monitoring and logs available

**Next Steps:**
1. Share URLs with beta testers
2. Monitor performance and errors
3. Collect feedback
4. Iterate based on user testing
5. Plan for production deployment

Good luck with your beta testing! 🚀
