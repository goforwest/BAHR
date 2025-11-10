# BAHR Platform - Starter Code Templates
## Ready-to-Use Boilerplate for Codex Implementation

---

## Backend Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration
│   ├── core/                   # Prosody engine (Week 1-2)
│   │   ├── __init__.py
│   │   ├── normalization.py
│   │   ├── phonetics.py
│   │   ├── taqti3.py
│   │   └── bahr_detector.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py
│   │           ├── analyze.py
│   │           ├── generate.py
│   │           └── bahrs.py
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── poem.py
│   │   ├── bahr.py
│   │   └── competition.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── analyze.py
│   │   └── generate.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   └── redis.py
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── competition.py
│   │   └── learning.py
│   └── utils/
│       ├── __init__.py
│       ├── security.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── fixtures/
│   │   └── test_verses.json
│   ├── core/
│   │   ├── test_normalization.py
│   │   ├── test_phonetics.py
│   │   ├── test_taqti3.py
│   │   └── test_accuracy.py
│   └── api/
│       └── v1/
│           └── test_analyze.py
├── migrations/                 # Alembic
│   ├── versions/
│   └── env.py
├── scripts/
│   ├── seed_bahrs.py
│   └── clean_poetry_data.py
├── .env.example
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── Dockerfile
└── README.md
```

---

## 1. Backend: FastAPI Main Application

### File: `backend/app/main.py`

```python
"""
BAHR Platform - FastAPI Application
Main entry point for the backend API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.api.v1.router import api_router
from app.config import settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Arabic Poetry Analysis and Generation Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json"
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# GZip Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("🚀 Starting BAHR Platform API...")
    logger.info(f"📝 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🗄️  Database: {settings.DATABASE_URL[:20]}...")

    # TODO: Initialize database connection
    # TODO: Initialize Redis connection
    # TODO: Load AI models if needed


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("👋 Shutting down BAHR Platform API...")
    # TODO: Close database connections
    # TODO: Close Redis connections


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "message": "مرحباً بك في منصة بَحْر",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Check actual DB connection
        "redis": "connected",     # TODO: Check actual Redis connection
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

---

## 2. Backend: Configuration

### File: `backend/app/config.py`

```python
"""
Configuration management using Pydantic Settings.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # Project Info
    PROJECT_NAME: str = "BAHR - Arabic Poetry Platform"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # Database
    DATABASE_URL: str = "postgresql://bahr_user:password@localhost:5432/bahr_db"
    DATABASE_ECHO: bool = False  # SQL query logging

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 86400  # 24 hours in seconds

    # Elasticsearch (optional for Phase 1)
    ELASTICSEARCH_URL: str = "http://localhost:9200"

    # Security
    JWT_SECRET_KEY: str = "CHANGE_THIS_TO_RANDOM_SECRET_KEY"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Password hashing
    BCRYPT_ROUNDS: int = 12

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100

    # External Services
    OPENAI_API_KEY: str = ""
    STRIPE_SECRET_KEY: str = ""
    SENDGRID_API_KEY: str = ""

    # AI Model Settings
    AI_MODEL_PATH: str = "./models/poet-v1"
    AI_GENERATION_MAX_LENGTH: int = 50
    AI_GENERATION_TIMEOUT: int = 10  # seconds

    # Feature Flags
    ENABLE_AI_GENERATION: bool = False  # Enable in Phase 2
    ENABLE_COMPETITIONS: bool = False   # Enable in Phase 3

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
```

### File: `backend/.env.example`

```bash
# Copy this to .env and fill in your values

# Environment
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=postgresql://bahr_user:password@localhost:5432/bahr_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security (CHANGE THESE!)
JWT_SECRET_KEY=your-super-secret-key-here-change-in-production
BCRYPT_ROUNDS=12

# External APIs (add when needed)
OPENAI_API_KEY=
STRIPE_SECRET_KEY=
SENDGRID_API_KEY=

# Feature Flags
ENABLE_AI_GENERATION=false
ENABLE_COMPETITIONS=false
```

---

## 3. Backend: Database Setup

### File: `backend/app/db/base.py`

```python
"""
SQLAlchemy base and imports.
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here for Alembic
from app.models.user import User
from app.models.bahr import Bahr, Taf3ila
from app.models.poem import Poem, Verse
# Add more as you create them
```

### File: `backend/app/db/session.py`

```python
"""
Database session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency for FastAPI endpoints.

    Usage:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### File: `backend/app/db/redis.py`

```python
"""
Redis connection and caching utilities.
"""

import redis.asyncio as redis
import json
from typing import Optional, Any
from app.config import settings


# Redis client (initialized on startup)
redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """Get Redis client instance."""
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    return redis_client


async def cache_set(key: str, value: Any, ttl: int = None):
    """
    Set value in cache.

    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        ttl: Time to live in seconds (default: settings.CACHE_TTL)
    """
    client = await get_redis()
    serialized = json.dumps(value, ensure_ascii=False)
    await client.setex(key, ttl or settings.CACHE_TTL, serialized)


async def cache_get(key: str) -> Optional[Any]:
    """
    Get value from cache.

    Args:
        key: Cache key

    Returns:
        Cached value or None if not found
    """
    client = await get_redis()
    value = await client.get(key)
    if value:
        return json.loads(value)
    return None


async def cache_delete(key: str):
    """Delete key from cache."""
    client = await get_redis()
    await client.delete(key)
```

---

## 4. Backend: SQLAlchemy Models

### File: `backend/app/models/user.py`

```python
"""
User model.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    full_name = Column(String(100))
    bio = Column(String(500))
    avatar_url = Column(String(500))

    # Gamification
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    coins = Column(Integer, default=0)

    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<User {self.username}>"
```

### File: `backend/app/models/bahr.py`

```python
"""
Bahr (meter) and Taf'ila models.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from app.db.base import Base


class Bahr(Base):
    __tablename__ = "bahrs"

    id = Column(Integer, primary_key=True, index=True)
    name_ar = Column(String(50), nullable=False, unique=True)
    name_en = Column(String(50))
    pattern = Column(String(255), nullable=False)  # Tafa'il pattern
    description = Column(Text)
    example_verse = Column(Text)

    def __repr__(self):
        return f"<Bahr {self.name_ar}>"


class Taf3ila(Base):
    __tablename__ = "tafa3il"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    pattern = Column(String(50), nullable=False)  # Prosodic pattern
    variations = Column(JSON)  # Zihafat variations
    bahr_id = Column(Integer, ForeignKey("bahrs.id"), nullable=True)

    def __repr__(self):
        return f"<Taf3ila {self.name}>"
```

### File: `backend/app/models/poem.py`

```python
"""
Poem and Verse models.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Poem(Base):
    __tablename__ = "poems"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(255))
    full_text = Column(Text)
    bahr = Column(String(50))
    is_complete = Column(Boolean, default=False)
    visibility = Column(String(20), default='public')  # public, private, unlisted

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    verses = relationship("Verse", back_populates="poem")

    def __repr__(self):
        return f"<Poem {self.title}>"


class Verse(Base):
    __tablename__ = "verses"

    id = Column(Integer, primary_key=True, index=True)
    poem_id = Column(Integer, ForeignKey("poems.id"), nullable=False)

    text = Column(Text, nullable=False)
    taqti3_pattern = Column(String(255))
    bahr = Column(String(50))
    line_number = Column(Integer)
    hemisphere = Column(String(10))  # 'sadr' or 'ajuz'

    # Relationships
    poem = relationship("Poem", back_populates="verses")

    def __repr__(self):
        return f"<Verse {self.id}>"
```

---

## 5. Backend: Pydantic Schemas

### File: `backend/app/schemas/analyze.py`

```python
"""
Pydantic schemas for analyze endpoint.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List


class AnalyzeRequest(BaseModel):
    """Request schema for verse analysis."""
    text: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Arabic verse text to analyze"
    )
    detect_bahr: bool = Field(
        default=True,
        description="Whether to detect bahr (meter)"
    )
    suggest_corrections: bool = Field(
        default=False,
        description="Whether to suggest corrections for errors"
    )

    @validator('text')
    def validate_arabic(cls, v):
        """Ensure text contains Arabic characters."""
        if not any('\u0600' <= c <= '\u06FF' for c in v):
            raise ValueError('Text must contain Arabic characters')
        return v


class BahrInfo(BaseModel):
    """Information about detected bahr."""
    name_ar: str = Field(..., description="Arabic name of bahr")
    name_en: str = Field(..., description="English name of bahr")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score (0.0 to 1.0)"
    )


class AnalyzeResponse(BaseModel):
    """Response schema for verse analysis."""
    text: str = Field(..., description="Original verse text")
    taqti3: str = Field(..., description="Prosodic scansion (tafa'il)")
    bahr: Optional[BahrInfo] = Field(None, description="Detected bahr")
    errors: List[str] = Field(default=[], description="Prosodic errors found")
    suggestions: List[str] = Field(default=[], description="Correction suggestions")
    score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Quality score (0-100)"
    )

    class Config:
        schema_extra = {
            "example": {
                "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
                "taqti3": "فعولن مفاعيلن فعولن مفاعيلن",
                "bahr": {
                    "name_ar": "الطويل",
                    "name_en": "at-Tawil",
                    "confidence": 0.98
                },
                "errors": [],
                "suggestions": [],
                "score": 95
            }
        }
```

---

## 6. Backend: API Endpoints

### File: `backend/app/api/v1/router.py`

```python
"""
Main API router for v1.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import analyze, bahrs

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    analyze.router,
    prefix="/analyze",
    tags=["Analysis"]
)

api_router.include_router(
    bahrs.router,
    prefix="/bahrs",
    tags=["Bahrs"]
)

# Add more routers as you build them:
# api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
# api_router.include_router(generate.router, prefix="/generate", tags=["Generation"])
```

### File: `backend/app/api/v1/endpoints/analyze.py`

```python
"""
Analyze endpoint - prosodic analysis of verses.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import hashlib
import logging

from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.core import BahrDetector, normalize_arabic_text, perform_taqti3
from app.db.session import get_db
from app.db.redis import cache_get, cache_set

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=AnalyzeResponse)
async def analyze_verse(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze Arabic verse for prosodic structure.

    - **text**: The Arabic verse to analyze
    - **detect_bahr**: Whether to detect the bahr (meter)
    - **suggest_corrections**: Whether to suggest corrections

    Returns prosodic analysis including taqti3 and bahr detection.
    """
    try:
        # Normalize text
        normalized = normalize_arabic_text(request.text)

        # Check cache
        cache_key = f"analysis:{hashlib.sha256(normalized.encode()).hexdigest()}"
        cached = await cache_get(cache_key)
        if cached:
            logger.info(f"Cache hit for: {normalized[:30]}...")
            return cached

        # Perform taqti3
        taqti3 = perform_taqti3(normalized)

        # Detect bahr if requested
        bahr_info = None
        if request.detect_bahr:
            detector = BahrDetector()
            bahr_result = detector.detect_bahr(taqti3)
            if bahr_result:
                bahr_info = {
                    "name_ar": bahr_result.name_ar,
                    "name_en": bahr_result.name_en,
                    "confidence": bahr_result.confidence
                }

        # Calculate score (simplified for now)
        score = int(bahr_info["confidence"] * 100) if bahr_info else 50

        # Build response
        response = {
            "text": request.text,
            "taqti3": taqti3,
            "bahr": bahr_info,
            "errors": [],  # TODO: Implement error detection
            "suggestions": [],  # TODO: Implement suggestions
            "score": score
        }

        # Cache result
        await cache_set(cache_key, response)

        logger.info(f"Analyzed verse: {normalized[:30]}... -> {bahr_info['name_ar'] if bahr_info else 'unknown'}")

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error analyzing verse: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### File: `backend/app/api/v1/endpoints/bahrs.py`

```python
"""
Bahrs endpoint - list available bahrs (meters).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.bahr import Bahr

router = APIRouter()


@router.get("/")
async def list_bahrs(db: Session = Depends(get_db)):
    """
    List all available Arabic poetry bahrs (meters).

    Returns list of bahrs with their patterns and descriptions.
    """
    # TODO: Query from database when seeded
    # For now, return hardcoded list
    bahrs = [
        {
            "id": 1,
            "name_ar": "الطويل",
            "name_en": "at-Tawil",
            "pattern": "فعولن مفاعيلن فعولن مفاعيلن",
            "description": "أكثر البحور استعمالاً في الشعر العربي"
        },
        {
            "id": 2,
            "name_ar": "الكامل",
            "name_en": "al-Kamil",
            "pattern": "متفاعلن متفاعلن متفاعلن",
            "description": "من أكثر البحور جزالة"
        },
        # Add more...
    ]

    return {"bahrs": bahrs, "total": len(bahrs)}
```

---

## 7. Backend: Requirements

### File: `backend/requirements.txt`

```txt
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

# AI/ML (for Phase 2)
# transformers==4.35.2
# torch==2.1.1

# Arabic NLP
# camel-tools==1.5.2

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Development
black==23.11.0
flake8==6.1.0
mypy==1.7.1
```

---

## 8. Frontend: Next.js Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── analyze/
│   │   │   └── page.tsx
│   │   ├── generate/
│   │   │   └── page.tsx
│   │   └── compete/
│   │       └── page.tsx
│   ├── components/
│   │   ├── ui/              # shadcn components
│   │   ├── AnalyzeForm.tsx
│   │   ├── AnalyzeResults.tsx
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   ├── utils.ts
│   │   └── constants.ts
│   ├── hooks/
│   │   ├── useAnalyze.ts
│   │   └── useWebSocket.ts
│   ├── types/
│   │   ├── analyze.ts
│   │   └── user.ts
│   └── styles/
│       └── globals.css
├── public/
│   ├── fonts/
│   │   ├── Cairo-Regular.ttf
│   │   └── Amiri-Regular.ttf
│   └── images/
├── .env.local
├── .env.example
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── README.md
```

---

## 9. Frontend: Next.js Setup

### File: `frontend/package.json`

```json
{
  "name": "bahr-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "next": "14.0.4",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "typescript": "5.3.3",
    "@tanstack/react-query": "5.12.2",
    "axios": "1.6.2",
    "zustand": "4.4.7",
    "react-hook-form": "7.48.2",
    "zod": "3.22.4",
    "@hookform/resolvers": "3.3.2",
    "socket.io-client": "4.6.0",
    "framer-motion": "10.16.16",
    "recharts": "2.10.3",
    "clsx": "2.0.0",
    "tailwind-merge": "2.1.0"
  },
  "devDependencies": {
    "tailwindcss": "3.3.6",
    "postcss": "8.4.32",
    "autoprefixer": "10.4.16",
    "@types/node": "20.10.4",
    "@types/react": "18.2.42",
    "@types/react-dom": "18.2.17",
    "eslint": "8.55.0",
    "eslint-config-next": "14.0.4"
  }
}
```

### File: `frontend/tailwind.config.ts`

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
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
```

### File: `frontend/src/app/layout.tsx`

```tsx
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
      <body className={`${cairo.variable} ${amiri.variable} font-arabic`}>
        {children}
      </body>
    </html>
  )
}
```

### File: `frontend/src/lib/api.ts`

```typescript
/**
 * API client for BAHR backend
 */

import axios from 'axios';
import type { AnalyzeRequest, AnalyzeResponse } from '@/types/analyze';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor (add auth token if needed)
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor (handle errors globally)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API functions

export async function analyzeVerse(data: AnalyzeRequest): Promise<AnalyzeResponse> {
  const response = await apiClient.post('/analyze', data);
  return response.data;
}

export async function getBahrs() {
  const response = await apiClient.get('/bahrs');
  return response.data;
}

// Add more API functions as needed...

export default apiClient;
```

---

## 10. Docker Setup

### File: `docker-compose.yml`

```yaml
version: '3.8'

services:
  # PostgreSQL Database
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

  # Redis Cache
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

  # Elasticsearch (Optional - for Phase 2+)
  # elasticsearch:
  #   image: elasticsearch:8.11.0
  #   container_name: bahr_elasticsearch
  #   environment:
  #     - discovery.type=single-node
  #     - xpack.security.enabled=false
  #   ports:
  #     - "9200:9200"
  #   volumes:
  #     - elasticsearch_data:/usr/share/elasticsearch/data

  # FastAPI Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: bahr_backend
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://bahr_user:bahr_password@postgres:5432/bahr_db
      REDIS_URL: redis://redis:6379/0
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Next.js Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: bahr_frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000/api/v1
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev

volumes:
  postgres_data:
  redis_data:
  # elasticsearch_data:
```

### File: `backend/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### File: `frontend/Dockerfile`

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application
COPY . .

# Expose port
EXPOSE 3000

# Run development server
CMD ["npm", "run", "dev"]
```

---

## Usage Instructions

### 1. Start Development Environment

```bash
# Clone/create project directories
mkdir -p backend frontend
cd your-project-root

# Copy template files (use files above)

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Access services:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### 2. Database Setup

```bash
# Enter backend container
docker exec -it bahr_backend bash

# Run migrations
alembic upgrade head

# Seed bahrs data
python scripts/seed_bahrs.py
```

### 3. Run Tests

```bash
# Backend tests
docker exec bahr_backend pytest tests/ -v

# Frontend tests
docker exec bahr_frontend npm test
```

---

## Next Steps for Codex

1. **Copy template files** to your project structure
2. **Implement Phase 1, Week 1-2** (Prosody Engine) using `PHASE_1_WEEK_1-2_SPEC.md`
3. **Run tests** to verify accuracy (target: 90%+)
4. **Continue to Week 3-4** (API & Database)

All templates are ready to use! 🚀
