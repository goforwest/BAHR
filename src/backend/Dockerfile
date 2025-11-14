# =============================================================================
# BAHR - Railway Optimized Production Dockerfile
# Target: < 3.5 GB final image (Railway limit: 4 GB)
# Optimizations: CPU-only PyTorch, aggressive cleanup, multi-stage build
# =============================================================================

# =============================================================================
# Stage 1: Builder - Install dependencies only
# =============================================================================
FROM python:3.11-slim-bookworm AS builder

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install ONLY build dependencies needed for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy ONLY requirements files (not entire project)
COPY requirements/base.txt requirements/production.txt ./requirements/
COPY requirements.txt ./

# Install Python dependencies - PyTorch CPU-only first, then everything else
RUN set -ex && \
    pip install --upgrade pip setuptools wheel && \
    # CRITICAL FIX: Install PyTorch CPU-only version using correct syntax
    # The key is using --index-url to point to CPU wheels, not --extra-index-url
    # Without this, pip will download the 2.6GB CUDA version instead of 600MB CPU version
    pip install --index-url https://download.pytorch.org/whl/cpu torch==2.5.1 && \
    python -c "import torch; print(f'✓ PyTorch CPU installed: {torch.__version__}')" && \
    # Install all other requirements (they'll use already-installed PyTorch)
    pip install -r requirements/production.txt && \
    python -c "import uvicorn, fastapi; print('✓ All base packages installed')" && \
    # Verify all packages work BEFORE cleanup
    python -c "import uvicorn, fastapi, torch, camel_tools, psycopg2; print('✓ All critical packages verified')" && \
    # Remove pip cache to save space
    rm -rf /root/.cache/pip && \
    # Remove test and doc directories (use -path to avoid -delete issues)
    find /usr/local/lib/python3.11/site-packages -type d -name "tests" -print0 | xargs -0 rm -rf 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -type d -name "test" -print0 | xargs -0 rm -rf 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -type d -name "docs" -print0 | xargs -0 rm -rf 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -type d -name "__pycache__" -print0 | xargs -0 rm -rf 2>/dev/null || true && \
    # Remove .pyc/.pyo files (safe with -delete on files only)
    find /usr/local/lib/python3.11/site-packages -type f -name "*.pyc" -delete 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -type f -name "*.pyo" -delete 2>/dev/null || true && \
    # Remove torch-specific test/include dirs (these are safe to delete)
    find /usr/local/lib/python3.11/site-packages/torch -type d -name "test" -print0 2>/dev/null | xargs -0 rm -rf 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages/torch -type d -name "include" -print0 2>/dev/null | xargs -0 rm -rf 2>/dev/null || true && \
    echo "=== Final package directory ===" && \
    du -sh /usr/local/lib/python3.11/site-packages && \
    # Final verification that packages are still importable after cleanup
    python -c "import uvicorn, fastapi, torch; print('✓ Packages still work after cleanup')"

# =============================================================================
# Stage 2: Runtime - Minimal production image
# =============================================================================
FROM python:3.11-slim-bookworm AS production

LABEL maintainer="BAHR Production Team"
LABEL description="BAHR Backend API - Railway Optimized"
LABEL version="2.0.0"

# Production environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENVIRONMENT=production \
    PATH=/usr/local/bin:$PATH

# Install ONLY runtime dependencies (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get autoclean

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# Copy binaries (for uvicorn executable, etc.)
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy ONLY application code (no tests, docs, scripts, etc.)
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./

# Create non-root user and verify installation
RUN useradd -m -u 1000 -s /bin/sh appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    # Clean up any cache
    find /app -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true && \
    # Verify uvicorn is installed and importable (fail build if not)
    python -c "import uvicorn, fastapi, torch; print('✓ All critical packages available in production image')"

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:${PORT:-8080}/health || exit 1

# Production startup - Railway will override CMD with .railway.json startCommand
# This CMD is for local Docker testing only (use port 8000 locally)
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 4 --log-level info"]

# =============================================================================
# BUILD INSTRUCTIONS FOR RAILWAY
# =============================================================================
# 1. Ensure .dockerignore excludes .venv/, node_modules/, frontend/
# 2. Build: docker build -t bahr-backend:railway .
# 3. Test: docker run -p 8000:8000 bahr-backend:railway
# 4. Expected size: 1.0-1.5 GB (well under 4 GB Railway limit)
# =============================================================================
# trigger rebuild
