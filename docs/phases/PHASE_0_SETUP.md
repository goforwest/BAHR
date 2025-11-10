# 🛠️ Phase 0: إعداد البيئة التطويرية
## دليل شامل للبدء من الصفر

---

## 🎯 الهدف من هذه المرحلة

إعداد بيئة تطويرية كاملة ومتكاملة تمكنك من:
- تطوير Backend (FastAPI + Python)
- تطوير Frontend (Next.js + React)  
- إدارة قواعد البيانات (PostgreSQL + Redis)
- نشر التطبيق (Docker + Cloud)

---

## ⏰ المدة المتوقعة: 3-5 أيام

---

## 📋 قائمة المتطلبات الأساسية

### 💻 النظام:
- **macOS** (محدّث)
- **RAM:** 8GB+ (مفضل 16GB)
- **Storage:** 20GB+ فراغ
- **Internet:** اتصال مستقر

### 🔧 الأدوات المطلوبة:

#### ✅ المطلوب تثبيته:
```bash
# Package Manager
- Homebrew

# Development Tools  
- Git
- Node.js (v18+)
- Python (v3.11+)
- Docker Desktop

# Code Editor
- VS Code + Extensions

# Databases
- PostgreSQL
- Redis

# Optional but Recommended
- Figma (للتصميم)
- Postman (لاختبار APIs)
```

---

## 🚀 خطوات التثبيت المفصلة

### 1️⃣ تثبيت Homebrew

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Verify installation
brew --version
```

### 2️⃣ تثبيت Git والإعداد

```bash
# Install Git
brew install git

# Configure Git (replace with your info)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify
git --version
git config --list
```

### 3️⃣ تثبيت Node.js و npm

```bash
# Install Node.js
brew install node

# Verify installation
node --version  # Should be v18+
npm --version
```

### 4️⃣ تثبيت Python والأدوات المرتبطة

```bash
# Install Python
brew install python@3.11

# Create symbolic link (if needed)
ln -sf /opt/homebrew/bin/python3.11 /opt/homebrew/bin/python

# Install pip packages
pip install --upgrade pip
pip install pipenv  # For virtual environments

# Verify
python --version  # Should be 3.11+
pip --version
```

### ⚠️ 4.5️⃣ اختبار توافق M1/M2 Mac (CRITICAL - يوم 1!)

```bash
# 🔴 IMPORTANT: Test CAMeL Tools compatibility IMMEDIATELY
# This is a known issue that can block Week 2-3 development!

# Check your architecture
uname -m  # Should show "arm64" for M1/M2

# Create test virtual environment
python -m venv test_env
source test_env/bin/activate

# Attempt 1: Install with ARM64 native
arch -arm64 pip install camel-tools==1.5.2

# Test import
python -c "from camel_tools.utils.normalize import normalize_unicode; print('✅ CAMeL Tools working!')"

# If the above FAILS, try Attempt 2: Rosetta 2
# Install Rosetta 2 if not already installed
softwareupdate --install-rosetta --agree-to-license

# Reinstall with x86_64 emulation
arch -x86_64 pip install camel-tools==1.5.2

# Test again
python -c "from camel_tools.utils.normalize import normalize_unicode; print('✅ CAMeL Tools working (via Rosetta)!')"

# Clean up test environment
deactivate
rm -rf test_env

# 📝 Document which method worked in PROGRESS_LOG.md
```

**Fallback Plan (if both fail):**
```bash
# Use Docker with amd64 platform (guaranteed to work)
# All NLP processing will run in Docker container
# Add to docker-compose.yml:
# platform: linux/amd64

# OR use cloud-based solution (not recommended for MVP)
```

**Expected Results:**
- ✅ **Best case:** ARM64 native works (fastest performance)
- ⚠️ **Acceptable:** Rosetta works (slight performance penalty ~10-15%)
- 🔴 **Fallback:** Docker amd64 (noticeable overhead but stable)

**Time Budget:** 30-60 minutes for testing (DAY 1!)

**Why This Matters:**
- CAMeL Tools is core dependency for Arabic NLP
- Failure to test early = Week 2 blocker
- Docker fallback adds complexity but is reliable

### 5️⃣ تثبيت Docker Desktop

```bash
# Install Docker via Homebrew Cask
brew install --cask docker

# Alternative: Download from Docker website
# https://www.docker.com/products/docker-desktop
```

**بعد التثبيت:**
1. افتح Docker Desktop من Applications
2. أكمل الإعداد الأولي
3. تأكد أنه يعمل:

```bash
docker --version
docker-compose --version
```

### 6️⃣ تثبيت قواعد البيانات

```bash
# Install PostgreSQL
brew install postgresql@15
brew services start postgresql@15

# Install Redis
brew install redis
brew services start redis

# Verify they're running
brew services list | grep -E "(postgresql|redis)"
```

### 7️⃣ إعداد VS Code والإضافات

```bash
# Install VS Code
brew install --cask visual-studio-code

# Install essential extensions (run after opening VS Code)
code --install-extension ms-python.python
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension bradlc.vscode-tailwindcss
code --install-extension ms-vscode.vscode-json
code --install-extension redhat.vscode-yaml
code --install-extension ms-vscode-remote.remote-containers
```

**الإضافات المفيدة للمشروع:**
- Arabic Language Support
- REST Client (لاختبار APIs)
- GitLens (لإدارة Git)
- Prettier (تنسيق الكود)
- Error Lens (عرض الأخطاء)

---

## 📁 إنشاء هيكل المشروع

```bash
# Navigate to your workspace
cd ~/Desktop/Personal/BAHR

# Create project structure
mkdir -p {backend,frontend,database,docs,scripts,tests}

# Create essential files
touch README.md
touch .gitignore
touch docker-compose.yml
touch Makefile

# Initialize Git repository
git init
git add .
git commit -m "Initial project structure"
```

### هيكل المجلدات المقترح:

```
BAHR/
├── README.md
├── docker-compose.yml
├── Makefile
├── .gitignore
├── .env.example
│
├── backend/                 # FastAPI Application
│   ├── app/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│
├── frontend/               # Next.js Application  
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── Dockerfile
│   └── __tests__/
│
├── database/              # Database Scripts & Migrations
│   ├── migrations/
│   ├── seeds/
│   └── backup/
│
├── docs/                  # Documentation (already created)
│   ├── phases/
│   ├── technical/
│   └── research/
│
├── scripts/               # Automation Scripts
│   ├── setup.sh
│   ├── deploy.sh
│   └── backup.sh
│
└── tests/                 # Integration Tests
    ├── e2e/
    └── api/
```

### 📂 هيكل مجلد البيانات (Dataset) – جديد
يُستخدم لتخزين الأبيات المُعنونة يدويًا وتطوير مجموعة التقييم:
```
dataset/
  raw/                # مصادر أولية قبل التنظيف
  labeled/            # JSONL ملفات بعد التطبيع (text, meter, era, source, notes)
  evaluation/         # عينات ثابتة للاختبارات (freeze)
  scripts/            # أدوات تحويل/تطبيع
```
أضف إلى `.gitignore`: أي ملفات > 5MB أو مصادر حقوق محفوظة.

### ✅ التحقق من استهلاك الذاكرة قبل تثبيت مكتبات NLP
استخدم الأمر:
```bash
python - <<'PY'
import psutil
print('RAM Available MB:', psutil.virtual_memory().available/1024/1024)
PY
```
إذا كانت الذاكرة المتاحة < 3000MB أغلق تطبيقات ثقيلة قبل تثبيت CAMeL Tools.

### 🧪 اختبار سريع بعد تثبيت CAMeL Tools
```bash
python - <<'PY'
from camel_tools.utils.charmap import CharMapper
norm = CharMapper.builtin_mapper('arclean')
print(norm.map("أَلا في سبيلِ المجدِ ما أَنا فاعلُ"))
PY
```
يجب أن تظهر نسخة من النص بعد التطبيع الأساسي.

---

## 🐳 إعداد Docker Compose

إنشاء ملف `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: bahr_db
      POSTGRES_USER: bahr_user
      POSTGRES_PASSWORD: bahr_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  # Backend API (FastAPI)
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://bahr_user:bahr_password@postgres:5432/bahr_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Frontend (Next.js)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev

volumes:
  postgres_data:
  redis_data:
```

### 🧪 فحص صحة الحاويات بعد التشغيل
```bash
docker compose up -d
docker compose ps
curl -s localhost:8000/api/v1/health || echo "Health endpoint not ready yet"
```

---

## ⚙️ إنشاء ملف .gitignore

```bash
# Create comprehensive .gitignore
cat > .gitignore << 'EOF'
# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.pytest_cache/

# IDEs
.vscode/settings.json
.vscode/launch.json
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
dist/
build/
.next/
out/

# Database
*.sqlite
*.sqlite3
*.db

# Docker
.dockerignore

# Temporary files
*.tmp
*.temp
.cache/

# AI/ML
*.model
*.pkl
*.h5
*.onnx
wandb/
.wandb/

# Secrets & Keys
*.key
*.pem
*.cert
secrets/
EOF
```

---

## 🔧 إنشاء Makefile للأوامر السريعة

```makefile
# Makefile for BAHR project

.PHONY: help setup start stop clean test

help:
	@echo "Available commands:"
	@echo "  setup     - Setup development environment"
	@echo "  start     - Start all services"
	@echo "  stop      - Stop all services" 
	@echo "  clean     - Clean Docker containers and volumes"
	@echo "  test      - Run tests"
	@echo "  logs      - Show logs for all services"

setup:
	@echo "Setting up development environment..."
	cp .env.example .env
	docker-compose build
	docker-compose up -d postgres redis
	@echo "Environment setup complete!"

start:
	@echo "Starting all services..."
	docker-compose up -d
	@echo "Services started! Check http://localhost:3000"

stop:
	@echo "Stopping all services..."
	docker-compose down

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	docker system prune -f

test:
	@echo "Running tests..."
	docker-compose exec backend pytest
	docker-compose exec frontend npm test

logs:
	docker-compose logs -f

backend-shell:
	docker-compose exec backend /bin/bash

frontend-shell:
	docker-compose exec frontend /bin/sh

db-shell:
	docker-compose exec postgres psql -U bahr_user -d bahr_db

backend-run:
  docker-compose exec backend uvicorn app.main:app --host 0.0.0.0 --port 8000

frontend-run:
  docker-compose exec frontend npm run dev

bench-prosody:
  python scripts/quick_bench.py dataset/evaluation/sample_verses.jsonl || echo "Bench script not yet implemented"
```

---

## 🌍 إعداد متغيرات البيئة

إنشاء ملف `.env.example`:

```bash
# Database Configuration
DATABASE_URL=postgresql://bahr_user:bahr_password@localhost:5432/bahr_db
REDIS_URL=redis://localhost:6379

# API Configuration  
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# AI/ML Configuration
OPENAI_API_KEY=your-openai-api-key-here
HUGGINGFACE_TOKEN=your-huggingface-token-here

# Email Configuration (for later)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Cloud Storage (for later)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET=bahr-storage

# Analytics (for later)  
MIXPANEL_PROJECT_TOKEN=your-mixpanel-token
GOOGLE_ANALYTICS_ID=your-ga-tracking-id

# Development
DEBUG=true
LOG_LEVEL=DEBUG
```

---

## ✅ اختبار الإعداد

### 1️⃣ اختبار قواعد البيانات:

```bash
# Test PostgreSQL
psql -h localhost -U postgres -c "SELECT version();"

# Test Redis
redis-cli ping
# Should return: PONG
```

### 2️⃣ اختبار Docker:

```bash
# Test Docker setup
make setup
make start

# Check running containers
docker ps

# Check logs
make logs
```

### 3️⃣ اختبار الاتصال:

```bash
# Test if services are accessible
curl http://localhost:8000/health  # Backend health check (will be created later)
curl http://localhost:3000         # Frontend (will show Next.js default page)
```

---

## 🎯 نقاط التحقق (Checkpoints)

### ✅ قائمة التحقق النهائية:

- [ ] Homebrew مثبت ويعمل
- [ ] Git مثبت ومضبوط
- [ ] Node.js v18+ مثبت
- [ ] Python 3.11+ مثبت  
- [ ] Docker Desktop مثبت ويعمل
- [ ] PostgreSQL يعمل على port 5432
- [ ] Redis يعمل على port 6379
- [ ] VS Code مثبت مع الإضافات
- [ ] هيكل المشروع منشأ
- [ ] Docker Compose يعمل
- [ ] ملفات الإعداد منشأة (.gitignore, Makefile, etc.)

---

## 🚨 حلول المشاكل الشائعة

### مشكلة: Port already in use

```bash
# Find process using port
lsof -ti:5432  # For PostgreSQL
lsof -ti:6379  # For Redis

# Kill process
kill -9 <PID>

# Or use different ports in docker-compose.yml
```

### مشكلة: Permission denied

```bash
# Fix Docker permissions
sudo chmod 666 /var/run/docker.sock

# Fix Python permissions
sudo chown -R $(whoami) /usr/local/lib/python3.11
```

### مشكلة: Docker build fails

```bash
# Clean Docker cache
docker system prune -af

# Rebuild from scratch
docker-compose build --no-cache
```

---

## 📖 الموارد المرجعية

### 📚 دوكيومنتيشن:
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

### 🎥 فيديوهات مفيدة:
- Docker for Developers (YouTube)
- PostgreSQL Crash Course
- Redis in 100 Seconds

---

## ➡️ الخطوة التالية

بعد إكمال هذه المرحلة بنجاح، انتقل إلى:
**[Phase 1: MVP Development](PHASE_1_MVP.md)**

---

## 📝 نصائح مهمة

1. **اسأل لو واجهت مشكلة** - لا تضيع وقت كثير في debugging لوحدك
2. **وثّق أي تغييرات** تعملها على الإعداد
3. **اعمل backup** للإعدادات المهمة
4. **اختبر كل شيء** قبل الانتقال للمرحلة التالية

---

**🎉 إذا وصلت هنا، تهانينا! البيئة التطويرية جاهزة للانطلاق!**