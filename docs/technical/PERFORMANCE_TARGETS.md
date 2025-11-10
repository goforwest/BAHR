# ⚡ أهداف الأداء والمعايير
## Performance Targets & Service Level Agreements (SLAs)

---

## 📋 نظرة عامة

معايير واضحة لأداء المنصة عبر جميع المراحل من MVP إلى Production.

**تم الإنشاء:** November 8, 2025  
**الأهمية:** حرجة - يجب تحقيق هذه المعايير قبل الإطلاق

---

## 🎯 أهداف أداء MVP (Week 1-12)

### 1️⃣ زمن استجابة API (API Latency)

#### تحليل بيت واحد (< 50 كلمة):

```yaml
P50 (50th percentile):
  Cold Start: < 300ms
  With Cache: < 30ms
  Target: ✅ Excellent UX

P95 (95th percentile):
  Cold Start: < 500ms
  With Cache: < 50ms
  Target: ✅ Acceptable

P99 (99th percentile):
  Cold Start: < 1000ms (1s)
  With Cache: < 100ms
  Target: ⚠️ Max acceptable limit

Timeout:
  Hard Limit: 5 seconds
  Action: Return error with partial results
```

#### تحليل قصيدة (< 200 كلمة):

```yaml
P50:
  Cold Start: < 1500ms (1.5s)
  With Cache: < 150ms

P95:
  Cold Start: < 2500ms (2.5s)
  With Cache: < 300ms

P99:
  Cold Start: < 5000ms (5s)
  With Cache: < 500ms

Timeout:
  Hard Limit: 10 seconds
```

#### تحليل مجموعة (< 1000 كلمة):

```yaml
P50: < 5 seconds
P95: < 10 seconds
P99: < 20 seconds
Timeout: 30 seconds

Note: Consider async processing for large texts
```

---

### 2️⃣ معدل النجاح (Success Rate)

```yaml
Analysis Success Rate:
  MVP Target: > 95%
  Production Target: > 99%
  
  Acceptable Failures:
    - Invalid input (non-Arabic text): User error
    - Unsupported meter (free verse): Expected behavior
    - Network timeouts: Infrastructure issue
    
  Unacceptable Failures:
    - Server crashes: 0% tolerance
    - Data corruption: 0% tolerance
    - Silent failures: 0% tolerance

Error Budget:
  Weekly: 5% of requests can fail (MVP)
  Monthly: 1% of requests can fail (Production)
```

---

### 3️⃣ دقة التحليل (Analysis Accuracy)

**Updated Targets (Post Expert Review):**

```yaml
Meter Detection Accuracy (Classical Poetry):
  Week 5 (Initial Engine): > 65% ✅ Realistic first target
  Week 7 (After Tuning): > 75% ✅ Good progress
  Week 12 (Beta Launch): > 80% ✅ MVP acceptable
  Week 13 (Production): > 80% ✅ Maintain quality
  6 Months Post-Launch: > 90% 🎯 Long-term goal
  
  Note: 16-meter coverage initially
  Fallback: If accuracy < 65% by Week 5, reduce scope to 8 most common meters
  
Confidence Thresholds:
  High Confidence (> 0.85): Expected 90%+ accuracy
  Medium Confidence (0.65-0.85): Expected 75%+ accuracy
  Low Confidence (< 0.65): Show "uncertain" warning to user
  
8-Meter Fallback Scope (if needed):
  1. الطويل (Most common)
  2. البسيط
  3. الكامل
  4. الوافر
  5. الرجز
  6. الرمل
  7. الخفيف
  8. المتقارب

Original Ambitious Target (Deferred):
  - Week 12: > 85% accuracy
  - Requires: More training data + ML model (Phase 2)

```yaml
Meter Detection Accuracy:
  Week 6 (Initial): > 65%
  Week 9 (Tuned): > 75%
  Week 12 (Launch): > 80%
  6 Months: > 90%
  
  Measurement:
    - Test on 500+ manually labeled verses
    - Coverage across all 16 meters
    - Include classical + modern samples
    
  Confidence Thresholds:
    High Confidence (> 0.85): Display with certainty
    Medium Confidence (0.65-0.85): Display with alternatives
    Low Confidence (< 0.65): Show "Unable to determine" message

Quality Score Correlation:
  - Should correlate 80%+ with expert ratings
  - Measured on 100+ expert-reviewed poems
```

---

### 4️⃣ معدل الإنتاجية (Throughput)

```yaml
Concurrent Users (MVP):
  Target: 100 concurrent users
  Per User: 1-2 requests per minute
  Total: 100-200 requests/minute sustained
  
  Peak Load (1.5x normal):
    150 concurrent users
    250 requests/minute

Database Connections:
  Pool Size: 10 connections
  Max Overflow: 5 connections
  Connection Timeout: 30 seconds
  
  Target:
    - < 50% pool utilization at normal load
    - < 80% pool utilization at peak

Cache Hit Rate:
  Redis Cache:
    Target: > 60% hit rate
    Popular verses: > 90% hit rate
    Unique texts: 0% hit rate (expected)
  
  Database Query Cache:
    Meter lookups: 100% hit rate (static data)
    User queries: 40-60% hit rate
```

---

### 5️⃣ استهلاك الموارد (Resource Usage)

#### Backend API (FastAPI):

```yaml
CPU Usage:
  Normal Load: < 40%
  Peak Load: < 70%
  Alert Threshold: > 80%
  
  Alert Thresholds:
    Warning: > 60% for 5 minutes
    Critical: > 80% for 2 minutes

Memory (RAM):
  Base Process: ~150MB (Python runtime)
  With CAMeL Tools loaded: ~400MB (+200MB for models)
  Under Normal Load: ~512MB ✅ MVP Target
  Under Peak Load: ~800MB
  Maximum Acceptable: < 1GB (leave headroom)
  Alert Threshold: > 900MB
  
  CAMeL Tools Memory Profile:
    - MorphologyDB: ~150MB
    - Analyzer models: ~50MB
    - Per-request overhead: ~5-10MB
    - Recommendation: Pre-load models at startup (avoid lazy loading)
  
  Alert Thresholds:
    Warning: > 700MB (75% of 1GB)
    Critical: > 900MB (90% of 1GB)

Disk I/O:
  Read Operations: < 100 IOPS
  Write Operations: < 50 IOPS
  Cache Directory: < 1GB
```

#### Database (PostgreSQL):

```yaml
CPU Usage:
  Normal: < 30%
  Peak: < 60%
  Alert: > 70%

Memory:
  Shared Buffers: 256MB (MVP), 1GB (Prod)
  Effective Cache: 512MB (MVP), 2GB (Prod)
  Work Mem: 16MB per query
  
Connections:
  Active: < 15 (MVP)
  Idle: < 10
  Max: 100

Query Performance (Critical Benchmarks):
  Simple SELECT (by ID): < 5ms ✅ Primary key lookup
  Analysis Lookup (by ID): < 10ms ✅ Cached results
  Meter Definitions: < 10ms ✅ Static data
  User Authentication: < 20ms ✅ Password verify + session
  JOIN queries (user + analysis): < 50ms ✅ Common operation
  Complex aggregations (stats): < 200ms ⚠️ Dashboard queries
  Full-text search (Arabic): < 500ms ⚠️ Search results page
  
  Index Requirements:
    - All foreign keys indexed
    - created_at indexed (DESC) for pagination
    - GIN index on JSONB columns (prosodic_pattern, alternative_meters)
    - GIN index on Arabic full-text search (to_tsvector)
  
  Slow Query Log:
    - Log queries > 100ms
    - Review weekly, optimize worst offenders
    - Target: 95% of queries < 50ms
```

#### Redis Cache:

```yaml
Memory:
  MVP Target: < 256MB ✅ Sufficient for 10k cached analyses
  Production Target: < 1GB
  Eviction Policy: allkeys-lru (Least Recently Used)
  
  Memory Breakdown:
    - Meter definitions (static): ~1MB
    - Analysis results cache (7-day TTL): ~200MB (MVP)
    - User sessions (30-min TTL): ~10MB
    - Rate limiting counters (1-hour TTL): ~5MB
  
  Eviction Behavior:
    - When memory limit reached, evict oldest unused keys
    - Critical data (meter definitions): Use PERSIST to prevent eviction
    - Session data: TTL-based expiration (automatic cleanup)

Response Time:
  GET: < 1ms ✅ In-memory lookup
  SET: < 2ms ✅ Write operation
  INCR (rate limiting): < 1ms ✅ Atomic counter
  
Connection Pool:
  Size: 10 connections (MVP), 50 connections (Production)
  Timeout: 5 seconds
  Retry: 3 attempts with exponential backoff

Cache Hit Ratio:
  Target: > 80% (MVP), > 90% (Production)
  Monitor: Track hit/miss ratio daily
  Action: If < 70%, investigate TTL settings or cache size
```

---

## 🌐 Frontend Performance

### Page Load Times:

```yaml
First Contentful Paint (FCP):
  Target: < 1.5 seconds
  Good: < 1.0 seconds
  
Largest Contentful Paint (LCP):
  Target: < 2.5 seconds
  Good: < 2.0 seconds
  
Time to Interactive (TTI):
  Target: < 3.5 seconds
  Good: < 3.0 seconds

Cumulative Layout Shift (CLS):
  Target: < 0.1
  Good: < 0.05
```

### JavaScript Bundle:

```yaml
Initial Bundle Size (Critical):
  Target: < 300KB (gzipped) ✅ MVP acceptable
  Good: < 200KB (gzipped) 🎯 Ideal for fast load
  Warning: > 400KB ⚠️ Investigate bundle bloat
  Critical: > 500KB 🚨 User experience degraded
  
  Breakdown:
    - React + Next.js core: ~100KB
    - UI Components (shadcn/Tailwind): ~50KB
    - Arabic text utilities: ~20KB
    - API client + state: ~30KB
    - Remaining budget: ~100KB for features
  
  Optimization Strategies:
    - Code splitting by route (Next.js automatic)
    - Dynamic imports for heavy components
    - Tree-shaking unused code
    - Minimize Arabic font files (subset to used glyphs)
    - Use Next.js Image optimization

Code Splitting:
  Home Page: < 150KB (minimal - hero + quick analyzer)
  Analysis Page: < 250KB (main feature - prosody visualization)
  Dashboard: < 200KB (user stats + history)
  About/Help Pages: < 100KB (static content)
  Lazy Load: Competition features (Phase 2), AI poet (Phase 2)

Arabic Font Loading:
  Primary Font (Amiri): ~150KB (WOFF2)
  Fallback Font (Noto Sans Arabic): ~100KB
  Strategy: 
    - Preload critical Arabic font
    - Subset fonts to include only used characters
    - Use font-display: swap (show text immediately)
  Target: Font load < 300ms on 3G connection

Lighthouse Score:
  Performance: > 90
  Accessibility: > 95
  Best Practices: > 90
  SEO: > 90
```

### API Calls from Frontend:

```yaml
Analysis Request:
  User Input → Backend: < 100ms network
  Backend Processing: < 500ms (cached)
  Response → Display: < 50ms rendering
  Total User Perceived: < 700ms

Debouncing:
  User Input: 300ms delay before API call
  Prevents: Unnecessary requests during typing
```

---

## 📊 Monitoring & Alerting Strategy (مُحدّث)

### Metrics Architecture:

```
┌─────────────────────────────────────────────┐
│         Application Instrumentation         │
│  ┌─────────────┐ ┌─────────────┐           │
│  │  FastAPI    │ │   Next.js   │           │
│  │  Metrics    │ │   Metrics   │           │
│  └──────┬──────┘ └──────┬──────┘           │
└─────────┼────────────────┼──────────────────┘
          │                │
┌─────────▼────────────────▼──────────────────┐
│          Prometheus Exporter                │
│    (Collects & Aggregates Metrics)          │
└─────────┬───────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────┐
│              Prometheus Server               │
│       (Time-series Database Storage)         │
└─────────┬───────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────┐
│           Grafana Dashboards                 │
│    (Visualization & Alerting)                │
└──────────────────────────────────────────────┘
```

### Metrics to Track (détaillés):

```yaml
# Application Metrics (FastAPI)
http_requests_total:
  Type: Counter
  Labels: [method, endpoint, status_code]
  Description: Total HTTP requests received

http_request_duration_seconds:
  Type: Histogram
  Labels: [method, endpoint]
  Buckets: [0.1, 0.5, 1.0, 2.0, 5.0]
  Description: Request latency distribution

prosody_analysis_duration_seconds:
  Type: Histogram
  Labels: [analysis_mode, detected_meter]
  Buckets: [0.05, 0.1, 0.25, 0.5, 1.0]
  Description: Prosody engine processing time

prosody_accuracy_score:
  Type: Gauge
  Labels: [meter_name]
  Description: Current accuracy score per meter

cache_hit_rate:
  Type: Gauge
  Labels: [cache_type]
  Description: Percentage of cache hits (Redis)

active_database_connections:
  Type: Gauge
  Description: Current number of active DB connections

# Business Metrics
analyses_completed_total:
  Type: Counter
  Labels: [meter_detected, confidence_level]
  Description: Total successful analyses

unique_users_daily:
  Type: Gauge
  Description: Daily active users count

low_confidence_results_total:
  Type: Counter
  Labels: [meter_name]
  Description: Results with confidence < 0.65
```

### Prometheus Configuration (`monitoring/prometheus.yml`):

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'bahr-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
    
  - job_name: 'bahr-frontend'
    static_configs:
      - targets: ['frontend:3000']
    metrics_path: '/api/metrics'
    
  - job_name: 'postgres-exporter'
    static_configs:
      - targets: ['postgres-exporter:9187']
    
  - job_name: 'redis-exporter'
    static_configs:
      - targets: ['redis-exporter:9121']

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - 'alerts.yml'
```

### Alert Rules (`monitoring/alerts.yml`):

```yaml
groups:
  - name: critical_alerts
    interval: 10s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status_code=~"5.."}[2m]) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }}% over 2 minutes"
      
      - alert: HighLatency
        expr: histogram_quantile(0.95, http_request_duration_seconds_bucket) > 3
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High API latency (P95 > 3s)"
          description: "P95 latency is {{ $value }}s"
      
      - alert: DatabaseConnectionPoolExhausted
        expr: active_database_connections > 14
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Database connection pool nearly exhausted"
          description: "{{ $value }} connections active out of 15"

  - name: warning_alerts
    interval: 30s
    rules:
      - alert: ModerateLatency
        expr: histogram_quantile(0.95, http_request_duration_seconds_bucket) > 1.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Moderate API latency increase"
          description: "P95 latency is {{ $value }}s"
      
      - alert: LowCacheHitRate
        expr: cache_hit_rate < 0.4
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Cache hit rate below target"
          description: "Cache hit rate is {{ $value }}%"
      
      - alert: HighLowConfidenceResults
        expr: rate(low_confidence_results_total[1h]) > 0.3
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "High percentage of low-confidence results"
          description: "{{ $value }}% of results have low confidence"
```

---

## 🚨 Monitoring Alert Rules (DETAILED)

### Critical Alerts (Page Immediately)

```yaml
# 1. Service Down
- alert: ServiceDown
  expr: up{job="bahr-api"} == 0
  for: 1m
  severity: critical
  notification: pagerduty, slack, sms
  description: "BAHR API is down - immediate attention required"

# 2. Error Rate Spike
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
  for: 2m
  severity: critical
  notification: pagerduty, slack
  description: "Error rate {{ $value | humanizePercentage }} - check logs immediately"

# 3. API Latency P95 Breach
- alert: HighAPILatencyP95
  expr: histogram_quantile(0.95, http_request_duration_seconds_bucket) > 1.0
  for: 5m
  severity: critical
  notification: pagerduty, slack
  description: "P95 latency {{ $value }}s exceeds 1s - performance degraded"

# 4. Database Connection Pool Exhausted
- alert: DatabasePoolExhausted
  expr: database_connections_active / database_connections_max > 0.95
  for: 2m
  severity: critical
  notification: pagerduty, slack
  description: "Database pool at {{ $value | humanizePercentage }} capacity - scale up"

# 5. Memory Usage Critical
- alert: MemoryUsageCritical
  expr: container_memory_usage_bytes{container="bahr-api"} / container_memory_limit_bytes > 0.90
  for: 3m
  severity: critical
  notification: pagerduty, slack
  description: "Memory usage {{ $value | humanizePercentage }} - risk of OOM"
```

### High Priority Alerts (Slack Notification)

```yaml
# 6. Accuracy Drop Week-over-Week
- alert: AccuracyDropWeekly
  expr: |
    (
      avg_over_time(prosody_accuracy_score[7d]) - 
      avg_over_time(prosody_accuracy_score[7d] offset 7d)
    ) / avg_over_time(prosody_accuracy_score[7d] offset 7d) < -0.05
  for: 1h
  severity: high
  notification: slack
  description: "Accuracy dropped {{ $value | humanizePercentage }} week-over-week - investigate"
  action: |
    1. Check recent code changes (git log)
    2. Review failed analysis logs
    3. Compare with golden set results
    4. Check for data distribution changes

# 7. Low Confidence Results Spike
- alert: LowConfidenceSpike
  expr: rate(prosody_analysis_confidence{level="low"}[1h]) / rate(prosody_analysis_total[1h]) > 0.30
  for: 30m
  severity: high
  notification: slack
  description: "{{ $value | humanizePercentage }} of results have low confidence"
  action: |
    1. Sample 10 low-confidence verses
    2. Check for meter distribution bias
    3. Review zihafat detection accuracy
    4. Check normalization issues

# 8. Cache Hit Rate Below Target
- alert: LowCacheHitRate
  expr: cache_hit_rate < 0.40
  for: 15m
  severity: high
  notification: slack
  description: "Cache hit rate {{ $value | humanizePercentage }} below 40% target"
  action: |
    1. Check Redis memory usage
    2. Review cache TTL settings
    3. Analyze query patterns
    4. Check for cache invalidation issues

# 9. API Latency P95 Warning
- alert: APILatencyP95Warning
  expr: histogram_quantile(0.95, http_request_duration_seconds_bucket{endpoint="/api/v1/analyze"}) > 0.500
  for: 10m
  severity: high
  notification: slack
  description: "P95 latency {{ $value }}s exceeds 500ms target"
  action: |
    1. Check CAMeL Tools memory usage
    2. Review slow queries in logs
    3. Check for database indexing issues
    4. Analyze verse length distribution

# 10. Rate Limit Breaches
- alert: RateLimitBreaches
  expr: rate(rate_limit_exceeded_total[5m]) > 10
  for: 5m
  severity: high
  notification: slack
  description: "{{ $value }} rate limit breaches per minute - potential abuse"
  action: |
    1. Check top offending IPs
    2. Review user agent patterns
    3. Consider IP blocking
    4. Check for DDoS patterns
```

### Medium Priority Alerts (Slack, No Page)

```yaml
# 11. Disk Space Warning
- alert: DiskSpaceWarning
  expr: node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes < 0.20
  for: 10m
  severity: medium
  notification: slack
  description: "Disk space {{ $value | humanizePercentage }} remaining"
  action: "Clean up old logs and backups"

# 12. Database Query Performance
- alert: SlowDatabaseQueries
  expr: rate(database_query_duration_seconds_sum[5m]) / rate(database_query_duration_seconds_count[5m]) > 0.100
  for: 10m
  severity: medium
  notification: slack
  description: "Average query time {{ $value }}s - review indexing"

# 13. High CPU Usage
- alert: HighCPUUsage
  expr: container_cpu_usage_seconds_total{container="bahr-api"} / container_cpu_limit > 0.80
  for: 10m
  severity: medium
  notification: slack
  description: "CPU usage {{ $value | humanizePercentage }} - scale if sustained"

# 14. Redis Memory Warning
- alert: RedisMemoryWarning
  expr: redis_memory_used_bytes / redis_memory_max_bytes > 0.80
  for: 10m
  severity: medium
  notification: slack
  description: "Redis memory {{ $value | humanizePercentage }} - eviction may occur"

# 15. Backup Failure
- alert: BackupFailure
  expr: time() - last_successful_backup_timestamp > 86400
  for: 1h
  severity: medium
  notification: slack
  description: "Backup hasn't succeeded in {{ $value | humanizeDuration }} - check backup job"
```

### Low Priority Alerts (Weekly Email Report)

```yaml
# 16. Meter Distribution Imbalance
- alert: MeterDistributionImbalance
  expr: |
    stddev(rate(prosody_analysis_by_meter_total[7d])) / 
    avg(rate(prosody_analysis_by_meter_total[7d])) > 0.5
  for: 24h
  severity: low
  notification: email
  description: "Meter distribution unbalanced - some meters rarely tested"
  frequency: weekly

# 17. User Growth Stagnation
- alert: UserGrowthStagnation
  expr: rate(user_registrations_total[7d]) == 0
  for: 7d
  severity: low
  notification: email
  description: "No new user registrations in 7 days"
  frequency: weekly

# 18. Low API Usage
- alert: LowAPIUsage
  expr: rate(http_requests_total[24h]) < 100
  for: 24h
  severity: low
  notification: email
  description: "API usage {{ $value }} req/day - unusually low"
  frequency: daily
```

---

## 📊 Alert Routing Configuration

```yaml
# Prometheus Alertmanager config
route:
  receiver: 'default'
  group_by: ['alertname', 'severity']
  group_wait: 10s
  group_interval: 5m
  repeat_interval: 3h
  
  routes:
    # Critical alerts -> PagerDuty + Slack
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      continue: true
    
    - match:
        severity: critical
      receiver: 'slack-critical'
    
    # High priority -> Slack
    - match:
        severity: high
      receiver: 'slack-high'
    
    # Medium priority -> Slack (batched)
    - match:
        severity: medium
      receiver: 'slack-medium'
      group_interval: 15m
    
    # Low priority -> Email weekly digest
    - match:
        severity: low
      receiver: 'email-digest'
      group_interval: 168h  # 7 days

receivers:
  - name: 'default'
    webhook_configs:
      - url: 'http://localhost:9093/webhook'
  
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: '<PAGERDUTY_KEY>'
        description: '{{ .GroupLabels.alertname }}: {{ .Annotations.description }}'
  
  - name: 'slack-critical'
    slack_configs:
      - api_url: '<SLACK_WEBHOOK_URL>'
        channel: '#alerts-critical'
        title: '🚨 CRITICAL: {{ .GroupLabels.alertname }}'
        text: '{{ .Annotations.description }}'
        color: 'danger'
  
  - name: 'slack-high'
    slack_configs:
      - api_url: '<SLACK_WEBHOOK_URL>'
        channel: '#alerts-high'
        title: '⚠️ HIGH: {{ .GroupLabels.alertname }}'
        text: '{{ .Annotations.description }}\n\nAction: {{ .Annotations.action }}'
        color: 'warning'
  
  - name: 'slack-medium'
    slack_configs:
      - api_url: '<SLACK_WEBHOOK_URL>'
        channel: '#alerts-medium'
        title: '📊 {{ .GroupLabels.alertname }}'
        color: '#439FE0'
  
  - name: 'email-digest'
    email_configs:
      - to: 'dev@bahr-platform.com'
        from: 'alerts@bahr-platform.com'
        subject: 'BAHR Weekly Alert Digest'
        html: '{{ range .Alerts }}{{ .Annotations.description }}<br>{{ end }}'
```

---

## 📈 Monitoring Dashboard Layout (Grafana)

### Dashboard 1: Overview (Real-time)

```yaml
Rows:
  1. Service Health:
     - Uptime (%)
     - Active Users
     - Request Rate (req/s)
     - Error Rate (%)
  
  2. API Performance:
     - P50/P95/P99 Latency (line chart)
     - Requests by Endpoint (bar chart)
     - Error Breakdown (pie chart)
  
  3. Prosody Engine:
     - Analysis Success Rate
     - Accuracy by Meter (gauge)
     - Confidence Distribution (histogram)
     - Avg Processing Time
  
  4. Infrastructure:
     - CPU Usage (%)
     - Memory Usage (MB)
     - Database Connections
     - Cache Hit Rate (%)

Refresh: 5 seconds
```

### Dashboard 2: Accuracy Tracking (Daily)

```yaml
Rows:
  1. Overall Accuracy:
     - Weekly Trend (line chart)
     - Accuracy by Meter (bar chart)
     - Confidence Distribution (stacked area)
  
  2. Error Analysis:
     - Failed Analysis Count
     - Error Types (pie chart)
     - Error Rate by Meter
  
  3. Data Quality:
     - Avg Verse Length
     - Zihafat Frequency
     - Era Distribution

Refresh: 1 minute
```

### Dashboard 3: User Behavior (Weekly)

```yaml
Rows:
  1. Usage Patterns:
     - Daily Active Users
     - Peak Usage Hours
     - Avg Verses per User
  
  2. Meter Popularity:
     - Most Analyzed Meters
     - Meter Distribution Over Time
  
  3. Performance by User:
     - Avg Response Time per User
     - Cache Hit Rate per User

Refresh: 5 minutes
```

---

## 🎯 SLA Commitments (Post-MVP)

### Grafana Dashboard Configuration:

```json
{
  "dashboard": {
    "title": "BAHR Poetry Platform - Overview",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate (req/s)",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ],
        "type": "graph"
      },
      {
        "id": 2,
        "title": "API Latency (P50/P95/P99)",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, http_request_duration_seconds_bucket)",
            "legendFormat": "P50"
          },
          {
            "expr": "histogram_quantile(0.95, http_request_duration_seconds_bucket)",
            "legendFormat": "P95"
          },
          {
            "expr": "histogram_quantile(0.99, http_request_duration_seconds_bucket)",
            "legendFormat": "P99"
          }
        ],
        "type": "graph",
        "yaxes": [{"format": "s"}]
      },
      {
        "id": 3,
        "title": "Error Rate (%)",
        "targets": [
          {
            "expr": "rate(http_requests_total{status_code=~\"5..\"}[5m]) / rate(http_requests_total[5m]) * 100"
          }
        ],
        "type": "graph",
        "alert": {
          "conditions": [
            {
              "evaluator": {"params": [5], "type": "gt"},
              "query": {"params": ["A", "5m", "now"]},
              "type": "query"
            }
          ]
        }
      },
      {
        "id": 4,
        "title": "Prosody Accuracy by Meter",
        "targets": [
          {
            "expr": "prosody_accuracy_score"
          }
        ],
        "type": "bargauge"
      },
      {
        "id": 5,
        "title": "Cache Hit Rate",
        "targets": [
          {
            "expr": "cache_hit_rate * 100"
          }
        ],
        "type": "stat",
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"value": 0, "color": "red"},
                {"value": 40, "color": "yellow"},
                {"value": 60, "color": "green"}
              ]
            }
          }
        }
      }
    ]
  }
}
```

### Log Aggregation Strategy:

```yaml
Logging Stack:
  Development:
    - Console logs (colored, structured)
    - Local file rotation (1GB max, 7 days retention)
    
  Production:
    - Structured JSON logs
    - Centralized aggregation (Loki or CloudWatch)
    - Log levels: INFO (default), WARNING, ERROR, CRITICAL
    - Retention: 30 days for INFO, 90 days for ERROR

Log Format (JSON):
  {
    "timestamp": "2025-11-08T10:30:45Z",
    "level": "INFO",
    "service": "bahr-backend",
    "endpoint": "/api/v1/analyze",
    "method": "POST",
    "status_code": 200,
    "duration_ms": 235,
    "user_id": "user-123",
    "detected_meter": "الطويل",
    "confidence": 0.92,
    "request_id": "req-abc-123"
  }

Critical Logs to Track:
  - All 5xx errors (with stack traces)
  - Authentication failures
  - Database connection errors
  - Cache misses on critical paths
  - Slow queries (> 500ms)
  - Low confidence analyses (< 0.65)
```

---

## 🧪 Performance Testing Strategy

### Load Testing:

```bash
# Using Locust (Python load testing framework)
# tests/performance/locustfile.py

from locust import HttpUser, task, between

class BahrUser(HttpUser):
    wait_time = between(1, 3)  # 1-3 seconds between requests
    
    @task(3)  # 3x more common than other tasks
    def analyze_verse(self):
        self.client.post("/api/v1/analyze", json={
            "text": "قِفا نَبكِ مِن ذِكرى حَبيبٍ وَمَنزِلِ",
            "options": {"analysis_mode": "accurate"}
        })
    
    @task(1)
    def get_meters(self):
        self.client.get("/api/v1/meters")

# Run test
# locust -f tests/performance/locustfile.py --host=http://localhost:8000
```

### Stress Testing:

```yaml
Test Scenarios:

Normal Load (Week 10):
  - 50 concurrent users
  - 5 minute duration
  - Target: All SLAs met

Peak Load (Week 11):
  - 150 concurrent users
  - 10 minute duration
  - Target: P95 latency < 2x normal

Spike Test (Week 11):
  - 0 → 200 users in 30 seconds
  - Hold for 2 minutes
  - Target: No crashes, graceful degradation

Endurance Test (Week 11):
  - 100 concurrent users
  - 2 hour duration
  - Target: No memory leaks, stable performance
```

### Benchmarking Commands:

```bash
# API Response Time
ab -n 1000 -c 10 -p verse.json -T application/json \
   http://localhost:8000/api/v1/analyze

# Database Query Performance
psql -c "EXPLAIN ANALYZE SELECT * FROM analyses WHERE detected_meter = 'الطويل';"

# Cache Performance
redis-cli --latency-history

# Frontend Performance
lighthouse --only-categories=performance http://localhost:3000
```

---

## 🎯 Performance Optimization Checklist

### Backend Optimizations:

```markdown
✅ Database:
  □ Indexes on all foreign keys
  □ JSONB GIN indexes for analysis_result
  □ Partial indexes for common queries
  □ Query result caching (Redis)
  □ Connection pooling configured
  □ Prepared statements for repeated queries

✅ API:
  □ Response compression (gzip)
  □ HTTP/2 enabled
  □ Static asset caching (CDN)
  □ Request validation at edge
  □ Rate limiting per user
  □ Batch endpoints for multiple texts

✅ Application:
  □ Singleton NLP analyzers
  □ LRU cache for patterns
  □ Lazy loading of heavy modules
  □ Async processing for slow tasks
  □ Memory profiling completed
  □ No N+1 query patterns
```

### Frontend Optimizations:

```markdown
✅ Build:
  □ Code splitting by route
  □ Tree shaking enabled
  □ Minification + uglification
  □ Dead code elimination
  □ Source maps for production debugging

✅ Runtime:
  □ React.memo for expensive components
  □ Virtual scrolling for long lists
  □ Debounced user inputs
  □ Optimistic UI updates
  □ Service worker for offline
  □ Image lazy loading

✅ Network:
  □ API request batching
  □ Response caching (React Query)
  □ Prefetching on hover
  □ WebSocket for real-time features
  □ CDN for static assets
```

---

## 📈 Performance Evolution Goals

```yaml
MVP Launch (Week 12):
  Meter Detection: 80% accuracy
  P95 Latency: < 500ms
  Concurrent Users: 100
  Cache Hit Rate: > 60%

3 Months Post-Launch:
  Meter Detection: 85% accuracy
  P95 Latency: < 300ms
  Concurrent Users: 500
  Cache Hit Rate: > 75%

6 Months Post-Launch:
  Meter Detection: 90% accuracy
  P95 Latency: < 200ms
  Concurrent Users: 1000
  Cache Hit Rate: > 80%

1 Year:
  Meter Detection: 95% accuracy
  P95 Latency: < 150ms
  Concurrent Users: 5000
  Cache Hit Rate: > 85%
```

---

## 🔍 Performance Monitoring Dashboard

### Grafana Dashboard Panels:

```yaml
Row 1 - Overview:
  - Total Requests (counter)
  - Active Users (gauge)
  - Error Rate (graph)
  - Success Rate (percentage)

Row 2 - Latency:
  - P50/P95/P99 Response Time (graph)
  - Slow Queries (table)
  - Cache Performance (graph)

Row 3 - Resources:
  - CPU Usage (graph)
  - Memory Usage (graph)
  - Database Connections (graph)
  - Redis Memory (graph)

Row 4 - Business:
  - Analyses per Hour (graph)
  - Most Common Meters (pie chart)
  - Accuracy Distribution (histogram)
  - User Engagement (graph)
```

---

## 🚨 Performance Incident Response

```yaml
When P95 Latency Exceeds Target:

Step 1: Immediate (< 1 min)
  - Check Grafana dashboard
  - Identify spike in traffic or errors
  - Check recent deployments

Step 2: Diagnosis (< 5 min)
  - Review slow query logs
  - Check cache hit rate
  - Monitor CPU/Memory
  - Check external dependencies

Step 3: Mitigation (< 15 min)
  - Scale horizontally if traffic spike
  - Clear cache if corrupted
  - Rollback if bad deployment
  - Enable read replica if DB overload

Step 4: Resolution (< 1 hour)
  - Fix root cause
  - Deploy hotfix if needed
  - Update monitoring
  - Document incident
```

---

**Last Updated:** November 8, 2025  
**Next Review:** Week 8 (before beta launch)  
**Owner:** Backend Lead
