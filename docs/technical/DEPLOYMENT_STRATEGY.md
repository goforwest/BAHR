# 🚀 دليل النشر (Deployment Guide)
## إستراتيجية نشر منصة بَحْر - الإصدار الأول (MVP)

---

## 🎯 الهدف
توفير خطوات واضحة وقابلة للتنفيذ لنشر المنصة (Backend + Frontend + DB + مراقبة) في بيئة تجريبية ثم إنتاجية، مع الحد الأدنى من التعقيد وتهيئة التوسع المستقبلي.

---

## 🧱 المكونات الأساسية للنشر
- Backend (FastAPI) حاوية Docker
- Frontend (Next.js) حاوية Docker (بناء static أو تشغيل Node حسب المرحلة)
- PostgreSQL مُدارة (يفضل Cloud: Supabase / RDS / Neon) أو حاوية مبدئية
- Redis (Caching + Rate Limiting) – حاوية أو خدمة مُدارة
- مراقبة: Prometheus + Grafana (Week 2+)
- أخطاء: Sentry (اختياري لاحقاً)

---

## 🏢 قرار استضافة الإنتاج (Production Hosting Decision)

### خيارات الاستضافة المقترحة:

#### **Option 1: Railway (موصى به للMVP) 💚**
```yaml
Pros:
  - نشر تلقائي من Git
  - PostgreSQL + Redis مدمجة
  - تسعير بسيط ($5-20/month للMVP)
  - دعم Docker native
  - SSL مجاني + Domain
Cons:
  - محدودية التخصيص
  - قد يكون مكلفًا مع النمو
Use Case: MVP + Beta (Week 1-12)
```

#### **Option 2: DigitalOcean App Platform**
```yaml
Pros:
  - مرونة أعلى من Railway
  - تسعير متوقع ($12-30/month)
  - PostgreSQL Managed Database
  - Monitoring مدمج
Cons:
  - تعقيد أعلى قليلاً
  - Redis يحتاج إعداد منفصل
Use Case: Post-MVP growth (3-6 months)
```

#### **Option 3: Vercel (Frontend) + Railway (Backend)**
```yaml
Pros:
  - Vercel مثالي لـ Next.js (تحسين تلقائي)
  - Railway للBackend + DB
  - أداء ممتاز للمستخدمين
Cons:
  - إدارة منصتين منفصلتين
  - تكلفة أعلى قليلاً
Use Case: Production launch (Week 13+)
```

**القرار الموصى به:**
- **MVP (Week 1-12):** Railway All-in-One
- **Production (Week 13+):** Migrate to Vercel (Frontend) + DigitalOcean (Backend)

---

## 🗂️ هيكل مجلد النشر (محدّث)
```
BAHR/
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── production.txt
│   │   └── development.txt
│   └── ...
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── next.config.js
│   └── ...
├── docker-compose.yml          # للتطوير المحلي
├── docker-compose.prod.yml     # للإنتاج (اختياري)
├── .env.example                # نموذج المتغيرات البيئية
├── railway.json                # تكوين Railway (إن استخدم)
└── scripts/
    ├── deploy_dev.sh
    ├── deploy_prod.sh
    ├── migrate.sh
    └── backup_db.sh
```

---

## 🐳 Dockerfiles (أمثلة مبسطة)

### Backend (`backend/Dockerfile`)
```dockerfile
# Multi-stage build for production optimization
FROM python:3.11-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install Python dependencies
COPY requirements/base.txt requirements/production.txt ./
RUN pip install -r production.txt

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Create non-root user
RUN useradd -m -u 1000 bahr && chown -R bahr:bahr /app
USER bahr

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/api/v1/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### Frontend (`frontend/Dockerfile`)
```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build Next.js app
RUN npm run build

# Production stage
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy built assets
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Change ownership
RUN chown -R nextjs:nodejs /app

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### Docker Compose للتطوير المحلي (`docker-compose.yml`)
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: bahr_postgres
    environment:
      POSTGRES_DB: bahr_dev
      POSTGRES_USER: bahr
      POSTGRES_PASSWORD: dev_password_change_me
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U bahr"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: bahr_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: bahr_backend
    environment:
      DATABASE_URL: postgresql://bahr:dev_password_change_me@postgres:5432/bahr_dev
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: dev_secret_key_change_in_production
      DEBUG: "True"
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: builder  # Use builder stage for hot reload
    container_name: bahr_frontend
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    depends_on:
      - backend
    command: npm run dev

  prometheus:
    image: prom/prometheus:latest
    container_name: bahr_prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    container_name: bahr_grafana
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin_change_me
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana-dashboards:/etc/grafana/provisioning/dashboards
    depends_on:
      - prometheus

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

---

## 🔄 استراتيجية المهاجرات (Database Migration Strategy)

### إعداد Alembic (Week 1)
```bash
# في مجلد backend/
alembic init alembic

# تحديث alembic.ini
# sqlalchemy.url = postgresql://user:pass@localhost/dbname
```

### إنشاء Migration جديد
```bash
# بعد تعديل models
alembic revision --autogenerate -m "Add meters table"

# مراجعة الملف المُنشأ في alembic/versions/
# تأكد من أن التغييرات صحيحة!
```

### تطبيق Migrations

**محلياً (Development):**
```bash
# تطبيق آخر migration
alembic upgrade head

# التراجع عن آخر migration
alembic downgrade -1

# عرض تاريخ Migrations
alembic history
```

**في Docker:**
```bash
# تطبيق migrations عند بدء الحاوية
docker compose run --rm backend alembic upgrade head

# أو إضافة في entrypoint.sh
#!/bin/bash
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**في الإنتاج (Railway/DigitalOcean):**
```bash
# Option 1: تشغيل migration كـ one-off command
railway run alembic upgrade head

# Option 2: في CI/CD pipeline
# .github/workflows/deploy.yml
- name: Run migrations
  run: |
    alembic upgrade head
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Best Practices للMigrations
```yaml
قبل إنشاء Migration:
  - ✅ قم بالـ backup للقاعدة قبل تطبيق migrations في الإنتاج
  - ✅ اختبر الـ migration على نسخة staging أولاً
  - ✅ راجع الـ SQL المُنشأ تلقائياً (قد يحتاج تعديل!)
  - ✅ أضف default values للأعمدة الجديدة لتجنب أخطاء NOT NULL

في الإنتاج:
  - ⚠️ لا تحذف أعمدة مباشرة - علّمها deprecated أولاً
  - ⚠️ استخدم transactions للعمليات الحرجة
  - ⚠️ احتفظ بنسخة backup قبل كل migration
  - ⚠️ توثيق كل migration بتعليق واضح
```

### مثال Migration Script
```python
# alembic/versions/001_add_meters_table.py
"""Add meters table

Revision ID: 001
Create Date: 2025-11-08
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # إنشاء جدول meters
    op.create_table(
        'meters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('english_name', sa.String(100)),
        sa.Column('base_pattern', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # إنشاء index
    op.create_index('idx_meters_name', 'meters', ['name'])
    
    # إدراج البحور الأساسية
    op.execute("""
        INSERT INTO meters (name, english_name, base_pattern) VALUES
        ('الطويل', 'At-Taweel', 'فعولن مفاعيلن فعولن مفاعيلن'),
        ('الكامل', 'Al-Kamil', 'متفاعلن متفاعلن متفاعلن'),
        ('الوافر', 'Al-Wafir', 'مفاعلتن مفاعلتن فعولن');
    """)

def downgrade():
    op.drop_index('idx_meters_name', table_name='meters')
    op.drop_table('meters')
```

---

## 🔐 إدارة المتغيرات البيئية (Environment Variables Management)

### ملف `.env.example` (نموذج للمطورين)
```bash
# Application
PROJECT_NAME=BAHR Poetry Analysis Platform
DEBUG=True
SECRET_KEY=your-secret-key-min-32-chars
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Database
DATABASE_URL=postgresql://bahr:password@localhost:5432/bahr_dev
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_MAX_CONNECTIONS=10

# API
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600

# CORS
ALLOWED_ORIGINS=http://localhost:3000

# Email (اختياري)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=

# Monitoring
SENTRY_DSN=
LOG_LEVEL=INFO

# External APIs (Phase 2+)
OPENAI_API_KEY=
HUGGINGFACE_TOKEN=
```

### إدارة Secrets في الإنتاج

#### Railway
```bash
# عبر واجهة Railway Dashboard
# 1. اذهب إلى Project Settings > Variables
# 2. أضف كل متغير بشكل منفصل
# 3. Railway يعيد النشر تلقائياً عند التغيير

# أو عبر CLI
railway variables set SECRET_KEY=your-production-secret
railway variables set DATABASE_URL=postgresql://...
```

#### GitHub Actions (للCI/CD)
```yaml
# .github/workflows/deploy.yml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  SECRET_KEY: ${{ secrets.SECRET_KEY }}
  REDIS_URL: ${{ secrets.REDIS_URL }}

# إضافة Secrets:
# GitHub Repo > Settings > Secrets > Actions > New repository secret
```

#### DigitalOcean App Platform
```bash
# عبر doctl CLI
doctl apps create-deployment <app-id> \
  --env "SECRET_KEY=your-secret" \
  --env "DATABASE_URL=postgresql://..."

# أو عبر Dashboard
# App > Settings > App-Level Environment Variables
```

### Best Practices للSecrets
```yaml
✅ DO:
  - استخدم secrets manager (Railway/GitHub/Vault)
  - قم بتدوير SECRET_KEY كل 3-6 أشهر
  - استخدم DATABASE_URL كاملة (تتضمن الاعتماديات)
  - افصل بيئات dev/staging/production بـ secrets مختلفة

❌ DON'T:
  - لا تضع secrets في Git EVER
  - لا تشارك .env files عبر email/slack
  - لا تستخدم secrets بسيطة (password123)
  - لا تضع API keys في frontend code
```

### توليد SECRET_KEY آمن
```python
# في Python
import secrets
print(secrets.token_urlsafe(32))
# Output: XYZ123ABC...  (استخدم هذا)

# أو في terminal
openssl rand -base64 32
```

---

## 🚦 إستراتيجية الإطلاق التدريجي
1. Dev: تشغيل محلي (`docker-compose.dev.yml`)
2. Staging: حاويات على VPS (مثلاً Hetzner) أو Render
3. Production: خدمة مُدارة لقاعدة البيانات + حاويات ثابتة + مراقبة

Rollback (مبسط):
- احتفظ بآخر صورتين (tags: `vX.Y.Z`, `vX.Y.Z-prev`)
- عند الفشل: أعد تشغيل الحاوية باستخدام الصورة السابقة:
```bash
docker compose pull backend:previous && docker compose up -d backend
```

---

## 📊 المراقبة الأساسية (Monitoring)
Prometheus Targets:
- Backend `/metrics` (أضِف لاحقًا)
- Redis Exporter (اختياري)
Grafana Dashboards:
- Latency (P50/P95/P99)
- Error Rate
- Cache Hit Rate
- DB Connections

Alert مثال (مستقبلاً):
- Error Rate > 5% لمدة 2 دقيقة → Slack/Webhook

---

## 📦 التخزين والنسخ الاحتياطي
PostgreSQL:
- تطوير: تفريغ بسيط (pg_dump يومي)
- إنتاج: خدمة مُدارة (تلقائي)
Redis:
- بيانات مؤقتة؛ لا حاجة لنسخ كامل في MVP

Script مثال:
```bash
pg_dump $DATABASE_URL > backup_$(date +%F).sql
```

---

## 🔄 Disaster Recovery & Business Continuity
**تمت الإضافة:** November 8, 2025 (Post Expert Review)

### استراتيجية النسخ الاحتياطي (Backup Strategy)

#### قاعدة البيانات (PostgreSQL):

```yaml
Backup Frequency:
  MVP (Week 1-12):
    - Daily automated backups (3 AM UTC)
    - Retention: 7 days
    - Storage: Platform-managed (Railway/DO)
  
  Production (Week 13+):
    - Automated backups every 6 hours
    - Retention: 30 days
    - Point-in-time recovery: Last 7 days
    - Storage: Separate cloud bucket (AWS S3 / DigitalOcean Spaces)

Backup Encryption:
  - AES-256 encryption at rest (handled by platform)
  - Transfer: TLS 1.3 during upload
  - Access Control: Restricted to admin user only

Backup Testing:
  - Monthly restore test (1st of each month)
  - Validate data integrity after restore
  - Document restore time (should be < 30 minutes for MVP database)

Automation Script:
  ```bash
  #!/bin/bash
  # backup_db.sh - Daily automated backup
  
  DATE=$(date +%Y-%m-%d-%H%M%S)
  BACKUP_DIR="/backups/postgres"
  RETENTION_DAYS=7
  
  # Create backup
  pg_dump $DATABASE_URL | gzip > $BACKUP_DIR/backup_$DATE.sql.gz
  
  # Encrypt backup (optional for extra security)
  gpg --encrypt --recipient admin@bahr.com $BACKUP_DIR/backup_$DATE.sql.gz
  
  # Upload to cloud storage (example: AWS S3)
  aws s3 cp $BACKUP_DIR/backup_$DATE.sql.gz.gpg s3://bahr-backups/postgres/
  
  # Clean up old backups (keep last 7 days)
  find $BACKUP_DIR -name "backup_*.sql.gz*" -mtime +$RETENTION_DAYS -delete
  
  # Verify backup integrity
  gunzip -t $BACKUP_DIR/backup_$DATE.sql.gz
  
  echo "Backup completed: backup_$DATE.sql.gz"
  ```
```

#### Redis Cache:

```yaml
Backup Strategy:
  - NO automated backups (MVP)
  - Rationale: Redis is ephemeral cache only
  - Recovery: Rebuild from PostgreSQL (acceptable delay)
  
  Production (Future):
    - RDB snapshots every 6 hours (if using Redis for sessions)
    - AOF (Append-Only File) for durability
```

#### User Uploads (Phase 2+):

```yaml
When Implemented:
  - Storage: S3-compatible object storage (R2, DO Spaces)
  - Versioning: Enabled (protect against accidental deletion)
  - Backup: Cross-region replication
  - Retention: 90 days for deleted files
```

### Recovery Objectives:

```yaml
Recovery Time Objective (RTO):
  MVP: 4 hours
    - Time to restore database from backup
    - Time to redeploy application
    - Time to verify functionality
  
  Production: 1 hour
    - Automated failover to standby
    - Manual verification and DNS update
  
  Breakdown:
    1. Detection: < 15 minutes (monitoring alerts)
    2. Decision: < 15 minutes (assess severity)
    3. Restore: < 2 hours (database + redeploy)
    4. Testing: < 1 hour (smoke tests + verification)
    5. Communication: < 30 minutes (notify users if needed)

Recovery Point Objective (RPO):
  MVP: 24 hours
    - Maximum data loss: 1 day of analyses
    - Daily backups at 3 AM UTC
    - Acceptable for beta users
  
  Production: 1 hour
    - Continuous replication to standby
    - 6-hour backup snapshots
    - Point-in-time recovery available
```

### Restore Procedures:

#### Database Restore (PostgreSQL):

```bash
# 1. Stop application (prevent new writes)
railway run --service backend pm2 stop all

# 2. Download backup from cloud storage
aws s3 cp s3://bahr-backups/postgres/backup_2025-11-08.sql.gz.gpg ./

# 3. Decrypt backup (if encrypted)
gpg --decrypt backup_2025-11-08.sql.gz.gpg > backup_2025-11-08.sql.gz

# 4. Decompress
gunzip backup_2025-11-08.sql.gz

# 5. Restore to database
# WARNING: This will overwrite existing data!
psql $DATABASE_URL < backup_2025-11-08.sql

# 6. Verify data integrity
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM analyses;"
psql $DATABASE_URL -c "SELECT MAX(created_at) FROM analyses;"  # Check latest data

# 7. Restart application
railway run --service backend pm2 restart all

# 8. Smoke test
curl -f https://api.bahr.com/api/v1/health
```

#### Full System Recovery (Worst Case):

```yaml
Scenario: Complete platform failure (Railway/DO down)

Steps:
  1. Provision new infrastructure:
     - Spin up new backend instance
     - Create new PostgreSQL database
     - Create new Redis instance
  
  2. Restore database:
     - Download latest backup from S3
     - Restore to new database
     - Verify data integrity
  
  3. Deploy application:
     - Pull latest Docker images
     - Update environment variables (new DB URLs)
     - Deploy backend + frontend
  
  4. Update DNS:
     - Point domain to new infrastructure
     - TTL: 5 minutes (fast propagation)
  
  5. Verify and monitor:
     - Run smoke tests
     - Monitor error rates
     - Check user reports
  
  Estimated Time: 3-4 hours (within RTO)
```

### Secrets & Configuration Backup:

```yaml
Critical Secrets to Backup:
  - JWT Secret Key (SECRET_KEY)
  - Database credentials (DATABASE_URL)
  - Redis URL (REDIS_URL)
  - API keys (OpenAI, Hugging Face)
  - SSL certificates
  - Environment variables (.env.production)

Storage:
  - 1Password / AWS Secrets Manager / HashiCorp Vault
  - NEVER commit to Git
  - Document which team members have access
  
Rotation Schedule:
  - JWT Secret: Every 90 days
  - Database password: Every 180 days
  - API keys: On compromise or annually
```

### Monitoring & Alerting:

```yaml
Critical Alerts (Page Immediately):
  - Database down (> 5 minutes)
  - Backend down (> 3 minutes)
  - Disk usage > 90%
  - Memory usage > 90%
  - Error rate > 10%

Non-Critical Alerts (Email):
  - Backup failed
  - Slow query detected (> 1 second)
  - API latency P95 > 1 second
  - Unusual traffic patterns

Alert Channels:
  - Slack: #bahr-alerts
  - Email: admin@bahr.com
  - SMS: Critical alerts only (production)
```

### Communication Plan:

```yaml
User Communication:
  Minor Issues (< 30 min downtime):
    - Post-mortem in changelog
    - No user notification needed
  
  Major Issues (> 30 min downtime):
    - Status page update: status.bahr.com
    - Twitter/Social media announcement
    - Email to active users (if > 2 hours)
  
  Data Loss:
    - Immediate notification to all affected users
    - Explanation of what was lost
    - Compensation plan (if applicable)

Template:
  "We experienced a technical issue from [TIME] to [TIME] affecting [FEATURE].
   The issue has been resolved. We apologize for the inconvenience.
   If you experience any problems, please contact support@bahr.com"
```

---

## 🧪 قائمة التحقق قبل كل نشر (Pre-Deploy Checklist)
- [ ] إصدارات الحاويات مبنية Tagged (`backend:vX.Y.Z`, `frontend:vX.Y.Z`)
- [ ] نجحت المهاجرات محلياً
- [ ] اختبارات وحدة API (تحليل، مصادقة) ناجحة
- [ ] قياس زمن تحليل بيت واحد ضمن الهدف
- [ ] لا يوجد مفاتيح حساسة في Git
- [ ] ملف CHANGELOG/CRITICAL_CHANGES مُحدّث

---

## ⏱️ إدارة الأداء الأولية
- تحقق من حجم الصورة: هدف < 200MB (backend)، < 300MB (frontend build)
- استخدم `--no-cache-dir` في pip لتقليل الحجم
- أضِف طبقة caching لاحقاً (Poetry + multi-stage)

---

## 🔐 الأمن الأساسي (Security Baseline)
- تفعيل CORS بنطاق محدد (localhost/النطاق الفعلي)
- منع رفع الملفات الكبيرة (الحد في الإعدادات)
- تسجيل محاولات تجاوز المعدل (Rate Limit) في سجل مستقل
- تأجيل ميزات متقدمة (RLS, JWT Rotation) لما بعد الإطلاق

---

## 🧪 اختبار الدخان (Smoke Test) بعد النشر
```bash
curl -f https://your-domain.com/api/v1/health
curl -f -X POST https://your-domain.com/api/v1/analyze -H 'Content-Type: application/json' -d '{"text":"قفا نبك من ذكرى"}'
```
إذا نجحا مع استجابة JSON صحيحة، اعتبر النشر الأول ناجح.

---

## 📌 ما هو مؤجل (Deferred Items)
- Kubernetes
- Autoscaling
- Message Queue (للتحليلات الكبيرة)
- ML Model Serving (Phase 2+)

---

## 📝 ملخص سريع
النشر في MVP بسيط ومتحكم به: حاويات + قاعدة بيانات مُدارة + مراقبة خفيفة. حافظ على خطوات قليلة وراجع قائمة التحقق في كل مرة. أي توسع لاحق سيُبنى على هذه القاعدة.

**آخر تحديث:** November 8, 2025
