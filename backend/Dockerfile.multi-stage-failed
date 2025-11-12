# =============================================================================
# BAHR - Arabic Poetry Analysis Platform
# Ultra-Optimized Dockerfile for Railway - Cache-Busted
# Target: <1.5GB final image (down from 15GB!)
# =============================================================================

# Cache buster - change this to force fresh build
ARG CACHE_BUST=v3

# =============================================================================
# Stage 1: Builder - Compile dependencies in isolated environment
# =============================================================================
FROM python:3.11.10-slim-bookworm AS builder

ARG CACHE_BUST
RUN echo "Cache bust: ${CACHE_BUST}"

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install ONLY build-time dependencies (minimal set)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment in a known location
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only requirements files (leverage Docker layer caching)
WORKDIR /build
COPY requirements/base.txt ./requirements/base.txt
COPY requirements/production.txt ./requirements/production.txt

# Install production dependencies with aggressive optimization flags
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --no-warn-script-location \
    -r requirements/production.txt

# CRITICAL: Strip unnecessary bloat from venv before copying to final image
RUN find /opt/venv -type d \( -name "tests" -o -name "test" -o -name "testing" \) -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -type f \( -name "*.pyc" -o -name "*.pyo" -o -name "*.pyd" \) -delete && \
    find /opt/venv -type f \( -name "*.c" -o -name "*.h" -o -name "*.cpp" \) -delete && \
    find /opt/venv -name "*.so" -exec strip --strip-unneeded {} + 2>/dev/null || true && \
    rm -rf /opt/venv/lib/python*/site-packages/pip* \
           /opt/venv/lib/python*/site-packages/setuptools* \
           /opt/venv/lib/python*/site-packages/wheel* \
           /opt/venv/lib/python*/site-packages/*/tests \
           /opt/venv/lib/python*/site-packages/*/*/tests \
           /opt/venv/share \
           /opt/venv/include \
           /root/.cache \
           /tmp/*

# =============================================================================
# Stage 2: Production - Minimal runtime-only image
# =============================================================================
FROM python:3.11.10-slim-bookworm AS production

LABEL maintainer="BAHR Production Team" \
      description="BAHR Backend API - Production Environment" \
      version="1.0.0"

# Runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production \
    DEBUG=false \
    PATH="/opt/venv/bin:$PATH"

# Install ONLY runtime dependencies (no build tools!)
# psycopg2-binary needs libpq5 at runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && rm -rf /tmp/* /var/tmp/*

WORKDIR /app

# Copy pre-built venv from builder (single layer, already cleaned)
COPY --from=builder /opt/venv /opt/venv

# Copy ONLY application code (no tests, no scripts, no docs)
COPY app/ ./app/
COPY database/ ./database/
COPY alembic.ini ./
COPY alembic/ ./alembic/

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/sh appuser && \
    chown -R appuser:appuser /app /opt/venv && \
    chmod -R 755 /app

USER appuser

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

EXPOSE 8000

# Production startup (use uvicorn directly from venv)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--log-level", "info"]

# =============================================================================
# Build Instructions:
#   docker build -f Dockerfile.optimized -t bahr-backend:optimized .
#   docker images bahr-backend:optimized  # Check size
# =============================================================================
