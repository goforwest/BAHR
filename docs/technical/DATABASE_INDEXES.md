# 📊 Database Indexes Specification
## Complete Index Strategy for BAHR Platform

---

**Created:** November 9, 2025
**Status:** ✅ **APPROVED** - Production Ready
**Priority:** 🔴 **CRITICAL** - Must create before production launch
**Review Status:** Addresses Technical Review Issue #2

---

## Executive Summary

**Problem Identified in Review:**
> No explicit CREATE INDEX statements in schema documentation. May forget critical indexes for performance optimization.

**Solution:**
This document provides **explicit SQL statements** for all indexes required for optimal query performance, organized by table and use case.

---

## 1. Index Strategy Overview

### Indexing Principles

```yaml
Index Strategy:
  1. Primary Keys: Automatic (clustered B-tree index)
  2. Foreign Keys: Always indexed for JOIN performance
  3. Lookup Columns: email, username, verse_text_hash
  4. Sort Columns: created_at (for pagination)
  5. Composite Indexes: For multi-column WHERE clauses
  6. Partial Indexes: For filtered queries (e.g., visibility='public')
```

### Performance Targets

| Query Type | Without Index | With Index | Target |
|------------|---------------|------------|--------|
| User login (email lookup) | 100ms | <5ms | ✅ <10ms |
| Verse analysis (hash lookup) | 200ms | <1ms | ✅ <5ms |
| User analyses (pagination) | 300ms | <10ms | ✅ <20ms |
| Leaderboard (ORDER BY xp) | 500ms | <20ms | ✅ <50ms |

---

## 2. Core Indexes (Phase 1 MVP)

### Users Table

```sql
-- ============================================================
-- USERS TABLE INDEXES
-- ============================================================

-- Primary key (automatic)
-- CREATE UNIQUE INDEX users_pkey ON users(id);

-- Email lookup (for login)
-- CRITICAL: Used on every login request
CREATE UNIQUE INDEX idx_users_email
ON users(email);

-- Username lookup (for profile pages)
-- UNIQUE constraint ensures no duplicate usernames
CREATE UNIQUE INDEX idx_users_username
ON users(username);

-- Leaderboard query (ORDER BY xp DESC)
-- Used for top poets ranking
CREATE INDEX idx_users_xp
ON users(xp DESC);

-- User level queries (filter by level)
CREATE INDEX idx_users_level
ON users(level);

-- Active users query (last_login recent)
CREATE INDEX idx_users_last_login
ON users(last_login DESC)
WHERE last_login IS NOT NULL;

-- Created date (for user growth analytics)
CREATE INDEX idx_users_created_at
ON users(created_at DESC);
```

**Query Optimization Examples:**

```sql
-- Login query (uses idx_users_email)
SELECT * FROM users WHERE email = 'user@example.com';
-- Expected: <5ms (index scan)

-- Leaderboard query (uses idx_users_xp)
SELECT username, xp FROM users
ORDER BY xp DESC
LIMIT 100;
-- Expected: <20ms (index scan + limit)

-- Active users (uses idx_users_last_login partial index)
SELECT COUNT(*) FROM users
WHERE last_login > NOW() - INTERVAL '30 days';
-- Expected: <10ms (bitmap index scan)
```

---

### User Roles Table (RBAC)

```sql
-- ============================================================
-- USER_ROLES TABLE INDEXES
-- ============================================================

-- Foreign key to users
CREATE INDEX idx_user_roles_user_id
ON user_roles(user_id);

-- Role lookup (find all admins)
CREATE INDEX idx_user_roles_role
ON user_roles(role);

-- Composite index for permission checks
CREATE INDEX idx_user_roles_user_role
ON user_roles(user_id, role);

-- Ensure unique user-role pairs
CREATE UNIQUE INDEX idx_user_roles_unique
ON user_roles(user_id, role);
```

**Query Optimization:**

```sql
-- Check if user is admin (uses idx_user_roles_user_role)
SELECT COUNT(*) FROM user_roles
WHERE user_id = 123 AND role = 'admin';
-- Expected: <1ms (unique index scan)

-- Find all moderators (uses idx_user_roles_role)
SELECT user_id FROM user_roles
WHERE role = 'moderator';
-- Expected: <5ms (index scan)
```

---

### Meters Table (Poetry Meters)

```sql
-- ============================================================
-- METERS TABLE INDEXES
-- ============================================================

-- Primary key (automatic)
-- CREATE UNIQUE INDEX meters_pkey ON meters(id);

-- Name lookup (Arabic)
CREATE UNIQUE INDEX idx_meters_name_ar
ON meters(name_ar);

-- Name lookup (English)
CREATE UNIQUE INDEX idx_meters_name_en
ON meters(name_en);

-- Pattern lookup (for fuzzy matching)
CREATE INDEX idx_meters_pattern
ON meters(pattern);

-- Full-text search on description (Arabic)
CREATE INDEX idx_meters_description_fts
ON meters
USING gin(to_tsvector('arabic', description));
```

**Query Optimization:**

```sql
-- Get meter by Arabic name (uses idx_meters_name_ar)
SELECT * FROM meters WHERE name_ar = 'الطويل';
-- Expected: <1ms (unique index scan)

-- Search meters by description (uses idx_meters_description_fts)
SELECT * FROM meters
WHERE to_tsvector('arabic', description) @@ to_tsquery('arabic', 'شعر');
-- Expected: <10ms (GIN index scan)
```

---

### Meter Variants Table

```sql
-- ============================================================
-- METER_VARIANTS TABLE INDEXES
-- ============================================================

-- Foreign key to meters
CREATE INDEX idx_meter_variants_meter_id
ON meter_variants(meter_id);

-- Composite index for meter + pattern lookup
CREATE INDEX idx_meter_variants_meter_pattern
ON meter_variants(meter_id, variant_pattern);
```

---

### Analyses Table (Critical for Performance)

```sql
-- ============================================================
-- ANALYSES TABLE INDEXES
-- ============================================================

-- Primary key (automatic)
-- CREATE UNIQUE INDEX analyses_pkey ON analyses(id);

-- ⭐ MOST CRITICAL INDEX: Cache lookup by hash
-- Used on EVERY analysis request to check cache
CREATE UNIQUE INDEX idx_analyses_verse_hash
ON analyses(verse_text_hash);

-- Foreign key to users
CREATE INDEX idx_analyses_user_id
ON analyses(user_id);

-- Foreign key to meters
CREATE INDEX idx_analyses_meter_id
ON analyses(detected_meter_id);

-- User's analysis history (pagination)
-- Composite index for: WHERE user_id = X ORDER BY created_at DESC
CREATE INDEX idx_analyses_user_created
ON analyses(user_id, created_at DESC);

-- Confidence threshold queries (find low-confidence analyses)
CREATE INDEX idx_analyses_confidence
ON analyses(confidence);

-- Quality score ranking
CREATE INDEX idx_analyses_quality_score
ON analyses(quality_score DESC);

-- Recent analyses (for analytics)
CREATE INDEX idx_analyses_created_at
ON analyses(created_at DESC);

-- Partial index for high-confidence results only
CREATE INDEX idx_analyses_high_confidence
ON analyses(detected_meter_id, quality_score DESC)
WHERE confidence >= 0.85;
```

**Query Optimization:**

```sql
-- Cache lookup (uses idx_analyses_verse_hash) ⭐
SELECT * FROM analyses
WHERE verse_text_hash = 'abc123...';
-- Expected: <1ms (unique index scan)
-- Hit rate: 40%+ (saves 200ms+ per cached request)

-- User analysis history (uses idx_analyses_user_created)
SELECT verse_text, detected_meter_id, created_at
FROM analyses
WHERE user_id = 42
ORDER BY created_at DESC
LIMIT 20 OFFSET 0;
-- Expected: <10ms (index scan + limit)

-- Low confidence analyses (uses idx_analyses_confidence)
SELECT COUNT(*) FROM analyses
WHERE confidence < 0.70;
-- Expected: <20ms (index scan)
```

---

## 3. Deferred Indexes (Phase 2+)

### Poems Table

```sql
-- ============================================================
-- POEMS TABLE INDEXES (Phase 4+)
-- ============================================================

-- Foreign key to users
CREATE INDEX idx_poems_user_id ON poems(user_id);

-- Foreign key to meters
CREATE INDEX idx_poems_meter_id ON poems(meter_id);

-- Public poems only (for discovery)
CREATE INDEX idx_poems_public
ON poems(created_at DESC)
WHERE visibility = 'public';

-- User's poems (pagination)
CREATE INDEX idx_poems_user_created
ON poems(user_id, created_at DESC);

-- Title search
CREATE INDEX idx_poems_title
ON poems USING gin(to_tsvector('arabic', title));

-- Full-text search on poem content
CREATE INDEX idx_poems_fulltext
ON poems USING gin(to_tsvector('arabic', full_text));
```

---

### Verses Table

```sql
-- ============================================================
-- VERSES TABLE INDEXES (Phase 4+)
-- ============================================================

-- Foreign key to poems
CREATE INDEX idx_verses_poem_id ON verses(poem_id);

-- Meter lookup
CREATE INDEX idx_verses_meter_id ON verses(meter_id);

-- Poem order (line_number)
CREATE INDEX idx_verses_poem_line
ON verses(poem_id, line_number);
```

---

### Social Features (Phase 3+)

```sql
-- ============================================================
-- FOLLOWS TABLE INDEXES (Phase 3+)
-- ============================================================

-- Foreign keys
CREATE INDEX idx_follows_follower_id ON follows(follower_id);
CREATE INDEX idx_follows_following_id ON follows(following_id);

-- Composite for relationship check
CREATE UNIQUE INDEX idx_follows_pair
ON follows(follower_id, following_id);

-- Recent follows
CREATE INDEX idx_follows_created_at ON follows(created_at DESC);

-- ============================================================
-- LIKES TABLE INDEXES (Phase 3+)
-- ============================================================

-- Foreign keys
CREATE INDEX idx_likes_user_id ON likes(user_id);
CREATE INDEX idx_likes_verse_id ON likes(verse_id);

-- Composite for like check
CREATE UNIQUE INDEX idx_likes_user_verse
ON likes(user_id, verse_id);

-- Verse like count (popular verses)
CREATE INDEX idx_likes_verse_created
ON likes(verse_id, created_at DESC);

-- ============================================================
-- COMMENTS TABLE INDEXES (Phase 3+)
-- ============================================================

-- Foreign keys
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_verse_id ON comments(verse_id);

-- Verse comments (pagination)
CREATE INDEX idx_comments_verse_created
ON comments(verse_id, created_at DESC);

-- Recent comments
CREATE INDEX idx_comments_created_at ON comments(created_at DESC);
```

---

### Competitions (Phase 3+)

```sql
-- ============================================================
-- COMPETITIONS TABLE INDEXES (Phase 3+)
-- ============================================================

-- Status queries (find upcoming/live competitions)
CREATE INDEX idx_competitions_status ON competitions(status);

-- Upcoming competitions (sorted by start time)
CREATE INDEX idx_competitions_start_time
ON competitions(start_time)
WHERE status IN ('upcoming', 'live');

-- ============================================================
-- COMPETITION_PARTICIPANTS TABLE INDEXES (Phase 3+)
-- ============================================================

-- Foreign keys
CREATE INDEX idx_participants_competition_id
ON competition_participants(competition_id);

CREATE INDEX idx_participants_user_id
ON competition_participants(user_id);

-- Leaderboard (sorted by score)
CREATE INDEX idx_participants_competition_rank
ON competition_participants(competition_id, final_score DESC);

-- User's competitions
CREATE INDEX idx_participants_user_joined
ON competition_participants(user_id, joined_at DESC);
```

---

### Learning (Phase 4+)

```sql
-- ============================================================
-- USER_PROGRESS TABLE INDEXES (Phase 4+)
-- ============================================================

-- Foreign keys
CREATE INDEX idx_user_progress_user_id
ON user_progress(user_id);

CREATE INDEX idx_user_progress_lesson_id
ON user_progress(lesson_id);

-- User's progress (course completion)
CREATE INDEX idx_user_progress_user_lesson
ON user_progress(user_id, lesson_id);

-- Completed lessons (for analytics)
CREATE INDEX idx_user_progress_completed
ON user_progress(user_id, completed_at)
WHERE status = 'completed';
```

---

### API & Billing (Phase 7+)

```sql
-- ============================================================
-- API_KEYS TABLE INDEXES (Phase 7+)
-- ============================================================

-- Key lookup (on every API request)
CREATE UNIQUE INDEX idx_api_keys_hash
ON api_keys(key_hash);

-- User's API keys
CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);

-- Active keys only (not expired)
CREATE INDEX idx_api_keys_active
ON api_keys(user_id, created_at DESC)
WHERE expires_at > NOW();

-- ============================================================
-- API_USAGE_LOGS TABLE INDEXES (Phase 7+)
-- ============================================================

-- Foreign key to API keys
CREATE INDEX idx_api_usage_api_key_id
ON api_usage_logs(api_key_id);

-- Timestamp (for time-series queries)
CREATE INDEX idx_api_usage_timestamp
ON api_usage_logs(timestamp DESC);

-- Composite for usage analytics
CREATE INDEX idx_api_usage_key_timestamp
ON api_usage_logs(api_key_id, timestamp DESC);

-- Endpoint analytics
CREATE INDEX idx_api_usage_endpoint ON api_usage_logs(endpoint);
```

---

## 4. Migration Scripts

### Alembic Migration: Initial Indexes (Phase 1)

**File:** `backend/alembic/versions/002_add_core_indexes.py`

```python
"""Add core indexes for Phase 1

Revision ID: 002_add_core_indexes
Revises: 001_initial_schema
Create Date: 2025-11-09 12:00:00.000000

"""
from alembic import op

# revision identifiers
revision = '002_add_core_indexes'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None


def upgrade():
    # Users table indexes
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    op.create_index('idx_users_username', 'users', ['username'], unique=True)
    op.create_index('idx_users_xp', 'users', ['xp'], postgresql_using='btree', postgresql_ops={'xp': 'DESC'})
    op.create_index('idx_users_level', 'users', ['level'])
    op.create_index('idx_users_last_login', 'users', ['last_login'], postgresql_using='btree', postgresql_ops={'last_login': 'DESC'}, postgresql_where=op.inline_literal('last_login IS NOT NULL'))
    op.create_index('idx_users_created_at', 'users', ['created_at'], postgresql_using='btree', postgresql_ops={'created_at': 'DESC'})

    # User roles indexes
    op.create_index('idx_user_roles_user_id', 'user_roles', ['user_id'])
    op.create_index('idx_user_roles_role', 'user_roles', ['role'])
    op.create_index('idx_user_roles_user_role', 'user_roles', ['user_id', 'role'])
    op.create_index('idx_user_roles_unique', 'user_roles', ['user_id', 'role'], unique=True)

    # Meters indexes
    op.create_index('idx_meters_name_ar', 'meters', ['name_ar'], unique=True)
    op.create_index('idx_meters_name_en', 'meters', ['name_en'], unique=True)
    op.create_index('idx_meters_pattern', 'meters', ['pattern'])
    # GIN index for full-text search (requires PostgreSQL extension)
    op.execute("CREATE INDEX idx_meters_description_fts ON meters USING gin(to_tsvector('arabic', description))")

    # Meter variants indexes
    op.create_index('idx_meter_variants_meter_id', 'meter_variants', ['meter_id'])
    op.create_index('idx_meter_variants_meter_pattern', 'meter_variants', ['meter_id', 'variant_pattern'])

    # Analyses indexes (CRITICAL FOR PERFORMANCE)
    op.create_index('idx_analyses_verse_hash', 'analyses', ['verse_text_hash'], unique=True)
    op.create_index('idx_analyses_user_id', 'analyses', ['user_id'])
    op.create_index('idx_analyses_meter_id', 'analyses', ['detected_meter_id'])
    op.create_index('idx_analyses_user_created', 'analyses', ['user_id', 'created_at'], postgresql_using='btree', postgresql_ops={'created_at': 'DESC'})
    op.create_index('idx_analyses_confidence', 'analyses', ['confidence'])
    op.create_index('idx_analyses_quality_score', 'analyses', ['quality_score'], postgresql_using='btree', postgresql_ops={'quality_score': 'DESC'})
    op.create_index('idx_analyses_created_at', 'analyses', ['created_at'], postgresql_using='btree', postgresql_ops={'created_at': 'DESC'})
    op.create_index('idx_analyses_high_confidence', 'analyses', ['detected_meter_id', 'quality_score'], postgresql_using='btree', postgresql_ops={'quality_score': 'DESC'}, postgresql_where=op.inline_literal('confidence >= 0.85'))


def downgrade():
    # Drop indexes in reverse order
    op.drop_index('idx_analyses_high_confidence', table_name='analyses')
    op.drop_index('idx_analyses_created_at', table_name='analyses')
    op.drop_index('idx_analyses_quality_score', table_name='analyses')
    op.drop_index('idx_analyses_confidence', table_name='analyses')
    op.drop_index('idx_analyses_user_created', table_name='analyses')
    op.drop_index('idx_analyses_meter_id', table_name='analyses')
    op.drop_index('idx_analyses_user_id', table_name='analyses')
    op.drop_index('idx_analyses_verse_hash', table_name='analyses')

    op.drop_index('idx_meter_variants_meter_pattern', table_name='meter_variants')
    op.drop_index('idx_meter_variants_meter_id', table_name='meter_variants')

    op.drop_index('idx_meters_description_fts', table_name='meters')
    op.drop_index('idx_meters_pattern', table_name='meters')
    op.drop_index('idx_meters_name_en', table_name='meters')
    op.drop_index('idx_meters_name_ar', table_name='meters')

    op.drop_index('idx_user_roles_unique', table_name='user_roles')
    op.drop_index('idx_user_roles_user_role', table_name='user_roles')
    op.drop_index('idx_user_roles_role', table_name='user_roles')
    op.drop_index('idx_user_roles_user_id', table_name='user_roles')

    op.drop_index('idx_users_created_at', table_name='users')
    op.drop_index('idx_users_last_login', table_name='users')
    op.drop_index('idx_users_level', table_name='users')
    op.drop_index('idx_users_xp', table_name='users')
    op.drop_index('idx_users_username', table_name='users')
    op.drop_index('idx_users_email', table_name='users')
```

---

## 5. Index Maintenance

### Monitoring Index Usage

```sql
-- Check index usage statistics
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Find unused indexes (candidates for removal)
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND idx_scan = 0
  AND indexname NOT LIKE '%_pkey'  -- Exclude primary keys
ORDER BY pg_relation_size(indexrelid) DESC;

-- Index size (disk usage)
SELECT
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Index Bloat (Rebuild When Needed)

```sql
-- Rebuild bloated index
REINDEX INDEX CONCURRENTLY idx_analyses_verse_hash;

-- Rebuild all indexes on a table (during maintenance window)
REINDEX TABLE CONCURRENTLY analyses;
```

### Vacuum and Analyze

```bash
# Run weekly (automate with cron)
psql $DATABASE_URL -c "VACUUM ANALYZE;"

# For specific table after bulk insert
psql $DATABASE_URL -c "VACUUM ANALYZE analyses;"
```

---

## 6. Testing Index Performance

### Benchmark Script: `scripts/test_indexes.sql`

```sql
-- ============================================================
-- INDEX PERFORMANCE TESTING
-- ============================================================

-- Enable timing
\timing on

-- Test 1: Email lookup (should use idx_users_email)
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'test@example.com';
-- Expected: Index Scan using idx_users_email (cost=0.28..8.29)

-- Test 2: Cache lookup (should use idx_analyses_verse_hash)
EXPLAIN ANALYZE
SELECT * FROM analyses WHERE verse_text_hash = 'abc123...';
-- Expected: Index Scan using idx_analyses_verse_hash (cost=0.28..8.29)

-- Test 3: User analysis history (should use idx_analyses_user_created)
EXPLAIN ANALYZE
SELECT * FROM analyses
WHERE user_id = 42
ORDER BY created_at DESC
LIMIT 20;
-- Expected: Index Scan using idx_analyses_user_created (cost=0.29..1000.00)

-- Test 4: Leaderboard (should use idx_users_xp)
EXPLAIN ANALYZE
SELECT username, xp FROM users
ORDER BY xp DESC
LIMIT 100;
-- Expected: Index Scan using idx_users_xp (cost=0.28..1500.00)

-- Test 5: Full-text search (should use idx_meters_description_fts)
EXPLAIN ANALYZE
SELECT * FROM meters
WHERE to_tsvector('arabic', description) @@ to_tsquery('arabic', 'شعر');
-- Expected: Bitmap Heap Scan + Bitmap Index Scan using idx_meters_description_fts
```

**Run tests:**
```bash
psql $DATABASE_URL < scripts/test_indexes.sql
```

**Success Criteria:**
- All queries use expected index (check EXPLAIN ANALYZE output)
- Query times meet performance targets (<20ms for most)
- No sequential scans on large tables

---

## 7. Index Size Estimates

### Expected Disk Usage (at scale)

| Index | Rows (1M users) | Size | Critical? |
|-------|----------------|------|-----------|
| idx_users_email | 1M | ~50 MB | ✅ Yes |
| idx_users_xp | 1M | ~20 MB | ⚠️ Medium |
| idx_analyses_verse_hash | 10M | ~500 MB | ✅ Yes |
| idx_analyses_user_created | 10M | ~300 MB | ✅ Yes |
| idx_poems_fulltext | 100k | ~200 MB | ⚠️ Medium |

**Total Index Size (Phase 1):** ~1 GB at 1M users, 10M analyses

**Storage Planning:**
- Phase 1 (1k users): <100 MB
- Phase 2 (10k users): ~500 MB
- Phase 3 (100k users): ~5 GB
- Scale (1M users): ~50 GB

---

## 8. Deployment Checklist

### Phase 1 MVP Launch

- [ ] Run Alembic migration `002_add_core_indexes.py`
- [ ] Verify all indexes created: `\di` in psql
- [ ] Run benchmark tests: `scripts/test_indexes.sql`
- [ ] Check EXPLAIN ANALYZE for critical queries
- [ ] Monitor index usage in production (pg_stat_user_indexes)
- [ ] Setup weekly VACUUM ANALYZE cron job

### Post-Launch Monitoring

- [ ] **Week 1:** Check idx_analyses_verse_hash hit rate (should be >40%)
- [ ] **Month 1:** Review unused indexes (idx_scan = 0)
- [ ] **Quarter 1:** Identify slow queries and add missing indexes
- [ ] **Yearly:** Rebuild indexes to reduce bloat (REINDEX CONCURRENTLY)

---

## 9. Advanced Indexing (Future)

### Partial Indexes (When Needed)

```sql
-- Index only active users (95% of queries filter on active)
CREATE INDEX idx_users_active_created
ON users(created_at DESC)
WHERE is_active = true;

-- Index only public poems (90% of queries)
CREATE INDEX idx_poems_public_created
ON poems(created_at DESC)
WHERE visibility = 'public';
```

### Covering Indexes (Include Columns)

```sql
-- PostgreSQL 11+ supports INCLUDE for covering indexes
CREATE INDEX idx_users_email_with_password
ON users(email)
INCLUDE (password_hash);
-- Avoids table lookup when fetching password for login
```

### Expression Indexes

```sql
-- Index for case-insensitive username search
CREATE INDEX idx_users_username_lower
ON users(LOWER(username));

-- Query:
SELECT * FROM users WHERE LOWER(username) = 'john_doe';
```

---

## 10. Summary & Recommendations

### ✅ Approved Index Strategy

**Phase 1 (MVP):**
- 18 indexes on 6 core tables
- Estimated size: <100 MB
- Expected performance: All queries <20ms

**Critical Indexes (Must Have):**
1. `idx_analyses_verse_hash` - Cache lookup (every request)
2. `idx_users_email` - Login (every session start)
3. `idx_analyses_user_created` - User history (frequent)

**Monitor After Launch:**
- Cache hit rate (via idx_analyses_verse_hash scans)
- Login latency (via idx_users_email)
- Slow query log (identify missing indexes)

---

## Approval Status

✅ **APPROVED FOR PRODUCTION**

**Reviewed by:** Senior Software Architect
**Approval Date:** November 9, 2025
**Next Review:** After 1 million analyses (validate index hit rates)

**Critical Action Required:**
- [ ] Run migration `002_add_core_indexes.py` in staging
- [ ] Test all critical queries with EXPLAIN ANALYZE
- [ ] Add index monitoring to Grafana dashboard
- [ ] Document index maintenance schedule

---

**Related Documents:**
- [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md) - Schema design
- [PERFORMANCE_TARGETS.md](./PERFORMANCE_TARGETS.md) - Performance SLAs
- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Deployment procedures
