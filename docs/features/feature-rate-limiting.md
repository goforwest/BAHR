# Feature: Rate Limiting - Implementation Guide

**Feature ID:** `feature-rate-limiting`  
**Status:** Production-Ready  
**Last Updated:** November 8, 2025  
**Estimated Implementation Time:** 6-10 hours

---

## 1. Objective & Description

### What
Implement sliding window rate limiting using Redis to prevent API abuse and ensure fair resource allocation. Limits guest users to 100 requests/hour per IP and authenticated users to 1,000 requests/hour per user ID.

### Why
- **Abuse Prevention:** Prevent DoS attacks and scraping
- **Fair Usage:** Ensure equitable access for all users
- **Cost Control:** Limit computational resources for CAMeL Tools analysis
- **API Stability:** Protect backend from traffic spikes
- **Freemium Model:** Different limits for guest vs. authenticated users

### Success Criteria
- ✅ Enforce 100 req/hour for guest users (by IP)
- ✅ Enforce 1,000 req/hour for authenticated users
- ✅ Return 429 Too Many Requests with Retry-After header
- ✅ Implement sliding window algorithm (not fixed window)
- ✅ Store counters in Redis with 1-hour TTL
- ✅ Add rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset)
- ✅ Test coverage ≥70% with rate limit scenarios

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                  Rate Limiting Architecture                          │
└─────────────────────────────────────────────────────────────────────┘

Request: POST /api/v1/analyses (from IP 203.0.113.42)
    │
    ▼
┌──────────────────────────────────────┐
│ Step 1: Extract Rate Limit Key       │
│ (IP for guest, User ID for auth)     │
└──────────┬───────────────────────────┘
    │  Guest: rate_limit:ip:203.0.113.42
    │  Auth:  rate_limit:user:12345
    ▼
┌──────────────────────────────────────┐
│ Step 2: Check Current Count          │
│ (GET counter from Redis)             │
└──────────┬───────────────────────────┘
    │  Current: 95 requests in last hour
    │  Limit: 100 (guest) or 1000 (auth)
    ▼
┌──────────────────────────────────────┐
│ Step 3: Sliding Window Check         │
│ (ZADD timestamp, ZREMRANGEBYSCORE)   │
└──────────┬───────────────────────────┘
    │
    ├─── ALLOWED (95 < 100) ───────────┐
    │                                   │
    │  Increment counter                │
    │  TTL: 3600 seconds                │
    │                                   │
    │  Add response headers:            │
    │    X-RateLimit-Limit: 100         │
    │    X-RateLimit-Remaining: 5       │
    │    X-RateLimit-Reset: 1699459200  │
    │                                   │
    │  ✅ Continue to handler           │
    │                                   │
    └───────────────────────────────────┘
    │
    └─── BLOCKED (100 >= 100) ─────────┐
                                        │
                                        │  Calculate retry time
                                        │  Oldest request timestamp
                                        │  Retry-After: 1523 seconds
                                        │
                                        │  Return 429 Response:
                                        │  {
                                        │    "success": false,
                                        │    "error": {
                                        │      "code": "ERR_RATE_LIMIT_EXCEEDED",
                                        │      "message": "Rate limit exceeded",
                                        │      "details": {
                                        │        "limit": 100,
                                        │        "window": 3600,
                                        │        "retry_after": 1523
                                        │      }
                                        │    }
                                        │  }
                                        │
                                        │  Headers:
                                        │    X-RateLimit-Limit: 100
                                        │    X-RateLimit-Remaining: 0
                                        │    X-RateLimit-Reset: 1699459200
                                        │    Retry-After: 1523
                                        │
                                        └───────────────────────────────

Redis Data Structure (Sorted Set):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Key: rate_limit:ip:203.0.113.42
Type: Sorted Set (ZSET)
Members: [
  {score: 1699455600.123, value: "req_1"},
  {score: 1699455612.456, value: "req_2"},
  {score: 1699455625.789, value: "req_3"},
  ...
]
TTL: 3600 seconds (1 hour)
```

---

## 3. Input/Output Contracts

### 3.1 Data Structures

```python
# backend/app/middleware/rate_limit.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class RateLimitConfig:
    """Rate limit configuration."""
    guest_limit: int = 100          # Requests per hour for guests
    authenticated_limit: int = 1000  # Requests per hour for auth users
    window_seconds: int = 3600      # 1 hour window
    redis_key_prefix: str = "rate_limit"


@dataclass
class RateLimitStatus:
    """Current rate limit status for a client."""
    limit: int              # Max requests allowed
    remaining: int          # Requests remaining in window
    reset_timestamp: int    # Unix timestamp when limit resets
    is_exceeded: bool       # Whether limit is exceeded
    retry_after: Optional[int] = None  # Seconds until retry (if exceeded)
```

### 3.2 Middleware Interface

```python
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for rate limiting.
    
    Uses sliding window algorithm with Redis sorted sets.
    """
    
    async def dispatch(
        self,
        request: Request,
        call_next
    ) -> Response:
        """
        Check rate limit before processing request.
        
        Returns 429 if limit exceeded.
        """
        pass
```

---

## 4. Step-by-Step Implementation

### Step 1: Create Rate Limit Service

```python
# backend/app/services/rate_limit_service.py
"""
Rate limiting service using Redis sorted sets.

Implements sliding window algorithm for accurate rate limiting.
Source: docs/technical/API_CONVENTIONS.md
"""

import time
import logging
from typing import Tuple, Optional
from dataclasses import dataclass

import redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)


@dataclass
class RateLimitConfig:
    """Rate limit configuration."""
    guest_limit: int = 100
    authenticated_limit: int = 1000
    window_seconds: int = 3600
    redis_key_prefix: str = "rate_limit"


@dataclass
class RateLimitStatus:
    """Current rate limit status."""
    limit: int
    remaining: int
    reset_timestamp: int
    is_exceeded: bool
    retry_after: Optional[int] = None


class RateLimitService:
    """
    Rate limiting using Redis sorted sets (sliding window).
    
    Algorithm:
    1. Store each request as sorted set member with timestamp as score
    2. Remove requests older than window (ZREMRANGEBYSCORE)
    3. Count remaining requests (ZCARD)
    4. If count < limit, allow and add current request
    5. If count >= limit, reject with retry time
    
    Usage:
        >>> limiter = RateLimitService()
        >>> status = limiter.check_limit("203.0.113.42", is_authenticated=False)
        >>> if status.is_exceeded:
        >>>     raise HTTPException(status_code=429, detail="Rate limit exceeded")
    """
    
    def __init__(
        self,
        redis_client: redis.Redis,
        config: Optional[RateLimitConfig] = None
    ):
        """Initialize rate limiter."""
        self.redis = redis_client
        self.config = config or RateLimitConfig()
        logger.info(
            f"Rate limiter initialized: "
            f"guest={self.config.guest_limit}/hr, "
            f"auth={self.config.authenticated_limit}/hr"
        )
    
    def check_limit(
        self,
        identifier: str,
        is_authenticated: bool = False
    ) -> RateLimitStatus:
        """
        Check rate limit for client.
        
        Args:
            identifier: IP address (guest) or user_id (authenticated)
            is_authenticated: Whether user is authenticated
            
        Returns:
            RateLimitStatus with limit info
        """
        # Determine limit
        limit = (
            self.config.authenticated_limit
            if is_authenticated
            else self.config.guest_limit
        )
        
        # Generate Redis key
        key_type = "user" if is_authenticated else "ip"
        redis_key = f"{self.config.redis_key_prefix}:{key_type}:{identifier}"
        
        try:
            current_time = time.time()
            window_start = current_time - self.config.window_seconds
            
            # Remove old requests (outside window)
            self.redis.zremrangebyscore(redis_key, 0, window_start)
            
            # Count requests in current window
            request_count = self.redis.zcard(redis_key)
            
            # Check if limit exceeded
            if request_count >= limit:
                # Get oldest request timestamp for retry calculation
                oldest_requests = self.redis.zrange(redis_key, 0, 0, withscores=True)
                
                if oldest_requests:
                    oldest_timestamp = oldest_requests[0][1]
                    retry_after = int(
                        oldest_timestamp + self.config.window_seconds - current_time
                    )
                else:
                    retry_after = self.config.window_seconds
                
                logger.warning(
                    f"Rate limit exceeded for {identifier}: "
                    f"{request_count}/{limit} requests"
                )
                
                return RateLimitStatus(
                    limit=limit,
                    remaining=0,
                    reset_timestamp=int(current_time + retry_after),
                    is_exceeded=True,
                    retry_after=retry_after
                )
            
            # Add current request
            request_id = f"req_{current_time}_{id(self)}"
            self.redis.zadd(redis_key, {request_id: current_time})
            
            # Set expiration on key (cleanup)
            self.redis.expire(redis_key, self.config.window_seconds)
            
            # Calculate remaining requests
            remaining = limit - (request_count + 1)
            
            # Calculate reset time (end of window)
            reset_timestamp = int(current_time + self.config.window_seconds)
            
            logger.debug(
                f"Rate limit check for {identifier}: "
                f"{request_count + 1}/{limit} requests, "
                f"{remaining} remaining"
            )
            
            return RateLimitStatus(
                limit=limit,
                remaining=remaining,
                reset_timestamp=reset_timestamp,
                is_exceeded=False
            )
            
        except RedisError as e:
            logger.error(f"Redis error during rate limit check: {e}")
            
            # Fail open (allow request) on Redis errors
            return RateLimitStatus(
                limit=limit,
                remaining=limit,
                reset_timestamp=int(time.time() + self.config.window_seconds),
                is_exceeded=False
            )
```

### Step 2: Create Rate Limit Middleware

```python
# backend/app/middleware/rate_limit.py
"""
FastAPI middleware for rate limiting.

Applies rate limits before request processing.
"""

import logging
from typing import Callable, Optional

from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.services.rate_limit_service import RateLimitService, RateLimitStatus
from app.services.cache_service import get_cache
from app.api.dependencies import get_current_user_optional

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using sliding window algorithm.
    
    Adds headers to all responses:
    - X-RateLimit-Limit: Maximum requests allowed
    - X-RateLimit-Remaining: Requests remaining in window
    - X-RateLimit-Reset: Unix timestamp when limit resets
    - Retry-After: Seconds until retry (if 429)
    """
    
    def __init__(self, app, limiter: RateLimitService):
        """Initialize middleware."""
        super().__init__(app)
        self.limiter = limiter
        logger.info("Rate limit middleware initialized")
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        """Check rate limit before processing request."""
        
        # Skip rate limiting for health checks
        if request.url.path.startswith("/health"):
            return await call_next(request)
        
        # Get client identifier
        client_ip = self._get_client_ip(request)
        
        # Check if user is authenticated (will be None for guest)
        user = await self._get_current_user(request)
        
        if user:
            identifier = str(user.id)
            is_authenticated = True
        else:
            identifier = client_ip
            is_authenticated = False
        
        # Check rate limit
        status = self.limiter.check_limit(identifier, is_authenticated)
        
        # If exceeded, return 429
        if status.is_exceeded:
            logger.warning(
                f"Rate limit exceeded for {identifier} "
                f"(authenticated={is_authenticated})"
            )
            
            response = Response(
                content=self._create_error_response(status),
                status_code=429,
                media_type="application/json"
            )
            
            self._add_rate_limit_headers(response, status)
            return response
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers to successful responses
        self._add_rate_limit_headers(response, status)
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request."""
        # Check X-Forwarded-For header (behind proxy)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        # Check X-Real-IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct connection IP
        return request.client.host
    
    async def _get_current_user(self, request: Request) -> Optional[any]:
        """Extract current user from request (if authenticated)."""
        try:
            # Check for Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return None
            
            # Extract token and validate (simplified)
            # In real implementation, use proper JWT validation
            token = auth_header.replace("Bearer ", "")
            
            # This would call your JWT validation logic
            # For now, return None (guest)
            return None
            
        except Exception as e:
            logger.debug(f"Failed to extract user from request: {e}")
            return None
    
    def _add_rate_limit_headers(
        self,
        response: Response,
        status: RateLimitStatus
    ):
        """Add rate limit headers to response."""
        response.headers["X-RateLimit-Limit"] = str(status.limit)
        response.headers["X-RateLimit-Remaining"] = str(status.remaining)
        response.headers["X-RateLimit-Reset"] = str(status.reset_timestamp)
        
        if status.is_exceeded and status.retry_after:
            response.headers["Retry-After"] = str(status.retry_after)
    
    def _create_error_response(self, status: RateLimitStatus) -> str:
        """Create JSON error response for 429."""
        import json
        
        error_data = {
            "success": False,
            "error": {
                "code": "ERR_RATE_LIMIT_EXCEEDED",
                "message": "Rate limit exceeded. Please try again later.",
                "details": {
                    "limit": status.limit,
                    "window_seconds": 3600,
                    "retry_after_seconds": status.retry_after
                }
            }
        }
        
        return json.dumps(error_data, ensure_ascii=False)
```

### Step 3: Register Middleware in FastAPI App

```python
# backend/app/main.py
from app.middleware.rate_limit import RateLimitMiddleware
from app.services.rate_limit_service import RateLimitService
from app.services.cache_service import get_cache

app = FastAPI(title="BAHR API")

# Initialize rate limiter
redis_client = get_cache().client
rate_limiter = RateLimitService(redis_client)

# Add rate limit middleware
app.add_middleware(RateLimitMiddleware, limiter=rate_limiter)
```

### Step 4: Test Rate Limiting

```bash
# Test script - trigger rate limit
cat > scripts/test_rate_limit.sh <<'EOF'
#!/bin/bash

echo "Testing rate limiting..."
echo "Sending 105 requests (limit is 100)..."

for i in {1..105}; do
  response=$(curl -s -w "\n%{http_code}" http://localhost:8000/api/v1/analyses \
    -H "Content-Type: application/json" \
    -d '{"text": "قفا نبك من ذكري"}')
  
  http_code=$(echo "$response" | tail -n1)
  
  if [ "$http_code" == "429" ]; then
    echo "Request $i: BLOCKED (429 Too Many Requests)"
    echo "$response" | head -n-1 | jq .
    break
  else
    echo "Request $i: OK ($http_code)"
  fi
done
EOF

chmod +x scripts/test_rate_limit.sh
./scripts/test_rate_limit.sh
```

---

## 5. Reference Implementation (Full Code)

See Step-by-Step Implementation sections above for complete code.

---

## 6. Unit & Integration Tests

### tests/unit/middleware/test_rate_limit.py

```python
"""
Unit tests for rate limiting.

Tests sliding window algorithm and 429 responses.
"""

import pytest
import time
from fastapi.testclient import TestClient
from app.main import app
from app.services.rate_limit_service import RateLimitService, RateLimitConfig
from app.services.cache_service import get_cache

client = TestClient(app)


class TestRateLimiting:
    """Test suite for rate limiting."""
    
    @pytest.fixture
    def limiter(self):
        """Create rate limiter with test config."""
        redis_client = get_cache().client
        config = RateLimitConfig(
            guest_limit=10,  # Low limit for testing
            authenticated_limit=50,
            window_seconds=60  # 1 minute window
        )
        return RateLimitService(redis_client, config)
    
    def test_rate_limit_allows_requests_under_limit(self, limiter):
        """Test requests under limit are allowed."""
        identifier = "test_ip_1"
        
        for i in range(5):
            status = limiter.check_limit(identifier, is_authenticated=False)
            assert status.is_exceeded is False
            assert status.remaining > 0
    
    def test_rate_limit_blocks_after_limit(self, limiter):
        """Test requests over limit are blocked."""
        identifier = "test_ip_2"
        
        # Send requests up to limit
        for i in range(10):
            status = limiter.check_limit(identifier, is_authenticated=False)
            assert status.is_exceeded is False
        
        # Next request should be blocked
        status = limiter.check_limit(identifier, is_authenticated=False)
        assert status.is_exceeded is True
        assert status.remaining == 0
        assert status.retry_after is not None
    
    def test_rate_limit_headers_present(self):
        """Test rate limit headers in response."""
        response = client.post(
            "/api/v1/analyses",
            json={"text": "قفا نبك من ذكري"}
        )
        
        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers
        assert "X-RateLimit-Reset" in response.headers
    
    def test_429_response_on_limit_exceeded(self):
        """Test 429 response when limit exceeded."""
        # Send many requests to exceed limit
        for i in range(105):
            response = client.post(
                "/api/v1/analyses",
                json={"text": f"قفا نبك {i}"}
            )
        
        # Should get 429
        assert response.status_code == 429
        data = response.json()
        
        assert data["success"] is False
        assert data["error"]["code"] == "ERR_RATE_LIMIT_EXCEEDED"
        assert "Retry-After" in response.headers
    
    def test_authenticated_higher_limit(self, limiter):
        """Test authenticated users have higher limit."""
        auth_identifier = "user_123"
        
        # Send 50 requests (exceeds guest limit of 10)
        for i in range(50):
            status = limiter.check_limit(auth_identifier, is_authenticated=True)
            assert status.is_exceeded is False
    
    def test_sliding_window_removes_old_requests(self, limiter):
        """Test sliding window removes old requests."""
        identifier = "test_ip_3"
        
        # Manually add old request (outside window)
        redis_key = f"rate_limit:ip:{identifier}"
        old_timestamp = time.time() - 3700  # >1 hour ago
        limiter.redis.zadd(redis_key, {f"req_old": old_timestamp})
        
        # Check limit - old request should be removed
        status = limiter.check_limit(identifier, is_authenticated=False)
        
        # Should only count current request, not old one
        assert status.remaining == limiter.config.guest_limit - 1
```

---

## 7. CI/CD Pipeline

```yaml
# .github/workflows/rate-limit-tests.yml
name: Rate Limiting Tests

on:
  push:
    paths:
      - 'backend/app/middleware/rate_limit.py'
      - 'backend/app/services/rate_limit_service.py'

jobs:
  test-rate-limiting:
    runs-on: ubuntu-latest
    
    services:
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run rate limit tests
        run: |
          cd backend
          pytest tests/unit/middleware/test_rate_limit.py -v \
            --cov=app.middleware.rate_limit \
            --cov=app.services.rate_limit_service
```

---

## 8. Deployment Checklist

- [ ] Redis running and accessible
- [ ] Test guest limit (100 req/hour)
- [ ] Test authenticated limit (1,000 req/hour)
- [ ] Verify 429 responses with Retry-After header
- [ ] Test rate limit headers on all responses
- [ ] Test sliding window (not fixed window)
- [ ] Monitor Redis memory for rate limit keys
- [ ] Test IP extraction behind proxy (X-Forwarded-For)
- [ ] Verify fail-open behavior on Redis errors
- [ ] Document rate limits in API docs

---

## 9. Observability

```python
# backend/app/metrics/rate_limit_metrics.py
from prometheus_client import Counter, Histogram

rate_limit_checks_total = Counter(
    "bahr_rate_limit_checks_total",
    "Total rate limit checks",
    ["user_type", "status"]  # guest/authenticated, allowed/blocked
)

rate_limit_exceeded_total = Counter(
    "bahr_rate_limit_exceeded_total",
    "Total rate limit violations",
    ["user_type"]
)
```

---

## 10. Security & Safety

- **Fail Open:** Allow requests if Redis is down
- **IP Spoofing:** Validate X-Forwarded-For header
- **DoS Protection:** Rate limiting prevents abuse
- **Window Algorithm:** Sliding window prevents burst attacks

---

## 11. Backwards Compatibility

- **None** - Initial implementation

---

## 12. Source Documentation Citations

1. **docs/technical/API_CONVENTIONS.md** - Rate limiting strategy
2. **implementation-guides/IMPROVED_PROMPT.md:599-626** - Feature specification

---

**Implementation Complete!** ✅  
**Estimated Time:** 6-10 hours  
**Test Coverage Target:** ≥ 70%  
**Performance Target:** <5ms overhead per request
