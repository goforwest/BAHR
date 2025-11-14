#!/bin/zsh
# BAHR Project Shell Aliases
# Add this to your ~/.zshrc file
# After adding, run: source ~/.zshrc

# ================================
# BAHR Project Configuration
# ================================

export BAHR_ROOT="$HOME/Desktop/Personal/BAHR"

# ================================
# Docker Compose Shortcuts
# ================================

alias bahr-dc='docker-compose -f $BAHR_ROOT/infrastructure/docker/docker-compose.yml'

bahr-start() {
    echo "🚀 Starting BAHR services..."
    bahr-dc up -d
    sleep 2
    bahr-dc ps
    echo "✅ BAHR databases ready"
}

bahr-stop() {
    echo "🛑 Stopping BAHR services..."
    bahr-dc down
    echo "✅ Services stopped"
}

bahr-restart() {
    echo "🔄 Restarting BAHR services..."
    bahr-dc restart
    echo "✅ Services restarted"
}

bahr-logs() {
    bahr-dc logs -f "$@"
}

# ================================
# Alembic Database Migrations
# ================================

bahr-alembic() {
    (cd "$BAHR_ROOT/src/backend" && alembic -c database/migrations/alembic.ini "$@")
}

bahr-migrate() {
    echo "📊 Running database migrations..."
    bahr-alembic upgrade head
    echo "✅ Migrations complete"
}

bahr-migrate-status() {
    bahr-alembic current
}

bahr-migrate-history() {
    bahr-alembic history
}

bahr-migrate-create() {
    if [ -z "$1" ]; then
        echo "Usage: bahr-migrate-create 'description'"
        return 1
    fi
    bahr-alembic revision --autogenerate -m "$1"
}

# ================================
# Database Management
# ================================

bahr-db-seed() {
    echo "🌱 Seeding database..."
    (cd "$BAHR_ROOT/src/backend" && python scripts/seed_database.py)
}

bahr-db-shell() {
    docker exec -it bahr_postgres psql -U bahr -d bahr_dev
}

bahr-db-reset() {
    echo "⚠️  WARNING: This will delete all data!"
    read "response?Are you sure? (y/N): "
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "🗑️  Resetting database..."
        bahr-dc down -v
        bahr-dc up -d
        sleep 3
        bahr-migrate
        bahr-db-seed
        echo "✅ Database reset complete"
    else
        echo "❌ Cancelled"
    fi
}

# ================================
# Testing Shortcuts
# ================================

bahr-test() {
    echo "🧪 Running backend tests..."
    (cd "$BAHR_ROOT/src/backend" && pytest tests/ -v "$@")
}

bahr-test-coverage() {
    echo "📊 Running tests with coverage..."
    (cd "$BAHR_ROOT/src/backend" && pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html)
    echo "📄 Coverage report: backend/htmlcov/index.html"
}

bahr-test-watch() {
    echo "👀 Running tests in watch mode..."
    (cd "$BAHR_ROOT/src/backend" && pytest-watch tests/ -- -v)
}

bahr-test-golden() {
    echo "🏆 Running golden set tests..."
    (cd "$BAHR_ROOT/dataset" && pytest tests/ -v)
}

# ================================
# Development Servers
# ================================

bahr-backend() {
    echo "🖥️  Starting backend server..."
    cd "$BAHR_ROOT/src/backend"
    source venv/bin/activate 2>/dev/null || echo "⚠️  Virtual env not found, using global Python"
    uvicorn app.main:app --reload --port 8000
}

bahr-frontend() {
    echo "🎨 Starting frontend server..."
    cd "$BAHR_ROOT/frontend"
    npm run dev
}

# ================================
# Quick Navigation
# ================================

alias bahr='cd $BAHR_ROOT'
alias bahr-b='cd $BAHR_ROOT/backend'
alias bahr-f='cd $BAHR_ROOT/frontend'
alias bahr-d='cd $BAHR_ROOT/docs'
alias bahr-ds='cd $BAHR_ROOT/dataset'
alias bahr-infra='cd $BAHR_ROOT/infrastructure'

# ================================
# Git Shortcuts
# ================================

bahr-status() {
    echo "📊 BAHR Repository Status"
    echo "========================"
    (cd "$BAHR_ROOT" && git status -sb)
}

bahr-pull() {
    echo "⬇️  Pulling latest changes..."
    (cd "$BAHR_ROOT" && git pull --rebase)
}

bahr-branches() {
    (cd "$BAHR_ROOT" && git branch -a)
}

# ================================
# Health Checks
# ================================

bahr-health() {
    echo "🏥 BAHR System Health Check"
    echo "==========================="
    
    echo "\n📦 Docker Services:"
    docker ps | grep bahr || echo "  ⚠️  No BAHR services running"
    
    echo "\n🗄️  Database:"
    docker exec bahr_postgres psql -U bahr -d bahr_dev -c "SELECT 1;" 2>/dev/null && echo "  ✅ PostgreSQL OK" || echo "  ❌ PostgreSQL not accessible"
    
    echo "\n🔴 Redis:"
    docker exec bahr_redis redis-cli PING 2>/dev/null && echo "  ✅ Redis OK" || echo "  ❌ Redis not accessible"
    
    echo "\n🐍 Backend:"
    (cd "$BAHR_ROOT/src/backend" && python -c "from app.main import app; print('  ✅ Backend imports OK')" 2>/dev/null || echo "  ❌ Backend imports failed")
    
    echo "\n🧪 Tests:"
    (cd "$BAHR_ROOT/src/backend" && pytest tests/ --collect-only -q 2>/dev/null | tail -1)
}

# ================================
# Complete Environment Setup
# ================================

bahr-setup() {
    echo "🔧 Setting up BAHR development environment..."
    echo "============================================="
    
    echo "\n1️⃣  Starting services..."
    bahr-start
    
    echo "\n2️⃣  Running migrations..."
    bahr-migrate
    
    echo "\n3️⃣  Seeding database..."
    bahr-db-seed
    
    echo "\n4️⃣  Health check..."
    bahr-health
    
    echo "\n✅ BAHR setup complete!"
    echo "💡 Use 'bahr-backend' and 'bahr-frontend' to start servers"
}

# ================================
# Help Function
# ================================

bahr-help() {
    cat << 'EOF'
🚀 BAHR Project Commands
========================

📁 Navigation:
  bahr              - Go to project root
  bahr-b            - Go to backend/
  bahr-f            - Go to frontend/
  bahr-d            - Go to docs/
  bahr-ds           - Go to dataset/
  bahr-infra        - Go to infrastructure/

🐳 Docker Services:
  bahr-start        - Start all services
  bahr-stop         - Stop all services
  bahr-restart      - Restart all services
  bahr-logs [svc]   - View service logs
  bahr-dc [cmd]     - Run docker-compose command

📊 Database:
  bahr-migrate              - Run migrations
  bahr-migrate-status       - Check migration status
  bahr-migrate-history      - View migration history
  bahr-migrate-create "msg" - Create new migration
  bahr-db-seed             - Seed database
  bahr-db-shell            - Open PostgreSQL shell
  bahr-db-reset            - Reset database (⚠️ deletes data)

🧪 Testing:
  bahr-test                - Run backend tests
  bahr-test-coverage       - Run tests with coverage
  bahr-test-golden         - Run golden set tests
  bahr-test-watch          - Run tests in watch mode

🖥️  Servers:
  bahr-backend      - Start backend server
  bahr-frontend     - Start frontend server

📊 Git:
  bahr-status       - Git status
  bahr-pull         - Pull latest changes
  bahr-branches     - List branches

🔧 Utilities:
  bahr-health       - System health check
  bahr-setup        - Complete environment setup
  bahr-help         - Show this help

📚 Documentation:
  Quick Start:    $BAHR_ROOT/QUICKSTART_NEW_PATHS.md
  Getting Started: $BAHR_ROOT/docs/onboarding/GETTING_STARTED.md
  Features:       $BAHR_ROOT/docs/features/
EOF
}

# ================================
# Initialization Message
# ================================

echo "✅ BAHR aliases loaded. Type 'bahr-help' for available commands."
