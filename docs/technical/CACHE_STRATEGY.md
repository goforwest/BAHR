# 🗄️ Cache Strategy & Invalidation
## Redis Caching Architecture for BAHR

**Last Updated:** November 9, 2025  
**Status:** Production-Ready  
**Priority:** High (Performance Critical)

---

## 📋 Overview

Comprehensive caching strategy for BAHR platform to achieve:
- **Performance:** P95 latency < 600ms
- **Hit Ratio:** > 40% cache hit rate
- **Consistency:** Stale data prevention
- **Scalability:** Support for 1000+ concurrent users

---

## 🏗️ Cache Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Cache Layers                            │
└─────────────────────────────────────────────────────────────┘

Application Layer
    ├── L1: In-Memory Cache (Python LRU)
    │   └── Pattern definitions (static)
    │
    ├── L2: Redis Cache (Distributed)
    │   ├── Analysis results
    │   ├── User sessions
    │   └── Rate limit counters
    │
    └── L3: Database (PostgreSQL)
        └── Persistent storage

Data Flow:
Request → L1 (check) → L2 (check) → L3 (fetch) → L2 (set) → L1 (set) → Response
```

---

## 🔑 Cache Key Design

### 1. Analysis Results Cache

```python
# Key Pattern
analysis:{hash}

# Hash Calculation
import hashlib

def generate_cache_key(normalized_text: str, options: dict) -> str:
    """
    Generate deterministic cache key for analysis results.
    
    Args:
        normalized_text: Text after normalization
        options: Analysis options (mode, diacritics, etc.)
    
    Returns:
        Redis key string
    """
    # Include only relevant options that affect output
    cache_inputs = {
        'text': normalized_text,
        'mode': options.get('analysis_mode', 'accurate'),
        'diacritics': options.get('remove_diacritics', True)
    }
    
    # Create deterministic JSON string
    canonical = json.dumps(cache_inputs, sort_keys=True, ensure_ascii=False)
    
    # Hash for key
    text_hash = hashlib.md5(canonical.encode('utf-8')).hexdigest()
    
    return f"analysis:{text_hash}"

# Example
# Input: "قفا نبك من ذكرى حبيب ومنزل"
# Key: "analysis:a1b2c3d4e5f6..."
```

### 2. User Session Cache

```python
# Key Pattern
session:{user_id}

# Example
session:12345
session:67890
```

### 3. Rate Limit Cache

```python
# Key Pattern
ratelimit:{identifier}:{window}

# Sliding Window Implementation
ratelimit:ip:192.168.1.1:1699545600
ratelimit:user:12345:1699545600

# Window = Unix timestamp rounded to hour
window = int(time.time()) // 3600 * 3600
```

### 4. Meter Patterns Cache

```python
# Key Pattern (In-Memory Only)
meter_pattern:{meter_name}

# Example
meter_pattern:الطويل
meter_pattern:الكامل
```

---

## ⏱️ TTL (Time-To-Live) Strategy

| Cache Type | TTL | Reasoning |
|-----------|-----|-----------|
| **Analysis Results** | 3600s (1 hour) | Balance freshness vs. performance |
| **User Sessions** | 1800s (30 min) | JWT access token expiry |
| **Rate Limit Counters** | 3600s (1 hour) | Sliding window period |
| **Meter Patterns** | ∞ (permanent) | Static reference data |
| **Settings** | 300s (5 min) | Allow dynamic config updates |

### TTL Configuration

```python
# app/core/cache/ttl.py
from enum import Enum

class CacheTTL(Enum):
    """Cache TTL values in seconds"""
    ANALYSIS = 3600      # 1 hour
    SESSION = 1800       # 30 minutes
    RATE_LIMIT = 3600    # 1 hour
    SETTINGS = 300       # 5 minutes
    PERMANENT = -1       # Never expire
```

---

## 🔄 Cache Invalidation Strategies

### 1. Time-Based Invalidation (Primary)

All caches use TTL for automatic expiration.

```python
# Redis SET with TTL
redis_client.setex(
    key="analysis:abc123",
    time=CacheTTL.ANALYSIS.value,
    value=json.dumps(result)
)
```

### 2. Event-Based Invalidation

```python
# Events that trigger cache invalidation
INVALIDATION_EVENTS = {
    'user_logout': ['session:{user_id}'],
    'settings_update': ['settings:*'],
    'meter_update': ['meter_pattern:*'],  # Rare, admin only
}

async def invalidate_cache(event: str, **kwargs):
    """
    Invalidate cache based on events.
    
    Args:
        event: Event name
        **kwargs: Event-specific parameters
    """
    if event == 'user_logout':
        user_id = kwargs['user_id']
        await redis_client.delete(f"session:{user_id}")
    
    elif event == 'settings_update':
        # Delete all settings keys
        keys = await redis_client.keys("settings:*")
        if keys:
            await redis_client.delete(*keys)
    
    elif event == 'meter_update':
        meter_name = kwargs.get('meter_name')
        if meter_name:
            # In-memory cache, restart required
            logger.warning(f"Meter {meter_name} updated - restart required")
```

### 3. Manual Invalidation (Admin)

```python
# Admin endpoint for cache clearing
@router.post("/api/v1/admin/cache/clear")
async def clear_cache(
    cache_type: str,
    current_user: User = Depends(require_admin)
):
    """
    Clear specific cache type.
    
    Args:
        cache_type: One of ['analysis', 'sessions', 'all']
    """
    if cache_type == 'analysis':
        keys = await redis_client.keys("analysis:*")
        await redis_client.delete(*keys)
        return {"cleared": len(keys)}
    
    elif cache_type == 'sessions':
        keys = await redis_client.keys("session:*")
        await redis_client.delete(*keys)
        return {"cleared": len(keys)}
    
    elif cache_type == 'all':
        await redis_client.flushdb()
        return {"cleared": "all"}
    
    raise ValueError(f"Invalid cache_type: {cache_type}")
```

### 4. Stale-While-Revalidate Pattern

For analysis results with high traffic:

```python
async def get_with_revalidation(key: str, ttl_short: int = 60):
    """
    Return cached value immediately, refresh in background if stale.
    
    Args:
        key: Cache key
        ttl_short: Grace period for stale data
    """
    # Check cache
    cached = await redis_client.get(key)
    
    if cached:
        # Check if approaching expiry
        ttl_remaining = await redis_client.ttl(key)
        
        if ttl_remaining < ttl_short:
            # Stale soon - trigger background refresh
            asyncio.create_task(refresh_cache(key))
        
        return json.loads(cached)
    
    # Cache miss - fetch and store
    result = await fetch_from_db(key)
    await redis_client.setex(key, CacheTTL.ANALYSIS.value, json.dumps(result))
    return result
```

---

## 📊 Cache Monitoring

### Metrics to Track

```python
# Prometheus metrics
from prometheus_client import Counter, Gauge, Histogram

cache_hit_total = Counter(
    'bahr_cache_hit_total',
    'Total cache hits',
    ['cache_type']
)

cache_miss_total = Counter(
    'bahr_cache_miss_total',
    'Total cache misses',
    ['cache_type']
)

cache_size_bytes = Gauge(
    'bahr_cache_size_bytes',
    'Current cache size in bytes',
    ['cache_type']
)

cache_operation_duration = Histogram(
    'bahr_cache_operation_duration_seconds',
    'Cache operation latency',
    ['operation']  # get, set, delete
)
```

### Cache Hit Ratio Calculation

```python
def calculate_hit_ratio() -> float:
    """
    Calculate cache hit ratio from metrics.
    
    Returns:
        Hit ratio (0.0 - 1.0)
    """
    hits = cache_hit_total._value.sum()
    misses = cache_miss_total._value.sum()
    total = hits + misses
    
    if total == 0:
        return 0.0
    
    return hits / total

# Target: > 0.40 (40% hit ratio)
```

---

## 🛡️ Cache Consistency Strategies

### 1. Write-Through Cache

```python
async def save_analysis(analysis: AnalysisResult, user_id: int = None):
    """
    Save analysis with write-through caching.
    
    Steps:
    1. Write to database
    2. Update cache
    3. Return result
    """
    # 1. Persist to database
    db_result = await db.analyses.create(analysis)
    
    # 2. Update cache
    cache_key = generate_cache_key(analysis.normalized_text, analysis.options)
    await redis_client.setex(
        cache_key,
        CacheTTL.ANALYSIS.value,
        json.dumps(analysis.dict())
    )
    
    # 3. Return
    return db_result
```

### 2. Cache-Aside (Lazy Loading)

```python
async def get_analysis(cache_key: str):
    """
    Get analysis with cache-aside pattern.
    
    Steps:
    1. Check cache
    2. If miss, fetch from DB
    3. Update cache
    4. Return result
    """
    # 1. Check cache
    cached = await redis_client.get(cache_key)
    if cached:
        cache_hit_total.labels(cache_type='analysis').inc()
        return json.loads(cached)
    
    # 2. Cache miss
    cache_miss_total.labels(cache_type='analysis').inc()
    
    # 3. Fetch from database
    result = await db.analyses.get_by_cache_key(cache_key)
    
    if result:
        # 4. Update cache
        await redis_client.setex(
            cache_key,
            CacheTTL.ANALYSIS.value,
            json.dumps(result)
        )
    
    return result
```

---

## 🚨 Cache Failure Handling

### Graceful Degradation

```python
async def get_with_fallback(key: str, fallback_fn):
    """
    Get from cache with fallback to database.
    
    Args:
        key: Cache key
        fallback_fn: Function to call on cache failure
    """
    try:
        cached = await redis_client.get(key)
        if cached:
            return json.loads(cached)
    except redis.ConnectionError:
        logger.error("Redis connection failed - using fallback")
        # Continue to fallback
    except redis.TimeoutError:
        logger.error("Redis timeout - using fallback")
        # Continue to fallback
    
    # Fallback to database
    return await fallback_fn()
```

### Circuit Breaker for Redis

```python
from datetime import datetime, timedelta

class RedisCircuitBreaker:
    """
    Circuit breaker for Redis to prevent cascading failures.
    """
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half_open
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == 'open':
            if self._should_attempt_reset():
                self.state = 'half_open'
            else:
                raise CircuitBreakerOpenError("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Reset on successful call"""
        self.failures = 0
        self.state = 'closed'
    
    def _on_failure(self):
        """Increment failures and potentially open circuit"""
        self.failures += 1
        self.last_failure_time = datetime.now()
        
        if self.failures >= self.failure_threshold:
            self.state = 'open'
            logger.error(f"Circuit breaker opened after {self.failures} failures")
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to retry"""
        if self.last_failure_time is None:
            return True
        
        elapsed = (datetime.now() - self.last_failure_time).seconds
        return elapsed >= self.timeout
```

---

## ⚙️ Configuration

```python
# app/core/cache/config.py
from pydantic_settings import BaseSettings

class CacheSettings(BaseSettings):
    """Cache configuration"""
    
    # Redis connection
    redis_url: str = "redis://localhost:6379/0"
    redis_max_connections: int = 50
    redis_socket_timeout: int = 5
    redis_socket_connect_timeout: int = 5
    
    # Cache behavior
    cache_enabled: bool = True
    cache_default_ttl: int = 3600
    
    # Performance
    cache_compression: bool = False  # Enable for large objects
    cache_max_size_mb: int = 512
    
    # Monitoring
    cache_hit_ratio_target: float = 0.40
    cache_eviction_policy: str = "allkeys-lru"
    
    class Config:
        env_prefix = "CACHE_"

cache_settings = CacheSettings()
```

---

## 📈 Performance Tuning

### 1. Cache Warming (Optional)

```python
async def warm_cache_on_startup():
    """
    Pre-populate cache with common queries on application startup.
    """
    logger.info("Warming cache...")
    
    # Load meter patterns (static data)
    meters = await db.meters.get_all()
    for meter in meters:
        key = f"meter_pattern:{meter.name}"
        await redis_client.set(key, json.dumps(meter.pattern))
    
    logger.info(f"Cache warmed with {len(meters)} meter patterns")
```

### 2. Compression for Large Objects

```python
import gzip
import base64

async def set_compressed(key: str, value: str, ttl: int):
    """
    Store compressed value in cache.
    
    Use for large objects (> 1KB).
    """
    compressed = gzip.compress(value.encode('utf-8'))
    encoded = base64.b64encode(compressed).decode('ascii')
    
    await redis_client.setex(key, ttl, encoded)

async def get_compressed(key: str) -> str:
    """Retrieve and decompress cached value"""
    encoded = await redis_client.get(key)
    if not encoded:
        return None
    
    compressed = base64.b64decode(encoded)
    return gzip.decompress(compressed).decode('utf-8')
```

---

## ✅ Cache Checklist

### Week 1 Implementation
- [ ] Redis connection configured
- [ ] Basic cache key generation
- [ ] Analysis results caching
- [ ] TTL configuration
- [ ] Cache metrics (hit/miss counters)

### Week 2 Enhancement
- [ ] Rate limiting cache
- [ ] Session caching
- [ ] Cache invalidation events
- [ ] Circuit breaker implementation
- [ ] Cache warming on startup

### Week 3 Optimization
- [ ] Compression for large objects
- [ ] Stale-while-revalidate pattern
- [ ] Admin cache clearing endpoint
- [ ] Cache size monitoring
- [ ] Hit ratio alerting

---

## 🔗 Related Documentation

- `ARCHITECTURE_OVERVIEW.md` - Overall system design
- `PERFORMANCE_TARGETS.md` - Performance requirements
- `feature-caching-redis.md` - Implementation guide
- `MONITORING_INTEGRATION.md` - Metrics and alerting

---

**References:**
- Redis Best Practices: https://redis.io/docs/manual/patterns/
- Cache Invalidation Strategies: https://martinfowler.com/bliki/TwoHardThings.html
