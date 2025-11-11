# Analytics Deployment Guide

## Quick Deployment Checklist

### 1. Deploy Backend Changes to Railway ✅

#### Files to Commit & Push:
```bash
git add backend/app/models/analytics.py
git add backend/app/schemas/analytics.py
git add backend/app/api/v1/endpoints/analytics.py
git add backend/app/db/base.py
git add backend/app/api/v1/router.py
git add backend/alembic/versions/b9f2c3d4e5f6_add_analytics_events_table.py
git commit -m "feat: add analytics tracking system"
git push origin main
```

#### Run Database Migration on Railway:
1. Go to Railway dashboard → Backend service
2. Open "Settings" → "Deploy" section
3. Add one-time migration command:
   ```bash
   alembic upgrade head
   ```
4. Or SSH into the service and run manually

### 2. Deploy Frontend Changes ✅

#### Files to Commit & Push:
```bash
git add frontend/src/types/analytics.ts
git add frontend/src/hooks/useAnalytics.ts
git add frontend/src/app/page.tsx
git add frontend/src/app/analyze/page.tsx
git add frontend/src/app/analytics/page.tsx
git commit -m "feat: integrate analytics tracking on frontend"
git push origin main
```

#### Verify Build:
```bash
cd frontend
npm run build  # Should complete successfully ✅
```

### 3. Environment Variables

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=https://backend-production-c17c.up.railway.app
```

#### Backend (Railway)
Already configured:
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis cache connection

### 4. Testing After Deployment

#### Test Analytics Endpoint:
```bash
curl -X POST https://backend-production-c17c.up.railway.app/api/v1/analytics \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test_event",
    "session_id": "test-session-123",
    "timestamp": 1699999999999
  }'
```

#### Test Stats Endpoint:
```bash
curl https://backend-production-c17c.up.railway.app/api/v1/analytics/stats?days=7
```

#### Visit Analytics Dashboard:
```
https://your-frontend-url.com/analytics
```

### 5. Verify Data Flow

1. **Visit Home Page** → Check browser console for "📊 Analytics: page_view"
2. **Analyze a Verse** → Check for "analyze_submit", "analyze_success" events
3. **Check localStorage** → Key: `bahr_analytics_session`
4. **Query Database** → Check `analytics_events` table has rows
5. **Visit /analytics** → Should show session stats and global stats

---

## Database Schema

### analytics_events Table
```sql
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    user_id VARCHAR(100),
    timestamp BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    properties JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    referrer TEXT
);

CREATE INDEX ix_analytics_events_event_name ON analytics_events(event_name);
CREATE INDEX ix_analytics_events_session_id ON analytics_events(session_id);
CREATE INDEX ix_analytics_events_user_id ON analytics_events(user_id);
CREATE INDEX ix_analytics_events_timestamp ON analytics_events(timestamp);
```

---

## API Endpoints

### POST /api/v1/analytics
Create a new analytics event.

**Request:**
```json
{
  "name": "analyze_submit",
  "session_id": "1699999999-abc123",
  "timestamp": 1699999999999,
  "properties": {
    "verse_length": 45,
    "has_diacritics": true
  }
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "event_name": "analyze_submit",
  "session_id": "1699999999-abc123",
  "timestamp": 1699999999999,
  "created_at": "2025-01-11T12:00:00.000Z"
}
```

### GET /api/v1/analytics/stats
Get aggregated usage statistics.

**Query Parameters:**
- `days` (optional, default: 7) - Number of days to analyze

**Response (200):**
```json
{
  "total_sessions": 1234,
  "total_events": 5678,
  "total_analyses": 890,
  "success_rate": 0.95,
  "top_events": [
    { "name": "page_view", "count": 1234 },
    { "name": "analyze_submit", "count": 890 }
  ],
  "recent_activity": [...]
}
```

---

## Troubleshooting

### Events Not Showing in Dashboard
1. Check browser console for errors
2. Verify `NEXT_PUBLIC_API_URL` is set correctly
3. Check Network tab for failed requests to /api/v1/analytics
4. Verify localStorage has `bahr_analytics_session` key

### Backend Errors
1. Check Railway logs for Python exceptions
2. Verify database migration ran successfully
3. Test endpoints directly with curl
4. Check PostgreSQL has `analytics_events` table

### Migration Issues
```bash
# Check current migration version
alembic current

# View migration history
alembic history

# Manually upgrade to latest
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

---

## Success Criteria ✅

- [x] Backend builds without errors
- [x] Frontend builds successfully
- [x] Migration file created and validated
- [x] All TypeScript/Python files pass syntax checks
- [x] useAnalytics hook tracks events
- [x] Analytics dashboard renders
- [ ] Database migration applied (do on Railway)
- [ ] Events persist to PostgreSQL (test in production)
- [ ] /analytics page shows real data (test in production)

**Ready to Deploy**: ✅ Yes
