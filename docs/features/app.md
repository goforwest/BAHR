# BAHR Application Guide - End-to-End Architecture

**Document Type:** Top-Level Application Guide  
**Status:** Production-Ready  
**Last Updated:** November 8, 2025  
**Version:** 1.0.0

---

## Executive Summary

**BAHR** (بَحْر - Arabic for "poetic meter") is an AI-powered platform for analyzing Classical Arabic poetry prosody. The MVP focuses on **prosodic analysis** - detecting meters (البحور الشعرية), identifying syllable patterns (التقطيع), and providing quality feedback.

### What BAHR Does
- **Analyzes** Arabic verse to detect Classical meters (16 بحور)
- **Segments** text into prosodic syllables using morphological analysis
- **Scores** confidence and quality of meter detection
- **Provides** educational feedback for students and poets
- **Caches** results for performance (<600ms P95 latency)

### MVP Scope (Weeks 1-6)
✅ Verse analysis API (REST)  
✅ User authentication (JWT)  
✅ PostgreSQL + Redis infrastructure  
✅ Next.js frontend with RTL support  
✅ Rate limiting (100 req/hr guests, 1000 req/hr authenticated)  
✅ Prometheus monitoring  

🔮 **Deferred to Phase 2:** AI poetry generation, social features, competitions

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Technology Stack](#2-technology-stack)
3. [Directory Structure](#3-directory-structure)
4. [Interface Contracts](#4-interface-contracts)
5. [Environment Configuration](#5-environment-configuration)
6. [Local Development Setup](#6-local-development-setup)
7. [Testing Strategy](#7-testing-strategy)
8. [Deployment Pipeline](#8-deployment-pipeline)
9. [Monitoring & Observability](#9-monitoring--observability)
10. [Troubleshooting Playbook](#10-troubleshooting-playbook)

---

## 1. System Architecture

### 1.1 High-Level Component Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         BAHR System Architecture                     │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐
│          Client Layer                │
│  ┌────────────┐  ┌────────────┐     │
│  │  Next.js   │  │   Mobile   │     │
│  │  Web App   │  │  (Phase 2) │     │
│  │  (React)   │  │            │     │
│  └─────┬──────┘  └─────┬──────┘     │
└────────┼────────────────┼─────────────┘
         │                │
         │  HTTPS/REST    │
         └────────┬───────┘
                  │
┌─────────────────▼────────────────────────────────────────────────────┐
│                 API Gateway (FastAPI)                                │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Middleware Stack:                                           │   │
│  │  • RequestIDMiddleware (X-Request-ID)                        │   │
│  │  • ResponseEnvelopeMiddleware (success/error/meta)           │   │
│  │  • RateLimitMiddleware (Redis sliding window)                │   │
│  │  • AuthMiddleware (JWT Bearer token)                         │   │
│  │  • MetricsMiddleware (Prometheus)                            │   │
│  │  • ExceptionHandlerMiddleware (ERR_* codes)                  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  API Routes (/api/v1):                                       │   │
│  │  • POST /auth/register, /login, /refresh                     │   │
│  │  • POST /analyses (create analysis)                          │   │
│  │  • GET  /analyses (list user analyses)                       │   │
│  │  • GET  /analyses/{id} (retrieve analysis)                   │   │
│  │  • GET  /meters (list all meters)                            │   │
│  │  • GET  /health, /health/detailed                            │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────┬───────────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌─────▼──────┐ ┌────▼─────────┐
│  Prosody     │ │   User     │ │   Cache      │
│  Engine      │ │  Service   │ │  Service     │
│              │ │            │ │              │
│ ┌──────────┐ │ │ ┌────────┐ │ │ ┌──────────┐ │
│ │Normalizer│ │ │ │ Auth   │ │ │ │  Redis   │ │
│ │Segmenter │ │ │ │ CRUD   │ │ │ │  Client  │ │
│ │Detector  │ │ │ │ Profile│ │ │ │  (Cache) │ │
│ └──────────┘ │ │ └────────┘ │ │ └──────────┘ │
└───────┬──────┘ └─────┬──────┘ └────┬─────────┘
        │              │              │
┌───────▼──────────────▼──────────────▼─────────┐
│          Data & Cache Layer                   │
│  ┌──────────────┐  ┌──────────────┐          │
│  │ PostgreSQL   │  │   Redis 7    │          │
│  │   Database   │  │              │          │
│  │   (15.x)     │  │ • Cache      │          │
│  │              │  │ • Rate Limit │          │
│  │ Tables:      │  │ • Sessions   │          │
│  │ • users      │  │              │          │
│  │ • analyses   │  │ TTL: 24h     │          │
│  │ • meters     │  └──────────────┘          │
│  └──────────────┘                            │
└───────────────────────────────────────────────┘

┌───────────────────────────────────────────────┐
│       Monitoring & Observability              │
│  ┌──────────────┐  ┌──────────────┐          │
│  │ Prometheus   │  │   Grafana    │          │
│  │ (Metrics)    │  │ (Dashboards) │          │
│  └──────────────┘  └──────────────┘          │
└───────────────────────────────────────────────┘
```

### 1.2 Request Flow (Analysis Endpoint)

```
Client Request: POST /api/v1/analyses
    │
    │ {"text": "أَلا عِم صَباحاً أَيُّها الطَلَلُ البالي"}
    │
    ▼
┌──────────────────────────────────────┐
│ 1. RequestIDMiddleware               │
│    • Extract X-Request-ID header     │
│    • Generate UUID if missing        │
│    • Store in request.state          │
└──────────┬───────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│ 2. RateLimitMiddleware               │
│    • Check Redis ZSET for IP/user    │
│    • Increment counter               │
│    • Return 429 if exceeded          │
└──────────┬───────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│ 3. AuthMiddleware (Optional)         │
│    • Verify JWT Bearer token         │
│    • Decode user_id                  │
│    • Attach user to request          │
└──────────┬───────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│ 4. Route Handler                     │
│    • Validate input (Pydantic)       │
│    • Call AnalysisService            │
└──────────┬───────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│ 5. AnalysisService.analyze()         │
│    ┌────────────────────────────┐   │
│    │ a) Normalize text          │   │
│    │    (8-stage pipeline)      │   │
│    └──────────┬─────────────────┘   │
│               ▼                      │
│    ┌────────────────────────────┐   │
│    │ b) Check cache (Redis)     │   │
│    │    key = SHA256(normalized)│   │
│    │    HIT → return cached     │   │
│    │    MISS → continue         │   │
│    └──────────┬─────────────────┘   │
│               ▼                      │
│    ┌────────────────────────────┐   │
│    │ c) Syllable Segmentation   │   │
│    │    (CAMeL Tools)           │   │
│    │    Result: ["فَ","عُو","لُن"]│ │
│    └──────────┬─────────────────┘   │
│               ▼                      │
│    ┌────────────────────────────┐   │
│    │ d) Meter Detection         │   │
│    │    • Pattern matching      │   │
│    │    • Fuzzy with Levenshtein│   │
│    │    • Confidence scoring    │   │
│    │    Result: "الطويل", 0.92  │   │
│    └──────────┬─────────────────┘   │
│               ▼                      │
│    ┌────────────────────────────┐   │
│    │ e) Save to cache (24h TTL) │   │
│    │ f) Persist to DB (if user) │   │
│    │ g) Emit metrics            │   │
│    └────────────────────────────┘   │
└──────────┬───────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│ 6. ResponseEnvelopeMiddleware        │
│    • Wrap in envelope                │
│    • Add meta (request_id, timestamp)│
│    • Calculate processing_time_ms    │
└──────────┬───────────────────────────┘
           ▼
JSON Response:
{
  "success": true,
  "data": {
    "id": "uuid",
    "text": "أَلا عِم صَباحاً...",
    "normalized_text": "الا عم صباحا...",
    "pattern": "//0/0 //0/0 //0/0 //0/0",
    "detected_meter": "الطويل",
    "confidence": 0.92,
    "syllable_count": 16,
    "processing_time_ms": 245
  },
  "error": null,
  "meta": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-11-08T12:00:00Z",
    "version": "1.0.0",
    "processing_time_ms": 245,
    "cached": false
  }
}
```

---

## 2. Technology Stack

### 2.1 Backend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Language** | Python | 3.11+ | Type safety, async support |
| **Framework** | FastAPI | 0.104.1 | REST API, auto docs, async |
| **ORM** | SQLAlchemy | 2.0.23 | Database abstraction |
| **Migrations** | Alembic | 1.12.1 | Schema versioning |
| **Validation** | Pydantic | 2.5.0 | Request/response schemas |
| **Auth** | python-jose | 3.3.0 | JWT encoding/decoding |
| **Passwords** | passlib[bcrypt] | 1.7.4 | Password hashing (cost=12) |
| **Cache/Queue** | redis | 5.0.1 | Caching + rate limiting |
| **DB Driver** | psycopg2-binary | 2.9.9 | PostgreSQL connector |
| **Testing** | pytest | 7.4.3 | Unit/integration tests |
| **Coverage** | pytest-cov | 4.1.0 | Code coverage (≥70%) |
| **Linting** | ruff | 0.1.6 | Fast Python linter |
| **Type Checking** | mypy | 1.7.1 | Static type checking |
| **Server** | uvicorn | 0.24.0 | ASGI server |
| **Metrics** | prometheus-client | 0.19.0 | Metrics collection |

### 2.2 Arabic NLP Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Morphology** | CAMeL Tools | 1.5.2 | Morphological analysis |
| **Arabic Utils** | PyArabic | 0.6.15 | Text normalization |
| **Fuzzy Matching** | python-Levenshtein | 0.21.1 | Pattern similarity |

### 2.3 Frontend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | Next.js | 14.0.0 | React framework, SSR/SSG |
| **Language** | TypeScript | 5.3.0 | Type safety |
| **UI Library** | Tailwind CSS | 3.3.0 | Utility-first CSS |
| **State** | TanStack Query | 5.8.0 | Server state management |
| **Forms** | React Hook Form | 7.48.0 | Form validation |
| **HTTP Client** | axios | 1.6.0 | API requests |
| **Font** | Tajawal (Google) | - | Arabic font (RTL) |

### 2.4 Infrastructure

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Database** | PostgreSQL | 15.x | Primary data store |
| **Cache** | Redis | 7.x | Caching + rate limiting |
| **Containers** | Docker | 24.x | Containerization |
| **Orchestration** | Docker Compose | 2.x | Local development |
| **CI/CD** | GitHub Actions | - | Automated testing/deployment |
| **Monitoring** | Prometheus | 2.x | Metrics collection |
| **Dashboards** | Grafana | 10.x | Metrics visualization |
| **Backend Host** | Railway | - | Managed hosting |
| **Frontend Host** | Vercel | - | Next.js deployment |

---

## 3. Directory Structure

### 3.1 Complete Project Layout

```
BAHR/
├── .github/
│   └── workflows/
│       ├── ci-cd.yml              # Main CI/CD pipeline
│       ├── backend-tests.yml      # Backend test workflow
│       ├── frontend-tests.yml     # Frontend test workflow
│       └── dataset-validation.yml # Dataset validation
│
├── backend/                       # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI app entry ✅
│   │   ├── response_envelope.py  # Response wrapper ✅
│   │   │
│   │   ├── api/                  # API routes
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── routes/
│   │   │       │   ├── auth.py   # POST /register, /login
│   │   │       │   ├── analyses.py # POST /analyses
│   │   │       │   ├── users.py  # GET /me
│   │   │       │   ├── meters.py # GET /meters
│   │   │       │   └── health.py # GET /health
│   │   │
│   │   ├── core/                 # Core utilities
│   │   │   ├── __init__.py
│   │   │   ├── config.py         # Settings (BaseSettings)
│   │   │   ├── security.py       # JWT, password hashing
│   │   │   ├── exceptions.py     # Custom exceptions
│   │   │   ├── error_codes.py    # ERR_* catalog
│   │   │   ├── logging_config.py # Structured logging
│   │   │   └── retry.py          # Retry logic
│   │   │
│   │   ├── db/                   # Database layer
│   │   │   ├── __init__.py
│   │   │   ├── base.py           # SQLAlchemy base
│   │   │   └── session.py        # Session management
│   │   │
│   │   ├── models/               # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # User, UserProfile
│   │   │   ├── analysis.py       # Analysis, Meter
│   │   │   └── base.py           # Base model mixins
│   │   │
│   │   ├── schemas/              # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # UserCreate, UserPublic
│   │   │   ├── analysis.py       # AnalysisRequest, AnalysisResult
│   │   │   ├── envelope.py       # ResponseEnvelope
│   │   │   └── dataset.py        # DatasetEntry
│   │   │
│   │   ├── services/             # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── analysis_service.py
│   │   │   ├── cache_service.py
│   │   │   └── rate_limit_service.py
│   │   │
│   │   ├── repositories/         # Data access layer
│   │   │   ├── __init__.py
│   │   │   ├── user_repository.py
│   │   │   └── analysis_repository.py
│   │   │
│   │   ├── prosody/              # Prosody engine ✅
│   │   │   ├── __init__.py
│   │   │   ├── engine.py         # Main orchestrator
│   │   │   ├── normalizer.py     # 8-stage normalization ✅
│   │   │   ├── segmenter.py      # Syllable segmentation ✅
│   │   │   └── detector.py       # Meter detection
│   │   │
│   │   ├── nlp/                  # NLP utilities
│   │   │   ├── __init__.py
│   │   │   └── arabic_utils.py   # Arabic text helpers
│   │   │
│   │   ├── middleware/           # FastAPI middleware
│   │   │   ├── __init__.py
│   │   │   ├── response_envelope.py ✅
│   │   │   ├── util_request_id.py ✅
│   │   │   ├── rate_limit.py
│   │   │   ├── auth.py
│   │   │   └── exception_handler.py
│   │   │
│   │   └── metrics/              # Prometheus metrics
│   │       ├── __init__.py
│   │       ├── analysis_metrics.py ✅
│   │       └── database_metrics.py
│   │
│   ├── alembic/                  # Database migrations
│   │   ├── versions/
│   │   │   └── 001_initial_schema.py
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── scripts/                  # Utility scripts
│   │   ├── validate_dataset.py
│   │   ├── import_dataset.py
│   │   └── export_dataset.py
│   │
│   ├── tests/                    # Test suite
│   │   ├── __init__.py
│   │   ├── conftest.py           # Pytest fixtures
│   │   ├── unit/
│   │   │   ├── test_normalizer.py
│   │   │   ├── test_segmenter.py
│   │   │   ├── test_detector.py
│   │   │   ├── test_exceptions.py
│   │   │   └── test_response_envelope.py
│   │   ├── integration/
│   │   │   ├── test_api_auth.py
│   │   │   ├── test_api_analysis.py
│   │   │   ├── test_database.py
│   │   │   └── test_envelope_middleware.py
│   │   └── e2e/
│   │       └── test_analysis_flow.py
│   │
│   ├── Dockerfile                # Multi-stage Docker build
│   ├── requirements.txt          # Python dependencies
│   ├── alembic.ini               # Alembic configuration
│   ├── railway.toml              # Railway deployment config
│   └── .env.example              # Environment variables template
│
├── frontend/                     # Next.js frontend
│   ├── app/
│   │   ├── layout.tsx            # Root layout (RTL)
│   │   ├── page.tsx              # Home page
│   │   ├── providers.tsx         # TanStack Query provider
│   │   ├── analyze/
│   │   │   └── page.tsx          # Analysis page
│   │   └── auth/
│   │       ├── login/page.tsx
│   │       └── register/page.tsx
│   │
│   ├── components/
│   │   ├── ui/                   # UI primitives
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Card.tsx
│   │   ├── VerseInputForm.tsx
│   │   ├── AnalysisResults.tsx
│   │   └── MeterVisualization.tsx
│   │
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts         # Axios instance
│   │   │   └── types.ts          # TypeScript types
│   │   └── utils/
│   │       └── rtl.ts            # RTL helpers
│   │
│   ├── hooks/
│   │   ├── useAnalysis.ts        # TanStack Query hook
│   │   └── useAuth.ts
│   │
│   ├── styles/
│   │   └── globals.css           # Tailwind CSS
│   │
│   ├── public/
│   │   └── fonts/                # Arabic fonts
│   │
│   ├── __tests__/
│   │   └── components/
│   │       └── VerseInputForm.test.tsx
│   │
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── vercel.json               # Vercel deployment config
│   └── .env.example
│
├── dataset/                      # Training/evaluation data
│   └── evaluation/
│       └── golden_set_v0_20.jsonl # 20 verified verses
│
├── docs/                         # Documentation (42 files)
│   ├── START_HERE.md
│   ├── START_HERE_DEVELOPER.md
│   ├── README.md
│   ├── phases/
│   │   ├── PHASE_0_SETUP.md
│   │   └── PHASE_1_MVP.md
│   ├── planning/
│   │   ├── PROJECT_TIMELINE.md
│   │   ├── DEFERRED_FEATURES.md
│   │   └── NON_GOALS.md
│   ├── research/
│   │   ├── ARABIC_NLP_RESEARCH.md
│   │   ├── DATASET_SPEC.md
│   │   └── TESTING_DATASETS.md
│   ├── technical/
│   │   ├── ARCHITECTURE_OVERVIEW.md ✅
│   │   ├── API_SPECIFICATION.yaml
│   │   ├── DATABASE_SCHEMA.md
│   │   ├── PROSODY_ENGINE.md
│   │   ├── ERROR_HANDLING_STRATEGY.md
│   │   ├── SECURITY.md
│   │   ├── DEPLOYMENT_GUIDE.md
│   │   ├── MONITORING_INTEGRATION.md
│   │   ├── PERFORMANCE_TARGETS.md
│   │   └── METRICS_REFERENCE.md
│   └── workflows/
│       └── DEVELOPMENT_WORKFLOW.md
│
├── implementation-guides/        # 14 feature guides + app.md
│   ├── README.md
│   ├── app.md                    # ← This document
│   ├── feature-authentication-jwt.md
│   ├── feature-arabic-text-normalization.md
│   ├── feature-syllable-segmentation.md
│   ├── feature-meter-detection.md
│   ├── feature-analysis-api.md
│   ├── feature-caching-redis.md
│   ├── feature-rate-limiting.md
│   ├── feature-monitoring-observability.md
│   ├── feature-database-orm.md
│   ├── feature-response-envelope.md
│   ├── feature-error-handling.md
│   ├── feature-frontend-nextjs.md
│   ├── feature-dataset-management.md
│   └── feature-deployment-cicd.md
│
├── docker-compose.yml            # Local dev environment ✅
├── .gitignore
├── .pre-commit-config.yaml
├── README.md
├── CONTRIBUTING.md
├── docs/vision/MASTER_PLAN.md   # Product vision
└── docs/project-management/PROGRESS_LOG_CURRENT.md
```

---

## 4. Interface Contracts

### 4.1 Core Interfaces (Python Protocols)

```python
# backend/app/prosody/interfaces.py
"""
Interface contracts for prosody engine components.

Source: docs/technical/ARCHITECTURE_OVERVIEW.md:89-147
"""

from typing import Protocol, List
from dataclasses import dataclass


@dataclass
class Syllable:
    """Prosodic syllable representation."""
    text: str              # Original text (e.g., "فَعُو")
    phonetic: str          # Phonetic form (e.g., "fa3ū")
    pattern: str           # CV pattern (e.g., "CVV")
    position: int          # Position in verse
    is_long: bool          # Long (CVV/CVC) vs short (CV)


@dataclass
class ProsodyPattern:
    """Prosodic pattern of verse."""
    syllables: List[Syllable]
    pattern_string: str    # E.g., "//0/0 //0/0 //0/0 //0/0"
    taqti3: str           # E.g., "فعولن مفاعيلن فعولن مفاعيلن"


@dataclass
class MeterResult:
    """Meter detection result."""
    meter: str            # E.g., "الطويل"
    confidence: float     # 0.0 - 1.0
    alternatives: List[tuple[str, float]]  # [(meter, confidence), ...]
    zihafat: List[str]    # Applied variations


class ITextNormalizer(Protocol):
    """
    Text normalization interface.
    
    Responsibility: Clean and normalize Arabic text without
    changing semantic meaning.
    """
    
    def normalize(self, text: str) -> str:
        """
        Normalize Arabic text.
        
        Stages:
        1. Unicode normalization (NFKC)
        2. Remove tatweel (ـ)
        3. Normalize alef variants (أ، إ، آ → ا)
        4. Normalize yaa/alef maqsura (ي، ى)
        5. Normalize hamza variants
        6. Remove/normalize tashkeel
        7. Remove non-Arabic characters
        8. Normalize whitespace
        
        Args:
            text: Raw Arabic text
        
        Returns:
            Normalized text
        """
        ...


class ISyllableSegmenter(Protocol):
    """
    Syllable segmentation interface.
    
    Responsibility: Convert normalized text to prosodic syllables.
    """
    
    def segment(self, text: str) -> List[Syllable]:
        """
        Segment text into prosodic syllables.
        
        Process:
        1. Morphological analysis (CAMeL Tools)
        2. Phonetic transcription
        3. Syllable boundary detection
        4. CV pattern classification
        
        Args:
            text: Normalized Arabic text
        
        Returns:
            List of syllables
        """
        ...


class IMeterDetector(Protocol):
    """
    Meter detection interface.
    
    Responsibility: Identify Classical Arabic meter from syllable pattern.
    """
    
    def detect(self, pattern: ProsodyPattern) -> MeterResult:
        """
        Detect meter from prosodic pattern.
        
        Process:
        1. Extract pattern string
        2. Fuzzy match against 16 meters
        3. Apply zihafat (metrical variations)
        4. Score confidence
        5. Return top candidates
        
        Args:
            pattern: Prosodic pattern
        
        Returns:
            Meter detection result
        """
        ...


class ICacheService(Protocol):
    """
    Cache service interface.
    
    Responsibility: Store/retrieve analysis results.
    """
    
    def get(self, key: str) -> dict | None:
        """Retrieve from cache."""
        ...
    
    def set(self, key: str, value: dict, ttl: int) -> None:
        """Store in cache with TTL."""
        ...
    
    def delete(self, key: str) -> None:
        """Remove from cache."""
        ...


class IAnalysisService(Protocol):
    """
    Analysis service interface (orchestrator).
    
    Responsibility: Coordinate all analysis steps.
    """
    
    def analyze(
        self,
        text: str,
        user_id: int | None = None
    ) -> dict:
        """
        Full verse analysis pipeline.
        
        Steps:
        1. Normalize text
        2. Check cache
        3. Segment syllables
        4. Detect meter
        5. Cache result
        6. Persist (if authenticated)
        7. Emit metrics
        
        Args:
            text: Original verse text
            user_id: Optional user identifier
        
        Returns:
            Analysis result dict
        """
        ...
```

### 4.2 Database Models (SQLAlchemy)

```python
# Simplified model definitions

# User model
class User(Base):
    id: int
    username: str (unique)
    email: str (unique)
    password_hash: str
    full_name: str
    role: UserRole (enum)
    created_at: datetime

# Analysis model
class Analysis(Base):
    id: UUID
    user_id: int (nullable, FK)
    original_text: str
    normalized_text: str
    pattern: str
    detected_meter: str
    confidence: float
    syllable_count: int
    created_at: datetime
    metadata: JSONB

# Meter model (reference data)
class Meter(Base):
    id: int
    name_arabic: str
    name_english: str
    pattern: str
    description: str
    examples: JSONB
```

### 4.3 API Schemas (Pydantic)

```python
# Request/Response schemas

class AnalysisRequest(BaseModel):
    text: str = Field(min_length=5, max_length=1000)
    language: str = "ar"

class AnalysisResult(BaseModel):
    id: UUID
    text: str
    normalized_text: str
    pattern: str
    detected_meter: str
    confidence: float
    syllable_count: int
    processing_time_ms: int
    created_at: datetime

class ResponseEnvelope(BaseModel):
    success: bool
    data: Any | None
    error: ErrorResponse | None
    meta: ResponseMeta
```

---

## 5. Environment Configuration

### 5.1 Environment Variables Catalog

```bash
# backend/.env.example

# ===== Application =====
PROJECT_NAME=BAHR API
API_VERSION=1.0.0
ENVIRONMENT=development  # development | staging | production
DEBUG=false

# ===== Database =====
DATABASE_URL=postgresql://bahr_user:bahr_password@localhost:5432/bahr_db
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# ===== Redis =====
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_ANALYSIS=86400  # 24 hours
CACHE_TTL_METER=604800    # 7 days

# ===== Authentication =====
SECRET_KEY=your-secret-key-here-change-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# ===== Rate Limiting =====
RATE_LIMIT_GUEST=100           # Requests per hour (IP-based)
RATE_LIMIT_AUTHENTICATED=1000  # Requests per hour (user-based)
RATE_LIMIT_WINDOW_SECONDS=3600

# ===== CORS =====
ALLOWED_ORIGINS=http://localhost:3000,https://bahr.example.com

# ===== Monitoring =====
PROMETHEUS_ENABLED=true
LOG_LEVEL=INFO  # DEBUG | INFO | WARNING | ERROR | CRITICAL
SENTRY_DSN=     # Optional error tracking

# ===== NLP =====
NLP_ENABLE_MORPHOLOGY=true
NLP_CACHE_MORPHOLOGY=true

# ===== Features =====
MAINTENANCE_MODE=false
```

```bash
# frontend/.env.example

# ===== API =====
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_VERSION=1.0.0

# ===== Analytics (Optional) =====
NEXT_PUBLIC_GA_ID=
```

### 5.2 Configuration Loading

```python
# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    PROJECT_NAME: str = "BAHR API"
    API_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str
    CACHE_TTL_ANALYSIS: int = 86400
    
    # Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_GUEST: int = 100
    RATE_LIMIT_AUTHENTICATED: int = 1000
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
```

---

## 6. Local Development Setup

### 6.1 Prerequisites

```bash
# Required software
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (recommended)
```

### 6.2 Quick Start (Docker Compose)

```bash
# 1. Clone repository
git clone https://github.com/your-org/bahr.git
cd bahr

# 2. Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 3. Start all services
docker-compose up -d

# 4. Run database migrations
docker-compose exec backend alembic upgrade head

# 5. Import golden dataset (optional)
docker-compose exec backend python scripts/import_dataset.py \
  dataset/evaluation/golden_set_v0_20.jsonl

# 6. Access services
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Frontend: http://localhost:3000
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

### 6.3 Manual Setup (Without Docker)

```bash
# === Backend Setup ===
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL and Redis
brew services start postgresql@15  # macOS
brew services start redis

# Create database
createdb bahr_db

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# === Frontend Setup ===
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Access at http://localhost:3000
```

### 6.4 Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app --cov-report=term --cov-report=html

# Frontend tests
cd frontend
npm test

# E2E tests (requires services running)
cd backend
pytest tests/e2e/ -v
```

---

## 7. Testing Strategy

### 7.1 Test Pyramid

```
        ┌─────────────┐
        │     E2E     │  10% (Full analysis flow)
        │   (5 tests) │
        ├─────────────┤
        │ Integration │  30% (API endpoints, DB)
        │  (30 tests) │
        ├─────────────┤
        │    Unit     │  60% (Business logic, utils)
        │ (100 tests) │
        └─────────────┘
```

### 7.2 Coverage Targets

| Layer | Coverage Target | Test Types |
|-------|----------------|------------|
| **Prosody Engine** | ≥80% | Unit (normalizer, segmenter, detector) |
| **API Routes** | ≥75% | Integration (auth, analysis, meters) |
| **Services** | ≥80% | Unit (business logic) |
| **Repositories** | ≥70% | Integration (DB operations) |
| **Middleware** | ≥85% | Integration (envelope, rate limit, auth) |
| **Overall** | ≥70% | Mixed |

### 7.3 Test Examples

```python
# Unit test example
def test_normalize_text():
    normalizer = ArabicTextNormalizer()
    result = normalizer.normalize("أَلا عِم صَباحاً")
    assert result == "الا عم صباحا"

# Integration test example
def test_create_analysis_authenticated(client, auth_headers):
    response = client.post(
        "/api/v1/analyses",
        json={"text": "أَلا عِم صَباحاً أَيُّها الطَلَلُ البالي"},
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["detected_meter"] == "الطويل"
    assert data["confidence"] > 0.8

# E2E test example
def test_full_analysis_flow(client):
    # Register user
    register_response = client.post("/api/v1/auth/register", json={...})
    token = register_response.json()["data"]["access_token"]
    
    # Analyze verse
    analysis_response = client.post(
        "/api/v1/analyses",
        json={"text": "..."},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Retrieve analysis
    analysis_id = analysis_response.json()["data"]["id"]
    get_response = client.get(f"/api/v1/analyses/{analysis_id}")
    
    assert get_response.status_code == 200
```

---

## 8. Deployment Pipeline

### 8.1 CI/CD Workflow

```
┌──────────────────────────────────────────────────────────┐
│         GitHub Actions CI/CD Pipeline                    │
└──────────────────────────────────────────────────────────┘

Trigger: git push / pull request
    │
    ▼
┌──────────────────────────────────────┐
│ 1. Lint & Type Check                │
│    • ruff (backend)                  │
│    • mypy (backend)                  │
│    • eslint (frontend)               │
└──────────┬───────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│ 2. Run Tests                         │
│    • pytest (backend, ≥70% coverage) │
│    • jest (frontend)                 │
│    • Integration tests               │
└──────────┬───────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│ 3. Build Docker Image (main only)   │
│    • Multi-stage Dockerfile         │
│    • Push to Docker Hub             │
└──────────┬───────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│ 4. Deploy to Railway (backend)      │
│    • Auto-deploy on main push       │
│    • Health check verification      │
└──────────┬───────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│ 5. Deploy to Vercel (frontend)      │
│    • Auto-deploy on main push       │
│    • Preview deployments on PRs     │
└──────────────────────────────────────┘
```

### 8.2 Deployment Checklist

**Pre-Deployment**
- [ ] All tests passing (≥70% coverage)
- [ ] Linters passing (ruff, mypy, eslint)
- [ ] Environment variables set (Railway/Vercel)
- [ ] Database migrations ready
- [ ] SECRET_KEY rotated (if needed)
- [ ] Dependencies updated

**Backend (Railway)**
- [ ] PostgreSQL plugin configured
- [ ] Redis plugin configured
- [ ] Environment variables set
- [ ] Run `alembic upgrade head`
- [ ] Verify `/health` endpoint
- [ ] Check logs for errors

**Frontend (Vercel)**
- [ ] NEXT_PUBLIC_API_URL set
- [ ] Production domain configured
- [ ] SSL certificate active
- [ ] Verify RTL rendering
- [ ] Test API connectivity

**Post-Deployment**
- [ ] Run smoke tests
- [ ] Monitor error rates (Sentry)
- [ ] Check Prometheus metrics
- [ ] Verify P95 latency <600ms
- [ ] Test authentication flow
- [ ] Verify analysis accuracy

---

## 9. Monitoring & Observability

### 9.1 Key Metrics (Prometheus)

| Metric | Type | Description | SLO |
|--------|------|-------------|-----|
| `bahr_requests_total` | Counter | Total HTTP requests | - |
| `bahr_request_duration_seconds` | Histogram | Request latency | P95 <600ms |
| `verse_analysis_latency_seconds` | Histogram | Analysis processing time | P95 <600ms |
| `bahr_analysis_cache_hit_total` | Counter | Cache hits | >40% hit rate |
| `bahr_meter_confidence` | Gauge | Last confidence score | - |
| `bahr_errors_total` | Counter | Errors by code | <2% error rate |
| `analysis_timeouts_total` | Counter | Analysis timeouts | <0.1% |

### 9.2 Alert Rules

```yaml
# prometheus/alerts.yml
groups:
  - name: bahr_alerts
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: rate(bahr_errors_total[5m]) > 0.05
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
      
      # High latency
      - alert: HighLatency
        expr: histogram_quantile(0.95, bahr_request_duration_seconds) > 0.8
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "P95 latency exceeds 800ms"
      
      # Cache inefficiency
      - alert: LowCacheHitRate
        expr: rate(bahr_analysis_cache_hit_total[1h]) < 0.25
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "Cache hit rate below 25%"
```

### 9.3 Structured Logging

```python
# Log format (JSON)
{
  "timestamp": "2025-11-08T12:00:00Z",
  "level": "INFO",
  "logger": "app.api.v1.routes.analyses",
  "message": "Analysis completed",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": 123,
  "meter": "الطويل",
  "confidence": 0.92,
  "processing_time_ms": 245,
  "cached": false
}
```

---

## 10. Troubleshooting Playbook

### 10.1 Common Issues

#### Issue: High Latency (P95 >600ms)

**Symptoms:**
- Prometheus alert: HighLatency
- Slow API responses
- User complaints

**Diagnosis:**
```bash
# Check Prometheus metrics
curl http://localhost:9090/api/v1/query?query=histogram_quantile(0.95,bahr_request_duration_seconds)

# Check slow queries (PostgreSQL)
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;

# Check Redis latency
redis-cli --latency
```

**Solutions:**
1. **Cache:** Increase cache TTL, verify hit rate
2. **Database:** Add indexes, optimize queries
3. **NLP:** Reduce morphological analysis scope
4. **Horizontal scaling:** Add more Railway instances

#### Issue: Low Cache Hit Rate (<40%)

**Symptoms:**
- Prometheus alert: LowCacheHitRate
- Increased database load
- High CPU usage

**Diagnosis:**
```bash
# Check cache statistics
redis-cli INFO stats

# Check cache keys
redis-cli KEYS analysis:*
```

**Solutions:**
1. **Normalization:** Ensure consistent text normalization
2. **TTL:** Increase cache TTL from 24h to 48h
3. **Eviction:** Check Redis memory limit, adjust `maxmemory-policy`

#### Issue: Authentication Failures

**Symptoms:**
- 401 Unauthorized responses
- "ERR_AUTH_101" (token expired)
- "ERR_AUTH_102" (invalid token)

**Diagnosis:**
```bash
# Check JWT configuration
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'

# Verify token
python -c "from jose import jwt; print(jwt.decode('TOKEN', 'SECRET', algorithms=['HS256']))"
```

**Solutions:**
1. **SECRET_KEY:** Verify SECRET_KEY matches across environments
2. **Expiry:** Check ACCESS_TOKEN_EXPIRE_MINUTES setting
3. **Clock skew:** Verify server time synchronization

#### Issue: Database Connection Pool Exhausted

**Symptoms:**
- "connection pool exhausted" errors
- "ERR_DB_400" errors
- Slow database queries

**Diagnosis:**
```bash
# Check active connections
SELECT count(*) FROM pg_stat_activity WHERE datname = 'bahr_db';

# Check pool settings
# In backend/.env
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
```

**Solutions:**
1. **Increase pool size:** Set `DATABASE_POOL_SIZE=10`
2. **Fix leaks:** Ensure sessions are closed in `finally` blocks
3. **Connection timeout:** Add `pool_pre_ping=True`

#### Issue: Analysis Accuracy Low (<70%)

**Symptoms:**
- Low confidence scores
- Wrong meter detection
- User reports

**Diagnosis:**
```bash
# Test with golden dataset
python scripts/validate_dataset.py dataset/evaluation/golden_set_v0_20.jsonl

# Check metrics
curl http://localhost:9090/api/v1/query?query=bahr_meter_confidence
```

**Solutions:**
1. **Normalization:** Review normalization pipeline
2. **Zihafat:** Enable more metrical variations
3. **Dataset:** Add more training examples
4. **Fuzzy matching:** Adjust Levenshtein threshold

### 10.2 Emergency Procedures

#### Rollback Deployment

```bash
# Railway (via CLI)
railway rollback

# Vercel (via CLI)
vercel rollback

# Docker (manual)
docker pull your-org/bahr-backend:previous-tag
docker-compose up -d
```

#### Enable Maintenance Mode

```bash
# Set environment variable
MAINTENANCE_MODE=true

# Restart service
railway restart

# Returns 503 with message:
# {"success": false, "error": {"code": "ERR_MAINTENANCE_001", ...}}
```

#### Database Restore

```bash
# Restore from backup
pg_restore -d bahr_db backup.dump

# Verify data
psql -d bahr_db -c "SELECT COUNT(*) FROM users;"
```

---

## Appendix A: Quick Reference

### API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/auth/register` | No | Register new user |
| POST | `/api/v1/auth/login` | No | Login (get JWT) |
| POST | `/api/v1/auth/refresh` | No | Refresh access token |
| POST | `/api/v1/analyses` | Optional | Create analysis |
| GET | `/api/v1/analyses` | Yes | List user analyses |
| GET | `/api/v1/analyses/{id}` | No | Get analysis by ID |
| GET | `/api/v1/meters` | No | List all meters |
| GET | `/api/v1/meters/{id}` | No | Get meter details |
| GET | `/health` | No | Health check |
| GET | `/health/detailed` | No | Detailed health check |
| GET | `/metrics` | No | Prometheus metrics |

### Error Codes

| Code Range | Category | Example |
|------------|----------|---------|
| ERR_INPUT_001-099 | Input validation | ERR_INPUT_001 (empty text) |
| ERR_AUTH_100-199 | Authentication | ERR_AUTH_101 (token expired) |
| ERR_ANALYSIS_200-299 | Analysis | ERR_ANALYSIS_201 (no meter) |
| ERR_RATE_300-399 | Rate limiting | ERR_RATE_300 (limit exceeded) |
| ERR_DB_400-499 | Database | ERR_DB_400 (connection failed) |
| ERR_UNKNOWN_900-999 | System | ERR_UNKNOWN_900 (internal error) |

### Performance Targets

| Metric | Target (Week 6) | Critical Threshold |
|--------|----------------|-------------------|
| P95 latency | <600ms | <800ms |
| Meter accuracy | 70-75% | >65% |
| Cache hit rate | >40% | >25% |
| Error rate | <2% | <5% |
| Uptime | 99.5% | 99% |

---

## Appendix B: Related Documentation

| Topic | Document | Path |
|-------|----------|------|
| **Architecture** | Architecture Overview | `docs/technical/ARCHITECTURE_OVERVIEW.md` |
| **API Spec** | OpenAPI 3.0.3 | `docs/technical/API_SPECIFICATION.yaml` |
| **Database** | Schema Design | `docs/technical/DATABASE_SCHEMA.md` |
| **Prosody** | Engine Details | `docs/technical/PROSODY_ENGINE.md` |
| **Security** | Security Guidelines | `docs/technical/SECURITY.md` |
| **Deployment** | Deploy Guide | `docs/technical/DEPLOYMENT_GUIDE.md` |
| **Monitoring** | Metrics & Alerts | `docs/technical/MONITORING_INTEGRATION.md` |
| **Features** | Implementation Guides | `implementation-guides/` (14 guides) |

---

## Appendix C: Implementation Order

### Week 1: Foundation
1. Database schema + migrations
2. Authentication (JWT)
3. Response envelope middleware
4. Error handling

### Week 2-3: Core NLP
5. Text normalization
6. Syllable segmentation
7. Meter detection
8. Analysis API

### Week 4: Infrastructure
9. Redis caching
10. Rate limiting
11. Prometheus monitoring
12. Dataset management

### Week 5-6: Frontend & Polish
13. Next.js frontend
14. Deployment (Railway/Vercel)
15. E2E testing
16. Documentation updates

---

**Ready to implement?**  
Start with the [Authentication guide](./feature-authentication-jwt.md) and work through the 14 feature guides in order.

**Questions?**  
- Review `docs/START_HERE_DEVELOPER.md` for onboarding
- Check `docs/technical/ARCHITECTURE_OVERVIEW.md` for deep dives
- Consult feature guides in `implementation-guides/` for specific components

**🚀 Let's build BAHR!**
