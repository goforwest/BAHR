# 🛠️ Monitoring & Observability Integration

هدف هذه الوثيقة: توفير دليل عملي سريع لتهيئة المقاييس (metrics) والتسجيل (logging) والتنبيهات (alerts) لـ BAHR خلال مرحلة الـ MVP، مع مسار واضح للتوسعة لاحقًا.

## 🎯 أهداف الـ MVP
- رؤية زمن استجابة تحليل البيت (p50 / p95 / p99).
- معدل الأخطاء (5xx و أخطاء منطقية محددة مثل METER_NOT_FOUND).
- عدد الطلبات لكل ساعة لكل Endpoint.
- مراقبة معدل حالات المهلة (timeouts_fallback) في التحليل.
- استخدام Dashboard أساسي في Grafana مع 6 Panels رئيسية.

## 📦 الحزم المطلوبة
```bash
pip install prometheus-fastapi-instrumentator==6.1.0
pip install structlog==23.2.0
```

## 📈 تفعيل /metrics
انظر المقتطف المُضاف في `BACKEND_API.md`. بعد تشغيل التطبيق سيصبح المسار:
```
GET http://localhost:8000/metrics
```
يعرِض مقاييس Prometheus القياسية + مقاييس FastAPI.

## ➕ مقاييس مخصصة (Custom Metrics)
مثال لإضافة Histogram لزمن تحليل البيت:
```python
# app/metrics/analysis_metrics.py
from prometheus_client import Histogram

VERSE_ANALYSIS_LATENCY = Histogram(
    'verse_analysis_latency_seconds',
    'Latency of single verse prosody analysis',
    buckets=(0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1, 2, 3, 5)
)

def record_latency(seconds: float):
    VERSE_ANALYSIS_LATENCY.observe(seconds)
```
دمجها في الخدمة:
```python
import time
from app.metrics.analysis_metrics import record_latency

start = time.perf_counter()
result = analyzer.analyze(text, options)
record_latency(time.perf_counter() - start)
```

## 🧪 تتبع حالات المهلة
عند حدوث مهلة (TimeoutError) في التحليل، سجّل عدّادًا:
```python
from prometheus_client import Counter
ANALYSIS_TIMEOUTS = Counter('analysis_timeouts_total', 'Total analysis timeouts triggering fallback')
```
وفي كتلة except:
```python
ANALYSIS_TIMEOUTS.inc()
```

## 📜 التسجيل (Structured Logging)
استخدم `structlog` لإضافة حقول سياقية (request_id, user_id, meter_detected, latency_ms):
```python
import structlog
logger = structlog.get_logger()
logger.info("analysis.completed", request_id=req_id, latency_ms=round(latency*1000), meter=meter_name)
```
اجعل صيغة الإنتاج JSON لتسهيل تجميعها عبر Loki أو ELK لاحقًا.

## 🗂️ مثال تكوين Prometheus (prometheus.yml)
```yaml
scrape_configs:
  - job_name: bahr_backend
    metrics_path: /metrics
    scrape_interval: 15s
    static_configs:
      - targets: ['backend:8000']
```

## 📊 لوحة Grafana (لوحة مبدئية)
Panels مقترحة:
1. Requests per endpoint (rate).
2. Verse analysis latency histogram & summary (p50/p95/p99).
3. Error rate (5xx vs 4xx).
4. Timeout fallback counter over time.
5. Top meters frequency (بعد توفر البيانات).
6. CPU / Memory (Node exporter أو cAdvisor لاحقًا).

## 🔔 التنبيهات (Alerts)
أمثلة قواعد مبدئية:
```yaml
- alert: HighErrorRate
  expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "High 5xx rate (>5%)"

- alert: AnalysisTimeoutSpike
  expr: increase(analysis_timeouts_total[10m]) > 20
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Spike in analysis timeouts"
```

## 🚀 توسعة بعد الـ MVP
- دمج تتبع (Tracing) عبر OpenTelemetry (FastAPI instrumentation) لإظهار السلاسل بين API وطبقة التحليل.
- إضافة Cardinality Limits للمقاييس ذات التسميات الديناميكية.
- جمع سجلات إلى Loki + ربط Panel "LogQL" في نفس لوحة Grafana.

## ✅ قائمة تحقق التنفيذ
- [ ] /metrics يعمل ويرجع مقاييس.
- [ ] Histogram زمن التحليل يُحدِث القيم.
- [ ] Counter للمهلة يزيد عند وقوع مهلة.
- [ ] لوحة Grafana بها 6 Panels أساسية.
- [ ] قاعدتا تنبيه (خطأ / مهلة) نشطتان.

راجع أيضًا: `PERFORMANCE_TARGETS.md`, `ERROR_HANDLING_STRATEGY.md`.
