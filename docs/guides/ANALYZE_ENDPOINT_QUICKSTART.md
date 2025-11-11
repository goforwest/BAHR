# Quick Start Guide - Analyze Endpoint

**Category:** Guide  
**Status:** 🎯 Active  
**Version:** 1.0  
**Last Updated:** 2025-11-10  
**Audience:** Developers, API Users  
**Purpose:** Quick reference for using the /analyze API endpoint  
**Related Docs:** [Backend API](../technical/BACKEND_API.md), [Getting Started](../onboarding/GETTING_STARTED.md)

---

## Prerequisites
- Docker and Docker Compose installed
- Python 3.11+ installed
- Backend dependencies installed

## Step-by-Step Setup

### 1. Start Infrastructure Services
```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Verify services are running
docker-compose ps
```

### 2. Install Python Dependencies (if not already done)
```bash
cd backend
pip install -r requirements.txt
```

### 3. Set Environment Variables (Optional)
```bash
# Create .env file or export variables
export REDIS_URL="redis://localhost:6379/0"
export DATABASE_URL="postgresql://bahr:bahr_dev_password@localhost:5432/bahr_dev"
```

### 4. Start the FastAPI Server
```bash
cd backend
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Will watch for changes in these directories: ['/path/to/BAHR/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
✓ Redis connection initialized
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 5. Test the Endpoint

#### Option A: Using curl
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
    "detect_bahr": true,
    "suggest_corrections": true
  }'
```

#### Option B: Using the test script
```bash
./test_analyze_endpoint.sh
```

#### Option C: Using Swagger UI
1. Open browser: http://localhost:8000/docs
2. Navigate to: **POST /api/v1/analyze**
3. Click "Try it out"
4. Enter request body:
   ```json
   {
     "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
     "detect_bahr": true,
     "suggest_corrections": true
   }
   ```
5. Click "Execute"

### 6. Expected Response
```json
{
  "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
  "taqti3": "فعولن مفاعيلن فعولن مفاعيلن",
  "bahr": {
    "name_ar": "الطويل",
    "name_en": "at-Tawil",
    "confidence": 0.95
  },
  "errors": [],
  "suggestions": ["التقطيع دقيق ومتسق"],
  "score": 95.0
}
```

## Troubleshooting

### Error: Redis connection failed
**Problem**: Redis is not running
**Solution**:
```bash
docker-compose up -d redis
# Verify
docker-compose ps redis
```

### Error: Import "redis.asyncio" could not be resolved
**Problem**: Redis package not installed or outdated
**Solution**:
```bash
pip install redis>=5.0.0
```

### Error: "Text must contain Arabic characters"
**Problem**: Input text doesn't contain Arabic
**Solution**: Ensure the `text` field contains Arabic characters (Unicode range U+0600 to U+06FF)

### Cache not working
**Problem**: Redis not connected or cache operations failing
**Solution**:
1. Check Redis logs: `docker-compose logs redis`
2. Test Redis connection: `redis-cli ping` (should return "PONG")
3. Check server logs for Redis errors

### Server won't start
**Problem**: Port 8000 already in use
**Solution**:
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001

# Or kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

## Verification Checklist

- [ ] Redis container running
- [ ] PostgreSQL container running
- [ ] Server starts without errors
- [ ] "✓ Redis connection initialized" appears in logs
- [ ] `/health` endpoint returns 200
- [ ] `/docs` page loads correctly
- [ ] POST /api/v1/analyze returns valid response
- [ ] Second identical request is faster (cached)
- [ ] Invalid input returns 422 error

## Testing Different Scenarios

### Test 1: Verse with diacritics (high confidence)
```json
{
  "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
  "detect_bahr": true
}
```
Expected: High confidence (~0.9+), "الطويل" meter

### Test 2: Verse without diacritics
```json
{
  "text": "إذا غامرت في شرف مروم",
  "detect_bahr": true
}
```
Expected: Still works, may have lower confidence

### Test 3: With suggestions
```json
{
  "text": "أَلا لَيتَ الشَبابَ يَعودُ يَوماً",
  "detect_bahr": true,
  "suggest_corrections": true
}
```
Expected: Returns suggestions based on confidence

### Test 4: Invalid input
```json
{
  "text": "Hello World"
}
```
Expected: 422 error with message "Text must contain Arabic characters"

### Test 5: Empty text
```json
{
  "text": ""
}
```
Expected: 422 error (minimum length validation)

## Monitoring

### View server logs
```bash
# Terminal where uvicorn is running shows logs
```

### Monitor Redis
```bash
# In separate terminal
redis-cli MONITOR
```

### Check cache keys
```bash
redis-cli KEYS "analysis:*"
```

### View cached value
```bash
redis-cli GET "analysis:<hash>"
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Next Steps After Verification

1. Run integration tests (when created)
2. Test with frontend (Conversation 17-19)
3. Deploy to staging (Conversation 21)
4. Performance testing with larger volumes
5. Monitor cache hit rates
6. Add metrics/monitoring

## Success Criteria

✅ Server starts without errors  
✅ Redis connection initialized  
✅ Endpoint returns valid responses  
✅ Cache working (second request faster)  
✅ Input validation working  
✅ Error handling working  
✅ Suggestions generated correctly  
✅ Meter detection working  
✅ Score calculation correct  
✅ API documentation accessible  

## Support

If issues persist:
1. Check ANALYZE_ENDPOINT_IMPLEMENTATION.md for details
2. Review server logs for errors
3. Check Docker container logs
4. Verify environment variables
5. Ensure all dependencies installed
