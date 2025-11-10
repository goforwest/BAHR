# 🔌 دليل Backend API الشامل
## FastAPI + Authentication + Validation

---

## 📋 نظرة عامة

دليل شامل لتطوير Backend API لمشروع بَحْر باستخدام FastAPI مع التركيز على:
- **Architecture متقدمة** مع dependency injection
- **Authentication & Authorization** كاملة
- **Request/Response Validation** دقيقة
- **Error Handling** شامل ومفيد
- **API Documentation** تلقائية مع Swagger
- **Testing Strategy** شاملة

---

## 🏗️ معمارية Backend

```
Backend Architecture:
┌─────────────────────────────────────────────┐
│               API Gateway Layer             │
│  ┌─────────────┐ ┌─────────────┐           │
│  │   FastAPI   │ │ Middleware  │           │
│  │   Router    │ │    Stack    │           │
│  └─────────────┘ └─────────────┘           │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│            Service Layer                    │
│  ┌─────────────┐ ┌─────────────┐           │
│  │  Business   │ │    Auth     │           │
│  │    Logic    │ │   Service   │           │
│  └─────────────┘ └─────────────┘           │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│          Repository Layer                   │
│  ┌─────────────┐ ┌─────────────┐           │
│  │  Database   │ │    Cache    │           │
│  │    Access   │ │   Service   │           │
│  └─────────────┘ └─────────────┘           │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│            Data Layer                       │
│     PostgreSQL + Redis + File Storage      │
└─────────────────────────────────────────────┘
```

---

## 📁 هيكل Backend المفصل

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration settings
│   ├── dependencies.py            # Global dependencies
│   │
│   ├── api/                       # API endpoints
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py          # Main API router
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py        # Authentication endpoints
│   │   │   │   ├── analyze.py     # Poetry analysis endpoints
│   │   │   │   ├── generate.py    # AI generation endpoints
│   │   │   │   ├── meters.py      # Prosodic meters endpoints
│   │   │   │   ├── users.py       # User management endpoints
│   │   │   │   ├── competitions.py # Competition endpoints
│   │   │   │   └── health.py      # Health check endpoints
│   │   │   └── dependencies.py    # API-specific dependencies
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── cors.py           # CORS middleware
│   │       ├── auth.py           # Authentication middleware
│   │       ├── logging.py        # Logging middleware
│   │       ├── rate_limit.py     # Rate limiting middleware
│   │       └── error_handler.py  # Global error handling
│   │
│   ├── core/                     # Core business logic
│   │   ├── __init__.py
│   │   ├── config.py             # Core configuration
│   │   ├── security.py           # Security utilities
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── jwt_handler.py    # JWT token management
│   │   │   ├── password.py       # Password hashing/verification
│   │   │   ├── oauth.py          # OAuth providers (Google, etc)
│   │   │   └── permissions.py    # Permission system
│   │   │
│   │   ├── prosody/              # Prosody analysis engine
│   │   │   ├── __init__.py
│   │   │   ├── analyzer.py       # Main analysis orchestrator
│   │   │   ├── normalizer.py     # Arabic text normalization
│   │   │   ├── segmenter.py      # Phonetic segmentation
│   │   │   ├── pattern_matcher.py # Pattern matching
│   │   │   ├── meter_detector.py # Meter detection
│   │   │   └── quality_scorer.py # Quality assessment
│   │   │
│   │   ├── ai/                   # AI services (future)
│   │   │   ├── __init__.py
│   │   │   ├── generator.py      # Poetry generation
│   │   │   └── fine_tuner.py     # Model fine-tuning
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── arabic.py         # Arabic text utilities
│   │       ├── cache.py          # Caching utilities
│   │       ├── validators.py     # Custom validators
│   │       └── helpers.py        # Helper functions
│   │
│   ├── db/                       # Database layer
│   │   ├── __init__.py
│   │   ├── session.py           # Database session management
│   │   ├── base.py              # Base model class
│   │   ├── repositories/        # Repository pattern
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # Base repository
│   │   │   ├── user.py          # User repository
│   │   │   ├── analysis.py      # Analysis repository
│   │   │   ├── meter.py         # Meter repository
│   │   │   └── competition.py   # Competition repository
│   │   └── migrations/          # Alembic migrations
│   │       ├── env.py
│   │       ├── script.py.mako
│   │       └── versions/
│   │
│   ├── models/                  # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base.py              # Base model with common fields
│   │   ├── user.py              # User model
│   │   ├── analysis.py          # Analysis models
│   │   ├── meter.py             # Prosody models
│   │   ├── competition.py       # Competition models
│   │   └── associations.py      # Many-to-many associations
│   │
│   ├── schemas/                 # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── base.py              # Base schemas
│   │   ├── user.py              # User schemas
│   │   ├── auth.py              # Authentication schemas
│   │   ├── analysis.py          # Analysis schemas
│   │   ├── meter.py             # Meter schemas
│   │   ├── competition.py       # Competition schemas
│   │   └── responses.py         # Standard response schemas
│   │
│   ├── services/                # Business logic services
│   │   ├── __init__.py
│   │   ├── user_service.py      # User business logic
│   │   ├── auth_service.py      # Authentication service
│   │   ├── analysis_service.py  # Analysis business logic
│   │   ├── meter_service.py     # Meter management
│   │   ├── competition_service.py # Competition logic
│   │   └── email_service.py     # Email notifications
│   │
│   └── tests/                   # Test suites
│       ├── __init__.py
│       ├── conftest.py          # Pytest configuration
│       ├── test_api/            # API endpoint tests
│       ├── test_services/       # Service layer tests
│       ├── test_models/         # Model tests
│       └── test_utils/          # Utility tests
│
├── requirements/               # Dependencies
│   ├── base.txt               # Base requirements
│   ├── development.txt        # Development dependencies
│   ├── production.txt         # Production dependencies
│   └── testing.txt           # Testing dependencies
│
├── scripts/                   # Utility scripts
│   ├── init_db.py            # Database initialization
│   ├── seed_data.py          # Seed data insertion
│   ├── migrate.py            # Migration runner
│   └── backup.py             # Database backup
│
├── docker/                   # Docker configurations
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── entrypoint.sh
│
├── .env.example              # Environment variables template
├── alembic.ini              # Alembic configuration
├── pytest.ini              # Pytest configuration
└── README.md                # Backend documentation
```

---

## ⚙️ Core Configuration

### Environment Configuration:

```python
# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "بَحْر - Poetry Analysis API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str
    REDIS_MAX_CONNECTIONS: int = 10
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 3600  # 1 hour
    
    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # External APIs
    OPENAI_API_KEY: Optional[str] = None
    HUGGINGFACE_TOKEN: Optional[str] = None
    
    # File Storage
    UPLOAD_MAX_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["txt", "pdf", "doc", "docx"]
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### FastAPI Application Setup:

```python
# app/main.py
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import time
import logging

from app.config import settings
from app.api.v1.router import api_router
from app.api.middleware import (
    LoggingMiddleware,
    RateLimitMiddleware,
    AuthenticationMiddleware
)
from app.core.exceptions import BahrException

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="API شاملة لتحليل الشعر العربي وعلم العروض",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None
    )
    
    # Add middleware
    setup_middleware(app)
    
    # Add routers
    app.include_router(api_router, prefix="/api/v1")
    
    # Add exception handlers
    setup_exception_handlers(app)
    
    # Add startup/shutdown events
    setup_events(app)
    
    return app

def setup_middleware(app: FastAPI) -> None:
    """Configure middleware stack."""
    
    # Trusted host middleware (security)
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*.bahr.app", "bahr.app"]
        )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    # Custom middleware
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(AuthenticationMiddleware)

def setup_exception_handlers(app: FastAPI) -> None:
    """Configure global exception handlers."""
    
    @app.exception_handler(BahrException)
    async def bahr_exception_handler(request: Request, exc: BahrException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "details": exc.details
                },
                "timestamp": time.time(),
                "path": str(request.url)
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "بيانات الإدخال غير صالحة",
                    "details": exc.errors()
                },
                "timestamp": time.time(),
                "path": str(request.url)
            }
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"Database error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "DATABASE_ERROR", 
                    "message": "خطأ في قاعدة البيانات",
                    "details": None if not settings.DEBUG else str(exc)
                },
                "timestamp": time.time(),
                "path": str(request.url)
            }
        )

def setup_events(app: FastAPI) -> None:
    """Configure startup/shutdown events."""
    
    @app.on_event("startup")
    async def startup_event():
        logger.info("🚀 بَحْر API starting up...")
        # Initialize database connections, cache, etc.
        
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("👋 بَحْر API shutting down...")
        # Clean up resources

# Create app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
```

---

## � Rate Limiting Specification (MVP)

Algorithm: Fixed Window + Redis counters (simple, predictable)  
Policy: 100 requests/hour per IP for public endpoints (`/api/v1/analyze`, `/api/v1/meters`), stricter for batch/dataset endpoints.

Redis Keys:
- `rate:{ip}:{window_start}` → integer count with TTL = RATE_LIMIT_PERIOD

Response on limit exceeded:
- HTTP 429 Too Many Requests
- Body conforms to ErrorSchema with code `ERR_RATE_001` (see `ERROR_HANDLING_STRATEGY.md`)

Graceful Degradation:
- Suggest user to retry after `Retry-After` seconds header
- Frontend displays localized message and disables analyze button until cooldown

Note: Authenticated users may get slightly higher quotas later; for MVP keep IP-based caps.

---

## 📦 Dataset Ingestion (Admin-only, for labeled verses)

Purpose: Enable bootstrapping and iterative improvement of the labeled dataset used for evaluation and calibration.  
Security: Protected by JWT + role check (admin) + payload size limit.

Endpoint:
- `POST /api/v1/datasets/verses` (batch insert, JSON or JSONL)

Request Schema (subset):
```json
{
    "records": [
        {"text": "قفا نبك...", "meter": "الطويل", "era": "classical", "source": "...", "notes": "..."}
    ]
}
```

Behavior:
- Deduplicate by normalized text hash + meter
- Validate Arabic content ratio
- Store into `datasets_verses` table (or `analyses` as gold set) with provenance

Rate limiting: 30 requests/hour/IP; max 1000 records per request; 413 if payload too large.

---

## 🧩 Fallback Analyzer Note

The analysis service uses a resilient path:
1) Primary rule-based analyzer  
2) If NLP library fails: fallback rule-only mode with warning `ERR_NLP_001`  
3) As last resort: basic analysis summary (no meter) with clear messaging

See: `ERROR_HANDLING_STRATEGY.md` (ResilientAnalyzer) and `PROSODY_ENGINE.md` (rules priority).

---

## �🔐 Authentication System

### JWT Token Management:

```python
# app/core/auth/jwt_handler.py
from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt, JWTError
from app.config import settings

class JWTHandler:
    """JWT token creation and verification."""
    
    @staticmethod
    def create_access_token(
        subject: Union[str, Any], 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        to_encode = {
            "exp": expire,
            "sub": str(subject),
            "type": "access"
        }
        
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(subject: Union[str, Any]) -> str:
        """Create JWT refresh token."""
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        
        to_encode = {
            "exp": expire,
            "sub": str(subject), 
            "type": "refresh"
        }
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def get_subject_from_token(token: str) -> Optional[str]:
        """Extract subject (user ID) from token."""
        payload = JWTHandler.verify_token(token)
        if payload:
            return payload.get("sub")
        return None
```

### Authentication Dependencies:

```python
# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.core.auth.jwt_handler import JWTHandler
from app.repositories.user import UserRepository
from app.models.user import User
from app.core.exceptions import AuthenticationException

security = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    
    if not credentials:
        raise AuthenticationException("مطلوب تسجيل الدخول للوصول لهذه الخدمة")
    
    # Verify token
    payload = JWTHandler.verify_token(credentials.credentials)
    if not payload:
        raise AuthenticationException("رمز الدخول غير صالح أو منتهي الصلاحية")
    
    # Check token type
    if payload.get("type") != "access":
        raise AuthenticationException("نوع رمز الدخول غير صحيح")
    
    # Get user
    user_id = payload.get("sub")
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(int(user_id))
    
    if not user:
        raise AuthenticationException("المستخدم غير موجود")
    
    if not user.is_active:
        raise AuthenticationException("حساب المستخدم معطل")
    
    return user

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user if authenticated, None otherwise."""
    try:
        return await get_current_user(credentials, db)
    except AuthenticationException:
        return None

def require_permissions(*permissions: str):
    """Decorator to require specific permissions."""
    def permission_checker(current_user: User = Depends(get_current_user)):
        user_permissions = [perm.name for perm in current_user.permissions]
        
        for permission in permissions:
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"مطلوب صلاحية {permission} للوصول لهذه الخدمة"
                )
        
        return current_user
    
    return permission_checker

def require_role(role: str):
    """Decorator to require specific role."""
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"مطلوب دور {role} للوصول لهذه الخدمة"
            )
        
        return current_user
    
    return role_checker
```

---

## 📊 Pydantic Schemas

### Base Schemas:

```python
# app/schemas/base.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, Dict
from datetime import datetime

class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        validate_assignment=True
    )

class TimestampedSchema(BaseSchema):
    """Schema with timestamp fields."""
    created_at: datetime
    updated_at: Optional[datetime] = None

class ResponseSchema(BaseSchema):
    """Standard API response schema."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None
    meta: Optional[Dict[str, Any]] = None

class ErrorSchema(BaseSchema):
    """Error response schema."""
    success: bool = False
    error: Dict[str, Any]
    timestamp: float
    path: str

class PaginatedResponseSchema(BaseSchema):
    """Paginated response schema."""
    success: bool = True
    data: list
    meta: Dict[str, Any]  # Contains pagination info
```

### Analysis Schemas:

```python
# app/schemas/analysis.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum

class AnalysisModeEnum(str, Enum):
    FAST = "fast"
    ACCURATE = "accurate"
    DETAILED = "detailed"

class AnalysisOptionsSchema(BaseSchema):
    """Analysis configuration options."""
    remove_diacritics: bool = Field(
        default=True,
        description="إزالة التشكيل من النص"
    )
    analysis_mode: AnalysisModeEnum = Field(
        default=AnalysisModeEnum.ACCURATE,
        description="نوع التحليل المطلوب"
    )
    return_alternatives: bool = Field(
        default=True,
        description="إرجاع البدائل المحتملة للبحور"
    )
    include_suggestions: bool = Field(
        default=True,
        description="تضمين اقتراحات التحسين"
    )

class AnalysisRequestSchema(BaseSchema):
    """Poetry analysis request."""
    text: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        description="النص الشعري المراد تحليله"
    )
    options: AnalysisOptionsSchema = Field(
        default_factory=AnalysisOptionsSchema,
        description="خيارات التحليل"
    )
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('النص لا يمكن أن يكون فارغاً')
        
        # Basic Arabic text validation
        arabic_chars = sum(1 for c in v if '\u0600' <= c <= '\u06FF')
        if arabic_chars < len(v.replace(' ', '')) * 0.7:
            raise ValueError('النص يجب أن يحتوي على نسبة عالية من الأحرف العربية')
        
        return v

---

## 🔤 Arabic Text Encoding Safety

### UTF-8 Configuration (Critical)

**Problem:** Arabic text encoding issues can cause:
- Garbled text display (مو�عظ instead of موعظة)
- Database insertion failures
- API response corruption
- Frontend rendering issues

**Solution:** Enforce UTF-8 everywhere

```python
# app/config.py - Database Configuration

DATABASE_URL = "postgresql://user:pass@localhost/bahr?client_encoding=utf8"

# SQLAlchemy Engine Configuration
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    # CRITICAL: Force UTF-8 encoding
    connect_args={
        "options": "-c client_encoding=utf8",
        "client_encoding": "utf8"
    },
    # Ensure proper Unicode handling
    encoding="utf-8"
)
```

```python
# app/main.py - FastAPI Configuration

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    # Default response class with UTF-8
    default_response_class=JSONResponse,
)

# Middleware to ensure UTF-8 responses
@app.middleware("http")
async def ensure_utf8_response(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response
```

```python
# app/core/utils/arabic.py - Text Handling Utilities

import unicodedata
from typing import Optional

class ArabicTextHandler:
    """Safe handling of Arabic text with proper encoding"""
    
    @staticmethod
    def normalize_unicode(text: str) -> str:
        """
        Normalize Unicode to prevent encoding issues
        
        Uses NFKC normalization which:
        - Decomposes characters
        - Recomposes in canonical form
        - Handles Arabic compatibility characters
        """
        if not text:
            return ""
        
        # NFKC: Compatibility decomposition + canonical composition
        normalized = unicodedata.normalize('NFKC', text)
        
        # Ensure it's valid UTF-8
        return normalized.encode('utf-8', errors='ignore').decode('utf-8')
    
    @staticmethod
    def safe_encode(text: str) -> bytes:
        """Safely encode Arabic text to UTF-8 bytes"""
        try:
            return text.encode('utf-8')
        except UnicodeEncodeError as e:
            # Log the error with problematic character
            logger.error(f"Encoding error: {e}. Text: {text[:100]}")
            # Replace problematic characters
            return text.encode('utf-8', errors='replace')
    
    @staticmethod
    def safe_decode(data: bytes) -> str:
        """Safely decode bytes to Arabic text"""
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError as e:
            logger.error(f"Decoding error: {e}")
            # Try other common encodings
            for encoding in ['utf-8', 'windows-1256', 'iso-8859-6']:
                try:
                    return data.decode(encoding)
                except:
                    continue
            # Fallback: ignore errors
            return data.decode('utf-8', errors='ignore')
```

### Edge Cases Testing

```python
# tests/test_arabic_encoding.py

import pytest
from app.core.utils.arabic import ArabicTextHandler

handler = ArabicTextHandler()

def test_arabic_text_basic():
    """Test basic Arabic text"""
    text = "قفا نبك من ذكرى حبيب ومنزل"
    normalized = handler.normalize_unicode(text)
    assert normalized == text
    assert normalized.encode('utf-8').decode('utf-8') == text

def test_mixed_arabic_english():
    """Test mixed Arabic and English"""
    text = "Poetry الشعر العربي BAHR"
    normalized = handler.normalize_unicode(text)
    assert "الشعر" in normalized
    assert "Poetry" in normalized
    assert normalized.encode('utf-8').decode('utf-8') == normalized

def test_arabic_with_emoji():
    """Test Arabic text with emoji (common in modern usage)"""
    text = "قصيدة جميلة 🌟 ماشاء الله 🎭"
    normalized = handler.normalize_unicode(text)
    # Emoji should be preserved
    assert "🌟" in normalized
    assert "🎭" in normalized
    assert "قصيدة" in normalized

def test_rtl_override_characters():
    """Test Right-to-Left override (security risk)"""
    # U+202E is RTL override - can be used for phishing
    malicious_text = "test\u202Eابرع"  # Appears as "عرباtest"
    normalized = handler.normalize_unicode(malicious_text)
    
    # Should remove or neutralize RTL override
    assert "\u202E" not in normalized
    # Or explicitly reject
    from app.api.v1.endpoints.analyze import validate_arabic_text
    with pytest.raises(ValueError, match="invisible characters"):
        validate_arabic_text(malicious_text)

def test_arabic_diacritics_overflow():
    """Test excessive diacritics (DoS attack vector)"""
    # Attacker might send 100+ diacritics on one character
    base_char = "ب"
    excessive_diacritics = base_char + ("\u064E" * 50)  # 50 fatha marks
    
    # Should normalize or reject
    normalized = handler.normalize_unicode(excessive_diacritics)
    diacritic_count = sum(1 for c in normalized if '\u064B' <= c <= '\u0652')
    assert diacritic_count <= 3, "Too many diacritics should be reduced"

def test_zero_width_characters():
    """Test zero-width joiners/non-joiners"""
    # U+200C (ZWNJ), U+200D (ZWJ) are valid in Arabic but can be abused
    text = "الـ\u200cـرحـ\u200dـمن"  # "الرحمن" with zero-width chars
    normalized = handler.normalize_unicode(text)
    
    # Optional: Remove excessive zero-width chars
    zw_count = normalized.count('\u200c') + normalized.count('\u200d')
    assert zw_count <= 2, "Excessive zero-width characters detected"

def test_arabic_presentation_forms():
    """Test Arabic presentation forms (should normalize)"""
    # U+FE70-U+FEFF are presentation forms
    presentation = "\uFEDF\uFEE0"  # ﻟﻠ (ligature)
    normalized = handler.normalize_unicode(presentation)
    
    # Should normalize to base forms
    assert "\uFEDF" not in normalized  # Presentation form removed
    # Should be: ل + ل
    assert "ل" in normalized

def test_url_with_arabic():
    """Test URLs containing Arabic (rare but valid)"""
    url = "https://example.com/قصيدة"
    # Should be properly URL-encoded
    from urllib.parse import quote
    encoded = quote(url.encode('utf-8'))
    assert "%D9%82%D8%B5%D9%8A%D8%AF%D8%A9" in encoded  # "قصيدة" encoded

def test_sql_injection_with_arabic():
    """Test SQL injection attempts with Arabic characters"""
    malicious = "'; DROP TABLE users; SELECT 'الشعر"
    
    # SQLAlchemy parameterized queries should handle this
    from app.models import Analysis
    from sqlalchemy import text
    
    # SAFE (parameterized):
    # session.query(Analysis).filter(Analysis.original_text == malicious)
    # This is safe because SQLAlchemy uses bind parameters
    
    # UNSAFE (string concatenation):
    # session.execute(f"SELECT * FROM analyses WHERE text = '{malicious}'")
    # Never do this!

def test_xss_with_arabic():
    """Test XSS attempts with Arabic text"""
    xss_attempt = "<script>alert('مرحبا')</script>الشعر"
    
    # Should be HTML-escaped before rendering
    from html import escape
    safe_text = escape(xss_attempt)
    assert "&lt;script&gt;" in safe_text
    assert "الشعر" in safe_text  # Arabic preserved
    assert "<script>" not in safe_text  # Tags escaped

def test_very_long_arabic_text():
    """Test handling of very long Arabic text (DoS prevention)"""
    long_text = "الشعر " * 10000  # 60,000 characters
    
    # Should either:
    # 1. Reject with 413 Payload Too Large
    # 2. Truncate gracefully
    from app.api.v1.endpoints.analyze import MAX_TEXT_LENGTH
    assert len(long_text) > MAX_TEXT_LENGTH
    
    # API should reject this
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    response = client.post("/api/v1/analyze", json={"text": long_text})
    assert response.status_code == 413  # Payload too large

def test_arabic_in_json_response():
    """Test Arabic text in JSON responses"""
    import json
    
    data = {
        "message": "تحليل ناجح",
        "result": {
            "meter": "الطويل",
            "confidence": 0.95
        }
    }
    
    # Should serialize correctly
    json_str = json.dumps(data, ensure_ascii=False)
    assert "تحليل ناجح" in json_str  # Not Unicode-escaped
    
    # Should deserialize correctly
    parsed = json.loads(json_str)
    assert parsed["message"] == "تحليل ناجح"

def test_arabic_in_database():
    """Test Arabic text storage and retrieval from database"""
    from app.models import Analysis
    from app.db.session import SessionLocal
    
    db = SessionLocal()
    try:
        # Create analysis with Arabic text
        analysis = Analysis(
            original_text="قفا نبك من ذكرى حبيب ومنزل",
            normalized_text="قفا نبك من ذكرى حبيب ومنزل",
            detected_meter="الطويل"
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        # Retrieve and verify
        retrieved = db.query(Analysis).filter_by(id=analysis.id).first()
        assert retrieved.original_text == "قفا نبك من ذكرى حبيب ومنزل"
        assert retrieved.detected_meter == "الطويل"
        
    finally:
        db.close()
```

### Frontend Integration (Next.js)

```typescript
// frontend/lib/api/client.ts

// Ensure UTF-8 in API requests
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'Accept': 'application/json; charset=utf-8',
  },
});

// Handle Arabic text in responses
apiClient.interceptors.response.use(
  (response) => {
    // Ensure proper UTF-8 decoding
    if (typeof response.data === 'string') {
      response.data = JSON.parse(response.data);
    }
    return response;
  },
  (error) => {
    // Log encoding errors
    if (error.response?.data) {
      console.error('API Error:', error.response.data);
    }
    return Promise.reject(error);
  }
);
```

### Common Pitfalls to Avoid

```python
# ❌ WRONG: String concatenation in SQL
def get_verse_by_text_UNSAFE(text: str):
    query = f"SELECT * FROM verses WHERE text = '{text}'"  # SQL injection!
    return db.execute(query)

# ✅ CORRECT: Parameterized query
def get_verse_by_text_SAFE(text: str):
    query = "SELECT * FROM verses WHERE text = :text"
    return db.execute(query, {"text": text})

# ❌ WRONG: Assuming Windows-1256 encoding
def read_file_UNSAFE(filename: str):
    with open(filename, 'r', encoding='windows-1256') as f:  # Legacy encoding
        return f.read()

# ✅ CORRECT: Always use UTF-8
def read_file_SAFE(filename: str):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

# ❌ WRONG: Not escaping HTML
def render_verse_UNSAFE(text: str):
    return f"<div>{text}</div>"  # XSS vulnerability!

# ✅ CORRECT: Escape HTML
from html import escape
def render_verse_SAFE(text: str):
    return f"<div>{escape(text)}</div>"

# ❌ WRONG: Ignoring encoding errors silently
def process_text_UNSAFE(text: str):
    try:
        return text.encode('utf-8').decode('utf-8')
    except:
        pass  # Silent failure!

# ✅ CORRECT: Log and handle errors
def process_text_SAFE(text: str):
    try:
        return text.encode('utf-8').decode('utf-8')
    except UnicodeError as e:
        logger.error(f"Encoding error: {e}. Text preview: {text[:50]}")
        raise ValueError("Invalid text encoding") from e
```

---

class ProsodyPatternSchema(BaseSchema):
    """Prosodic pattern information."""
    taqti3: str = Field(description="التقطيع العروضي")
    pattern: str = Field(description="النمط الإيقاعي")
    syllable_count: int = Field(description="عدد المقاطع")
    stress_pattern: Optional[str] = Field(description="نمط النبر")

class MeterAlternativeSchema(BaseSchema):
    """Alternative meter suggestion."""
    name: str = Field(description="اسم البحر")
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="مستوى الثقة"
    )
    reason: Optional[str] = Field(description="سبب الاقتراح")

class MeterDetectionSchema(BaseSchema):
    """Meter detection results."""
    detected_meter: Optional[str] = Field(description="البحر المكتشف")
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="مستوى الثقة في الكشف"
    )
    alternatives: List[MeterAlternativeSchema] = Field(
        default_factory=list,
        description="البحور البديلة المحتملة"
    )

class AnalysisResultSchema(BaseSchema):
    """Complete analysis result."""
    input_text: str = Field(description="النص الأصلي")
    normalized_text: str = Field(description="النص بعد التطبيع")
    prosodic_analysis: ProsodyPatternSchema
    meter_detection: MeterDetectionSchema
    quality_score: float = Field(
        ge=0.0,
        le=1.0,
        description="تقييم جودة البيت"
    )
    suggestions: List[str] = Field(
        default_factory=list,
        description="اقتراحات وملاحظات"
    )
    processing_time_ms: int = Field(description="وقت المعالجة بالميللي ثانية")
    analysis_id: Optional[str] = Field(description="معرف التحليل")

class AnalysisResponseSchema(ResponseSchema):
    """Analysis API response."""
    data: AnalysisResultSchema
```

### User Schemas:

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
import re

from app.schemas.base import BaseSchema, TimestampedSchema

class UserRole(str, Enum):
    STUDENT = "student"
    POET = "poet" 
    TEACHER = "teacher"
    MODERATOR = "moderator"
    ADMIN = "admin"

class UserCreateSchema(BaseSchema):
    """User registration schema."""
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="اسم المستخدم"
    )
    email: EmailStr = Field(description="البريد الإلكتروني")
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="كلمة المرور"
    )
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="الاسم الكامل"
    )
    role: UserRole = Field(
        default=UserRole.STUDENT,
        description="دور المستخدم"
    )
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_\u0600-\u06FF]+$', v):
            raise ValueError('اسم المستخدم يجب أن يحتوي على أحرف وأرقام فقط')
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('كلمة المرور يجب أن تحتوي على أحرف')
        if not re.search(r'\d', v):
            raise ValueError('كلمة المرور يجب أن تحتوي على أرقام')
        return v

class UserLoginSchema(BaseSchema):
    """User login schema."""
    email: EmailStr = Field(description="البريد الإلكتروني")
    password: str = Field(description="كلمة المرور")

class UserUpdateSchema(BaseSchema):
    """User update schema."""
    full_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100
    )
    bio: Optional[str] = Field(
        None,
        max_length=500,
        description="نبذة عن المستخدم"
    )
    avatar_url: Optional[str] = Field(description="رابط الصورة الشخصية")

class UserResponseSchema(TimestampedSchema):
    """User response schema."""
    id: int
    username: str
    email: str
    full_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    role: UserRole
    level: int = Field(default=1)
    xp: int = Field(default=0)
    coins: int = Field(default=0)
    is_active: bool = Field(default=True)
    last_login: Optional[datetime] = None

class TokenResponseSchema(BaseSchema):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponseSchema
```

---

## 🔗 API Endpoints

### Authentication Endpoints:

```python
# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer

from app.db.session import get_db
from app.schemas.user import (
    UserCreateSchema, 
    UserLoginSchema,
    TokenResponseSchema,
    UserResponseSchema
)
from app.schemas.base import ResponseSchema
from app.services.auth_service import AuthService
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

@router.post(
    "/register",
    response_model=ResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="تسجيل مستخدم جديد"
)
async def register_user(
    user_data: UserCreateSchema,
    db: Session = Depends(get_db)
):
    """
    تسجيل مستخدم جديد في النظام.
    
    - **username**: اسم المستخدم (فريد)
    - **email**: البريد الإلكتروني (فريد)
    - **password**: كلمة المرور (8 أحرف على الأقل)
    - **full_name**: الاسم الكامل
    - **role**: دور المستخدم (افتراضي: student)
    """
    auth_service = AuthService(db)
    
    try:
        user = await auth_service.register_user(user_data)
        return ResponseSchema(
            message="تم تسجيل المستخدم بنجاح",
            data={"user_id": user.id, "username": user.username}
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post(
    "/login",
    response_model=TokenResponseSchema,
    summary="تسجيل الدخول"
)
async def login(
    credentials: UserLoginSchema,
    db: Session = Depends(get_db)
):
    """
    تسجيل دخول المستخدم والحصول على رمز الوصول.
    
    - **email**: البريد الإلكتروني
    - **password**: كلمة المرور
    
    Returns:
    - Access token (صالح لمدة 30 دقيقة)
    - Refresh token (صالح لمدة 7 أيام)
    - معلومات المستخدم
    """
    auth_service = AuthService(db)
    
    try:
        result = await auth_service.authenticate_user(
            credentials.email, 
            credentials.password
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post(
    "/refresh",
    response_model=TokenResponseSchema,
    summary="تجديد رمز الوصول"
)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """تجديد رمز الوصول باستخدام refresh token."""
    auth_service = AuthService(db)
    
    try:
        result = await auth_service.refresh_access_token(refresh_token)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post(
    "/logout",
    response_model=ResponseSchema,
    summary="تسجيل الخروج"
)
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """تسجيل خروج المستخدم وإلغاء رمز الوصول."""
    auth_service = AuthService(db)
    
    await auth_service.logout_user(current_user.id)
    
    return ResponseSchema(message="تم تسجيل الخروج بنجاح")

@router.get(
    "/me",
    response_model=UserResponseSchema,
    summary="معلومات المستخدم الحالي"
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """الحصول على معلومات المستخدم المسجل حالياً."""
    return current_user

@router.post(
    "/forgot-password",
    response_model=ResponseSchema,
    summary="نسيان كلمة المرور"
)
async def forgot_password(
    email: EmailStr,
    db: Session = Depends(get_db)
):
    """إرسال رابط استعادة كلمة المرور."""
    auth_service = AuthService(db)
    
    await auth_service.send_password_reset_email(email)
    
    return ResponseSchema(
        message="تم إرسال رابط استعادة كلمة المرور إلى بريدك الإلكتروني"
    )

@router.post(
    "/reset-password",
    response_model=ResponseSchema,
    summary="إعادة تعيين كلمة المرور"
)
async def reset_password(
    token: str,
    new_password: str = Field(..., min_length=8),
    db: Session = Depends(get_db)
):
    """إعادة تعيين كلمة المرور باستخدام رمز الاستعادة."""
    auth_service = AuthService(db)
    
    try:
        await auth_service.reset_password(token, new_password)
        return ResponseSchema(message="تم تغيير كلمة المرور بنجاح")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

### Analysis Endpoints:

```python
# app/api/v1/endpoints/analyze.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.analysis import (
    AnalysisRequestSchema,
    AnalysisResponseSchema,
    AnalysisResultSchema
)
from app.schemas.base import ResponseSchema, PaginatedResponseSchema
from app.services.analysis_service import AnalysisService
from app.dependencies import get_current_user_optional, get_current_user
from app.models.user import User
from app.core.cache import cache_manager

router = APIRouter(prefix="/analyze", tags=["Poetry Analysis"])

@router.post(
    "/",
    response_model=AnalysisResponseSchema,
    summary="تحليل النص الشعري"
)
async def analyze_poetry(
    analysis_request: AnalysisRequestSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    تحليل النص الشعري لتحديد البحر والتفاعيل.
    
    - **text**: النص الشعري (مطلوب)
    - **options**: خيارات التحليل (اختيارية)
    
    Returns:
    - التقطيع العروضي
    - البحر المكتشف مع مستوى الثقة
    - تقييم جودة البيت
    - اقتراحات للتحسين
    """
    analysis_service = AnalysisService(db)
    
    try:
        # Check cache first
        cache_key = analysis_service.generate_cache_key(
            analysis_request.text,
            analysis_request.options
        )
        
        cached_result = await cache_manager.get(cache_key)
        if cached_result:
            return AnalysisResponseSchema(data=cached_result)
        
        # Perform analysis
        result = await analysis_service.analyze_text(
            text=analysis_request.text,
            options=analysis_request.options,
            user_id=current_user.id if current_user else None
        )
        
        # Cache result
        background_tasks.add_task(
            cache_manager.set,
            cache_key,
            result,
            expire=3600  # 1 hour
        )
        
        # Save to history (if user is logged in)
        if current_user:
            background_tasks.add_task(
                analysis_service.save_to_history,
                result,
                current_user.id
            )
        
        return AnalysisResponseSchema(data=result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في التحليل: {str(e)}"
        )

@router.get(
    "/history",
    response_model=PaginatedResponseSchema,
    summary="سجل التحليلات السابقة"
)
async def get_analysis_history(
    page: int = 1,
    per_page: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """الحصول على سجل التحليلات السابقة للمستخدم."""
    analysis_service = AnalysisService(db)
    
    result = await analysis_service.get_user_analysis_history(
        user_id=current_user.id,
        page=page,
        per_page=per_page
    )
    
    return result

@router.get(
    "/history/{analysis_id}",
    response_model=AnalysisResponseSchema,
    summary="تحليل محدد من السجل"
)
async def get_analysis_by_id(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """الحصول على تحليل محدد من السجل."""
    analysis_service = AnalysisService(db)
    
    result = await analysis_service.get_analysis_by_id(
        analysis_id=analysis_id,
        user_id=current_user.id
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="التحليل المطلوب غير موجود"
        )
    
    return AnalysisResponseSchema(data=result)

@router.delete(
    "/history/{analysis_id}",
    response_model=ResponseSchema,
    summary="حذف تحليل من السجل"
)
async def delete_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """حذف تحليل محدد من السجل."""
    analysis_service = AnalysisService(db)
    
    success = await analysis_service.delete_analysis(
        analysis_id=analysis_id,
        user_id=current_user.id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="التحليل المطلوب غير موجود"
        )
    
    return ResponseSchema(message="تم حذف التحليل بنجاح")

@router.post(
    "/batch",
    response_model=List[AnalysisResponseSchema],
    summary="تحليل متعدد للنصوص"
)
async def analyze_multiple_texts(
    texts: List[str] = Field(..., max_items=10),
    analysis_options: AnalysisOptionsSchema = AnalysisOptionsSchema(),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """تحليل عدة نصوص شعرية في طلب واحد (حد أقصى 10 نصوص)."""
    analysis_service = AnalysisService(db)
    
    results = []
    for text in texts:
        request = AnalysisRequestSchema(text=text, options=analysis_options)
        try:
            result = await analysis_service.analyze_text(
                text=text,
                options=analysis_options,
                user_id=current_user.id if current_user else None
            )
            results.append(AnalysisResponseSchema(data=result))
        except Exception as e:
            results.append(
                AnalysisResponseSchema(
                    success=False,
                    data=None,
                    error={"message": str(e)}
                )
            )
    
    return results

@router.get(

---

## 📈 المراقبة والت計يس (Instrumentation)

لتمكين لوحات Prometheus/Grafana المذكورة في `PERFORMANCE_TARGETS.md`، أضف أداة `prometheus-fastapi-instrumentator` إلى تطبيق FastAPI.

### التثبيت (dev/prod):

```bash
pip install prometheus-fastapi-instrumentator==6.1.0
```

### التفعيل في `app/main.py`:

```python
# app/main.py (excerpt)
from prometheus_fastapi_instrumentator import Instrumentator

def setup_metrics(app: FastAPI) -> None:
    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
    ).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

def create_app() -> FastAPI:
    app = FastAPI(...)
    setup_middleware(app)
    app.include_router(api_router, prefix="/api/v1")
    setup_exception_handlers(app)
    setup_events(app)
    setup_metrics(app)  # <- expose /metrics
    return app
```

سيبدأ Prometheus بسحب المقاييس من `backend:8000/metrics` كما هو موثق.

---

## ⏱️ مهلة التحليل وحدود الطلب (Timeouts & Limits)

- مهلة تحليل البيت الواحد (Hard Limit): 5 ثوانٍ. عند تجاوزها، نرجع نتيجة "fallback/basic" مع رسالة ودية، ونُسجّل الحدث للمراقبة.
- حدود حجم الطلب: 100KB كحد أقصى لـ JSON body في `/analyze` لمنع إساءة الاستخدام وتقليل زمن التحليل.

### تطبيق مهلة التحليل (مثال):

```python
# app/services/analysis_service.py (excerpt)
import asyncio

ANALYSIS_TIMEOUT_SECONDS = 5

async def analyze_text(self, text: str, options: AnalysisOptionsSchema, user_id: int | None = None):
    async def _run():
        return self._analyzer.analyze(text, options)

    try:
        result = await asyncio.wait_for(_run(), timeout=ANALYSIS_TIMEOUT_SECONDS)
    except asyncio.TimeoutError:
        # graceful fallback
        result = self._fallback_analyzer.basic(text)
        result["warning"] = "timeout_fallback"
    return result
```

### تحديد حجم الطلب (ASGI Middleware بسيط):

```python
# app/api/middleware/request_size.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class MaxBodySizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_body_size: int = 100 * 1024):
        super().__init__(app)
        self.max_body_size = max_body_size

    async def dispatch(self, request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_body_size:
            return JSONResponse(status_code=413, content={
                "success": False,
                "error": {"code": "PAYLOAD_TOO_LARGE", "message": "الحجم الأقصى للطلب 100KB"}
            })
        return await call_next(request)

# in setup_middleware(app):
# app.add_middleware(MaxBodySizeMiddleware, max_body_size=100*1024)
```

---

## 🔐 قائمة أمان مختصرة (MVP Security Checklist)

- تفعيل CORS لبيئات الإنتاج فقط (Origins محددة).  
- تحديد حجم الـ body (100KB) ووقت التحليل (≤ 5s) كما أعلاه.  
- تفعيل Security Headers (HSTS, X-Content-Type-Options, X-Frame-Options).  
- استخدام JWT مع مدة صلاحية قصيرة للوصول وتجديد عبر refresh.  
- تسجيل جميع أخطاء 5xx مع request_id، وربطها بلوحة Grafana/تنبيهات.  
- تحديد معدل الطلبات (Redis) كما وثّقنا: 100 طلب/ساعة لكل IP.  
- تعطيل Swagger/OpenAPI في الإنتاج أو خلف auth.  
- تشفير متغيرات البيئة/الأسرار وإدارتها خارج المستودع.

انظر أيضًا: `ERROR_HANDLING_STRATEGY.md` و`PERFORMANCE_TARGETS.md` و`docs/technical/MONITORING_INTEGRATION.md`.
    "/stats",
    summary="إحصائيات التحليلات"
)
async def get_analysis_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """إحصائيات تحليلات المستخدم."""
    analysis_service = AnalysisService(db)
    
    stats = await analysis_service.get_user_analysis_stats(current_user.id)
    
    return ResponseSchema(data=stats)
```

---

## 🧪 Testing Strategy

### Test Configuration:

```python
# tests/conftest.py
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import get_db
from app.db.base import Base
from app.config import settings
from app.core.auth.jwt_handler import JWTHandler

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def db_session():
    """Create test database session."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop tables
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    """Create test client with database dependency override."""
    def get_test_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = get_test_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user_data():
    """Test user data."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }

@pytest.fixture
def authenticated_client(client, test_user_data, db_session):
    """Create authenticated test client."""
    # Register user
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 201
    
    # Login user
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    
    token_data = response.json()
    access_token = token_data["access_token"]
    
    # Set authorization header
    client.headers = {"Authorization": f"Bearer {access_token}"}
    
    return client
```

### API Tests:

```python
# tests/test_api/test_auth.py
import pytest
from fastapi import status

class TestAuthEndpoints:
    """Test authentication endpoints."""
    
    def test_register_user_success(self, client, test_user_data):
        """Test successful user registration."""
        response = client.post("/api/v1/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["success"] is True
        assert "user_id" in data["data"]
    
    def test_register_user_duplicate_email(self, client, test_user_data):
        """Test registration with duplicate email."""
        # Register first user
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Try to register with same email
        response = client.post("/api/v1/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_login_success(self, client, test_user_data):
        """Test successful login."""
        # Register user first
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Login
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client, test_user_data):
        """Test login with invalid credentials."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user(self, authenticated_client):
        """Test getting current user info."""
        response = authenticated_client.get("/api/v1/auth/me")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "username" in data
        assert "email" in data

# tests/test_api/test_analyze.py
import pytest
from fastapi import status

class TestAnalysisEndpoints:
    """Test poetry analysis endpoints."""
    
    @pytest.fixture
    def analysis_request(self):
        """Sample analysis request."""
        return {
            "text": "قفا نبك من ذكرى حبيب ومنزل",
            "options": {
                "remove_diacritics": True,
                "analysis_mode": "accurate",
                "return_alternatives": True
            }
        }
    
    def test_analyze_poetry_success(self, client, analysis_request):
        """Test successful poetry analysis."""
        response = client.post("/api/v1/analyze/", json=analysis_request)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["success"] is True
        assert "data" in data
        
        result = data["data"]
        assert "prosodic_analysis" in result
        assert "meter_detection" in result
        assert "quality_score" in result
    
    def test_analyze_poetry_invalid_text(self, client):
        """Test analysis with invalid text."""
        request = {
            "text": "",  # Empty text
            "options": {}
        }
        response = client.post("/api/v1/analyze/", json=request)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_analysis_history_authenticated(self, authenticated_client, analysis_request):
        """Test getting analysis history for authenticated user."""
        # Perform analysis first
        authenticated_client.post("/api/v1/analyze/", json=analysis_request)
        
        # Get history
        response = authenticated_client.get("/api/v1/analyze/history")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
    
    def test_get_analysis_history_unauthenticated(self, client):
        """Test getting analysis history without authentication."""
        response = client.get("/api/v1/analyze/history")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_batch_analysis(self, client):
        """Test batch analysis of multiple texts."""
        request = {
            "texts": [
                "قفا نبك من ذكرى حبيب ومنزل",
                "ألا في سبيل المجد ما أنا فاعل"
            ],
            "analysis_options": {
                "analysis_mode": "fast"
            }
        }
        response = client.post("/api/v1/analyze/batch", json=request)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2  # Two results
```

---

## 📈 Performance & Monitoring

### Response Time Monitoring:

```python
# app/api/middleware/logging.py
import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging and timing."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_ip": request.client.host
            }
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log response
        logger.info(
            f"Response: {response.status_code} in {process_time:.4f}s",
            extra={
                "status_code": response.status_code,
                "process_time": process_time,
                "path": request.url.path
            }
        )
        
        # Alert on slow requests
        if process_time > 5.0:  # 5 seconds
            logger.warning(
                f"Slow request detected: {request.url.path} took {process_time:.2f}s"
            )
        
        return response
```

### Health Check Endpoint:

```python
# app/api/v1/endpoints/health.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
import time
import psutil
import redis

from app.db.session import get_db
from app.config import settings

router = APIRouter(prefix="/health", tags=["Health Check"])

@router.get("/", summary="Health Check")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.VERSION
    }

@router.get("/detailed", summary="Detailed Health Check")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with dependencies."""
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.VERSION,
        "checks": {}
    }
    
    # Database check
    try:
        db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database error: {str(e)}"
        }
        health_status["status"] = "unhealthy"
    
    # Redis check
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        redis_client.ping()
        health_status["checks"]["redis"] = {
            "status": "healthy",
            "message": "Redis connection successful"
        }
    except Exception as e:
        health_status["checks"]["redis"] = {
            "status": "unhealthy",
            "message": f"Redis error: {str(e)}"
        }
        health_status["status"] = "unhealthy"
    
    # System resources
    health_status["checks"]["system"] = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }
    
    status_code = status.HTTP_200_OK if health_status["status"] == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return health_status
```

---

## 🎯 Next Steps

مع إكمال Backend API Documentation، المطلوب التالي:

1. **[Database Design Document](DATABASE_SCHEMA.md)** - تصميم قاعدة البيانات المفصل
2. **[Development Workflow Guide](DEVELOPMENT_WORKFLOW.md)** - Git workflow والاختبارات
3. **[Arabic NLP Research](ARABIC_NLP_RESEARCH.md)** - مراجع وتطبيق

---

## 📝 ملاحظات مهمة

### أولويات التطوير:
1. **Authentication أولاً** - نظام آمن وموثوق
2. **Analysis API** - المحرك الأساسي للمشروع  
3. **Validation دقيقة** - منع الأخطاء مبكراً
4. **Testing شامل** - ضمان الجودة والاستقرار
5. **Monitoring مستمر** - تتبع الأداء والمشاكل

### Best Practices:
- **استخدام Dependency Injection** لسهولة الاختبار
- **Error Handling موحد** عبر النظام  
- **Logging مفصل** لتسهيل التتبع
- **Rate Limiting** لحماية الـ API
- **Documentation تلقائية** مع Swagger

---

**🔌 هذا يكمل دليل Backend API - الأساس التقني القوي للمشروع!**