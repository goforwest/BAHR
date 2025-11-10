# 🏛️ Architecture Decision Records (ADR)
## BAHR Platform - Key Technical Decisions

---

**Created:** November 9, 2025
**Status:** ✅ **APPROVED** - Living Document
**Purpose:** Document all major architectural and technical decisions
**Review Status:** Addresses Technical Review Issue #3, #4

---

## ADR Format

Each decision follows this structure:
```yaml
Decision: [Title]
Status: [Proposed | Accepted | Superseded | Deprecated]
Date: [YYYY-MM-DD]
Context: Why this decision was needed
Decision: What we decided
Consequences: Positive and negative outcomes
Alternatives Considered: Other options we evaluated
```

---

## Table of Contents

1. [ADR-001: API Gateway Strategy - Native FastAPI vs Kong](#adr-001)
2. [ADR-002: Database Performance Indexes](#adr-002)
3. [ADR-003: Elasticsearch Integration Timing](#adr-003)
4. [ADR-004: CORS Policy for Frontend](#adr-004)
5. [ADR-005: Database Backup Strategy](#adr-005)
6. [ADR-006: Secrets Management in Production](#adr-006)
7. [ADR-007: Caching Strategy - Redis Implementation](#adr-007)
8. [ADR-008: Authentication - JWT vs Session Cookies](#adr-008)
9. [ADR-009: Frontend Framework - Next.js vs Alternatives](#adr-009)
10. [ADR-010: Deployment Platform for MVP](#adr-010)
11. [ADR-011: Testing Strategy - Pytest vs Alternatives](#adr-011)

---

<a name="adr-001"></a>
## ADR-001: API Gateway Strategy

**Status:** ✅ **ACCEPTED**
**Date:** 2025-11-09
**Deciders:** Technical Architect, Senior Reviewer
**Review Issue:** Technical Review #3

### Context

The implementation plan mentioned both "Kong API Gateway" and "native FastAPI middleware" for handling cross-cutting concerns (authentication, rate limiting, request logging). This ambiguity could lead to confusion during implementation.

**Requirements:**
- Authentication enforcement (JWT validation)
- Rate limiting (100 req/hour for free tier)
- Request/response logging
- CORS handling
- Error response standardization
- API versioning support

### Decision

**Use Native FastAPI Middleware for Phase 1-3, defer Kong to Phase 4+ (if needed)**

**Implementation:**
```python
# app/main.py
from fastapi import FastAPI
from app.middleware.auth import AuthMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.cors import setup_cors

app = FastAPI(title="BAHR API", version="1.0.0")

# Setup CORS
setup_cors(app)

# Add middleware stack (order matters!)
app.add_middleware(LoggingMiddleware)      # Log all requests
app.add_middleware(RateLimitMiddleware)    # Rate limit before auth
app.add_middleware(AuthMiddleware)         # Validate JWT tokens
```

### Consequences

**Positive:**
- ✅ **Simpler setup** - No separate infrastructure to manage
- ✅ **Zero additional cost** - No Kong licensing or hosting
- ✅ **Faster development** - Can start coding immediately
- ✅ **Python-native** - Same language as backend, easier debugging
- ✅ **Good enough for MVP** - Handles 1k-10k users easily

**Negative:**
- ⚠️ **Less feature-rich** - Kong has built-in analytics, plugins, etc.
- ⚠️ **Manual implementation** - Need to write rate limiting, logging ourselves
- ⚠️ **Scaling limits** - May need Kong at 100k+ requests/sec

### Alternatives Considered

#### Option A: Kong API Gateway
- **Pros:** Industry standard, plugin ecosystem, built-in observability
- **Cons:** Additional infrastructure, $50-100/month, complexity
- **Verdict:** Overkill for MVP

#### Option B: AWS API Gateway
- **Pros:** Serverless, auto-scaling, AWS integration
- **Cons:** Vendor lock-in, cost per request, latency overhead
- **Verdict:** Not suitable (not using AWS Lambda)

#### Option C: Nginx + Lua
- **Pros:** Very fast, low latency
- **Cons:** Different language (Lua), steep learning curve
- **Verdict:** Unnecessary complexity

### Migration Path to Kong (if needed)

**Trigger:** When we exceed 100k requests/sec or need advanced features

**Steps:**
1. Deploy Kong in front of FastAPI
2. Migrate middleware logic to Kong plugins
3. Remove middleware from FastAPI (keep business logic only)
4. Update deployment configuration

**Estimated Effort:** 1-2 weeks

### Status: CLOSED ✅

**Approved for:** Phase 1, 2, 3 (MVP through initial scale)
**Revisit when:** Traffic exceeds 100k req/sec or need advanced API management

---

<a name="adr-002"></a>
## ADR-002: Database Performance Indexes

**Status:** ✅ **ACCEPTED & IMPLEMENTED**
**Date:** 2025-11-10
**Deciders:** Technical Lead
**Implementation:** Alembic migration `a8bdbba834b3_initial_schema.py`

### Context

The initial schema review identified no explicit CREATE INDEX statements in the implementation plan. Database performance heavily depends on proper indexing strategy, especially for:
- User lookups by email (authentication)
- Meter/tafila name searches
- Analysis history queries
- Cache key lookups

Without indexes, queries would perform full table scans, causing poor performance as data grows.

### Decision

**Implement 8 strategic indexes in initial migration covering all critical query patterns**

**Implementation:**
```sql
-- Users table indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);

-- Meters table indexes  
CREATE INDEX idx_meters_name_ar ON meters(name_ar);
CREATE INDEX idx_meters_name_en ON meters(name_en);

-- Tafail table index
CREATE INDEX idx_tafail_name_ar ON tafail(name_ar);

-- Analyses table indexes
CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_created_at ON analyses(created_at DESC);
```

### Index Strategy Rationale

#### User Indexes
- **`idx_users_email`**: Login queries (`WHERE email = ?`)
- **`idx_users_username`**: Profile lookups, public pages
- **`idx_users_role`**: Admin queries filtering by role

#### Meter/Tafail Indexes
- **`idx_meters_name_ar/en`**: Autocomplete, meter selection
- **`idx_tafail_name_ar`**: Tafila reference lookups

#### Analysis Indexes
- **`idx_analyses_user_id`**: User history (`WHERE user_id = ?`)
- **`idx_analyses_created_at`**: Recent analyses (`ORDER BY created_at DESC`)

### Consequences

**Positive:**
- ✅ **Fast authentication** - Email lookup O(log n) instead of O(n)
- ✅ **Efficient user queries** - Username/role filters optimized
- ✅ **Quick meter lookups** - Autocomplete responses <50ms
- ✅ **Scalable analysis history** - Pagination performs well up to 1M+ records
- ✅ **Production-ready** - Indexes deployed from day 1

**Negative:**
- ⚠️ **Write overhead** - ~10-15% slower INSERTs (acceptable trade-off)
- ⚠️ **Storage overhead** - ~20% additional disk space (minimal concern)
- ⚠️ **Maintenance** - Need to monitor index bloat (yearly REINDEX)

### Performance Benchmarks

Expected query performance with indexes:

```yaml
User login (email lookup):
  Without index: 50ms @ 10k users, 500ms @ 100k users
  With index: 1-2ms constant (B-tree lookup)

User analysis history:
  Without index: 100ms @ 1k analyses, 1000ms @ 10k analyses  
  With index: 5-10ms constant

Meter autocomplete:
  Without index: 20ms @ 16 meters (tolerable but wasteful)
  With index: 1ms (instant)
```

### Monitoring Plan

Track index effectiveness via PostgreSQL stats:

```sql
-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;

-- Find unused indexes (idx_scan = 0 after 1 month)
```

**Action:** Remove unused indexes if idx_scan = 0 after 30 days

### Migration Safety

The migration includes:
- ✅ Reversible `downgrade()` function
- ✅ Non-blocking index creation (PostgreSQL CONCURRENTLY not needed for initial migration)
- ✅ Foreign key constraints
- ✅ Enum types for type safety

### Status: IMPLEMENTED ✅

**Migration File:** `alembic/versions/a8bdbba834b3_initial_schema.py`
**Deployed:** November 9, 2025
**Verified:** All 8 indexes created successfully

---

<a name="adr-003"></a>
## ADR-003: Elasticsearch Integration Timing

**Status:** ✅ **ACCEPTED**
**Date:** 2025-11-09
**Deciders:** Technical Architect, Senior Reviewer
**Review Issue:** Technical Review #4

### Context

The implementation plan marked Elasticsearch as "optional for Phase 1" but did not specify when to integrate it or what threshold triggers its adoption. This created ambiguity around search functionality and data migration planning.

**Search Requirements:**
- Full-text search on poetry content (Arabic text)
- Search by poet name, era, theme
- Autocomplete for meter names
- Fuzzy search tolerance (typos, variations)

### Decision

**Defer Elasticsearch to 50k+ verses, use PostgreSQL full-text search for MVP**

**Phase 1-3 (MVP, <50k verses):**
```sql
-- Use PostgreSQL built-in full-text search
CREATE INDEX idx_verses_fulltext
ON verses
USING gin(to_tsvector('arabic', text));

-- Query
SELECT * FROM verses
WHERE to_tsvector('arabic', text) @@ to_tsquery('arabic', 'شعر');
```

**Phase 4+ (>50k verses):**
- Migrate to Elasticsearch
- Backfill existing data
- Implement advanced search features

### Consequences

**Positive:**
- ✅ **Simpler stack** - One less service to manage
- ✅ **Zero additional cost** - No Elasticsearch hosting
- ✅ **Good enough for MVP** - PostgreSQL FTS handles <50k docs well
- ✅ **Faster development** - No learning curve for Elasticsearch
- ✅ **Arabic support** - PostgreSQL has `arabic` text search configuration

**Negative:**
- ⚠️ **Less powerful** - No advanced features (boosting, highlighting, facets)
- ⚠️ **Slower at scale** - PostgreSQL FTS degrades after 100k+ documents
- ⚠️ **Migration overhead** - Will need to backfill data when switching

### Alternatives Considered

#### Option A: Elasticsearch from Day 1
- **Pros:** Best search performance, feature-rich
- **Cons:** Additional infrastructure, complexity, cost
- **Verdict:** Premature optimization

#### Option B: Typesense (Lightweight alternative)
- **Pros:** Easier than Elasticsearch, good performance
- **Cons:** Still requires separate infrastructure
- **Verdict:** Good option, but defer to Phase 4

#### Option C: Cloud Search (Algolia, MeiliSearch Cloud)
- **Pros:** Fully managed, zero ops
- **Cons:** Expensive ($100+/month), vendor lock-in
- **Verdict:** Too expensive for MVP

### Thresholds for Migration

**Trigger Elasticsearch Migration when:**
- ✅ Total verses exceed 50,000
- ✅ Search queries exceed 1,000/hour
- ✅ Users complain about search slowness (P95 >500ms)
- ✅ Need advanced features (faceted search, autocomplete, fuzzy matching)

### Migration Plan (when triggered)

**Week 1:**
- Deploy Elasticsearch cluster (Docker or managed service)
- Create index mapping for verses

**Week 2:**
- Backfill existing verses from PostgreSQL
- Implement dual-write (write to both PostgreSQL and Elasticsearch)

**Week 3:**
- Update search API to query Elasticsearch
- Monitor performance, fix bugs

**Week 4:**
- Deprecate PostgreSQL FTS
- Remove PostgreSQL full-text indexes (save disk space)

**Estimated Effort:** 3-4 weeks

### Status: CLOSED ✅

**Approved for:** Defer to Phase 4 or 50k verses threshold
**Revisit when:** Verse count exceeds 50k or search performance degrades

---

<a name="adr-003"></a>
## ADR-004: CORS Policy for Frontend

**Status:** ✅ **ACCEPTED**
**Date:** 2025-11-09
**Deciders:** Security Team, Technical Architect
**Review Issue:** Technical Review #5

### Context

The security documentation did not specify allowed CORS origins, which could lead to frontend requests being blocked or overly permissive CORS settings creating security risks.

### Decision

**Implement strict CORS policy with environment-specific allowed origins**

**Development:**
```python
CORS_ORIGINS = [
    "http://localhost:3000",      # Next.js dev server
    "http://localhost:8000",      # FastAPI dev server (for testing)
    "http://127.0.0.1:3000",      # Alternative localhost
]
```

**Staging:**
```python
CORS_ORIGINS = [
    "https://staging.bahr.app",
    "https://staging-api.bahr.app",
]
```

**Production:**
```python
CORS_ORIGINS = [
    "https://bahr.app",
    "https://www.bahr.app",
    "https://api.bahr.app",
]
```

**Implementation:**
```python
# app/middleware/cors.py
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

def setup_cors(app):
    """Configure CORS middleware"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,  # Strict whitelist
        allow_credentials=True,               # Allow cookies (for future sessions)
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],                  # Allow all headers
        expose_headers=["X-Request-ID"],      # Expose custom headers
        max_age=600,                          # Cache preflight requests for 10 minutes
    )
```

### Consequences

**Positive:**
- ✅ **Secure** - Only whitelisted origins can access API
- ✅ **Environment-specific** - Different origins for dev/staging/prod
- ✅ **Credential support** - Allows future cookie-based authentication

**Negative:**
- ⚠️ **Manual updates** - Need to add new domains to whitelist
- ⚠️ **Subdomain handling** - Wildcard (*) not allowed for security

### Alternatives Considered

#### Option A: Allow All Origins (`*`)
- **Pros:** No configuration needed
- **Cons:** Major security risk, credentials not allowed
- **Verdict:** REJECTED - Insecure

#### Option B: Wildcard Subdomain (`*.bahr.app`)
- **Pros:** Flexible for new subdomains
- **Cons:** Not supported by CORS spec when credentials enabled
- **Verdict:** REJECTED - Incompatible with credentials

### Mobile App Support (Future)

When adding mobile apps (Phase 5):
```python
# Add custom scheme for mobile apps
CORS_ORIGINS = [
    # ... existing origins
    "capacitor://localhost",    # iOS app
    "http://localhost",          # Android app
    "https://ionic.bahr.app",    # PWA fallback
]
```

### Status: CLOSED ✅

**Implementation File:** `app/middleware/cors.py`
**Configuration:** `app/config.py` (environment-specific)
**Testing:** Verify preflight requests return correct headers

---

<a name="adr-004"></a>
## ADR-005: Database Backup Strategy

**Status:** ✅ **ACCEPTED**
**Date:** 2025-11-09
**Deciders:** DevOps, Technical Architect
**Review Issue:** Technical Review #6

### Context

No automated backup strategy was documented, creating risk of data loss and unclear recovery procedures.

### Decision

**Implement automated daily backups with point-in-time recovery (PITR)**

**Backup Strategy:**

| Environment | Frequency | Retention | Method |
|-------------|-----------|-----------|--------|
| **Development** | None | N/A | Rebuild from migrations |
| **Staging** | Daily | 7 days | Railway automated backups |
| **Production** | Hourly | 30 days | Railway PITR + S3 snapshots |

**Implementation:**

### Railway Automated Backups (MVP)

```yaml
# Railway automatically backs up PostgreSQL databases
Backup Configuration:
  Frequency: Every 6 hours
  Retention: 7 days (free tier), 30 days (pro tier)
  Type: Full snapshot
  Restore: One-click via Railway dashboard
```

**Enable in Railway:**
1. Go to Railway project → PostgreSQL service
2. Settings → Backups → Enable Automated Backups
3. Set retention: 30 days (production), 7 days (staging)

### Manual Backup Script (Disaster Recovery)

**File:** `scripts/backup_db.sh`

```bash
#!/bin/bash
# Manual database backup to S3

set -e

# Configuration
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="bahr_backup_${TIMESTAMP}.sql.gz"
S3_BUCKET="bahr-db-backups"
DATABASE_URL="${DATABASE_URL}"

echo "🗄️  Starting database backup..."

# Dump database (compressed)
pg_dump ${DATABASE_URL} | gzip > ${BACKUP_FILE}

echo "📦 Backup created: ${BACKUP_FILE}"

# Upload to S3 (requires AWS CLI)
if command -v aws &> /dev/null; then
    echo "☁️  Uploading to S3..."
    aws s3 cp ${BACKUP_FILE} s3://${S3_BUCKET}/production/${BACKUP_FILE}
    echo "✅ Backup uploaded to S3"
else
    echo "⚠️  AWS CLI not found, skipping S3 upload"
fi

# Keep only last 7 local backups
ls -t bahr_backup_*.sql.gz | tail -n +8 | xargs rm -f

echo "✅ Backup complete!"
```

**Automate with cron (production server):**
```cron
# Run daily backup at 2 AM UTC
0 2 * * * /app/scripts/backup_db.sh >> /var/log/backup.log 2>&1
```

### Restore Procedure

**From Railway Backup:**
```bash
# Via Railway dashboard
1. Go to PostgreSQL service → Backups
2. Select backup timestamp
3. Click "Restore"
4. Confirm (will create new database instance)

# Via Railway CLI
railway pg:restore <backup-id>
```

**From Manual S3 Backup:**
```bash
# Download from S3
aws s3 cp s3://bahr-db-backups/production/bahr_backup_20251109_020000.sql.gz .

# Decompress
gunzip bahr_backup_20251109_020000.sql.gz

# Restore (WARNING: This will overwrite current database!)
psql ${DATABASE_URL} < bahr_backup_20251109_020000.sql
```

### Consequences

**Positive:**
- ✅ **Automated** - No manual intervention needed
- ✅ **Point-in-time recovery** - Restore to any point in last 30 days
- ✅ **Zero downtime** - Backups run without locking database
- ✅ **Disaster recovery** - S3 backups survive Railway outage

**Negative:**
- ⚠️ **Cost** - S3 storage cost (~$0.50/month for 10 GB)
- ⚠️ **Manual testing** - Need to test restore procedure quarterly

### Data Retention Policy

**User Data:**
- Active users: Indefinite retention
- Deleted accounts: Hard delete after 30 days (GDPR compliance)

**Analysis Data:**
- Free users: 1 year retention, then delete
- Premium users: Indefinite retention

**Logs:**
- Application logs: 90 days
- Audit logs: 1 year (compliance requirement)

### Testing Backups

**Quarterly Backup Drill:**
1. Restore latest backup to staging environment
2. Verify data integrity (run sanity checks)
3. Document any issues
4. Update restore procedures if needed

**Checklist:**
- [ ] Restore completes without errors
- [ ] User count matches production
- [ ] Analyses count matches production
- [ ] API endpoints work after restore

### Status: CLOSED ✅

**Implementation:** Enable Railway backups before production launch
**Testing:** Run first backup drill in Week 4 of Phase 1
**Documentation:** Update runbook with restore procedures

---

<a name="adr-005"></a>
## ADR-005: Secrets Management in Production

**Status:** ✅ **ACCEPTED**
**Date:** 2025-11-09
**Deciders:** Security Team, Technical Architect
**Review Issue:** Technical Review #1 (CRITICAL)

### Context

Initial plan used `.env` files for all environments, which is insecure for production (visible to all processes, logged in crash dumps, no audit trail).

### Decision

**Use Railway Secrets for production, `.env` only for local development**

**See full specification:** [SECRETS_MANAGEMENT.md](./technical/SECRETS_MANAGEMENT.md)

**Summary:**
- **Development:** `.env` files (local only)
- **Staging/Production:** Railway environment variables (encrypted at rest)
- **Future:** Migrate to HashiCorp Vault if multi-cloud needed

### Status: CLOSED ✅

**Detailed Documentation:** [docs/technical/SECRETS_MANAGEMENT.md](./technical/SECRETS_MANAGEMENT.md)

---

<a name="adr-006"></a>
## ADR-006: Caching Strategy

**Status:** ✅ **ACCEPTED**
**Date:** 2025-11-08
**Deciders:** Backend Team

### Context

Analysis requests are computationally expensive (100-300ms). Caching can reduce latency and server load.

### Decision

**Use Redis for analysis result caching with SHA256 hash keys**

**Implementation:**
```python
# Cache key: SHA256 hash of normalized text
cache_key = f"analysis:{hashlib.sha256(normalized_text.encode()).hexdigest()}"

# TTL: 1 hour (3600 seconds)
redis.setex(cache_key, 3600, json.dumps(result))
```

**Expected Hit Rate:** 40-60%

### Consequences

**Positive:**
- ✅ Reduces P95 latency from 500ms → 50ms (10x improvement)
- ✅ Saves compute costs (40% fewer analysis calculations)
- ✅ Scales well (Redis handles 100k+ ops/sec)

**Negative:**
- ⚠️ Memory cost (~$10/month for 1GB Redis)
- ⚠️ Cache invalidation complexity (if algorithm changes)

### Status: CLOSED ✅

**Documentation:** [CACHE_STRATEGY.md](./technical/CACHE_STRATEGY.md)

---

<a name="adr-007"></a>
## ADR-007: Authentication Method

**Status:** ✅ **ACCEPTED**
**Date:** 2025-11-08
**Deciders:** Security Team

### Context

Need to choose between JWT tokens and session cookies for user authentication.

### Decision

**Use JWT (JSON Web Tokens) with refresh token rotation**

**Rationale:**
- ✅ Stateless (no session storage needed)
- ✅ Mobile-friendly (works with native apps)
- ✅ Scales horizontally (no session sharing)

**Configuration:**
- Access token: 30 minutes
- Refresh token: 7 days
- Algorithm: HS256

### Consequences

**Positive:**
- ✅ No session database needed
- ✅ API can scale independently
- ✅ Works with multiple frontends (web, mobile, API)

**Negative:**
- ⚠️ Cannot revoke tokens immediately (must wait for expiry)
- ⚠️ Refresh token rotation adds complexity

### Status: CLOSED ✅

**Documentation:** [SECURITY.md](./technical/SECURITY.md#authentication)

---

<a name="adr-008"></a>
## ADR-008: Frontend Framework

**Status:** ✅ **ACCEPTED**
**Date:** 2025-11-08
**Deciders:** Frontend Team

### Context

Need to choose a React framework for the web frontend.

### Decision

**Use Next.js 14 with App Router**

**Rationale:**
- ✅ Best React framework for production
- ✅ Built-in SSR and static generation
- ✅ Excellent performance (automatic code splitting)
- ✅ Vercel deployment (zero-config)
- ✅ RTL support for Arabic

**Alternatives Considered:**
- Create React App: Deprecated, no SSR
- Remix: Good, but less mature ecosystem
- Vite + React: Fast, but no SSR out of box

### Status: CLOSED ✅

**Documentation:** [FRONTEND_GUIDE.md](./technical/FRONTEND_GUIDE.md)

---

<a name="adr-009"></a>
## ADR-009: Deployment Platform for MVP

**Status:** ✅ **ACCEPTED**
**Date:** 2025-11-08
**Deciders:** DevOps, Product Team

### Context

Need to choose hosting platform that balances cost, simplicity, and scalability.

### Decision

**Use Railway for backend + PostgreSQL + Redis, Vercel for frontend**

**Rationale:**
- ✅ Railway: All-in-one platform ($5-20/month for MVP)
- ✅ Zero DevOps overhead (no Kubernetes, Docker registry)
- ✅ Git-based deploys (push to deploy)
- ✅ Built-in PostgreSQL and Redis
- ✅ Vercel: Best Next.js hosting, free tier sufficient

**Migration Path:**
- 1k-10k users: Stay on Railway
- 10k-100k users: Migrate to DigitalOcean App Platform
- 100k+ users: Migrate to AWS/GCP with Kubernetes

### Consequences

**Positive:**
- ✅ Fastest time to market (deploy in hours, not days)
- ✅ Low cost for MVP ($20-50/month total)
- ✅ Automatic SSL certificates
- ✅ Zero-downtime deployments

**Negative:**
- ⚠️ Vendor lock-in (but easy to migrate using Docker)
- ⚠️ Cost increases with scale (may need migration)

### Status: CLOSED ✅

**Documentation:** [DEPLOYMENT_GUIDE.md](./technical/DEPLOYMENT_GUIDE.md)

---

<a name="adr-010"></a>
## ADR-010: Testing Framework

**Status:** ✅ **ACCEPTED**
**Date:** 2025-11-08
**Deciders:** Development Team

### Context

Need to choose testing framework for Python backend.

### Decision

**Use pytest for all Python tests**

**Rationale:**
- ✅ Industry standard for Python
- ✅ Rich plugin ecosystem (pytest-cov, pytest-asyncio)
- ✅ Fixtures for database/Redis setup
- ✅ Excellent FastAPI support

**Test Structure:**
```
backend/tests/
  ├── core/              # Unit tests (prosody engine)
  ├── api/               # Integration tests (endpoints)
  ├── e2e/               # End-to-end tests
  └── fixtures/          # Test data
```

**Coverage Target:** ≥80% for core modules

### Status: CLOSED ✅

**Documentation:** [INTEGRATION_E2E_TESTING.md](./technical/INTEGRATION_E2E_TESTING.md)

---

## Decision Status Summary

| ADR | Decision | Status | Phase |
|-----|----------|--------|-------|
| 001 | API Gateway: Native FastAPI | ✅ Accepted | 1-3 |
| 002 | Elasticsearch: Defer to 50k verses | ✅ Accepted | 4+ |
| 003 | CORS: Strict whitelist | ✅ Accepted | 1 |
| 004 | Backups: Railway + S3 | ✅ Accepted | 1 |
| 005 | Secrets: Railway in prod | ✅ Accepted | 1 |
| 006 | Caching: Redis with hash keys | ✅ Accepted | 1 |
| 007 | Auth: JWT + refresh tokens | ✅ Accepted | 1 |
| 008 | Frontend: Next.js 14 | ✅ Accepted | 1 |
| 009 | Hosting: Railway + Vercel | ✅ Accepted | 1 |
| 010 | Testing: pytest | ✅ Accepted | 1 |

---

## How to Propose New ADRs

1. **Create new ADR** following format above
2. **Assign ADR number** (next available)
3. **Set status** to "Proposed"
4. **Get approval** from technical lead
5. **Update status** to "Accepted"
6. **Reference in code** comments where relevant

---

## Change Log

| Date | ADR | Change |
|------|-----|--------|
| 2025-11-09 | 001-004 | Created to address technical review feedback |
| 2025-11-08 | 005-010 | Documented existing architectural decisions |

---

**Maintained by:** Technical Architecture Team
**Review Frequency:** Quarterly or when major changes proposed
**Last Review:** 2025-11-09
