# 📊 Metrics Reference (Prometheus + Observability)
آخر تحديث: 2025-11-08

## الهدف
تحديد المقاييس المبدئية، أنواعها، دلالتها، وحدودها، وخطة التطوير.

---
## 1. المقاييس الأساسية (Core)
| Metric | Type | Labels | وصف | SLO/SLA |
|--------|------|--------|-----|---------|
| bahr_request_duration_seconds | Histogram | endpoint, method | زمن كل طلب HTTP | P95 < 800ms (MVP), <600ms (Week6) |
| verse_analysis_latency_seconds | Histogram | mode | زمن تحليل بيت واحد | P95 < 600ms |
| bahr_analysis_cache_hit_total | Counter | - | عدد ضربات الكاش | معدل hit > 40% |
| bahr_meter_confidence | Gauge | meter | آخر ثقة معايرة | مراقبة انخفاضات مفاجئة |
| analysis_timeouts_total | Counter | - | عدد حالات مهلة | يجب أن يبقى ~0 في الطبيعي |
| bahr_errors_total | Counter | code | إجمالي الأخطاء المصنفة | <2% من إجمالي الطلبات |

---
## 2. Buckets مقترحة
`verse_analysis_latency_seconds`:
```
(0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1, 2, 3)
```
تجنب عدد كبير جدًا من الـ buckets في البداية (الاكتفاء بعملية ضبط لاحق).

---
## 3. تسجيل الثقة (Confidence)
- تحديث gauge عند إتمام التحليل فقط.
- لا تخزن قيم منخفضة للغاية دون حاجة؛ يمكن مراقبة المتوسط لاحقًا بإضافة summary.

---
## 4. اشتقاق مؤشرات (Derived KPIs)
| KPI | صيغة | الغرض |
|-----|------|-------|
| Cache Hit Ratio | cache_hits / (cache_hits + misses) | تقييم فعالية التطبيع + التخزين |
| Error Rate | errors_total / requests_total | جودة و استقرار |
| Avg Confidence | sum(confidence)/count(analyses) | تتبع تطور المحرك |
| Timeout % | analysis_timeouts_total / analyses_total | اكتشاف ضيق موارد أو أخطاء منطق |

---
## 5. تنبيهات أولية (Alerts)
| Alert | Expr | Window | Severity |
|-------|------|--------|---------|
| HighErrorRate | error_rate > 0.05 | 10m | warning |
| HighLatency | P95(verse_analysis_latency_seconds) > 0.8 | 15m | warning |
| CacheInefficiency | cache_hit_ratio < 0.25 | 30m | info |
| ConfidenceDrop | avg_confidence < 0.55 | 1h | info |
| TimeoutSpike | increase(analysis_timeouts_total[10m]) > 20 | 5m | critical |

---
## 6. أفضل الممارسات
- لا تضف label بقيم عالية الكاردينالية (مثل user_id).
- endpoint label يجب أن يكون عام (لا يشمل معرفات ديناميكية).
- راجع حجم السلاسل الزمنية كل شهر.

---
## 7. توسعة مستقبلية
Phase 2:
- إضافة tracing (OpenTelemetry) لقياس أجزاء pipeline داخلي.
- Histogram مخصص لـ segmentation و meter detection.
- Metric لعدد البدائل المعروضة للبحور.

Phase 3:
- مقاييس لتوليد الشعر (generation_latency_seconds, plagiarism_score_distribution).

---
## 8. دمج مع Grafana
Panels مقترحة:
1. Latency (histogram + quantiles)
2. Error Rate
3. Cache Hit Ratio
4. Confidence Trend
5. Timeouts Trend
6. Requests Per Endpoint

---
## 9. اختبارات المقاييس (Testing Strategy)
- اختبار وجود `/metrics` (status 200) في بيئة التطوير.
- محاكاة تحليل بيتين، تأكد من زيادة histogram.
- حقن خطأ صناعي و تحقق من زيادة counter.

---
## 10. تحديثات مطلوبة عند التغيير
أي إضافة/إزالة Metric:
1. تحديث هذا الملف.
2. تحديث `ARCHITECTURE_OVERVIEW.md` (قسم المقاييس إن لزم).
3. إضافة سطر في `CRITICAL_CHANGES.md` مع rationale.

---
## 11. خاتمة
مقياس قليل واضح أفضل من كثير مربك في مرحلة MVP. ركّز على التأثير المباشر (سرعة، ثقة، أخطاء، كاش).
