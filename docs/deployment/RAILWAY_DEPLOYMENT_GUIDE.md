# Railway Deployment Guide - BAHR Platform

> **Status**: Configuration files ready ✅
> **Goal**: Deploy frontend and backend to Railway with proper environment configuration
> **Time**: ~20 minutes (excluding build time)

## Prerequisites

- [x] GitHub repository with BAHR code
- [x] Railway account (sign up at [railway.app](https://railway.app))
- [x] Configuration files created (`.env` files in this commit)

## Overview

This guide walks you through deploying the BAHR Arabic Poetry Analysis Platform to Railway with proper frontend-backend connectivity.

### Architecture After Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                    Railway Deployment                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Frontend Service                                           │
│  ├─ Domain: bahr-frontend-production.up.railway.app        │
│  ├─ Framework: Next.js 16                                  │
│  ├─ Env: NEXT_PUBLIC_API_URL → Backend URL                 │
│  └─ Port: 3000 (auto-configured)                           │
│                      │                                       │
│                      │ HTTPS POST /api/v1/analyze/          │
│                      ▼                                       │
│  Backend Service                                            │
│  ├─ Domain: bahr-backend-production.up.railway.app         │
│  ├─ Framework: FastAPI (Python)                            │
│  ├─ Env: CORS_ORIGINS → Frontend URL                       │
│  ├─ Env: SECRET_KEY → Generated secure key                 │
│  └─ Port: Assigned by Railway ($PORT)                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Part 1: Deploy Backend (15 minutes)

### Step 1.1: Create Railway Project

1. **Login to Railway**: [https://railway.app](https://railway.app)
2. **New Project**:
   - Click "+ New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Select repository: `goforwest/BAHR`

### Step 1.2: Configure Backend Service

3. **Select Backend Directory**:
   - Railway will detect multiple services
   - Click "Add Service" → Select "backend"
   - Or manually configure:
     - Settings → Root Directory → `/backend`

4. **Configure Build**:
   - Railway auto-detects Python (via `nixpacks.toml`)
   - Verify build command: Uses `nixpacks.toml` configuration
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     (This is already configured in `backend/.railway.json`)

### Step 1.3: Set Backend Environment Variables

5. **Add Environment Variables**:
   - Railway Dashboard → Backend Service → **Variables** tab
   - Click "+ New Variable"

   Add the following variables:

   | Variable Name | Value | Notes |
   |--------------|-------|-------|
   | `SECRET_KEY` | `0f84f0a54d20cbe3d457d02e396fd69d07f3c9cb6c842cedb40338c7f54c2cc7` | Already generated ✅ |
   | `CORS_ORIGINS` | `http://localhost:3000` | Temporary - will update after frontend deploy |
   | `PROJECT_NAME` | `BAHR API` | Optional |
   | `LOG_LEVEL` | `INFO` | Optional |
   | `ENVIRONMENT` | `production` | Optional |

   > **Note**: We'll update `CORS_ORIGINS` in Step 2.6 after frontend is deployed

### Step 1.4: Deploy Backend

6. **Trigger Deployment**:
   - Click "Deploy" button (Railway auto-deploys on variable changes)
   - Wait for build to complete (~5-10 minutes)

7. **Monitor Build Logs**:
   - Click "View Logs" to watch deployment
   - Look for:
     ```
     ✓ Installing Python dependencies
     ✓ Installing requirements/base.txt
     ✓ Building complete
     ✓ Application startup complete
     ```

### Step 1.5: Get Backend URL

8. **Copy Backend URL**:
   - Railway Dashboard → Backend Service → **Settings** → **Domains**
   - Railway generates a domain like:
     ```
     https://bahr-backend-production.up.railway.app
     ```
   - **SAVE THIS URL** - you'll need it for frontend configuration!

### Step 1.6: Verify Backend Health

9. **Test Health Endpoint**:
   ```bash
   # Replace with your actual backend URL
   curl https://bahr-backend-production.up.railway.app/health
   ```

   **Expected Response**:
   ```json
   {
     "status": "healthy",
     "timestamp": 1699999999.999,
     "version": "1.0.0"
   }
   ```

   ✅ **If you see this, backend is live!**

---

## Part 2: Deploy Frontend (10 minutes)

### Step 2.1: Add Frontend Service

1. **Add Another Service**:
   - Same Railway Project → "+ New" → "Service"
   - Deploy from same GitHub repo
   - Or create new project (recommended for separate management)

### Step 2.2: Configure Frontend Service

2. **Select Frontend Directory**:
   - Settings → Root Directory → `/frontend`

3. **Configure Build** (auto-detected by Railway):
   - Build command: `npm run build`
   - Start command: `npm start`
   - Port: 3000 (default Next.js)

### Step 2.3: Set Frontend Environment Variables

4. **Add Critical Environment Variable**:
   - Railway Dashboard → Frontend Service → **Variables** tab
   - Add variable:

   | Variable Name | Value |
   |--------------|-------|
   | `NEXT_PUBLIC_API_URL` | `https://bahr-backend-production.up.railway.app/api/v1` |

   > **IMPORTANT**: Replace with YOUR actual backend URL from Step 1.5!

   **Example**:
   ```
   NEXT_PUBLIC_API_URL=https://bahr-backend-production-abc123.up.railway.app/api/v1
   ```

   ⚠️ **Common Mistake**: Don't forget `/api/v1` suffix!

### Step 2.4: Deploy Frontend

5. **Trigger Deployment**:
   - Click "Deploy"
   - Wait for build (~3-5 minutes)

6. **Monitor Build Logs**:
   ```
   ✓ Installing dependencies (npm install)
   ✓ Building Next.js app (npm run build)
   ✓ Optimizing production build
   ✓ Starting server (npm start)
   ```

### Step 2.5: Get Frontend URL

7. **Copy Frontend URL**:
   - Railway Dashboard → Frontend Service → Settings → Domains
   - Example:
     ```
     https://bahr-frontend-production.up.railway.app
     ```
   - **SAVE THIS URL** - you'll need it for backend CORS configuration!

### Step 2.6: Update Backend CORS Configuration

8. **Add Frontend URL to Backend CORS**:
   - Go back to: Railway Dashboard → **Backend Service** → Variables
   - Find `CORS_ORIGINS` variable
   - Update value to:
     ```
     https://bahr-frontend-production.up.railway.app
     ```

   Or if you have multiple domains:
   ```
   https://bahr-frontend-production.up.railway.app,https://www.your-custom-domain.com
   ```

9. **Redeploy Backend**:
   - Changing variables triggers auto-redeploy
   - Wait ~1-2 minutes for backend to restart

---

## Part 3: Verification (5 minutes)

### Step 3.1: Test Frontend Access

1. **Open Frontend URL**:
   ```
   https://bahr-frontend-production.up.railway.app
   ```

2. **Check Browser Console**:
   - Open Developer Tools (F12)
   - Console tab
   - Run:
     ```javascript
     console.log(process.env.NEXT_PUBLIC_API_URL)
     ```

   **Expected Output**:
   ```
   https://bahr-backend-production.up.railway.app/api/v1
   ```

   ✅ **If correct**: Environment variable is set!
   ❌ **If localhost or undefined**: Redeploy frontend

### Step 3.2: Test Backend Connection

3. **Navigate to Analyze Page**:
   ```
   https://your-frontend-url.railway.app/analyze
   ```

4. **Test Analysis**:
   - Enter verse: `إذا غامَرتَ في شَرَفٍ مَرومِ`
   - Click "تحليل" (Analyze)

5. **Check Network Tab**:
   - Developer Tools → Network tab
   - Look for `POST /analyze/` request
   - Click on request → Headers tab

   **Expected**:
   - Status: `200 OK` ✅
   - Request URL: `https://backend.../api/v1/analyze/`
   - Response: JSON with `taqti3`, `bahr`, `score`

   **Common Issues**:
   - Status `0` (Failed) + CORS error → Backend CORS not configured
   - Status `404` → Wrong API URL in frontend
   - Timeout → Backend crashed, check logs

### Step 3.3: Test BAHR v2.0 Endpoint

6. **Test Enhanced Endpoint** (optional):
   ```bash
   curl -X POST https://your-backend-url.railway.app/api/v1/analyze-v2/ \
     -H "Content-Type: application/json" \
     -H "Origin: https://your-frontend-url.railway.app" \
     -d '{
       "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
       "detect_bahr": true,
       "suggest_corrections": true
     }'
   ```

   **Expected Response** (should include explainability):
   ```json
   {
     "bahr": {
       "name_ar": "الطويل",
       "confidence": 0.95,
       "match_quality": "strong",
       "transformations": ["base", "قبض", "base"],
       "explanation_ar": "مطابقة مع زحافات: قبض"
     }
   }
   ```

### Step 3.4: Check Backend Logs

7. **Verify No CORS Errors**:
   - Railway Dashboard → Backend Service → Logs
   - Look for successful requests:
     ```
     → POST /api/v1/analyze/ Origin: https://frontend...
     ← POST /api/v1/analyze/ Status: 200
     ```

   ❌ **If you see**: CORS errors or rejected requests
   → Double-check `CORS_ORIGINS` includes exact frontend URL

---

## Part 4: Optional Enhancements

### Add Redis for Caching (Optional)

1. **Add Redis Service**:
   - Railway Dashboard → "+ New" → "Database" → "Redis"
   - Railway creates Redis instance automatically

2. **Connect to Backend**:
   - Backend Service → Variables → "+ New Variable"
   - Name: `REDIS_URL`
   - Value: `${{Redis.REDIS_URL}}` (Railway magic variable)

3. **Redeploy Backend**:
   - Backend will now use Redis for caching
   - Check logs for: `✓ Redis connection initialized`

### Add PostgreSQL for Persistence (Optional)

1. **Add PostgreSQL Service**:
   - Railway → "+ New" → "Database" → "PostgreSQL"

2. **Connect to Backend**:
   - Backend Variables → `DATABASE_URL` = `${{Postgres.DATABASE_URL}}`

3. **Run Migrations**:
   ```bash
   # In Railway backend service terminal or locally:
   alembic upgrade head
   ```

### Add Custom Domain (Optional)

1. **Frontend Custom Domain**:
   - Frontend Service → Settings → Domains
   - Click "+ Add Domain"
   - Enter: `www.your-domain.com`
   - Update DNS records as instructed

2. **Update Backend CORS**:
   - Add custom domain to `CORS_ORIGINS`:
     ```
     https://bahr-frontend.railway.app,https://www.your-domain.com
     ```

---

## Troubleshooting

### Issue: Frontend shows "Connection Refused"

**Symptoms**: Network tab shows failed requests, status 0

**Solution**:
1. Check `NEXT_PUBLIC_API_URL` is set in Railway frontend variables
2. Verify backend URL is correct (with `/api/v1` suffix)
3. Redeploy frontend after adding variable

**Verification**:
```javascript
// In browser console:
console.log(process.env.NEXT_PUBLIC_API_URL)
// Must show: https://backend-url.railway.app/api/v1
```

---

### Issue: CORS Error in Browser Console

**Symptoms**:
```
Access to XMLHttpRequest at 'https://backend...' from origin 'https://frontend...'
has been blocked by CORS policy
```

**Solution**:
1. Backend Service → Variables
2. Update `CORS_ORIGINS` to include exact frontend URL
3. Redeploy backend

**Verification**:
```bash
curl -I -X OPTIONS https://backend-url.railway.app/api/v1/analyze/ \
  -H "Origin: https://frontend-url.railway.app"

# Look for response header:
# Access-Control-Allow-Origin: https://frontend-url.railway.app
```

---

### Issue: Backend Build Fails

**Symptoms**: Build logs show dependency errors

**Common Causes**:
1. Missing dependencies in `requirements/base.txt`
2. Python version mismatch
3. CAMeL Tools installation issues (M1/M2 Macs)

**Solution**:
- Check `backend/nixpacks.toml` for Python version
- Review build logs for specific error
- Ensure `runtime.txt` specifies correct Python version

---

### Issue: Frontend Shows Localhost URL in Production

**Symptoms**: API calls go to `http://localhost:8000`

**Solution**:
1. Verify `NEXT_PUBLIC_API_URL` is set in Railway
2. **Important**: Must set BEFORE build (not after)
3. Redeploy frontend to trigger new build

**Note**: Next.js bakes environment variables at BUILD TIME, not runtime!

---

## Monitoring & Maintenance

### Health Checks

**Backend Health**:
```bash
curl https://your-backend-url.railway.app/health
```

**Detailed Health** (includes BAHR v2.0 status):
```bash
curl https://your-backend-url.railway.app/health/detailed
```

### View Logs

**Railway Dashboard**:
- Backend Service → Logs → Real-time logs
- Frontend Service → Logs → Build and runtime logs

**Filter Logs**:
- Search for: `ERROR`, `CORS`, `analyze`, `BAHR`

### Performance Monitoring

**Railway Metrics** (in dashboard):
- CPU usage
- Memory usage
- Request count
- Response times

---

## Summary Checklist

After completing this guide, you should have:

- [x] ✅ Backend deployed to Railway
- [x] ✅ Frontend deployed to Railway
- [x] ✅ `NEXT_PUBLIC_API_URL` set in frontend
- [x] ✅ `CORS_ORIGINS` set in backend
- [x] ✅ `SECRET_KEY` configured
- [x] ✅ Health endpoint responding
- [x] ✅ Frontend can reach backend
- [x] ✅ Analysis functionality working
- [x] ✅ BAHR v2.0 meter detection operational

### Quick Reference

**Backend URL Format**:
```
https://bahr-backend-production.up.railway.app
```

**Frontend Environment Variable**:
```
NEXT_PUBLIC_API_URL=https://bahr-backend-production.up.railway.app/api/v1
```

**Backend CORS Configuration**:
```
CORS_ORIGINS=https://bahr-frontend-production.up.railway.app
```

---

## Next Steps

1. **Test Thoroughly**: Try different verses, check all features
2. **Add Monitoring**: Set up Sentry for error tracking (optional)
3. **Add Redis**: For better performance with caching
4. **Custom Domain**: Point your domain to Railway deployment
5. **CI/CD**: Enable auto-deploy on git push

---

## Support

**Issues?**
- Check Railway logs first
- Review this troubleshooting guide
- Verify all environment variables are set
- Test health endpoints

**BAHR v2.0 Verification**:
```bash
# Test that BAHR v2.0 is working:
curl -X POST https://backend-url/api/v1/analyze-v2/ \
  -H "Content-Type: application/json" \
  -d '{"text":"إذا غامَرتَ في شَرَفٍ مَرومِ","detect_bahr":true}'

# Should return meter detection with transformations
```

---

**Deployment Complete!** 🎉

Your BAHR platform is now live with full frontend-backend connectivity and BAHR v2.0 Zihafat Rules Engine operational.
