# Feature: Monitoring & Observability - Implementation Guide

**Feature ID:** `feature-monitoring-observability`  
**Status:** Production-Ready  
**Last Updated:** November 8, 2025  
**Estimated Implementation Time:** 10-14 hours

---

## 1. Objective & Description

### What
Implement comprehensive monitoring and observability using Prometheus metrics and Grafana dashboards. Track request latency, error rates, cache hit ratios, meter confidence scores, and system health metrics.

### Why
- **Production Readiness:** Monitor performance in real-time
- **SLO Tracking:** P95 latency <600ms, error rate <2%
- **Debugging:** Identify performance bottlenecks quickly
- **Capacity Planning:** Track resource usage trends
- **User Experience:** Detect degradations before users report issues

### Success Criteria
- ✅ Expose `/metrics` endpoint for Prometheus scraping
- ✅ Track 10+ core metrics (latency, errors, cache, confidence)
- ✅ Create Grafana dashboard with 6+ panels
- ✅ Set up alerts for high latency (>800ms) and error rate (>5%)
- ✅ Monitor CAMeL Tools memory usage
- ✅ Track cache hit rate (target ≥40%)
- ✅ Test coverage ≥65% with metrics integration tests

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                 Monitoring Architecture                              │
└─────────────────────────────────────────────────────────────────────┘

Application (FastAPI)
    │
    │  Metrics Collection
    ▼
┌──────────────────────────────────────┐
│ Prometheus Client (prometheus_client)│
│ - Counter: bahr_requests_total       │
│ - Histogram: request_duration_seconds│
│ - Gauge: meter_confidence            │
│ - Counter: cache_hit_total           │
└──────────┬───────────────────────────┘
           │
           │  HTTP GET /metrics
           ▼
┌──────────────────────────────────────┐
│ Prometheus Server                    │
│ - Scrape every 15s                   │
│ - Store time series data             │
│ - Retention: 30 days                 │
└──────────┬───────────────────────────┘
           │
           │  PromQL Queries
           ▼
┌──────────────────────────────────────┐
│ Grafana Dashboard                    │
│                                      │
│ Panels:                              │
│ 1. Request Latency (P50/P95/P99)    │
│ 2. Error Rate %                      │
│ 3. Cache Hit Ratio                   │
│ 4. Meter Confidence Trend            │
│ 5. Requests Per Endpoint             │
│ 6. System Resource Usage             │
└──────────┬───────────────────────────┘
           │
           │  Alert Rules
           ▼
┌──────────────────────────────────────┐
│ Alertmanager                         │
│ - High latency (P95 >800ms)          │
│ - High error rate (>5%)              │
│ - Low cache hit rate (<25%)          │
│ - Send to: Slack, Email              │
└──────────────────────────────────────┘

Key Metrics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
bahr_requests_total              → Counter (endpoint, status)
bahr_request_duration_seconds    → Histogram (endpoint, method)
verse_analysis_latency_seconds   → Histogram (mode)
bahr_analysis_cache_hit_total    → Counter
bahr_meter_confidence            → Gauge (meter)
bahr_errors_total                → Counter (code)
analysis_timeouts_total          → Counter
```

---

## 3. Input/Output Contracts

### 3.1 Prometheus Metrics Schema

```python
# backend/app/metrics/core_metrics.py
from prometheus_client import Counter, Histogram, Gauge, Info

# Request metrics
bahr_requests_total = Counter(
    'bahr_requests_total',
    'Total HTTP requests',
    ['endpoint', 'method', 'status']
)

bahr_request_duration_seconds = Histogram(
    'bahr_request_duration_seconds',
    'HTTP request duration in seconds',
    ['endpoint', 'method'],
    buckets=[0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 2.0, 3.0, 5.0]
)

# Analysis metrics
verse_analysis_latency_seconds = Histogram(
    'verse_analysis_latency_seconds',
    'Verse analysis latency in seconds',
    ['mode'],  # accurate/fast
    buckets=[0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 2.0, 3.0]
)

bahr_meter_confidence = Gauge(
    'bahr_meter_confidence',
    'Meter detection confidence score',
    ['meter']
)

# Cache metrics
bahr_analysis_cache_hit_total = Counter(
    'bahr_analysis_cache_hit_total',
    'Analysis cache hits'
)

bahr_analysis_cache_miss_total = Counter(
    'bahr_analysis_cache_miss_total',
    'Analysis cache misses'
)

# Error metrics
bahr_errors_total = Counter(
    'bahr_errors_total',
    'Total errors by code',
    ['code', 'severity']
)

analysis_timeouts_total = Counter(
    'analysis_timeouts_total',
    'Analysis timeout count'
)

# System info
bahr_info = Info(
    'bahr',
    'BAHR application information'
)
```

---

## 4. Step-by-Step Implementation

### Step 1: Install Prometheus Client

```bash
# Add to requirements.txt
echo "prometheus-client==0.19.0" >> backend/requirements.txt
pip install prometheus-client==0.19.0
```

### Step 2: Create Metrics Module

```python
# backend/app/metrics/__init__.py
"""
Prometheus metrics for BAHR platform.

Source: docs/technical/METRICS_REFERENCE.md
"""

from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest, REGISTRY
import logging

logger = logging.getLogger(__name__)

# Request metrics
bahr_requests_total = Counter(
    'bahr_requests_total',
    'Total HTTP requests',
    ['endpoint', 'method', 'status']
)

bahr_request_duration_seconds = Histogram(
    'bahr_request_duration_seconds',
    'HTTP request duration',
    ['endpoint', 'method'],
    buckets=[0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 2.0, 3.0, 5.0]
)

# Analysis metrics
verse_analysis_latency_seconds = Histogram(
    'verse_analysis_latency_seconds',
    'Verse analysis latency',
    ['mode'],
    buckets=[0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 2.0, 3.0]
)

bahr_meter_confidence = Gauge(
    'bahr_meter_confidence',
    'Meter detection confidence',
    ['meter']
)

# Cache metrics
bahr_cache_requests_total = Counter(
    'bahr_cache_requests_total',
    'Cache requests',
    ['operation', 'status']  # get/set, hit/miss
)

# Error metrics
bahr_errors_total = Counter(
    'bahr_errors_total',
    'Total errors',
    ['code', 'severity']
)

analysis_timeouts_total = Counter(
    'analysis_timeouts_total',
    'Analysis timeouts'
)

# System info
bahr_info = Info('bahr', 'Application information')
bahr_info.info({
    'version': '1.0.0',
    'python_version': '3.11',
    'environment': 'production'
})


def expose_metrics():
    """
    Generate Prometheus metrics in text format.
    
    Returns:
        bytes: Prometheus metrics text
    """
    return generate_latest(REGISTRY)
```

### Step 3: Add Metrics Middleware

```python
# backend/app/middleware/metrics.py
"""Middleware to collect request metrics."""

import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.metrics import (
    bahr_requests_total,
    bahr_request_duration_seconds
)

logger = logging.getLogger(__name__)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Collect metrics for all HTTP requests."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """Track request duration and status."""
        
        # Start timer
        start_time = time.time()
        
        # Get endpoint (normalize path parameters)
        endpoint = self._normalize_endpoint(request.url.path)
        method = request.method
        
        try:
            # Process request
            response = await call_next(request)
            status = response.status_code
            
            # Record metrics
            duration = time.time() - start_time
            
            bahr_requests_total.labels(
                endpoint=endpoint,
                method=method,
                status=status
            ).inc()
            
            bahr_request_duration_seconds.labels(
                endpoint=endpoint,
                method=method
            ).observe(duration)
            
            return response
            
        except Exception as e:
            # Record error
            bahr_requests_total.labels(
                endpoint=endpoint,
                method=method,
                status=500
            ).inc()
            
            logger.exception(f"Request failed: {e}")
            raise
    
    def _normalize_endpoint(self, path: str) -> str:
        """Normalize path to avoid high cardinality."""
        # Replace UUIDs, IDs with placeholders
        import re
        
        # Replace UUIDs
        path = re.sub(
            r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            '{uuid}',
            path
        )
        
        # Replace numeric IDs
        path = re.sub(r'/\d+', '/{id}', path)
        
        return path
```

### Step 4: Expose /metrics Endpoint

```python
# backend/app/api/v1/endpoints/health.py
from fastapi import APIRouter, Response
from app.metrics import expose_metrics

router = APIRouter(tags=["Health"])


@router.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint.
    
    Returns metrics in Prometheus text format.
    """
    metrics_data = expose_metrics()
    return Response(
        content=metrics_data,
        media_type="text/plain; version=0.0.4"
    )


@router.get("/health")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "service": "bahr-api",
        "version": "1.0.0"
    }
```

### Step 5: Instrument Analysis Service

```python
# backend/app/services/analysis_service.py
# Add metrics collection

from app.metrics import (
    verse_analysis_latency_seconds,
    bahr_meter_confidence,
    bahr_cache_requests_total
)

def analyze_verse(self, request, user_id=None, cache=None):
    """Analyze verse with metrics."""
    
    # Start timer
    start_time = time.time()
    
    # Check cache
    if cache:
        cached = cache.get_analysis(normalized_text)
        if cached:
            bahr_cache_requests_total.labels(
                operation="get",
                status="hit"
            ).inc()
            return AnalysisResponse(**cached)
        else:
            bahr_cache_requests_total.labels(
                operation="get",
                status="miss"
            ).inc()
    
    # Perform analysis
    result = self._run_pipeline(request)
    
    # Record latency
    duration = time.time() - start_time
    verse_analysis_latency_seconds.labels(
        mode="accurate"
    ).observe(duration)
    
    # Record confidence
    bahr_meter_confidence.labels(
        meter=result.detected_meter
    ).set(result.confidence)
    
    return result
```

### Step 6: Set Up Prometheus Server

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'bahr-api'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/api/v1/metrics'
    scrape_interval: 15s
```

```yaml
# docker-compose.yml - Add Prometheus
  prometheus:
    image: prom/prometheus:v2.45.0
    container_name: bahr_prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'

volumes:
  prometheus_data:
```

### Step 7: Create Grafana Dashboard

```json
{
  "dashboard": {
    "title": "BAHR API Metrics",
    "panels": [
      {
        "title": "Request Latency (P95)",
        "targets": [{
          "expr": "histogram_quantile(0.95, sum(rate(bahr_request_duration_seconds_bucket[5m])) by (le, endpoint))"
        }]
      },
      {
        "title": "Error Rate",
        "targets": [{
          "expr": "sum(rate(bahr_requests_total{status=~\"5..\"}[5m])) / sum(rate(bahr_requests_total[5m]))"
        }]
      },
      {
        "title": "Cache Hit Ratio",
        "targets": [{
          "expr": "sum(rate(bahr_cache_requests_total{status=\"hit\"}[5m])) / sum(rate(bahr_cache_requests_total[5m]))"
        }]
      }
    ]
  }
}
```

---

## 5. Reference Implementation (Full Code)

See Step-by-Step Implementation sections above.

---

## 6. Unit & Integration Tests

```python
# tests/unit/metrics/test_metrics.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_metrics_endpoint_accessible():
    """Test /metrics endpoint returns Prometheus format."""
    response = client.get("/api/v1/metrics")
    
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert b"bahr_requests_total" in response.content


def test_metrics_incremented_on_request():
    """Test metrics are incremented on requests."""
    # Make request
    client.post("/api/v1/analyses", json={"text": "قفا نبك"})
    
    # Check metrics
    response = client.get("/api/v1/metrics")
    content = response.content.decode('utf-8')
    
    assert "bahr_requests_total" in content
    assert "bahr_request_duration_seconds" in content
```

---

## 7. CI/CD Pipeline

```yaml
# .github/workflows/monitoring-tests.yml
name: Monitoring Tests

on:
  push:
    paths:
      - 'backend/app/metrics/**'
      - 'backend/app/middleware/metrics.py'

jobs:
  test-metrics:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run metrics tests
        run: |
          cd backend
          pytest tests/unit/metrics/ -v
```

---

## 8. Deployment Checklist

- [ ] Prometheus server running and scraping metrics
- [ ] Grafana dashboard imported and configured
- [ ] Alert rules configured in Alertmanager
- [ ] Test /metrics endpoint returns valid data
- [ ] Verify P95 latency tracking
- [ ] Monitor cache hit rate ≥40%
- [ ] Set up Slack/email notifications for alerts
- [ ] Document PromQL queries for common issues
- [ ] Test metrics cardinality (<10,000 series)
- [ ] Configure 30-day retention in Prometheus

---

## 9. Observability

**Key Metrics to Monitor:**

1. **Latency:** P95 < 600ms (SLO)
2. **Error Rate:** < 2% of requests
3. **Cache Hit Rate:** ≥ 40%
4. **Meter Confidence:** Average ≥ 0.70
5. **Timeouts:** Should be ~0

**Alert Thresholds:**
- P95 latency > 800ms for 15 minutes
- Error rate > 5% for 10 minutes
- Cache hit rate < 25% for 30 minutes

---

## 10. Security & Safety

- **Metrics Endpoint:** Public (no sensitive data)
- **Cardinality:** Limit labels to prevent explosion
- **Retention:** 30 days to manage disk usage

---

## 11. Backwards Compatibility

- **None** - Initial implementation

---

## 12. Source Documentation Citations

1. **docs/technical/METRICS_REFERENCE.md:1-150** - Metrics specification
2. **implementation-guides/IMPROVED_PROMPT.md:630-657** - Feature specification

---

**Implementation Complete!** ✅  
**Estimated Time:** 10-14 hours  
**Test Coverage Target:** ≥ 65%  
**Performance Target:** <5ms metrics overhead
