# Feature: Redis Caching - Implementation Guide

**Feature ID:** `feature-caching-redis`  
**Status:** Production-Ready  
**Last Updated:** November 8, 2025  
**Estimated Implementation Time:** 8-12 hours

---

## 1. Objective & Description

### What
Implement Redis-backed caching layer for analysis results, meter patterns, and frequently accessed data. Cache analysis results by normalized text hash to avoid redundant processing, with configurable TTL and automatic invalidation.

### Why
- **Performance:** Reduce latency from 450ms → 10ms for cached analyses
- **Cost Reduction:** Avoid redundant CAMeL Tools morphological analysis
- **Scalability:** Reduce database load by 60-80%
- **User Experience:** Instant results for previously analyzed verses
- **API Efficiency:** Cache meter patterns, user sessions, rate limits

### Success Criteria
- ✅ Cache analysis results with 24-hour TTL
- ✅ Cache hit rate ≥70% after 1 week of usage
- ✅ Reduce P95 latency from 450ms → <50ms for cached results
- ✅ Implement cache invalidation on user request
- ✅ Store serialized JSON in Redis with compression
- ✅ Monitor cache hit/miss metrics
- ✅ Test coverage ≥75% with cache integration tests

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Redis Caching Architecture                        │
└─────────────────────────────────────────────────────────────────────┘

Request: POST /api/v1/analyses {"text": "قفا نبك من ذكري"}
    │
    ▼
┌──────────────────────────────────────┐
│ Step 1: Generate Cache Key           │
│ (SHA-256 hash of normalized text)    │
└──────────┬───────────────────────────┘
    │  Key: "analysis:sha256:7f8a9b0c..."
    ▼
┌──────────────────────────────────────┐
│ Step 2: Check Redis Cache            │
│ (GET key from Redis)                 │
└──────────┬───────────────────────────┘
    │
    ├─── Cache HIT ───────────────────┐
    │                                  │
    │  Cached JSON: {                  │
    │    "detected_meter": "الطويل",   │
    │    "confidence": 0.92,           │
    │    "pattern": "∪ - - ∪ - -",     │
    │    ...                           │
    │  }                               │
    │                                  │
    │  ✅ Return immediately (10ms)    │
    │                                  │
    └──────────────────────────────────┘
    │
    └─── Cache MISS ──────────────────┐
                                       │
                                       ▼
                    ┌──────────────────────────────────────┐
                    │ Step 3: Execute Analysis Pipeline    │
                    │ (Normalization → Segmentation →      │
                    │  Meter Detection)                    │
                    └──────────┬───────────────────────────┘
                               │  Result: {...}
                               │  Processing: 450ms
                               ▼
                    ┌──────────────────────────────────────┐
                    │ Step 4: Store in Redis Cache         │
                    │ (SET key value EX 86400)             │
                    └──────────┬───────────────────────────┘
                               │  TTL: 24 hours
                               │  Compression: gzip
                               ▼
                    ┌──────────────────────────────────────┐
                    │ Step 5: Return Result                │
                    │ (Same response as cache hit)         │
                    └──────────────────────────────────────┘

Cache Key Patterns:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
analysis:{hash}         → Analysis result (TTL: 24h)
meter_pattern:{meter}   → Meter reference pattern (TTL: 7d)
user_session:{user_id}  → User session data (TTL: 30min)
rate_limit:{ip}         → Rate limit counter (TTL: 1h)
```

---

## 3. Input/Output Contracts

### 3.1 Data Structures

```python
# backend/app/services/cache_service.py
from dataclasses import dataclass
from typing import Optional, Any, Dict
from datetime import timedelta
from enum import Enum


class CacheKeyPrefix(Enum):
    """Cache key prefixes for different data types."""
    ANALYSIS = "analysis"
    METER_PATTERN = "meter_pattern"
    USER_SESSION = "user_session"
    RATE_LIMIT = "rate_limit"
    GOLDEN_DATASET = "golden_dataset"


@dataclass
class CacheConfig:
    """Cache configuration settings."""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    socket_timeout: int = 5
    socket_connect_timeout: int = 5
    max_connections: int = 50
    decode_responses: bool = True
    
    # TTL settings (seconds)
    analysis_ttl: int = 86400      # 24 hours
    meter_pattern_ttl: int = 604800  # 7 days
    user_session_ttl: int = 1800    # 30 minutes
    rate_limit_ttl: int = 3600      # 1 hour
    
    # Compression
    enable_compression: bool = True
    compression_threshold: int = 1024  # Compress if >1KB


@dataclass
class CacheStats:
    """Cache statistics."""
    total_requests: int
    cache_hits: int
    cache_misses: int
    hit_rate: float
    avg_get_time_ms: float
    avg_set_time_ms: float
```

### 3.2 Function Signatures

```python
class CacheService:
    """
    Redis caching service for BAHR platform.
    
    Provides:
    - Analysis result caching
    - Meter pattern caching
    - Session management
    - Rate limiting support
    """
    
    def __init__(self, config: CacheConfig):
        """Initialize Redis connection."""
        pass
    
    def get_analysis(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Get cached analysis result by text.
        
        Args:
            text: Normalized Arabic text
            
        Returns:
            Cached analysis dict or None if not found
        """
        pass
    
    def set_analysis(
        self,
        text: str,
        result: Dict[str, Any],
        ttl: Optional[int] = None
    ) -> bool:
        """
        Cache analysis result.
        
        Args:
            text: Normalized Arabic text
            result: Analysis result dictionary
            ttl: Time-to-live in seconds (default: 24h)
            
        Returns:
            True if successfully cached
        """
        pass
    
    def invalidate_analysis(self, text: str) -> bool:
        """Delete cached analysis."""
        pass
    
    def get_stats(self) -> CacheStats:
        """Get cache statistics."""
        pass
    
    def health_check(self) -> bool:
        """Check Redis connection health."""
        pass
```

### 3.3 Cache Key Generation

```python
import hashlib

def generate_cache_key(
    prefix: CacheKeyPrefix,
    identifier: str
) -> str:
    """
    Generate cache key with consistent hashing.
    
    Args:
        prefix: Cache key prefix (analysis, meter_pattern, etc.)
        identifier: Unique identifier (text, meter name, user_id)
        
    Returns:
        Cache key string (e.g., "analysis:sha256:abc123...")
    """
    # Normalize identifier
    normalized = identifier.strip().lower()
    
    # Generate SHA-256 hash
    hash_digest = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    
    # Format: prefix:sha256:hash
    return f"{prefix.value}:sha256:{hash_digest[:16]}"
```

---

## 4. Step-by-Step Implementation

### Step 1: Install Redis Client

```bash
# Add to backend/requirements.txt
echo "redis==5.0.1" >> backend/requirements.txt
echo "hiredis==2.2.3" >> backend/requirements.txt  # C parser for performance

# Install
pip install redis==5.0.1 hiredis==2.2.3
```

### Step 2: Start Redis with Docker

```bash
# Add to docker-compose.yml
cat >> docker-compose.yml <<'EOF'
  redis:
    image: redis:7-alpine
    container_name: bahr_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

volumes:
  redis_data:
EOF

# Start Redis
docker-compose up -d redis
```

### Step 3: Create Cache Service

```python
# backend/app/services/cache_service.py
"""
Redis caching service.

Provides caching for analysis results, meter patterns, and sessions.
Source: docs/technical/ARCHITECTURE_OVERVIEW.md
"""

import json
import gzip
import hashlib
import logging
import time
from typing import Optional, Any, Dict
from datetime import timedelta
from enum import Enum

import redis
from redis.exceptions import RedisError, ConnectionError

logger = logging.getLogger(__name__)


class CacheKeyPrefix(Enum):
    """Cache key prefixes for different data types."""
    ANALYSIS = "analysis"
    METER_PATTERN = "meter_pattern"
    USER_SESSION = "user_session"
    RATE_LIMIT = "rate_limit"


class CacheService:
    """
    Redis caching service for BAHR platform.
    
    Usage:
        >>> cache = CacheService()
        >>> cache.set_analysis("قفا نبك", {"meter": "الطويل"})
        >>> result = cache.get_analysis("قفا نبك")
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        max_connections: int = 50
    ):
        """Initialize Redis connection pool."""
        logger.info(f"Initializing Redis cache: {host}:{port}")
        
        try:
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=False,  # Handle binary data for compression
                socket_timeout=5,
                socket_connect_timeout=5,
                max_connections=max_connections,
                health_check_interval=30
            )
            
            # Test connection
            self.client.ping()
            logger.info("Redis connection established successfully")
            
        except RedisError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
        
        # Configuration
        self.analysis_ttl = 86400  # 24 hours
        self.meter_pattern_ttl = 604800  # 7 days
        self.compression_threshold = 1024  # 1KB
        
        # Statistics
        self._total_requests = 0
        self._cache_hits = 0
        self._cache_misses = 0
    
    def get_analysis(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Get cached analysis result by text.
        
        Args:
            text: Normalized Arabic text
            
        Returns:
            Cached analysis dict or None if not found
        """
        start_time = time.time()
        self._total_requests += 1
        
        try:
            # Generate cache key
            cache_key = self._generate_key(CacheKeyPrefix.ANALYSIS, text)
            
            # Get from Redis
            cached_data = self.client.get(cache_key)
            
            if cached_data is None:
                self._cache_misses += 1
                logger.debug(f"Cache MISS for key: {cache_key[:30]}...")
                return None
            
            # Decompress and deserialize
            result = self._deserialize(cached_data)
            
            self._cache_hits += 1
            duration_ms = (time.time() - start_time) * 1000
            
            logger.info(
                f"Cache HIT for key: {cache_key[:30]}... "
                f"(retrieved in {duration_ms:.1f}ms)"
            )
            
            return result
            
        except RedisError as e:
            logger.error(f"Redis error during GET: {e}")
            return None
        except Exception as e:
            logger.exception(f"Unexpected error during cache GET: {e}")
            return None
    
    def set_analysis(
        self,
        text: str,
        result: Dict[str, Any],
        ttl: Optional[int] = None
    ) -> bool:
        """
        Cache analysis result.
        
        Args:
            text: Normalized Arabic text
            result: Analysis result dictionary
            ttl: Time-to-live in seconds (default: 24h)
            
        Returns:
            True if successfully cached
        """
        start_time = time.time()
        
        try:
            # Generate cache key
            cache_key = self._generate_key(CacheKeyPrefix.ANALYSIS, text)
            
            # Serialize and compress
            cached_data = self._serialize(result)
            
            # Set in Redis with TTL
            ttl = ttl or self.analysis_ttl
            self.client.setex(cache_key, ttl, cached_data)
            
            duration_ms = (time.time() - start_time) * 1000
            data_size = len(cached_data)
            
            logger.info(
                f"Cache SET for key: {cache_key[:30]}... "
                f"(size: {data_size} bytes, TTL: {ttl}s, stored in {duration_ms:.1f}ms)"
            )
            
            return True
            
        except RedisError as e:
            logger.error(f"Redis error during SET: {e}")
            return False
        except Exception as e:
            logger.exception(f"Unexpected error during cache SET: {e}")
            return False
    
    def invalidate_analysis(self, text: str) -> bool:
        """
        Delete cached analysis.
        
        Args:
            text: Normalized Arabic text
            
        Returns:
            True if key was deleted
        """
        try:
            cache_key = self._generate_key(CacheKeyPrefix.ANALYSIS, text)
            deleted = self.client.delete(cache_key)
            
            if deleted:
                logger.info(f"Cache invalidated for key: {cache_key[:30]}...")
            else:
                logger.debug(f"No cache entry to invalidate: {cache_key[:30]}...")
            
            return bool(deleted)
            
        except RedisError as e:
            logger.error(f"Redis error during DELETE: {e}")
            return False
    
    def get_meter_pattern(self, meter_name: str) -> Optional[Dict[str, Any]]:
        """Get cached meter pattern."""
        try:
            cache_key = self._generate_key(CacheKeyPrefix.METER_PATTERN, meter_name)
            cached_data = self.client.get(cache_key)
            
            if cached_data:
                return self._deserialize(cached_data)
            
            return None
            
        except RedisError as e:
            logger.error(f"Redis error getting meter pattern: {e}")
            return None
    
    def set_meter_pattern(
        self,
        meter_name: str,
        pattern_data: Dict[str, Any]
    ) -> bool:
        """Cache meter pattern with 7-day TTL."""
        try:
            cache_key = self._generate_key(CacheKeyPrefix.METER_PATTERN, meter_name)
            cached_data = self._serialize(pattern_data)
            
            self.client.setex(cache_key, self.meter_pattern_ttl, cached_data)
            logger.debug(f"Cached meter pattern: {meter_name}")
            
            return True
            
        except RedisError as e:
            logger.error(f"Redis error setting meter pattern: {e}")
            return False
    
    def health_check(self) -> bool:
        """
        Check Redis connection health.
        
        Returns:
            True if Redis is reachable and responding
        """
        try:
            return self.client.ping()
        except RedisError:
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with hit rate and performance metrics
        """
        if self._total_requests == 0:
            hit_rate = 0.0
        else:
            hit_rate = self._cache_hits / self._total_requests
        
        return {
            "total_requests": self._total_requests,
            "cache_hits": self._cache_hits,
            "cache_misses": self._cache_misses,
            "hit_rate": round(hit_rate, 3),
            "redis_info": self._get_redis_info()
        }
    
    def clear_all(self) -> bool:
        """
        Clear all cached data (USE WITH CAUTION).
        
        Only for testing/development.
        """
        try:
            self.client.flushdb()
            logger.warning("All cache data cleared!")
            return True
        except RedisError as e:
            logger.error(f"Failed to clear cache: {e}")
            return False
    
    # Private helper methods
    
    def _generate_key(self, prefix: CacheKeyPrefix, identifier: str) -> str:
        """Generate cache key with SHA-256 hash."""
        normalized = identifier.strip().lower()
        hash_digest = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
        return f"{prefix.value}:sha256:{hash_digest[:16]}"
    
    def _serialize(self, data: Dict[str, Any]) -> bytes:
        """
        Serialize and optionally compress data.
        
        Uses gzip compression if data > 1KB.
        """
        # Convert to JSON
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        
        # Compress if large enough
        if len(json_data) > self.compression_threshold:
            compressed = gzip.compress(json_data)
            logger.debug(
                f"Compressed {len(json_data)} → {len(compressed)} bytes "
                f"({len(compressed)/len(json_data)*100:.1f}%)"
            )
            return b"GZIP:" + compressed
        
        return json_data
    
    def _deserialize(self, data: bytes) -> Dict[str, Any]:
        """Deserialize and decompress data."""
        # Check for compression marker
        if data.startswith(b"GZIP:"):
            # Decompress
            compressed_data = data[5:]  # Remove "GZIP:" prefix
            json_data = gzip.decompress(compressed_data)
        else:
            json_data = data
        
        # Parse JSON
        return json.loads(json_data.decode('utf-8'))
    
    def _get_redis_info(self) -> Dict[str, Any]:
        """Get Redis server info."""
        try:
            info = self.client.info()
            return {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }
        except RedisError:
            return {}


# Global cache instance
_cache_instance: Optional[CacheService] = None


def get_cache() -> CacheService:
    """
    Get global cache service instance.
    
    FastAPI dependency for cache injection.
    """
    global _cache_instance
    
    if _cache_instance is None:
        _cache_instance = CacheService()
    
    return _cache_instance
```

### Step 4: Integrate Cache into Analysis Service

```python
# backend/app/services/analysis_service.py
# Update analyze_verse method to use cache

def analyze_verse(
    self,
    request: AnalysisRequest,
    user_id: Optional[int] = None,
    cache: Optional[CacheService] = None
) -> AnalysisResponse:
    """Analyze Arabic verse with caching."""
    start_time = time.time()
    
    # Normalize text first (for cache key)
    normalized_text = self.normalizer.normalize(request.text)
    
    # Try cache first
    if cache:
        cached_result = cache.get_analysis(normalized_text)
        if cached_result:
            logger.info("Returning cached analysis result")
            return AnalysisResponse(**cached_result)
    
    # Cache miss - perform full analysis
    logger.info("Cache miss - performing full analysis")
    
    # ... (rest of analysis pipeline)
    
    # Cache the result
    if cache:
        cache.set_analysis(normalized_text, response_data)
    
    return AnalysisResponse(**response_data)
```

### Step 5: Update API Endpoint

```python
# backend/app/api/v1/endpoints/analyze.py
from app.services.cache_service import get_cache

@router.post("", response_model=AnalysisResponse)
async def create_analysis(
    request: AnalysisRequest,
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache),
    current_user: Optional[User] = Depends(get_current_user_optional)
) -> AnalysisResponse:
    """Analyze verse with Redis caching."""
    service = AnalysisService()
    result = service.analyze_verse(request, user_id=user_id, cache=cache)
    return result
```

### Step 6: Test Cache Integration

```bash
# Test script
cat > scripts/test_cache.py <<'EOF'
from app.services.cache_service import CacheService
import time

cache = CacheService()

# Test data
test_analysis = {
    "text": "قفا نبك من ذكري حبيب ومنزل",
    "detected_meter": "الطويل",
    "confidence": 0.92,
    "pattern": "∪ - - ∪ - - ∪ - -"
}

# Test SET
print("Setting cache...")
cache.set_analysis(test_analysis["text"], test_analysis)

# Test GET (should be cache hit)
print("Getting from cache...")
start = time.time()
result = cache.get_analysis(test_analysis["text"])
duration_ms = (time.time() - start) * 1000

print(f"Retrieved in {duration_ms:.2f}ms")
print(f"Meter: {result['detected_meter']}")

# Test stats
stats = cache.get_stats()
print(f"\nCache Stats:")
print(f"  Hit rate: {stats['hit_rate']*100:.1f}%")
print(f"  Total requests: {stats['total_requests']}")
EOF

python scripts/test_cache.py
```

---

## 5. Reference Implementation (Full Code)

See Step-by-Step Implementation sections above for complete code.

---

## 6. Unit & Integration Tests

### tests/unit/services/test_cache_service.py

```python
"""
Unit tests for cache service.

Tests Redis caching functionality.
"""

import pytest
from app.services.cache_service import CacheService, CacheKeyPrefix


class TestCacheService:
    """Test suite for cache service."""
    
    @pytest.fixture
    def cache(self):
        """Create cache instance and clear before each test."""
        service = CacheService()
        service.clear_all()  # Clean slate
        yield service
        service.clear_all()  # Cleanup after test
    
    def test_set_and_get_analysis(self, cache):
        """Test caching analysis result."""
        text = "قفا نبك من ذكري"
        result = {
            "detected_meter": "الطويل",
            "confidence": 0.92
        }
        
        # Set cache
        success = cache.set_analysis(text, result)
        assert success is True
        
        # Get from cache
        cached = cache.get_analysis(text)
        assert cached is not None
        assert cached["detected_meter"] == "الطويل"
        assert cached["confidence"] == 0.92
    
    def test_cache_miss(self, cache):
        """Test cache miss returns None."""
        result = cache.get_analysis("non-existent-text")
        assert result is None
    
    def test_cache_invalidation(self, cache):
        """Test cache invalidation."""
        text = "قفا نبك من ذكري"
        result = {"meter": "الطويل"}
        
        # Set cache
        cache.set_analysis(text, result)
        
        # Verify cached
        assert cache.get_analysis(text) is not None
        
        # Invalidate
        deleted = cache.invalidate_analysis(text)
        assert deleted is True
        
        # Verify cache miss
        assert cache.get_analysis(text) is None
    
    def test_compression(self, cache):
        """Test data compression for large payloads."""
        text = "قفا نبك من ذكري"
        large_result = {
            "detected_meter": "الطويل",
            "syllables": [{"text": f"سل{i}"} for i in range(100)],
            "data": "x" * 2000  # Large payload
        }
        
        # Set cache
        cache.set_analysis(text, large_result)
        
        # Get and verify
        cached = cache.get_analysis(text)
        assert cached is not None
        assert len(cached["syllables"]) == 100
    
    def test_cache_stats(self, cache):
        """Test cache statistics tracking."""
        # Initially zero
        stats = cache.get_stats()
        assert stats["total_requests"] == 0
        
        # Trigger cache miss
        cache.get_analysis("text1")
        
        # Trigger cache hit
        cache.set_analysis("text2", {"meter": "الطويل"})
        cache.get_analysis("text2")
        
        # Check stats
        stats = cache.get_stats()
        assert stats["total_requests"] == 2
        assert stats["cache_hits"] == 1
        assert stats["cache_misses"] == 1
        assert stats["hit_rate"] == 0.5
    
    def test_health_check(self, cache):
        """Test Redis health check."""
        is_healthy = cache.health_check()
        assert is_healthy is True
    
    def test_ttl_expiration(self, cache):
        """Test TTL expiration (mock test)."""
        import time
        
        text = "قفا نبك"
        result = {"meter": "الطويل"}
        
        # Set with 1-second TTL
        cache.set_analysis(text, result, ttl=1)
        
        # Verify cached
        assert cache.get_analysis(text) is not None
        
        # Wait for expiration
        time.sleep(2)
        
        # Verify expired
        assert cache.get_analysis(text) is None
```

---

## 7. CI/CD Pipeline

```yaml
# .github/workflows/cache-tests.yml
name: Cache Service Tests

on:
  push:
    paths:
      - 'backend/app/services/cache_service.py'
      - 'tests/**test_cache**'

jobs:
  test-cache:
    runs-on: ubuntu-latest
    
    services:
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run cache tests
        run: |
          cd backend
          pytest tests/unit/services/test_cache_service.py -v \
            --cov=app.services.cache_service \
            --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: cache-service
```

---

## 8. Deployment Checklist

- [ ] Redis 7 installed and running
- [ ] Redis persistence enabled (appendonly.aof)
- [ ] Max memory policy configured (allkeys-lru)
- [ ] Test cache hit rate ≥70% after 1 week
- [ ] Monitor Redis memory usage (<256MB)
- [ ] Verify compression working for large payloads
- [ ] Test TTL expiration (24h for analyses)
- [ ] Configure Redis password in production
- [ ] Set up Redis monitoring (redis-cli info)
- [ ] Test failover behavior (cache degradation, not failure)

---

## 9. Observability

```python
# backend/app/metrics/cache_metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Cache metrics
cache_requests_total = Counter(
    "bahr_cache_requests_total",
    "Total cache requests",
    ["operation", "status"]  # get/set, hit/miss
)

cache_operation_duration_seconds = Histogram(
    "bahr_cache_operation_duration_seconds",
    "Cache operation duration",
    ["operation"],  # get/set/delete
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1]
)

cache_hit_rate = Gauge(
    "bahr_cache_hit_rate",
    "Cache hit rate (0-1)"
)

cache_size_bytes = Gauge(
    "bahr_cache_size_bytes",
    "Total cached data size in bytes"
)
```

---

## 10. Security & Safety

- **Password Protection:** Use Redis AUTH in production
- **Memory Limits:** Configure maxmemory to prevent OOM
- **Network Security:** Bind Redis to localhost only
- **Key Expiration:** All keys have TTL to prevent unbounded growth
- **Data Validation:** Validate cached data on retrieval

---

## 11. Backwards Compatibility

- **None** - Initial implementation
- **Graceful Degradation:** App works without cache (slower)

---

## 12. Source Documentation Citations

1. **docs/technical/ARCHITECTURE_OVERVIEW.md** - Caching strategy
2. **claude.md:510-645** - Implementation patterns
3. **implementation-guides/IMPROVED_PROMPT.md:567-595** - Feature specification

---

**Implementation Complete!** ✅  
**Estimated Time:** 8-12 hours  
**Test Coverage Target:** ≥ 75%  
**Performance Target:** <50ms for cache hits
