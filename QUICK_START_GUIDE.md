# BAHR Platform - Quick Start Guide
## Get Your Development Environment Running in 30 Minutes

---

## Prerequisites

Before starting, ensure you have:
- **Git** installed
- **Docker** and **Docker Compose** installed
- **Node.js** 18+ and **npm** installed
- **Python** 3.11+ installed
- **Code editor** (VS Code recommended)
- **Terminal** access

**System Requirements:**
- macOS, Linux, or Windows with WSL2
- 8GB+ RAM
- 10GB+ free disk space

---

## Step 1: Create Project Structure (5 minutes)

### 1.1 Create Project Directory

```bash
# Create main project directory
mkdir BAHR
cd BAHR

# Create backend and frontend directories
mkdir backend frontend

# Verify structure
ls -la
# Should show: backend/ frontend/
```

### 1.2 Initialize Git Repository

```bash
# Initialize Git
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
.pytest_cache/

# Node
node_modules/
.next/
out/
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env

# Database
*.db
*.sqlite

# OS
.DS_Store
Thumbs.db

# Docker
*.log
EOF

# Create README
cat > README.md << 'EOF'
# بَحْر - Arabic Poetry Analysis Platform

AI-powered platform for Arabic poetry analysis, generation, and competition.

## Quick Start

See [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) for setup instructions.

## Documentation

- [Implementation Plan](IMPLEMENTATION_PLAN_FOR_CODEX.md)
- [Phase 1 Specification](PHASE_1_WEEK_1-2_SPEC.md)
- [Starter Templates](PROJECT_STARTER_TEMPLATE.md)
- [Project Tracker](PROJECT_TRACKER.md)

## Tech Stack

**Backend:** FastAPI, Python 3.11+, PostgreSQL, Redis
**Frontend:** Next.js 14, React, TypeScript, Tailwind CSS
**AI/ML:** PyTorch, Hugging Face Transformers

## License

[Your License Here]
EOF

# Initial commit
git add .
git commit -m "Initial commit: Project structure"
```

---

## Step 2: Setup Backend (10 minutes)

### 2.1 Create Backend Project Structure

```bash
cd backend

# Create directory structure
mkdir -p app/{core,api/v1/endpoints,models,schemas,db,services,utils}
mkdir -p tests/{core,api/v1,fixtures}
mkdir -p migrations/versions
mkdir scripts

# Create __init__.py files
touch app/__init__.py
touch app/core/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/api/v1/endpoints/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/db/__init__.py
touch app/services/__init__.py
touch app/utils/__init__.py
touch tests/__init__.py
touch tests/core/__init__.py
touch tests/api/__init__.py

# Verify structure
tree -L 3 app/
```

### 2.2 Create Requirements File

```bash
cat > requirements.txt << 'EOF'
# FastAPI
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9

# Redis
redis==5.0.1

# Pydantic
pydantic==2.5.0
pydantic-settings==2.1.0

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Development
black==23.11.0
flake8==6.1.0
mypy==1.7.1
EOF
```

### 2.3 Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi; print(f'FastAPI {fastapi.__version__} installed')"
```

### 2.4 Create Basic FastAPI App

```bash
# Create main.py (use template from PROJECT_STARTER_TEMPLATE.md Section 1)
cat > app/main.py << 'EOF'
"""BAHR Platform - FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BAHR - Arabic Poetry Platform",
    description="Arabic Poetry Analysis and Generation API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "مرحباً بك في منصة بَحْر", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
EOF

# Test server
uvicorn app.main:app --reload &
sleep 3
curl http://localhost:8000/
# Should return JSON with "مرحباً بك في منصة بَحْر"
pkill -f uvicorn
```

### 2.5 Create Environment File

```bash
cat > .env.example << 'EOF'
# Environment
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=postgresql://bahr_user:bahr_password@localhost:5432/bahr_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
JWT_SECRET_KEY=CHANGE_THIS_TO_RANDOM_SECRET_KEY_IN_PRODUCTION
BCRYPT_ROUNDS=12

# Feature Flags
ENABLE_AI_GENERATION=false
ENABLE_COMPETITIONS=false
EOF

# Copy to .env
cp .env.example .env

# Generate random secret key
python3 -c "import secrets; print(f'JWT_SECRET_KEY={secrets.token_urlsafe(32)}')" >> .env
```

---

## Step 3: Setup Frontend (10 minutes)

### 3.1 Create Next.js Project

```bash
cd ../frontend

# Create Next.js app
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir --import-alias "@/*"

# Answer prompts:
# ✔ Would you like to use TypeScript? Yes
# ✔ Would you like to use ESLint? Yes
# ✔ Would you like to use Tailwind CSS? Yes
# ✔ Would you like to use `src/` directory? No
# ✔ Would you like to use App Router? Yes
# ✔ Would you like to customize the default import alias? Yes (@/*)
```

### 3.2 Install Additional Dependencies

```bash
npm install @tanstack/react-query axios zustand react-hook-form zod @hookform/resolvers
npm install framer-motion recharts clsx tailwind-merge
npm install -D @types/node
```

### 3.3 Configure Tailwind for RTL and Arabic Fonts

```bash
# Update tailwind.config.ts
cat > tailwind.config.ts << 'EOF'
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        arabic: ['Cairo', 'sans-serif'],
        poetry: ['Amiri', 'serif'],
      },
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
      },
    },
  },
  plugins: [],
}
export default config
EOF
```

### 3.4 Setup Root Layout with RTL

```bash
# Create app/layout.tsx
cat > app/layout.tsx << 'EOF'
import type { Metadata } from 'next'
import { Cairo, Amiri } from 'next/font/google'
import './globals.css'

const cairo = Cairo({
  subsets: ['arabic'],
  variable: '--font-cairo',
})

const amiri = Amiri({
  weight: ['400', '700'],
  subsets: ['arabic'],
  variable: '--font-amiri',
})

export const metadata: Metadata = {
  title: 'بَحْر - منصة الشعر العربي',
  description: 'محلل ومولد الشعر العربي بالذكاء الاصطناعي',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ar" dir="rtl">
      <body className={`${cairo.variable} ${amiri.variable} font-arabic antialiased`}>
        {children}
      </body>
    </html>
  )
}
EOF
```

### 3.5 Create Simple Home Page

```bash
cat > app/page.tsx << 'EOF'
import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center">
      <div className="text-center px-4">
        <h1 className="text-7xl font-bold mb-4 text-blue-600 font-arabic">
          بَحْر
        </h1>
        <p className="text-2xl text-gray-700 mb-8 font-arabic">
          محلل الشعر العربي بالذكاء الاصطناعي
        </p>
        <p className="text-lg text-gray-600 mb-12 max-w-2xl mx-auto">
          اكتشف البحور الشعرية، حلل الأبيات، ولّد شعراً جديداً بقوة الذكاء الاصطناعي
        </p>
        <div className="flex gap-4 justify-center">
          <Link href="/analyze">
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-xl font-arabic transition-colors">
              ابدأ التحليل الآن
            </button>
          </Link>
        </div>
      </div>
    </main>
  )
}
EOF
```

### 3.6 Create Environment File

```bash
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
EOF

cat > .env.example << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
EOF
```

### 3.7 Test Frontend

```bash
npm run dev
# Opens on http://localhost:3000
# You should see the home page with Arabic text
```

---

## Step 4: Setup Docker (5 minutes)

### 4.1 Create Docker Compose File

```bash
cd ..  # Back to project root

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: bahr_postgres
    environment:
      POSTGRES_USER: bahr_user
      POSTGRES_PASSWORD: bahr_password
      POSTGRES_DB: bahr_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U bahr_user"]
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
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
EOF
```

### 4.2 Start Docker Services

```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Verify services are running
docker-compose ps

# Expected output:
# NAME              STATUS    PORTS
# bahr_postgres     Up        0.0.0.0:5432->5432/tcp
# bahr_redis        Up        0.0.0.0:6379->6379/tcp

# Test PostgreSQL connection
docker exec bahr_postgres psql -U bahr_user -d bahr_db -c "SELECT version();"

# Test Redis connection
docker exec bahr_redis redis-cli ping
# Should return: PONG
```

---

## Step 5: Verify Everything Works (5 minutes)

### 5.1 Test Backend

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# .\venv\Scripts\activate  # Windows

# Start FastAPI server
uvicorn app.main:app --reload

# In another terminal, test endpoints:
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Open in browser for Swagger UI

# Stop server (Ctrl+C)
```

### 5.2 Test Frontend

```bash
cd ../frontend

# Start Next.js dev server
npm run dev

# Open browser: http://localhost:3000
# You should see Arabic text with RTL layout
```

### 5.3 Test Full Stack Integration

```bash
# Start both servers (use 2 terminals or tmux)

# Terminal 1 - Backend:
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend:
cd frontend
npm run dev

# Browser Test:
# 1. Open http://localhost:3000
# 2. Click "ابدأ التحليل الآن"
# 3. Should navigate to /analyze (even if page doesn't exist yet)
```

---

## Step 6: Setup Development Tools (Optional)

### 6.1 VS Code Extensions

Install these recommended extensions:
- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)
- **ES7+ React/Redux/React-Native snippets**
- **Tailwind CSS IntelliSense**
- **GitLens**
- **Docker**
- **Arabic Support** (for RTL preview)

### 6.2 Configure VS Code Settings

```bash
# Create .vscode/settings.json
mkdir -p .vscode
cat > .vscode/settings.json << 'EOF'
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
EOF
```

### 6.3 Setup Git Hooks (Pre-commit)

```bash
# Install pre-commit (Python tool)
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.55.0
    hooks:
      - id: eslint
        files: \.[jt]sx?$
        types: [file]
EOF

# Install hooks
pre-commit install
```

---

## Step 7: Create Helper Scripts

### 7.1 Backend Development Script

```bash
# Create backend/dev.sh
cat > backend/dev.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
export $(cat .env | xargs)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF

chmod +x backend/dev.sh
```

### 7.2 Frontend Development Script

```bash
# Create frontend/dev.sh
cat > frontend/dev.sh << 'EOF'
#!/bin/bash
npm run dev
EOF

chmod +x frontend/dev.sh
```

### 7.3 Full Stack Start Script

```bash
# Create start.sh in project root
cat > start.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting BAHR Development Environment..."

# Start Docker services
echo "📦 Starting PostgreSQL and Redis..."
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to be healthy..."
sleep 5

# Start backend in background
echo "🐍 Starting FastAPI backend..."
cd backend
source venv/bin/activate
export $(cat .env | xargs)
uvicorn app.main:app --reload &
BACKEND_PID=$!
cd ..

# Start frontend
echo "⚛️  Starting Next.js frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Development environment ready!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Trap Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; docker-compose down; exit" INT

# Wait
wait
EOF

chmod +x start.sh
```

---

## Step 8: Verify Complete Setup

### 8.1 Checklist

Run through this checklist:

```bash
# 1. Docker services running
docker-compose ps | grep "Up"

# 2. PostgreSQL accessible
docker exec bahr_postgres psql -U bahr_user -d bahr_db -c "SELECT 1;"

# 3. Redis accessible
docker exec bahr_redis redis-cli ping

# 4. Backend can connect to database
cd backend
python3 << 'EOF'
from sqlalchemy import create_engine
engine = create_engine("postgresql://bahr_user:bahr_password@localhost:5432/bahr_db")
with engine.connect() as conn:
    result = conn.execute("SELECT 1")
    print("✅ Database connection successful")
EOF

# 5. Backend can connect to Redis
python3 << 'EOF'
import redis
r = redis.from_url("redis://localhost:6379/0")
r.ping()
print("✅ Redis connection successful")
EOF

# 6. Backend server starts
uvicorn app.main:app --reload &
sleep 3
curl -s http://localhost:8000/health | grep "healthy"
pkill -f uvicorn

# 7. Frontend builds successfully
cd ../frontend
npm run build

echo ""
echo "✅ All checks passed! You're ready to start development."
```

---

## Quick Reference Commands

### Daily Development

```bash
# Start everything (from project root)
./start.sh

# Or manually:
# Terminal 1: Start Docker services
docker-compose up -d

# Terminal 2: Start backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Terminal 3: Start frontend
cd frontend && npm run dev
```

### Testing

```bash
# Backend tests
cd backend
source venv/bin/activate
pytest tests/ -v

# Frontend tests (when added)
cd frontend
npm test
```

### Database Management

```bash
# Access PostgreSQL
docker exec -it bahr_postgres psql -U bahr_user -d bahr_db

# Reset database (⚠️ destroys all data)
docker-compose down -v
docker-compose up -d

# Run migrations (after Alembic setup)
cd backend
alembic upgrade head
```

### Stopping Services

```bash
# Stop all
docker-compose down

# Stop and remove volumes (⚠️ destroys data)
docker-compose down -v
```

---

## Troubleshooting

### Problem: Port Already in Use

```bash
# Find process using port
lsof -ti:8000  # Backend port
lsof -ti:3000  # Frontend port
lsof -ti:5432  # PostgreSQL port

# Kill process
kill -9 <PID>
```

### Problem: Docker Services Won't Start

```bash
# View logs
docker-compose logs postgres
docker-compose logs redis

# Restart services
docker-compose restart

# Full reset
docker-compose down -v
docker-compose up -d
```

### Problem: Python Dependencies Won't Install

```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Try installing one by one
pip install fastapi
pip install uvicorn[standard]
# etc.

# Check Python version
python --version  # Should be 3.11+
```

### Problem: npm Install Fails

```bash
# Clear cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Problem: Arabic Fonts Not Loading

```bash
# Verify fonts in browser DevTools
# Network tab -> Filter: font
# Should see Cairo and Amiri loading from Google Fonts

# If blocked, download fonts locally:
# 1. Download from Google Fonts
# 2. Place in frontend/public/fonts/
# 3. Update font imports in layout.tsx
```

---

## Next Steps

Now that your environment is set up:

1. **Start Phase 1, Week 1-2**: Implement the Prosody Engine
   - Reference: `PHASE_1_WEEK_1-2_SPEC.md`
   - Start with Issue #7: Text Normalization

2. **Create GitHub Repository**:
   ```bash
   git remote add origin https://github.com/yourusername/bahr.git
   git branch -M main
   git push -u origin main
   ```

3. **Create GitHub Issues**:
   - Use templates from `PROJECT_TRACKER.md`
   - Create Milestone for Phase 1

4. **Begin Development**:
   - Follow sprint plan (4 two-week sprints)
   - Update issues as you complete tasks
   - Run tests frequently

---

## Success! 🎉

Your BAHR development environment is fully set up. You should have:

✅ Backend FastAPI server running on http://localhost:8000
✅ Frontend Next.js app running on http://localhost:3000
✅ PostgreSQL database running on localhost:5432
✅ Redis cache running on localhost:6379
✅ RTL layout working with Arabic fonts
✅ API documentation at http://localhost:8000/docs

**Total setup time: ~30 minutes**

Ready to build the future of Arabic poetry analysis! 🎭🚀
