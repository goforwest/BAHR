# Railway Deployment - Quick Reference Card

> **Quick access guide for common Railway deployment tasks**

## 🚀 Initial Setup (One-Time)

### Backend Configuration

**Railway Variables** (Backend Service → Variables):

```env
SECRET_KEY=0f84f0a54d20cbe3d457d02e396fd69d07f3c9cb6c842cedb40338c7f54c2cc7
CORS_ORIGINS=https://bahr-frontend-production.up.railway.app
PROJECT_NAME=BAHR API
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### Frontend Configuration

**Railway Variables** (Frontend Service → Variables):

```env
NEXT_PUBLIC_API_URL=https://bahr-backend-production.up.railway.app/api/v1
```

---

## 🔍 Quick Verification Commands

### Check Backend Health

```bash
curl https://your-backend-url.railway.app/health
```

**Expected**: `{"status":"healthy",...}`

### Test CORS

```bash
curl -I -X OPTIONS https://backend-url/api/v1/analyze/ \
  -H "Origin: https://frontend-url" \
  -H "Access-Control-Request-Method: POST"
```

**Expected**: `Access-Control-Allow-Origin: https://frontend-url`

### Test Analysis Endpoint

```bash
curl -X POST https://backend-url/api/v1/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"text":"إذا غامَرتَ في شَرَفٍ مَرومِ","detect_bahr":true}'
```

**Expected**: JSON with `taqti3`, `bahr`, `score`

### Run Full Verification Script

```bash
./scripts/verify-deployment.sh \
  https://backend-url.railway.app \
  https://frontend-url.railway.app
```

---

## 🐛 Common Issues & Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| **CORS Error** | Browser console: "blocked by CORS policy" | Backend Variables → Update `CORS_ORIGINS` to include frontend URL → Redeploy |
| **404 Not Found** | Frontend can't reach backend | Frontend Variables → Check `NEXT_PUBLIC_API_URL` has `/api/v1` suffix |
| **Localhost in Production** | API calls go to localhost | Frontend Variables → Add `NEXT_PUBLIC_API_URL` → Redeploy |
| **Backend Crash** | Health check fails | Backend Logs → Check for errors → Fix dependencies/code |
| **Build Failed** | Deployment stuck at "Building" | Check build logs → Fix dependency issues |

---

## 📝 Environment Variable Checklist

### ✅ Backend Must Have:

- [x] `SECRET_KEY` (generated, never default)
- [x] `CORS_ORIGINS` (includes frontend URL)

### ✅ Frontend Must Have:

- [x] `NEXT_PUBLIC_API_URL` (points to backend with `/api/v1`)

### ⚠️ Optional but Recommended:

- [ ] `REDIS_URL` (for caching)
- [ ] `DATABASE_URL` (for persistence)
- [ ] `SENTRY_DSN` (for error tracking)

---

## 🔗 Important URLs

### Backend Endpoints

```
Health Check:        /health
API Docs:           /docs
Analyze V1:         /api/v1/analyze/
Analyze V2:         /api/v1/analyze-v2/ (BAHR v2.0)
Analytics:          /api/v1/analytics/
Metrics:            /metrics
```

### Frontend Pages

```
Home:               /
Analyze:            /analyze
Analytics:          /analytics
API Test:           /test-api
```

---

## 📊 Monitoring

### View Logs

**Backend**:
```
Railway → Backend Service → Logs
Filter: ERROR, CORS, analyze
```

**Frontend**:
```
Railway → Frontend Service → Logs
Filter: build, error, api
```

### Check Metrics

**Railway Dashboard**:
- CPU usage
- Memory usage
- Request count

**Prometheus (Backend)**:
```
curl https://backend-url/metrics
```

---

## 🔄 Redeploy Checklist

When you need to redeploy:

### Backend Changes

1. Push code to GitHub
2. Railway auto-deploys (if enabled)
3. Or manually: Railway → Backend → Deploy

**After code changes**:
- [x] Check logs for startup success
- [x] Test `/health` endpoint
- [x] Verify BAHR v2.0 still works

### Frontend Changes

1. Push code to GitHub
2. Railway auto-deploys
3. Or manually: Railway → Frontend → Deploy

**After code changes**:
- [x] Check build logs
- [x] Test frontend loads
- [x] Verify API calls work

### Environment Variable Changes

**Important**: Changing variables triggers automatic redeploy!

1. Update variable in Railway UI
2. Wait for redeploy (~2-5 minutes)
3. Verify changes took effect

---

## 🆘 Emergency Procedures

### Backend Down

```bash
# 1. Check health
curl https://backend-url/health

# 2. Check Railway status
Railway Dashboard → Backend → Metrics

# 3. View logs
Railway → Backend → Logs (real-time)

# 4. Restart service
Railway → Backend → Settings → Restart

# 5. Redeploy if needed
Railway → Backend → Deploy
```

### Frontend Down

```bash
# 1. Check accessibility
curl https://frontend-url

# 2. Check build logs
Railway → Frontend → Deployments → Latest → Logs

# 3. Verify environment variables
Railway → Frontend → Variables

# 4. Redeploy
Railway → Frontend → Deploy
```

### CORS Suddenly Broken

**Cause**: Backend redeployed without correct CORS_ORIGINS

**Fix**:
1. Railway → Backend → Variables
2. Verify `CORS_ORIGINS` = `https://frontend-url`
3. If wrong: Update → Auto-redeploys
4. Test: `./scripts/verify-deployment.sh`

---

## 🎯 Performance Tuning

### Add Redis Caching

1. Railway → Project → "+ New" → Redis
2. Backend Variables → Add:
   ```
   REDIS_URL=${{Redis.REDIS_URL}}
   ```
3. Redeploy backend
4. Check logs: `✓ Redis connection initialized`

**Impact**: 50-80% faster response times for repeated queries

### Database Persistence

1. Railway → Project → "+ New" → PostgreSQL
2. Backend Variables → Add:
   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   ```
3. Run migrations:
   ```bash
   # In Railway backend terminal or locally:
   alembic upgrade head
   ```

---

## 📞 Support Resources

| Resource | Link |
|----------|------|
| Full Deployment Guide | `RAILWAY_DEPLOYMENT_GUIDE.md` |
| Verification Script | `./scripts/verify-deployment.sh` |
| Backend Config | `backend/.env.example` |
| Frontend Config | `frontend/.env.production.example` |
| Railway Docs | https://docs.railway.app |
| BAHR v2.0 Info | `DETECTOR_V2_SUMMARY.md` |

---

## ✅ Success Indicators

Your deployment is working correctly if:

- ✅ Backend health check returns `{"status":"healthy"}`
- ✅ Frontend loads at deployed URL
- ✅ Analysis page successfully analyzes verses
- ✅ No CORS errors in browser console
- ✅ BAHR v2.0 returns `transformations` in response
- ✅ Verification script shows "6/6 tests passed"

---

**Last Updated**: 2025-11-12
**For detailed instructions**: See `RAILWAY_DEPLOYMENT_GUIDE.md`
