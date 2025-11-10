# ✅ Implementation Checklist (MVP Phase 1)
آخر تحديث: 2025-11-08

الغرض: قائمة تنفيذ عملية يمكن المرور عليها بسرعة للتأكد من جاهزية النظام من ناحية الكود والبنية.

---
## 1. البيئة و المتغيرات
- [ ] أنشأت `.env` مطابقًا للجدول في `ARCHITECTURE_OVERVIEW.md`
- [ ] SECRET_KEY قوي (>= 32 chars) وليس افتراضيًا
- [ ] قاعدة البيانات متاحة (`psql` اختبار اتصال)
- [ ] Redis يعمل (PING)

## 2. الهيكل الأساسي للكود (Backend)
- [ ] مجلد `backend/app/` يحتوي `main.py`
- [ ] مجلد `middleware/` يحوي `response_envelope.py`
- [ ] مجلد `metrics/` يحوي `analysis_metrics.py`
- [ ] واجهات التحليل (interfaces أو طبقة الخدمات) معرفة

## 3. الاستجابة الموحدة (Response Envelope)
- [ ] كل Endpoint يعيد `{success, data|null, error|null, meta{request_id,timestamp}}`
- [ ] توجد Middleware تضيف `request_id` إذا لم يرسل من العميل
- [ ] الأخطاء تستعمل قاموس الرسائل `ERROR_HANDLING_STRATEGY.md`

## 4. التحليل العروضي
- [ ] Normalizer يعمل على أمثلة بها تشكيل وبدونه
- [ ] Segmenter ينتج نمط مقاطع ثابت لثلاثة أبيات اختبار
- [ ] Pattern matcher يعطي تفاعيل أولية
- [ ] MeterDetector يرجع بحر + بدائل + raw_confidence
- [ ] ConfidenceCalibrator فعّال ويعدل القيم في حالات (سهل/صعب)

## 5. التخزين المؤقت (Cache)
- [ ] مفتاح النتيجة `analysis:{md5(normalized_text)}`
- [ ] TTL الافتراضي 3600s
- [ ] مسار تحليل يميز النتائج المخزنة (meta.cached=true)

## 6. الأمان الأساسي
- [ ] bcrypt rounds=12 مفعلة في كلمة المرور
- [ ] JWT access (30m) + refresh (7d) يعملان
- [ ] رفض طلبات بلا صلاحية إلى مسارات محمية
- [ ] لا توجد كلمات مرور نصية في السجلات

## 7. المقاييس (Metrics)
- [ ] `/metrics` يعمل (Prometheus instrumentator)
- [ ] Histogram لـ `verse_analysis_latency_seconds` يسجل قيمًا
- [ ] Counter `analysis_timeouts_total` يزيد عند فشل متعمد تجريبي

## 8. التسجيل (Logging)
- [ ] سجل منظم يحتوي: level, timestamp, request_id, path
- [ ] حدث `analysis.completed` يسجل meter و latency_ms

## 9. الأخطاء و التدهور التدريجي
- [ ] تحليل فشل → fallback rule-based → basic
- [ ] يعاد خطأ موحد مع code من التصنيف
- [ ] حالات timeout مجربة (محاكاة sleep > حد زمني)

## 10. الأداء المبدئي
- [ ] P95 تحليل 10 أبيات اختبار < 800ms (مبدئي)
- [ ] قياس أولي للدقة (≥ 60%) على مجموعة صغيرة (10–15 بيت)

## 11. الهجرة (Migrations)
- [ ] Alembic baseline (users, meters, analyses, system_settings)
- [ ] تطبيق `alembic upgrade head` بدون أخطاء
- [ ] إدراج بيانات البحور الأساسية ناجح

## 12. خطة المخاطر السريعة
- [ ] pyarabic وظائف حرجة معاد تنفيذها داخليًا أو مخطط لذلك
- [ ] سجل مراقبة للذاكرة (اختياري) لمراقبة نمو غير طبيعي

## 13. التكامل المستقبلي (Hooks)
- [ ] واجهات منفصلة للتحليل (ITextNormalizer ..) تسمح بحقن ML لاحقًا
- [ ] حقل `analysis_engine_version` في meta

## 14. المراقبة والتنبيهات (اختياري Week 2)
- [ ] Dashboard أولي (latency/error/cache) في Grafana
- [ ] تنبيه خطأ مرتفع (إذا محقق)

## 15. التوثيق المراجع
- [ ] `ARCHITECTURE_OVERVIEW.md` محدث
- [ ] روابط في `README.md` تشير للملف الجديد

---
## تمرير نهائي (Go / No-Go)
- [ ] كل العناصر الحرجة (1–10) مكتملة
- [ ] المخاطر المعروفة مسجلة في `CRITICAL_CHANGES.md`
- [ ] لا يوجد سر حساس داخل المستودع
- [ ] يمكن تشغيل تحليل بيت من curl / client بنجاح

عند اكتمال القائمة: وسم المهمة "Finalize developer-readiness" مكتملة.
