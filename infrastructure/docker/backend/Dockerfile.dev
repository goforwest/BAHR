# =============================================================================
# BAHR - Arabic Poetry Analysis Platform
# Multi-stage Dockerfile for Backend API
# =============================================================================

# =============================================================================
# Stage 1: Base Image
# =============================================================================
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.7.0

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Build tools
    gcc \
    g++ \
    make \
    # PostgreSQL client
    libpq-dev \
    # Common utilities
    curl \
    wget \
    git \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# Stage 2: Development Image
# =============================================================================
FROM base as development

LABEL maintainer="BAHR Development Team"
LABEL description="BAHR Backend API - Development Environment"
LABEL version="1.0.0"

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Debugging tools
    vim \
    nano \
    htop \
    # Network tools
    net-tools \
    iputils-ping \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files (including modular requirements directory)
COPY requirements.txt ./
COPY requirements/ ./requirements/

# Install Python dependencies (development)
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt && \
    pip install pytest httpx prometheus-client

# Copy application code
COPY . .

# Create non-root user for development
RUN useradd -m -u 1000 -s /bin/bash devuser && \
    chown -R devuser:devuser /app

# Switch to non-root user
USER devuser

# Expose ports
EXPOSE 8000 9090

# Development startup command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug"]

# =============================================================================
# Stage 3: Builder (for production)
# =============================================================================
FROM base as builder

# Copy requirements (including modular requirements directory)
COPY requirements.txt ./
COPY requirements/ ./requirements/

# Install dependencies to a specific location
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-warn-script-location -r requirements.txt

# =============================================================================
# Stage 4: Production Image
# =============================================================================
FROM python:3.11-slim as production

LABEL maintainer="BAHR Production Team"
LABEL description="BAHR Backend API - Production Environment"
LABEL version="1.0.0"

# Set environment variables for production
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENVIRONMENT=production \
    DEBUG=false

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # PostgreSQL client library (runtime only)
    libpq5 \
    # Curl for health checks
    curl \
    # Cleanup
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create application directory
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Create non-root user for production
RUN useradd -m -u 1000 -s /bin/sh appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

# Production startup command with Gunicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--log-level", "info"]

# =============================================================================
# Stage 5: Testing Image (optional)
# =============================================================================
FROM development as testing

LABEL description="BAHR Backend API - Testing Environment"

# Install additional testing tools
RUN pip install pytest-xdist pytest-benchmark

# Copy test data
COPY tests/ tests/
COPY pytest.ini ./

# Default command runs tests
CMD ["pytest", "-v", "--cov=app", "--cov-report=html", "--cov-report=term"]

# =============================================================================
# BUILD INSTRUCTIONS
# =============================================================================
#
# Build development image:
#   docker build --target development -t bahr-backend:dev .
#
# Build production image:
#   docker build --target production -t bahr-backend:prod .
#
# Build testing image:
#   docker build --target testing -t bahr-backend:test .
#
# Run development container:
#   docker run -p 8000:8000 -v $(pwd):/app bahr-backend:dev
#
# Run production container:
#   docker run -p 8000:8000 -e DATABASE_URL=... bahr-backend:prod
#
# Run tests:
#   docker run bahr-backend:test
#
# Build with buildx (multi-platform):
#   docker buildx build --platform linux/amd64,linux/arm64 -t bahr-backend:latest .
#
# =============================================================================
# DEPLOYMENT NOTES
# =============================================================================
#
# Environment Variables Required:
#   - DATABASE_URL: PostgreSQL connection string
#   - REDIS_URL: Redis connection string
#   - SECRET_KEY: JWT signing key
#   - ENVIRONMENT: production|staging|development
#
# Optional Environment Variables:
#   - SENTRY_DSN: Error tracking
#   - LOG_LEVEL: Logging verbosity
#   - WORKERS: Number of Uvicorn workers (default: 4)
#
# Volume Mounts (development):
#   - ./:/app: Source code hot-reload
#
# Networking:
#   - Ensure PostgreSQL and Redis are accessible
#   - Use Docker networks or external DNS
#
# Security:
#   - Never run as root in production ✓
#   - Use secrets management for sensitive data
#   - Scan images for vulnerabilities: docker scan bahr-backend:prod
#   - Keep base images updated
#
# Performance:
#   - Adjust workers based on CPU cores (2-4 × cores)
#   - Use connection pooling for database
#   - Configure Redis for caching
#   - Enable HTTP/2 in reverse proxy
#
# Monitoring:
#   - Health check endpoint: /health
#   - Metrics endpoint: /metrics (Prometheus format)
#   - Logs: JSON format to stdout
#
# =============================================================================
