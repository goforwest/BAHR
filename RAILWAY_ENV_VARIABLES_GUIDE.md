# Railway Environment Variables Configuration

## Complete guide for setting up environment variables in Railway dashboard

---

## Backend Service Variables

### Required Variables

Copy these into Railway Dashboard → Backend Service → Variables:

```bash
# Application
PROJECT_NAME=BAHR API
API_VERSION=1.0.0
ANALYSIS_ENGINE_VERSION=1.0.0
ENVIRONMENT=staging
LOG_LEVEL=INFO

# Security (IMPORTANT: Generate a new secret key!)
# Run locally: openssl rand -hex 32
SECRET_KEY=your-generated-secret-key-here-32-bytes-hex

# Database (Auto-populated by Railway when you add PostgreSQL service)
DATABASE_URL=${{Postgres.DATABASE_URL}}
DATABASE_ECHO=false

# Redis (Auto-populated by Railway when you add Redis service)
REDIS_URL=${{Redis.REDIS_URL}}
CACHE_TTL=86400

# CORS (Update with your actual URLs after deployment)
CORS_ORIGINS=https://your-backend-url.railway.app,https://your-frontend-url.railway.app

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600

# Maintenance
MAINTENANCE_MODE=false
```

### How to Set in Railway

1. **Navigate to Backend Service**
   - Go to your Railway project
   - Click on the backend service

2. **Go to Variables Tab**
   - Click "Variables" in the left sidebar

3. **Add Variables**
   - Click "+ New Variable"
   - Enter name and value
   - Click "Add"
   - Repeat for each variable

4. **Use Railway References for Database**
   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   REDIS_URL=${{Redis.REDIS_URL}}
   ```
   Railway will automatically resolve these to the actual connection strings.

---

## Frontend Service Variables

### Required Variables

Copy these into Railway Dashboard → Frontend Service → Variables:

```bash
# Backend API URL (Update with your actual backend URL)
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app/api/v1

# Node Environment
NODE_ENV=production
```

### How to Set in Railway

1. **Navigate to Frontend Service**
   - Go to your Railway project
   - Click on the frontend service

2. **Go to Variables Tab**
   - Click "Variables" in the left sidebar

3. **Add Variables**
   - Click "+ New Variable"
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: Your backend URL + `/api/v1`
   - Click "Add"
   
   - Click "+ New Variable"
   - Name: `NODE_ENV`
   - Value: `production`
   - Click "Add"

---

## Getting Your URLs

### Backend URL

1. Go to Backend Service → Settings → Networking
2. Click "Generate Domain"
3. Copy the URL (e.g., `bahr-backend-production-xxxx.up.railway.app`)
4. Use this for:
   - Frontend's `NEXT_PUBLIC_API_URL` (add `/api/v1`)
   - Backend's `CORS_ORIGINS`

### Frontend URL

1. Go to Frontend Service → Settings → Networking
2. Click "Generate Domain"
3. Copy the URL (e.g., `bahr-frontend-production-xxxx.up.railway.app`)
4. Use this for:
   - Backend's `CORS_ORIGINS`
   - Sharing with beta testers

---

## Step-by-Step Variable Configuration

### Step 1: Generate Secret Key

On your local machine:
```bash
openssl rand -hex 32
```

Copy the output (64-character hex string).

### Step 2: Backend Variables - First Pass

Set these immediately (before first deployment):

```
PROJECT_NAME=BAHR API
API_VERSION=1.0.0
SECRET_KEY=<your-generated-key>
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
LOG_LEVEL=INFO
ENVIRONMENT=staging
```

### Step 3: Deploy Backend

Click "Deploy" and wait for backend to deploy.

### Step 4: Get Backend URL

After deployment:
1. Settings → Networking → Generate Domain
2. Copy URL (e.g., `https://bahr-backend-abc123.railway.app`)

### Step 5: Backend Variables - Second Pass

Update CORS with actual URL:
```
CORS_ORIGINS=https://bahr-backend-abc123.railway.app,https://placeholder-frontend.com
```

### Step 6: Frontend Variables

Add to frontend service:
```
NEXT_PUBLIC_API_URL=https://bahr-backend-abc123.railway.app/api/v1
NODE_ENV=production
```

### Step 7: Deploy Frontend

Click "Deploy" and wait for frontend to deploy.

### Step 8: Get Frontend URL

After deployment:
1. Settings → Networking → Generate Domain
2. Copy URL (e.g., `https://bahr-frontend-xyz789.railway.app`)

### Step 9: Backend Variables - Final Pass

Update CORS with both actual URLs:
```
CORS_ORIGINS=https://bahr-backend-abc123.railway.app,https://bahr-frontend-xyz789.railway.app
```

### Step 10: Redeploy Backend

Click "Deploy" to apply CORS changes.

---

## Railway Variable Features

### Service References

Railway allows you to reference other services:

```bash
# Reference PostgreSQL
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Reference Redis
REDIS_URL=${{Redis.REDIS_URL}}

# Reference another service
OTHER_SERVICE_URL=${{OtherService.RAILWAY_PUBLIC_DOMAIN}}
```

### Environment-Specific Variables

Railway automatically provides:
```bash
PORT=<auto-assigned>              # Port your app should listen on
RAILWAY_ENVIRONMENT=production    # Environment name
RAILWAY_PUBLIC_DOMAIN=<domain>    # Your service's public domain
```

Don't set these manually - Railway provides them automatically.

### Private Variables

For sensitive data (like SECRET_KEY):
1. Click "New Variable"
2. Name: `SECRET_KEY`
3. Value: Your secret
4. Railway will encrypt and hide the value

---

## Verification

### Check Variables Are Set

**Via Railway CLI:**
```bash
# Backend variables
railway variables --service backend

# Frontend variables
railway variables --service frontend
```

**Via Dashboard:**
1. Click on service
2. Click "Variables"
3. All variables should be listed

### Test Database Connection

```bash
railway run --service backend python -c "from app.db.session import SessionLocal; db = SessionLocal(); print('✓ Database connected')"
```

### Test Redis Connection

```bash
railway run --service backend python -c "import os; import redis; r = redis.from_url(os.getenv('REDIS_URL')); print('✓ Redis connected:', r.ping())"
```

---

## Common Issues

### Issue: DATABASE_URL not set

**Problem:** Backend can't connect to database

**Solution:**
1. Verify PostgreSQL service exists in project
2. Check variable is set: `${{Postgres.DATABASE_URL}}`
3. Redeploy backend

### Issue: CORS errors

**Problem:** Frontend requests blocked

**Solution:**
1. Check CORS_ORIGINS includes both URLs
2. Use HTTPS URLs (Railway default)
3. No trailing slashes in URLs
4. Redeploy backend after updating

### Issue: Frontend can't find API

**Problem:** API calls return 404

**Solution:**
1. Verify `NEXT_PUBLIC_API_URL` includes `/api/v1`
2. Check backend URL is correct
3. Test backend health: `curl <backend-url>/health`
4. Redeploy frontend after updating

---

## Environment Variable Checklist

### Backend Service
- [ ] `PROJECT_NAME` set
- [ ] `API_VERSION` set
- [ ] `SECRET_KEY` generated and set (32 bytes hex)
- [ ] `DATABASE_URL` references PostgreSQL
- [ ] `REDIS_URL` references Redis
- [ ] `CORS_ORIGINS` includes both URLs (no trailing slashes)
- [ ] `LOG_LEVEL` set to `INFO`
- [ ] `ENVIRONMENT` set to `staging`

### Frontend Service
- [ ] `NEXT_PUBLIC_API_URL` includes `/api/v1`
- [ ] `NODE_ENV` set to `production`
- [ ] Backend URL is correct and accessible

### Services
- [ ] PostgreSQL service added to project
- [ ] Redis service added to project
- [ ] Both services show "Active" status
- [ ] Domains generated for backend and frontend

---

## Quick Copy Templates

### Backend (Copy-Paste Ready)

```bash
PROJECT_NAME=BAHR API
API_VERSION=1.0.0
ANALYSIS_ENGINE_VERSION=1.0.0
ENVIRONMENT=staging
LOG_LEVEL=INFO
SECRET_KEY=REPLACE_WITH_OPENSSL_RAND_HEX_32
DATABASE_URL=${{Postgres.DATABASE_URL}}
DATABASE_ECHO=false
REDIS_URL=${{Redis.REDIS_URL}}
CACHE_TTL=86400
CORS_ORIGINS=REPLACE_WITH_YOUR_URLS
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600
MAINTENANCE_MODE=false
```

### Frontend (Copy-Paste Ready)

```bash
NEXT_PUBLIC_API_URL=REPLACE_WITH_BACKEND_URL/api/v1
NODE_ENV=production
```

---

## Advanced: Railway CLI

### Set Variables via CLI

```bash
# Backend
railway variables --service backend set SECRET_KEY=$(openssl rand -hex 32)
railway variables --service backend set PROJECT_NAME="BAHR API"

# Frontend
railway variables --service frontend set NEXT_PUBLIC_API_URL="https://your-backend.railway.app/api/v1"
```

### Bulk Import from .env File

```bash
# Create .env.railway
cat > .env.railway << EOF
PROJECT_NAME=BAHR API
SECRET_KEY=$(openssl rand -hex 32)
LOG_LEVEL=INFO
EOF

# Import (not directly supported, but can script it)
while IFS='=' read -r key value; do
  railway variables --service backend set "$key" "$value"
done < .env.railway
```

---

## Security Best Practices

1. **Never commit .env files** with real secrets
2. **Generate unique SECRET_KEY** for each environment
3. **Use Railway's encryption** for sensitive variables
4. **Rotate secrets** periodically
5. **Limit CORS_ORIGINS** to only your domains
6. **Use HTTPS URLs** (Railway default)
7. **Review variables** before deployment

---

## Summary

After setting all variables correctly:

✅ Backend can connect to PostgreSQL  
✅ Backend can connect to Redis  
✅ Backend allows frontend CORS requests  
✅ Frontend knows where to find backend API  
✅ All services can communicate securely  

**Test with:**
```bash
./scripts/verify_deployment.sh
```

If all tests pass, your environment variables are configured correctly! 🎉
