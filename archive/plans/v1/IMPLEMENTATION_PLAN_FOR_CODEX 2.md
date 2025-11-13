# ⚠️ DEPRECATED - DO NOT USE

**This implementation plan has been superseded by [IMPLEMENTATION_PLAN_REVISED_FINAL.md](./IMPLEMENTATION_PLAN_REVISED_FINAL.md)**

This file is kept for historical reference only. All development should follow the revised final plan (v2.0).

**Deprecated:** November 9, 2025
**Reason:** Architecture review identified 10 critical issues requiring comprehensive revision
**Review Report:** See [archive/reviews/TECHNICAL_ARCHITECTURE_REVIEW_REPORT.md](./archive/reviews/TECHNICAL_ARCHITECTURE_REVIEW_REPORT.md)
**Revision Summary:** See [archive/reviews/REVISION_SUMMARY_REPORT.md](./archive/reviews/REVISION_SUMMARY_REPORT.md)

**Current Plan (v2.0):** [IMPLEMENTATION_PLAN_REVISED_FINAL.md](./IMPLEMENTATION_PLAN_REVISED_FINAL.md) ✅

---

# BAHR - AI Poetry Platform Implementation Plan (v1.0 - DEPRECATED)
## For AI Code Assistants (ChatGPT Codex / Claude)

---

## Executive Summary

**Platform Name:** بَحْر (BAHR) - Digital Suq Okaz
**Purpose:** Arabic poetry analysis, generation, competition, and learning platform powered by AI
**Target:** Arabic-speaking students, poets, teachers, and enthusiasts
**Core Value:** Preserve and modernize Arabic poetic heritage through AI technology

---

## 1. Core Platform Modules

### 1.1 Poetry Analyzer (محلل شعري)
**Functionality:** Automatic prosodic analysis of Arabic verse
- Taqti' (تقطيع) - phonetic breakdown
- Bahr detection (16 classical meters)
- Tafa'il identification
- Error detection
- Quality scoring
- Improvement suggestions

### 1.2 AI Poet (شاعر ذكي)
**Functionality:** AI-powered poetry generation
- Generate verse on any bahr (meter)
- Complete partial verses
- Full poem composition
- Style variants (classical, modern, dialect)
- Persona-based writing (e.g., "write like Al-Mutanabbi")

### 1.3 Competition Arena (ساحة المنافسة)
**Functionality:** Real-time poetry competitions
- User vs. User duels
- User vs. AI battles
- Tournament brackets
- Live audience voting
- Gamification (XP, levels, badges, coins)
- Global leaderboards

### 1.4 Learning Academy (أكاديمية العروض)
**Functionality:** Interactive prosody education
- 30+ lessons across 3 difficulty levels
- Video lessons, quizzes, exercises
- AI tutor (RAG-based chatbot)
- Progress tracking
- Certificate generation

### 1.5 Digital Library (مكتبة الدواوين)
**Functionality:** Searchable Arabic poetry archive
- 100k+ classical verses
- Full-text search (Elasticsearch)
- Filter by poet, era, meter, theme
- Audio versions (TTS)
- OCR for manuscripts
- User annotations

### 1.6 Social Features (المجتمع)
**Functionality:** Community engagement
- User profiles with personal divans
- Follow/like/comment system
- Groups and collaborative poems
- Virtual poetry events
- Newsletter

### 1.7 Developer API
**Functionality:** Public API for third-party developers
- RESTful endpoints for analysis, generation, competition
- Tiered pricing (Free, Basic, Pro, Enterprise)
- Rate limiting
- OAuth 2.0 authentication
- SDKs in Python, JavaScript, PHP

---

## 2. Technical Architecture

### 2.1 System Overview

```
┌─────────────────────────────────────────┐
│   Client Layer                          │
│   [Web App] [iOS] [Android] [Desktop]  │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│   API Gateway (Kong)                    │
│   Auth, Rate Limiting, Routing          │
└───────────────┬─────────────────────────┘
                │
        ┌───────┴───────┐
        │               │
┌───────▼─────┐  ┌──────▼─────────┐
│  FastAPI    │  │  WebSocket     │
│  REST API   │  │  (Real-time)   │
└───────┬─────┘  └──────┬─────────┘
        │               │
┌───────▼───────────────▼─────────┐
│   Core Services                  │
│   - Prosody Analyzer             │
│   - AI Poet Engine (LLM)         │
│   - Competition Engine           │
│   - Learning Management          │
│   - Search Engine                │
└───────┬──────────────────────────┘
        │
┌───────▼──────────────────────────┐
│   Data Layer                     │
│   - PostgreSQL (main DB)         │
│   - Elasticsearch (search)       │
│   - Redis (cache/queue)          │
│   - S3 (media storage)           │
└──────────────────────────────────┘
```

### 2.2 Tech Stack Specifications

#### Frontend
- **Framework:** Next.js 14 (React 18 + TypeScript)
- **Styling:** Tailwind CSS + shadcn/ui
- **State Management:** Zustand or Jotai
- **Forms:** React Hook Form + Zod validation
- **Real-time:** Socket.io-client
- **Charts:** Recharts
- **Animation:** Framer Motion
- **RTL Support:** Native CSS with rtl-detect

#### Backend
- **API Framework:** FastAPI (Python 3.11+)
- **Validation:** Pydantic v2
- **ORM:** SQLAlchemy 2.0
- **Migrations:** Alembic
- **Background Jobs:** Celery
- **Message Broker:** Redis
- **WebSocket:** Socket.io (Python)

#### AI/ML
- **Base LLM:** Fine-tuned Jais-13b or AraGPT2
- **Framework:** PyTorch 2.0+
- **Transformers:** Hugging Face Transformers
- **Serving:** vLLM for fast inference
- **Orchestration:** LangChain
- **Experiment Tracking:** Weights & Biases
- **Optimization:** ONNX runtime

#### Data Storage
- **Primary DB:** PostgreSQL 15
  - Extensions: pgvector (embeddings)
- **Search:** Elasticsearch 8
- **Cache/Queue:** Redis 7
- **Object Storage:** AWS S3 or Cloudflare R2
- **CDN:** Cloudflare

#### DevOps
- **Containerization:** Docker + Docker Compose
- **Orchestration:** Kubernetes (production)
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana
- **Error Tracking:** Sentry
- **Logging:** ELK Stack
- **Analytics:** Mixpanel or PostHog

#### Security
- **Auth:** JWT + OAuth 2.0
- **Secrets Management:** AWS Secrets Manager
- **SSL/TLS:** Let's Encrypt + Cloudflare
- **DDoS Protection:** Cloudflare

---

## 3. Database Schema (PostgreSQL)

### 3.1 Core Tables

#### Users & Authentication
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    bio TEXT,
    avatar_url VARCHAR(500),
    level INT DEFAULT 1,
    xp INT DEFAULT 0,
    coins INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

CREATE TABLE user_roles (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    role VARCHAR(20) -- 'admin', 'moderator', 'poet', 'student'
);
```

#### Poetry Content
```sql
CREATE TABLE poems (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    title VARCHAR(255),
    full_text TEXT,
    bahr VARCHAR(50),
    is_complete BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    visibility VARCHAR(20) DEFAULT 'public' -- 'public', 'private', 'unlisted'
);

CREATE TABLE verses (
    id SERIAL PRIMARY KEY,
    poem_id INT REFERENCES poems(id),
    text TEXT NOT NULL,
    taqti3_pattern VARCHAR(255), -- phonetic pattern
    bahr VARCHAR(50),
    line_number INT,
    hemisphere VARCHAR(10) -- 'sadr' (صدر) or 'ajuz' (عجز)
);
```

#### Prosody Reference Data
```sql
CREATE TABLE bahrs (
    id SERIAL PRIMARY KEY,
    name_ar VARCHAR(50) NOT NULL,
    name_en VARCHAR(50),
    pattern VARCHAR(255), -- base tafa'il pattern
    description TEXT,
    example_verse TEXT
);

CREATE TABLE tafa3il (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    pattern VARCHAR(50),
    variations JSONB, -- array of zihafat variations
    bahr_id INT REFERENCES bahrs(id)
);
```

#### Analysis Cache
```sql
CREATE TABLE analysis_cache (
    id SERIAL PRIMARY KEY,
    verse_text_hash VARCHAR(64) UNIQUE, -- SHA-256 hash
    taqti3 VARCHAR(255),
    bahr_id INT REFERENCES bahrs(id),
    confidence DECIMAL(3,2), -- 0.00 to 1.00
    cached_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_verse_hash ON analysis_cache(verse_text_hash);
```

#### Competitions
```sql
CREATE TABLE competitions (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50), -- 'duel', 'tournament', 'meter_challenge'
    status VARCHAR(20), -- 'upcoming', 'live', 'finished'
    title VARCHAR(255),
    description TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    prize_amount DECIMAL(10,2),
    max_participants INT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE competition_participants (
    id SERIAL PRIMARY KEY,
    competition_id INT REFERENCES competitions(id),
    user_id INT REFERENCES users(id),
    joined_at TIMESTAMP DEFAULT NOW(),
    final_score DECIMAL(5,2),
    rank INT
);

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    competition_id INT REFERENCES competitions(id),
    participant1_id INT REFERENCES users(id),
    participant2_id INT REFERENCES users(id),
    verse1_id INT REFERENCES verses(id),
    verse2_id INT REFERENCES verses(id),
    winner_id INT REFERENCES users(id),
    audience_votes JSONB, -- {user_id: vote}
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Learning
```sql
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    level VARCHAR(20), -- 'beginner', 'intermediate', 'advanced'
    description TEXT,
    duration_hours INT
);

CREATE TABLE lessons (
    id SERIAL PRIMARY KEY,
    course_id INT REFERENCES courses(id),
    title VARCHAR(255),
    order INT,
    content_type VARCHAR(20), -- 'video', 'text', 'quiz', 'exercise'
    content_url VARCHAR(500),
    duration_minutes INT
);

CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    lesson_id INT REFERENCES lessons(id),
    status VARCHAR(20), -- 'not_started', 'in_progress', 'completed'
    score DECIMAL(5,2),
    completed_at TIMESTAMP,
    UNIQUE(user_id, lesson_id)
);
```

#### Social Features
```sql
CREATE TABLE follows (
    id SERIAL PRIMARY KEY,
    follower_id INT REFERENCES users(id),
    following_id INT REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(follower_id, following_id)
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    verse_id INT REFERENCES verses(id),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, verse_id)
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    verse_id INT REFERENCES verses(id),
    text TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    edited_at TIMESTAMP
);
```

#### Gamification
```sql
CREATE TABLE achievements (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    badge_icon_url VARCHAR(500),
    xp_reward INT
);

CREATE TABLE user_achievements (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    achievement_id INT REFERENCES achievements(id),
    unlocked_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, achievement_id)
);
```

#### API & Billing
```sql
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    key_hash VARCHAR(255) UNIQUE,
    tier VARCHAR(20), -- 'free', 'basic', 'pro', 'enterprise'
    rate_limit INT, -- requests per day
    requests_used INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

CREATE TABLE api_usage_logs (
    id SERIAL PRIMARY KEY,
    api_key_id INT REFERENCES api_keys(id),
    endpoint VARCHAR(255),
    timestamp TIMESTAMP DEFAULT NOW(),
    status_code INT,
    response_time_ms INT
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    type VARCHAR(20), -- 'purchase', 'prize', 'refund'
    amount DECIMAL(10,2),
    currency VARCHAR(3) DEFAULT 'USD',
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 4. API Endpoints Specification

### 4.1 Authentication

```
POST /api/v1/auth/register
Body: {email, username, password, full_name}
Response: {user_id, token}

POST /api/v1/auth/login
Body: {email, password}
Response: {token, user: {...}}

POST /api/v1/auth/logout
Headers: {Authorization: Bearer <token>}
Response: {success: true}

POST /api/v1/auth/refresh
Body: {refresh_token}
Response: {token}
```

### 4.2 Poetry Analysis

```
POST /api/v1/analyze
Headers: {Authorization: Bearer <token>}
Body: {
  text: "إذا غامَرتَ في شَرَفٍ مَرومِ",
  options: {
    detect_bahr: true,
    suggest_corrections: true
  }
}
Response: {
  text: "...",
  taqti3: "فعولن مفاعيلن فعولن مفاعيلن",
  bahr: {
    name_ar: "الطويل",
    name_en: "at-Tawil",
    confidence: 0.98
  },
  errors: [],
  suggestions: [...],
  score: 95
}
```

### 4.3 AI Generation

```
POST /api/v1/generate
Headers: {Authorization: Bearer <token>}
Body: {
  bahr: "الطويل",
  theme: "الحكمة",
  length: 2, // number of verses
  temperature: 0.7,
  persona: "المتنبي" // optional
}
Response: {
  verses: [
    {text: "...", taqti3: "...", bahr: "الطويل"},
    ...
  ],
  generation_time_ms: 3200
}

POST /api/v1/complete
Body: {
  sadr: "إذا غامَرتَ في شَرَفٍ مَرومِ",
  bahr: "الطويل" // optional, auto-detect if not provided
}
Response: {
  ajuz: "فَلا تَقنَع بِما دونَ النُجومِ",
  full_verse: "..."
}
```

### 4.4 Competitions

```
GET /api/v1/competitions
Query: ?status=live&type=duel
Response: {
  competitions: [{id, title, type, status, ...}, ...]
}

POST /api/v1/competitions/{id}/join
Headers: {Authorization: Bearer <token>}
Response: {success: true, participant_id: 123}

POST /api/v1/competitions/{id}/submit
Body: {verse_text: "..."}
Response: {
  verse_id: 456,
  score: {meter: 40, meaning: 28, beauty: 19, total: 87}
}

GET /api/v1/leaderboard
Query: ?scope=global&limit=100
Response: {
  leaderboard: [
    {rank: 1, user: {...}, total_score: 15420, wins: 87},
    ...
  ]
}
```

### 4.5 Learning

```
GET /api/v1/courses
Response: {courses: [{id, title, level, lessons_count}, ...]}

GET /api/v1/courses/{id}
Response: {
  id, title, description, lessons: [...], user_progress: {...}
}

POST /api/v1/lessons/{id}/complete
Body: {score: 85}
Response: {
  success: true,
  xp_earned: 50,
  next_lesson_id: 12
}

POST /api/v1/tutor/ask
Body: {question: "ما هو بحر الطويل؟"}
Response: {
  answer: "بحر الطويل هو...",
  sources: [{lesson_id: 3, title: "البحور الأساسية"}]
}
```

### 4.6 Library

```
GET /api/v1/search
Query: ?q=المتنبي&bahr=الطويل&limit=20
Response: {
  results: [
    {verse_id, text, poet, bahr, era, relevance_score},
    ...
  ],
  total: 487
}

GET /api/v1/poets
Response: {poets: [{id, name, era, poems_count}, ...]}

GET /api/v1/poets/{id}/poems
Response: {poems: [{id, title, verses_count, bahr}, ...]}

GET /api/v1/bahrs
Response: {
  bahrs: [
    {id, name_ar, name_en, pattern, example_verse},
    ...
  ]
}
```

### 4.7 Social

```
POST /api/v1/users/{id}/follow
Response: {success: true}

POST /api/v1/verses/{id}/like
Response: {success: true, total_likes: 42}

POST /api/v1/verses/{id}/comment
Body: {text: "رائع!"}
Response: {comment_id: 789}

GET /api/v1/feed
Response: {
  items: [
    {type: 'new_verse', user: {...}, verse: {...}, timestamp},
    {type: 'achievement', user: {...}, achievement: {...}},
    ...
  ]
}
```

---

## 5. Implementation Roadmap

### Phase 0: Pre-Development (Weeks 1-2)

**Objective:** Set up infrastructure and development environment

**Tasks:**
1. Initialize Git repository
   - Structure: monorepo or separate repos for frontend/backend
   - Branching strategy: main, develop, feature/*
2. Setup Docker development environment
   - `docker-compose.yml` with PostgreSQL, Redis, Elasticsearch
3. Initialize Next.js project
   - `npx create-next-app@latest --typescript`
   - Configure Tailwind CSS, RTL support
4. Initialize FastAPI project
   - Project structure: app/, tests/, migrations/, scripts/
   - Configure Poetry or pip-tools for dependencies
5. Setup CI/CD pipeline (GitHub Actions)
   - Linting (ESLint, Black, Flake8)
   - Unit tests
   - Build Docker images
6. Design system and mockups (Figma)
   - Color palette, typography, components
   - Key screens: Home, Analyze, Generate, Compete

**Deliverables:**
- ✅ Repository with basic structure
- ✅ Local development environment running
- ✅ Design system documented
- ✅ CI/CD pipeline configured

---

### Phase 1: MVP - Prosody Analyzer (Months 1-2)

**Objective:** Build core poetry analysis engine with basic web interface

#### Week 1-2: Prosody Engine Core

**Tasks:**

1. **Text Normalization Module** (`app/core/normalization.py`)
   ```python
   def normalize_arabic_text(text: str) -> str:
       """
       - Remove tashkeel (diacritics) optionally
       - Normalize hamza variants (أ، إ، آ → ا)
       - Normalize alef variants (ى → ي)
       - Handle tatweel (ـ)
       - Normalize tanween
       """
       pass
   ```

2. **Phonetic Analysis Module** (`app/core/phonetics.py`)
   ```python
   def text_to_phonemes(text: str) -> List[str]:
       """
       Convert Arabic text to phonetic representation
       - Handle shadda (double consonant)
       - Identify short vowels (a, i, u)
       - Identify long vowels (aa, ii, uu)
       - Mark sukun (no vowel)
       Returns: List of phonemes
       """
       pass
   ```

3. **Taqti' Algorithm** (`app/core/taqti3.py`)
   ```python
   def perform_taqti3(verse: str) -> str:
       """
       Break verse into prosodic pattern
       Rules:
       - Consonant with harakah = / (متحرك)
       - Consonant without harakah = o (ساكن)
       - Pattern: /o = short syllable, //o = long syllable
       Returns: Pattern string like "/o//o/o//o"
       """
       pass
   ```

4. **Bahr Detection** (`app/core/bahr_detector.py`)
   ```python
   class BahrDetector:
       def __init__(self):
           # Load 16 bahr patterns from database
           self.bahrs = load_bahrs()

       def detect_bahr(self, taqti3_pattern: str) -> Dict:
           """
           Match taqti3 pattern to known bahrs
           - Exact match
           - Fuzzy match (allow minor variations for zihafat)
           Returns: {bahr_name, confidence, tafa3il_breakdown}
           """
           pass
   ```

5. **Unit Tests** (`tests/core/test_taqti3.py`)
   ```python
   def test_taqti3_tawil():
       verse = "إذا غامَرتَ في شَرَفٍ مَرومِ"
       result = perform_taqti3(verse)
       expected = "فعولن مفاعيلن فعولن مفاعيلن"
       assert result == expected

   # Test cases for all 16 bahrs
   # Target: 80%+ code coverage
   ```

**Acceptance Criteria:**
- Analyzer correctly identifies bahr for 90%+ of test verses
- Handles verses with and without tashkeel
- Response time <200ms per verse

---

#### Week 3-4: API & Database

**Tasks:**

1. **Database Schema Setup**
   - Create Alembic migration for core tables
   - Seed `bahrs` table with 16 classical meters
   - Seed `tafa3il` table with patterns

2. **FastAPI Application Structure**
   ```
   app/
   ├── main.py              # FastAPI app initialization
   ├── core/                # Prosody engine (from Week 1-2)
   ├── api/
   │   ├── v1/
   │   │   ├── endpoints/
   │   │   │   ├── auth.py
   │   │   │   ├── analyze.py
   │   │   │   └── bahrs.py
   │   │   └── router.py
   ├── models/              # SQLAlchemy models
   ├── schemas/             # Pydantic schemas
   ├── db/
   │   ├── session.py       # Database connection
   │   └── base.py
   └── utils/
   ```

3. **Implement `/analyze` endpoint** (`app/api/v1/endpoints/analyze.py`)
   ```python
   from fastapi import APIRouter, Depends
   from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
   from app.core.taqti3 import perform_taqti3
   from app.core.bahr_detector import BahrDetector

   router = APIRouter()

   @router.post("/analyze", response_model=AnalyzeResponse)
   async def analyze_verse(request: AnalyzeRequest):
       # 1. Normalize text
       normalized = normalize_arabic_text(request.text)

       # 2. Check cache (Redis)
       cache_key = sha256(normalized).hexdigest()
       cached = await redis.get(f"analysis:{cache_key}")
       if cached:
           return json.loads(cached)

       # 3. Perform taqti3
       taqti3 = perform_taqti3(normalized)

       # 4. Detect bahr
       detector = BahrDetector()
       bahr_result = detector.detect_bahr(taqti3)

       # 5. Build response
       response = {
           "text": request.text,
           "taqti3": taqti3,
           "bahr": bahr_result,
           "errors": [],  # TODO: error detection
           "score": calculate_score(bahr_result)
       }

       # 6. Cache result (24h TTL)
       await redis.setex(f"analysis:{cache_key}", 86400, json.dumps(response))

       return response
   ```

4. **Request/Response Schemas** (`app/schemas/analyze.py`)
   ```python
   from pydantic import BaseModel, Field

   class AnalyzeRequest(BaseModel):
       text: str = Field(..., min_length=5, max_length=500)
       detect_bahr: bool = True
       suggest_corrections: bool = False

   class BahrInfo(BaseModel):
       name_ar: str
       name_en: str
       confidence: float = Field(..., ge=0.0, le=1.0)

   class AnalyzeResponse(BaseModel):
       text: str
       taqti3: str
       bahr: Optional[BahrInfo]
       errors: List[str]
       score: int
   ```

5. **Redis Caching Layer**
   - Connection pooling
   - Cache key strategy: `analysis:{verse_hash}`
   - TTL: 24 hours

6. **API Documentation**
   - Swagger UI auto-generated at `/docs`
   - ReDoc at `/redoc`
   - Add descriptions to all endpoints

**Acceptance Criteria:**
- `/analyze` endpoint returns correct results
- Response time <200ms (with cache)
- Cache hit rate >50% in testing
- API documentation complete

---

#### Week 5-6: Frontend (Web App)

**Tasks:**

1. **Next.js Project Setup**
   ```bash
   npx create-next-app@latest bahr-web --typescript
   cd bahr-web
   npm install tailwindcss @tailwindcss/rtl
   npm install @tanstack/react-query axios zustand
   npm install react-hook-form zod @hookform/resolvers
   ```

2. **RTL Configuration** (`tailwind.config.js`)
   ```javascript
   module.exports = {
     content: ['./src/**/*.{js,ts,jsx,tsx}'],
     theme: {
       extend: {
         fontFamily: {
           arabic: ['Cairo', 'sans-serif'],
           poetry: ['Amiri', 'serif'],
         },
       },
     },
     plugins: [require('@tailwindcss/rtl')],
   }
   ```

3. **Directory Structure**
   ```
   src/
   ├── app/
   │   ├── layout.tsx       # Root layout (RTL)
   │   ├── page.tsx         # Home page
   │   ├── analyze/
   │   │   └── page.tsx
   │   └── api/             # API routes (proxy to FastAPI)
   ├── components/
   │   ├── ui/              # shadcn components
   │   ├── AnalyzeForm.tsx
   │   ├── AnalyzeResults.tsx
   │   └── PatternVisualization.tsx
   ├── lib/
   │   ├── api.ts           # Axios instance
   │   └── utils.ts
   └── types/
       └── analyze.ts
   ```

4. **Home Page** (`src/app/page.tsx`)
   ```tsx
   import Link from 'next/link';

   export default function Home() {
     return (
       <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white" dir="rtl">
         <div className="container mx-auto px-4 py-16">
           <h1 className="text-6xl font-bold text-center mb-8 font-arabic">
             بَحْر
           </h1>
           <p className="text-2xl text-center text-gray-700 mb-12">
             محلل الشعر العربي بالذكاء الاصطناعي
           </p>

           <div className="max-w-2xl mx-auto">
             <Link href="/analyze">
               <button className="w-full bg-blue-600 text-white py-4 rounded-lg text-xl">
                 ابدأ التحليل الآن
               </button>
             </Link>
           </div>
         </div>
       </main>
     );
   }
   ```

5. **Analyze Page** (`src/app/analyze/page.tsx`)
   ```tsx
   'use client';
   import { useState } from 'react';
   import { useForm } from 'react-hook-form';
   import { zodResolver } from '@hookform/resolvers/zod';
   import { z } from 'zod';
   import { analyzeVerse } from '@/lib/api';
   import AnalyzeResults from '@/components/AnalyzeResults';

   const schema = z.object({
     text: z.string().min(5, 'الرجاء إدخال بيت شعري'),
   });

   export default function AnalyzePage() {
     const [result, setResult] = useState(null);
     const [loading, setLoading] = useState(false);

     const { register, handleSubmit, formState: { errors } } = useForm({
       resolver: zodResolver(schema),
     });

     const onSubmit = async (data) => {
       setLoading(true);
       try {
         const response = await analyzeVerse(data.text);
         setResult(response);
       } catch (error) {
         console.error(error);
       } finally {
         setLoading(false);
       }
     };

     return (
       <div className="container mx-auto px-4 py-8" dir="rtl">
         <h1 className="text-4xl font-bold mb-8">محلل الشعر</h1>

         <form onSubmit={handleSubmit(onSubmit)} className="mb-8">
           <textarea
             {...register('text')}
             className="w-full p-4 border-2 rounded-lg font-poetry text-xl"
             rows={4}
             placeholder="إذا غامَرتَ في شَرَفٍ مَرومِ"
           />
           {errors.text && <p className="text-red-500">{errors.text.message}</p>}

           <button
             type="submit"
             disabled={loading}
             className="mt-4 bg-blue-600 text-white px-8 py-3 rounded-lg"
           >
             {loading ? 'جارٍ التحليل...' : 'حلّل'}
           </button>
         </form>

         {result && <AnalyzeResults data={result} />}
       </div>
     );
   }
   ```

6. **Results Component** (`src/components/AnalyzeResults.tsx`)
   ```tsx
   export default function AnalyzeResults({ data }) {
     return (
       <div className="bg-white p-6 rounded-lg shadow-lg">
         <h2 className="text-2xl font-bold mb-4">نتائج التحليل</h2>

         <div className="mb-4">
           <h3 className="font-semibold">البيت:</h3>
           <p className="font-poetry text-xl">{data.text}</p>
         </div>

         <div className="mb-4">
           <h3 className="font-semibold">التقطيع:</h3>
           <p className="font-mono text-lg">{data.taqti3}</p>
         </div>

         <div className="mb-4">
           <h3 className="font-semibold">البحر:</h3>
           <p className="text-xl">
             {data.bahr.name_ar} ({data.bahr.name_en})
             <span className="text-sm text-gray-500 mr-2">
               ({(data.bahr.confidence * 100).toFixed(0)}% دقة)
             </span>
           </p>
         </div>

         <div>
           <h3 className="font-semibold">التقييم:</h3>
           <div className="w-full bg-gray-200 rounded-full h-4">
             <div
               className="bg-green-500 h-4 rounded-full"
               style={{ width: `${data.score}%` }}
             />
           </div>
           <p className="text-center mt-2">{data.score}/100</p>
         </div>
       </div>
     );
   }
   ```

7. **API Client** (`src/lib/api.ts`)
   ```typescript
   import axios from 'axios';

   const api = axios.create({
     baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
   });

   export async function analyzeVerse(text: string) {
     const response = await api.post('/analyze', { text });
     return response.data;
   }
   ```

**Acceptance Criteria:**
- Home page renders correctly with RTL support
- Analyze page successfully calls API and displays results
- Mobile responsive design
- Arabic fonts load correctly (Cairo, Amiri)

---

#### Week 7-8: Testing & Deployment

**Tasks:**

1. **Integration Tests**
   - Test full flow: input → API → database → response
   - Test edge cases (empty verse, very long verse, non-Arabic text)

2. **Load Testing** (using Locust or k6)
   ```python
   from locust import HttpUser, task

   class PoetryUser(HttpUser):
       @task
       def analyze_verse(self):
           self.client.post("/api/v1/analyze", json={
               "text": "إذا غامَرتَ في شَرَفٍ مَرومِ"
           })
   ```
   - Target: 100 concurrent users
   - Response time p95 <500ms

3. **Deployment to Staging**
   - Option A: Railway (easy, free tier)
     - Connect GitHub repo
     - Auto-deploy on push
   - Option B: Render
     - Web service for FastAPI
     - Static site for Next.js
   - Option C: Docker on DigitalOcean

4. **Database Migration**
   - Use Supabase (managed PostgreSQL) or Railway's PostgreSQL
   - Run Alembic migrations on production DB

5. **Beta Testing**
   - Recruit 10 users (students, poets)
   - Collect feedback via Google Forms
   - Bug tracking in GitHub Issues

6. **Bug Fixes & Iteration**
   - Address critical bugs
   - Improve accuracy based on feedback
   - UI/UX tweaks

**Deliverables:**
- ✅ Working analyzer live at [staging-url]
- ✅ 90%+ accuracy on common bahrs (Tawil, Kamil, Wafir, Ramal)
- ✅ Response time <200ms (cached), <500ms (uncached)
- ✅ 10+ beta testers provided feedback
- ✅ Documentation for API usage

---

### Phase 2: AI Poet - Generation (Months 3-5)

**Objective:** Train and deploy AI model for poetry generation

#### Month 3: Data Collection & Preparation

**Tasks:**

1. **Data Scraping** (Ethical, with robots.txt compliance)
   - Sources:
     - aldiwan.net (public domain classical poetry)
     - adab.com
     - Wikisource Arabic poetry
   - Tools: BeautifulSoup, Scrapy
   - Rate limiting: 1 request/second

2. **Data Cleaning Script** (`scripts/clean_poetry_data.py`)
   ```python
   import pandas as pd
   from app.core.normalization import normalize_arabic_text
   from app.core.taqti3 import perform_taqti3
   from app.core.bahr_detector import BahrDetector

   def clean_dataset(raw_csv: str, output_csv: str):
       df = pd.read_csv(raw_csv)

       # Remove duplicates
       df = df.drop_duplicates(subset=['text'])

       # Normalize text
       df['text_normalized'] = df['text'].apply(normalize_arabic_text)

       # Validate each verse
       detector = BahrDetector()
       valid_verses = []

       for idx, row in df.iterrows():
           try:
               taqti3 = perform_taqti3(row['text_normalized'])
               bahr = detector.detect_bahr(taqti3)

               if bahr['confidence'] > 0.85:
                   valid_verses.append({
                       'text': row['text'],
                       'taqti3': taqti3,
                       'bahr': bahr['name_ar'],
                       'poet': row.get('poet', 'Unknown'),
                       'era': row.get('era', 'Unknown')
                   })
           except Exception as e:
               print(f"Error processing verse {idx}: {e}")

       # Save cleaned data
       clean_df = pd.DataFrame(valid_verses)
       clean_df.to_csv(output_csv, index=False)

       print(f"Cleaned {len(clean_df)} verses from {len(df)} total")
   ```

3. **Dataset Annotation**
   - Label each verse with bahr (using analyzer)
   - Mark tafa'il boundaries
   - Quality filtering (confidence >85%)
   - Target: 100,000+ verses across 16 bahrs

4. **Train/Val/Test Split**
   - 80% training (80k verses)
   - 10% validation (10k verses)
   - 10% test (10k verses)
   - Stratified by bahr (ensure all bahrs represented)

5. **Store in Database & Files**
   - PostgreSQL for metadata
   - Parquet files for training data (efficient storage)

**Acceptance Criteria:**
- 100k+ verses collected
- All 16 bahrs represented (minimum 1000 verses per bahr)
- Quality validated (>85% analyzer confidence)
- Data saved in training-ready format

---

#### Month 4: Model Training

**Tasks:**

1. **Model Selection**
   - Evaluate base models:
     - **AraGPT2** (aubmindlab) - 135M params, Arabic-focused
     - **Jais-13b** (Core42) - 13B params, high quality
     - **mGPT** - Multilingual, if needed
   - Decision criteria: quality vs. inference cost

2. **Training Environment Setup**
   - Cloud GPU rental:
     - Google Colab Pro+ (A100, $50/month)
     - RunPod (A100, ~$1.50/hour)
     - Lambda Labs (A100, ~$1.10/hour)
   - Or use local GPU if available

3. **Data Preparation for Training** (`scripts/prepare_training_data.py`)
   ```python
   from transformers import AutoTokenizer

   tokenizer = AutoTokenizer.from_pretrained("aubmindlab/aragpt2-base")

   def format_verse_for_training(verse: dict) -> str:
       """
       Format: <|bahr|>بحر الطويل<|verse|>إذا غامَرتَ في شَرَفٍ مَرومِ<|endoftext|>
       """
       return f"<|bahr|>{verse['bahr']}<|verse|>{verse['text']}<|endoftext|>"

   # Process all verses
   with open('training_data.txt', 'w', encoding='utf-8') as f:
       for verse in verses:
           f.write(format_verse_for_training(verse) + '\n')
   ```

4. **Fine-tuning Script** (`scripts/train_poet_model.py`)
   ```python
   from transformers import (
       AutoModelForCausalLM,
       AutoTokenizer,
       TrainingArguments,
       Trainer,
       DataCollatorForLanguageModeling
   )
   import torch

   # Load base model
   model = AutoModelForCausalLM.from_pretrained("aubmindlab/aragpt2-base")
   tokenizer = AutoTokenizer.from_pretrained("aubmindlab/aragpt2-base")

   # Add special tokens
   special_tokens = {"additional_special_tokens": ["<|bahr|>", "<|verse|>"]}
   tokenizer.add_special_tokens(special_tokens)
   model.resize_token_embeddings(len(tokenizer))

   # Load dataset
   from datasets import load_dataset
   dataset = load_dataset('text', data_files='training_data.txt')

   def tokenize_function(examples):
       return tokenizer(examples['text'], truncation=True, max_length=128)

   tokenized_dataset = dataset.map(tokenize_function, batched=True)

   # Training arguments
   training_args = TrainingArguments(
       output_dir="./models/poet-v1",
       overwrite_output_dir=True,
       num_train_epochs=3,
       per_device_train_batch_size=8,
       per_device_eval_batch_size=8,
       learning_rate=5e-5,
       warmup_steps=500,
       weight_decay=0.01,
       logging_steps=100,
       save_steps=1000,
       eval_steps=500,
       save_total_limit=3,
       fp16=True,  # Mixed precision for A100
   )

   # Data collator
   data_collator = DataCollatorForLanguageModeling(
       tokenizer=tokenizer, mlm=False
   )

   # Trainer
   trainer = Trainer(
       model=model,
       args=training_args,
       data_collator=data_collator,
       train_dataset=tokenized_dataset["train"],
       eval_dataset=tokenized_dataset["validation"],
   )

   # Train
   trainer.train()

   # Save final model
   model.save_pretrained("./models/poet-v1-final")
   tokenizer.save_pretrained("./models/poet-v1-final")
   ```

5. **Prosody-Aware Training (Advanced)**
   - Custom loss function that penalizes incorrect meter
   - During generation, validate each token's prosodic contribution
   - Implementation: Constrained decoding with prosody rules

6. **Evaluation**
   ```python
   def evaluate_generated_verse(generated_text: str, expected_bahr: str):
       # Meter accuracy
       taqti3 = perform_taqti3(generated_text)
       detected_bahr = detector.detect_bahr(taqti3)
       meter_correct = (detected_bahr['name_ar'] == expected_bahr)

       # Coherence (human eval needed, or use GPT-4 as judge)

       # Diversity (unique n-grams)

       return {
           'meter_accuracy': meter_correct,
           'confidence': detected_bahr['confidence']
       }
   ```

7. **Iterative Improvement**
   - Monitor validation loss
   - Adjust hyperparameters (learning rate, batch size)
   - Try LoRA (Low-Rank Adaptation) for efficient fine-tuning
   - Experiment with quantization (8-bit, 4-bit) for smaller model size

**Acceptance Criteria:**
- Model generates verses with >85% meter accuracy
- Perplexity on validation set <20
- Human evaluation: >7/10 rating for meaning and beauty
- Model size optimized for inference (<2GB)

---

#### Month 5: Model Integration & Serving

**Tasks:**

1. **Model Optimization**
   - Convert to ONNX for faster inference
   - Or use vLLM for optimized serving

2. **Inference API** (`app/api/v1/endpoints/generate.py`)
   ```python
   from transformers import pipeline
   from app.core.bahr_detector import BahrDetector

   # Load model at startup
   generator = pipeline(
       "text-generation",
       model="./models/poet-v1-final",
       device=0  # GPU
   )

   @router.post("/generate", response_model=GenerateResponse)
   async def generate_verse(request: GenerateRequest):
       # Format prompt
       prompt = f"<|bahr|>{request.bahr}<|verse|>"

       # Generate
       result = generator(
           prompt,
           max_length=50,
           temperature=request.temperature,
           top_p=0.9,
           num_return_sequences=1
       )

       generated_text = result[0]['generated_text']
       verse = generated_text.split("<|verse|>")[1].split("<|endoftext|>")[0]

       # Validate meter
       taqti3 = perform_taqti3(verse)
       bahr_detected = BahrDetector().detect_bahr(taqti3)

       return {
           "verses": [{
               "text": verse,
               "taqti3": taqti3,
               "bahr": bahr_detected['name_ar']
           }],
           "generation_time_ms": ...
       }
   ```

3. **Rate Limiting**
   - Free users: 5 generations/day
   - Premium users: unlimited
   - Implement with Redis counters

4. **Frontend Integration** (`src/app/generate/page.tsx`)
   - UI for selecting bahr, theme, temperature
   - Display generated verses
   - "Regenerate" button
   - Option to save to profile

5. **A/B Testing**
   - Test different models (AraGPT2 vs Jais)
   - Test different temperatures (0.7 vs 0.9)
   - Measure user satisfaction (thumbs up/down)

**Deliverables:**
- ✅ AI generation endpoint live
- ✅ >85% verses follow correct meter
- ✅ <5 seconds generation time
- ✅ Integrated in web app
- ✅ Rate limiting implemented

---

### Phase 3: Competition Arena (Months 6-8)

**Objective:** Build real-time competition system with gamification

#### Month 6: Backend Systems

**Tasks:**

1. **Competition Engine** (`app/services/competition.py`)
   ```python
   class CompetitionService:
       async def create_competition(self, data: CompetitionCreate):
           """Admin creates a new competition"""
           pass

       async def join_competition(self, user_id: int, competition_id: int):
           """User joins a competition"""
           pass

       async def create_match(self, competition_id: int):
           """Matchmaking algorithm (ELO-based)"""
           # Pair users with similar skill levels
           pass

       async def submit_verse(self, match_id: int, user_id: int, verse_text: str):
           """User submits verse in a match"""
           # 1. Analyze verse (meter, quality)
           # 2. Calculate score
           # 3. Store in database
           pass

       async def judge_match(self, match_id: int):
           """Determine winner"""
           # Score formula:
           # 40% meter correctness
           # 30% meaning quality (AI judge)
           # 20% beauty (vocabulary richness)
           # 10% audience votes
           pass
   ```

2. **Scoring Algorithm** (`app/services/scoring.py`)
   ```python
   def calculate_verse_score(verse: str, bahr_expected: str) -> float:
       # Meter score (40 points)
       taqti3 = perform_taqti3(verse)
       bahr = BahrDetector().detect_bahr(taqti3)
       meter_score = 40 * bahr['confidence'] if bahr['name_ar'] == bahr_expected else 0

       # Meaning quality (30 points) - use GPT-4 or custom model
       meaning_score = evaluate_meaning_quality(verse)  # 0-30

       # Beauty score (20 points) - vocabulary richness
       beauty_score = calculate_beauty(verse)  # 0-20

       # Audience votes (10 points) - calculated later

       return meter_score + meaning_score + beauty_score
   ```

3. **Leaderboard System** (Redis sorted sets)
   ```python
   async def update_leaderboard(user_id: int, score: int):
       await redis.zadd("leaderboard:global", {user_id: score})

   async def get_leaderboard(limit: int = 100):
       results = await redis.zrevrange("leaderboard:global", 0, limit-1, withscores=True)
       return [{"user_id": uid, "score": score} for uid, score in results]
   ```

4. **Real-time Notifications** (WebSocket)
   ```python
   from fastapi import WebSocket

   @router.websocket("/ws/match/{match_id}")
   async def match_websocket(websocket: WebSocket, match_id: int):
       await websocket.accept()

       # Subscribe to match events
       pubsub = redis.pubsub()
       await pubsub.subscribe(f"match:{match_id}")

       async for message in pubsub.listen():
           if message['type'] == 'message':
               await websocket.send_json(json.loads(message['data']))
   ```

5. **Database Migrations**
   - Implement competitions, matches, participants tables
   - Add indexes for fast queries

**Acceptance Criteria:**
- Competition can be created and joined
- Matchmaking pairs users correctly
- Scoring algorithm works accurately
- Leaderboard updates in real-time

---

#### Month 7: Frontend & Gamification

**Tasks:**

1. **Competition Lobby** (`src/app/compete/page.tsx`)
   - List all competitions (upcoming, live, past)
   - Filters and search
   - "Join" button

2. **Match Interface** (`src/app/compete/match/[id]/page.tsx`)
   ```tsx
   'use client';
   import { useState, useEffect } from 'react';
   import { useWebSocket } from '@/hooks/useWebSocket';

   export default function MatchPage({ params }) {
     const [timeLeft, setTimeLeft] = useState(60);
     const [verse, setVerse] = useState('');
     const { messages, send } = useWebSocket(`/ws/match/${params.id}`);

     useEffect(() => {
       const timer = setInterval(() => {
         setTimeLeft(prev => prev > 0 ? prev - 1 : 0);
       }, 1000);
       return () => clearInterval(timer);
     }, []);

     const handleSubmit = () => {
       send({ type: 'submit_verse', verse });
     };

     return (
       <div className="container mx-auto p-8" dir="rtl">
         <h1 className="text-3xl font-bold mb-4">المبارزة الشعرية</h1>

         <div className="mb-4 text-2xl">
           الوقت المتبقي: {timeLeft}s
         </div>

         <div className="mb-4">
           <label>البحر المطلوب: الطويل</label>
         </div>

         <textarea
           value={verse}
           onChange={e => setVerse(e.target.value)}
           className="w-full p-4 border-2 rounded-lg font-poetry text-xl"
           rows={4}
           placeholder="اكتب بيتك هنا..."
         />

         <button
           onClick={handleSubmit}
           disabled={timeLeft === 0}
           className="mt-4 bg-green-600 text-white px-8 py-3 rounded-lg"
         >
           إرسال
         </button>

         {/* Real-time analysis as user types */}
         <div className="mt-4 bg-gray-100 p-4 rounded">
           <h3>التحليل المباشر:</h3>
           {/* Show taqti3 and meter detection in real-time */}
         </div>
       </div>
     );
   }
   ```

3. **Spectator Mode** (`src/app/compete/watch/[id]/page.tsx`)
   - Watch live matches
   - Vote for favorite verse
   - Live chat

4. **Results Screen**
   - Winner announcement with animation
   - Detailed score breakdown
   - Social sharing buttons

5. **Leaderboard** (`src/app/leaderboard/page.tsx`)
   - Top 100 poets
   - User's current rank
   - Stats (win rate, favorite bahr)

6. **Gamification System**
   - XP calculation logic
   - Level progression (مبتدئ → متمرس → شاعر → فحل)
   - Badge unlocking
   - Coin economy
   - Daily quests

**Acceptance Criteria:**
- Matches run smoothly in real-time
- Spectators can watch and vote
- Leaderboard updates correctly
- Gamification features engage users

---

#### Month 8: Launch & Iteration

**Tasks:**

1. **Beta Tournament**
   - Invite 50 users
   - Run test competition
   - Monitor for bugs and performance issues

2. **Anti-cheat Measures**
   - Detect copy-paste from existing poetry
   - Rate limiting on submissions
   - Plagiarism checking (compare against database)

3. **Rules & Guidelines**
   - Write competition rules
   - Fair play policy
   - Dispute resolution process

4. **Performance Optimization**
   - Load testing with 100+ concurrent matches
   - Optimize WebSocket connections
   - Database query optimization

5. **Feedback & Iteration**
   - Collect user feedback
   - Fix critical bugs
   - UI/UX improvements

**Deliverables:**
- ✅ Competition system fully functional
- ✅ 1000+ matches completed in beta
- ✅ 60%+ user retention (return for 2nd match)
- ✅ Leaderboard with 100+ active users

---

### Phase 4: Learning Academy (Months 9-11)

**Objective:** Build interactive educational platform with AI tutor

#### Month 9: Content Creation

**Tasks:**

1. **Curriculum Development**
   - Write 30 lessons across 3 levels:
     - **Beginner:** 10 lessons (basics, first 3 bahrs)
     - **Intermediate:** 12 lessons (all 16 bahrs, zihafat)
     - **Advanced:** 8 lessons (prosodic music, criticism)

2. **Video Production**
   - Script writing for each lesson
   - Animation (use Manim, After Effects, or hire animator)
   - Voiceover (professional or high-quality TTS like ElevenLabs)
   - Subtitles in Arabic

3. **Exercise Design**
   ```json
   {
     "lesson_id": 3,
     "exercises": [
       {
         "type": "multiple_choice",
         "question": "ما هو بحر البيت التالي: 'إذا غامَرتَ في شَرَفٍ مَرومِ'؟",
         "options": ["الطويل", "الكامل", "الوافر", "الرمل"],
         "correct": 0
       },
       {
         "type": "fill_blank",
         "question": "أكمل التقطيع: 'فعولن مفاعيلن ___'",
         "correct": "فعولن مفاعيلن"
       },
       {
         "type": "compose",
         "question": "اكتب بيتاً على بحر الطويل",
         "grading": "ai"  // AI-graded using analyzer
       }
     ]
   }
   ```

4. **Certificate Templates**
   - Design PDF certificate
   - Include: user name, course name, completion date, score

**Acceptance Criteria:**
- 30 lessons with video, text, exercises
- All videos <10 minutes each
- Exercises cover key concepts
- Certificate design approved

---

#### Month 10: Backend Development

**Tasks:**

1. **Course Management System** (`app/services/learning.py`)
   ```python
   class LearningService:
       async def enroll_user(self, user_id: int, course_id: int):
           """Enroll user in course"""
           pass

       async def get_user_progress(self, user_id: int, course_id: int):
           """Get user's progress in a course"""
           pass

       async def complete_lesson(self, user_id: int, lesson_id: int, score: float):
           """Mark lesson as complete and award XP"""
           # Update user_progress table
           # Award XP
           # Check if course completed → generate certificate
           pass

       async def recommend_next_lesson(self, user_id: int):
           """AI-based recommendation"""
           # Analyze user's strengths/weaknesses
           # Suggest personalized next lesson
           pass
   ```

2. **Quiz Engine** (`app/api/v1/endpoints/quizzes.py`)
   ```python
   @router.post("/quizzes/{quiz_id}/submit")
   async def submit_quiz(quiz_id: int, answers: List[Answer]):
       # Grade quiz
       quiz = get_quiz(quiz_id)
       score = 0

       for i, answer in enumerate(answers):
           if quiz.questions[i].type == "multiple_choice":
               if answer.choice == quiz.questions[i].correct:
                   score += 1
           elif quiz.questions[i].type == "compose":
               # AI grading using analyzer
               result = analyze_verse(answer.text)
               if result.bahr.confidence > 0.85:
                   score += 1

       total = len(quiz.questions)
       return {"score": score, "total": total, "percentage": score/total * 100}
   ```

3. **Certificate Generation** (`app/services/certificates.py`)
   ```python
   from reportlab.pdfgen import canvas
   from reportlab.lib.pagesizes import A4

   def generate_certificate(user_id: int, course_id: int) -> str:
       user = get_user(user_id)
       course = get_course(course_id)

       pdf_path = f"certificates/{user_id}_{course_id}.pdf"
       c = canvas.Canvas(pdf_path, pagesize=A4)

       # Arabic font support
       from reportlab.pdfbase import pdfmetrics
       from reportlab.pdfbase.ttfonts import TTFont
       pdfmetrics.registerFont(TTFont('Arabic', 'fonts/Cairo-Regular.ttf'))

       c.setFont('Arabic', 24)
       c.drawRightString(500, 700, f"شهادة إتمام")
       c.setFont('Arabic', 18)
       c.drawRightString(500, 650, f"{user.full_name}")
       c.drawRightString(500, 600, f"أتم بنجاح دورة: {course.title}")

       c.save()
       return pdf_path
   ```

4. **Recommendation Algorithm**
   - Track which lessons user struggles with
   - Suggest remedial lessons
   - Adaptive difficulty

**Acceptance Criteria:**
- Users can enroll in courses
- Progress tracking works correctly
- Quizzes grade accurately (including AI-graded exercises)
- Certificates generate properly with Arabic text

---

#### Month 11: AI Tutor & Frontend

**Tasks:**

1. **RAG System for AI Tutor** (`app/services/tutor.py`)
   ```python
   from langchain.embeddings import OpenAIEmbeddings
   from langchain.vectorstores import Chroma
   from langchain.llms import OpenAI
   from langchain.chains import RetrievalQA

   # Index all lesson content
   def build_tutor_index():
       lessons = get_all_lessons()
       texts = [f"{l.title}\n{l.content}" for l in lessons]

       embeddings = OpenAIEmbeddings()
       vectorstore = Chroma.from_texts(texts, embeddings)

       return vectorstore

   # Answer questions
   def ask_tutor(question: str) -> str:
       vectorstore = load_tutor_index()
       qa = RetrievalQA.from_chain_type(
           llm=OpenAI(temperature=0),
           retriever=vectorstore.as_retriever()
       )

       answer = qa.run(question)
       return answer
   ```

2. **Tutor API Endpoint**
   ```python
   @router.post("/tutor/ask", response_model=TutorResponse)
   async def ask_tutor_question(request: TutorRequest):
       answer = ask_tutor(request.question)

       # Find relevant lessons
       sources = find_relevant_lessons(request.question)

       return {
           "answer": answer,
           "sources": sources
       }
   ```

3. **Academy Frontend** (`src/app/academy/page.tsx`)
   - Course catalog
   - User progress dashboard
   - Enrolled courses

4. **Course Page** (`src/app/academy/courses/[id]/page.tsx`)
   - Lesson list with completion status
   - Video player
   - Quiz interface
   - Progress bar

5. **AI Tutor Widget** (`src/components/TutorWidget.tsx`)
   ```tsx
   'use client';
   import { useState } from 'react';
   import { askTutor } from '@/lib/api';

   export default function TutorWidget() {
     const [question, setQuestion] = useState('');
     const [answer, setAnswer] = useState(null);

     const handleAsk = async () => {
       const result = await askTutor(question);
       setAnswer(result);
     };

     return (
       <div className="fixed bottom-4 left-4 bg-white shadow-lg rounded-lg p-4 w-80" dir="rtl">
         <h3 className="font-bold mb-2">المعلم الذكي</h3>
         <input
           value={question}
           onChange={e => setQuestion(e.target.value)}
           placeholder="اسأل عن علم العروض..."
           className="w-full p-2 border rounded mb-2"
         />
         <button onClick={handleAsk} className="bg-blue-600 text-white px-4 py-2 rounded">
           اسأل
         </button>

         {answer && (
           <div className="mt-4">
             <p className="text-sm">{answer.answer}</p>
             {answer.sources.length > 0 && (
               <div className="mt-2 text-xs text-gray-600">
                 المصادر: {answer.sources.map(s => s.title).join(', ')}
               </div>
             )}
           </div>
         )}
       </div>
     );
   }
   ```

**Deliverables:**
- ✅ 3 complete courses (30 lessons)
- ✅ AI tutor functional
- ✅ 100+ students enrolled
- ✅ Certificate system working
- ✅ 50%+ course completion rate

---

### Phase 5: Mobile Apps (Months 12-15)

**Objective:** Launch iOS and Android apps with feature parity to web

#### Month 12: iOS Development

**Tasks:**

1. **React Native Setup** (or Flutter)
   ```bash
   npx react-native init BahrMobile --template react-native-template-typescript
   ```

2. **Code Sharing**
   - Share business logic with web app
   - Platform-specific UI components

3. **Core Screens:**
   - Onboarding flow
   - Home/Feed
   - Analyze
   - Generate
   - Compete
   - Learn
   - Profile

4. **iOS-Specific Features:**
   - Face ID / Touch ID for login
   - Share sheet integration
   - Siri Shortcuts ("Analyze a verse")
   - Home screen widget (verse of the day)

5. **App Store Submission:**
   - Screenshots (6.5" and 5.5" displays)
   - Description in Arabic and English
   - Privacy policy
   - App review (1-2 weeks)

6. **TestFlight Beta:**
   - Invite 100 beta testers
   - Collect feedback via TestFlight

**Acceptance Criteria:**
- iOS app approved on App Store
- Feature parity with web
- >4.0 rating
- No critical bugs

---

#### Month 13-14: Android & Optimization

**Tasks:**

1. **Android-Specific Development**
   - Material Design 3 components
   - Android widgets
   - Google Assistant integration

2. **Performance Optimization**
   - App size <50 MB
   - Image optimization
   - Lazy loading
   - Code splitting

3. **Offline Mode**
   - Cache analyzed verses
   - Download courses for offline learning
   - Local SQLite database

4. **Push Notifications** (Firebase Cloud Messaging)
   - Competition reminders
   - Daily verse
   - Achievement unlocked

5. **Google Play Submission**

**Deliverables:**
- ✅ Android app on Google Play
- ✅ 1000+ combined installs
- ✅ >4.0 rating on both stores
- ✅ Offline mode working

---

### Phase 6: Monetization & Scale (Months 16-24)

**Objective:** Achieve profitability and sustainable growth

#### Revenue Streams

1. **Freemium Subscriptions**
   - Free: 10 analyses/day, 3 generations/day, ads
   - Premium ($4.99/month): unlimited, ad-free, exclusive badges
   - Pro ($14.99/month): + API access, advanced analytics

2. **API Revenue**
   - Pricing tiers (see earlier section)
   - Target: $1k-5k MRR from API

3. **Sponsorships**
   - Cultural organizations
   - Bookstores
   - Universities

4. **Competition Entry Fees**
   - Premium tournaments: $5 entry
   - 70% prize pool, 30% platform fee

5. **In-app Purchases**
   - Coin packs
   - Exclusive themes/avatars

#### Marketing Strategy

1. **SEO Optimization**
   - Rank for "علم العروض", "بحور الشعر", "محلل الشعر"

2. **Content Marketing**
   - Blog posts about prosody
   - YouTube tutorials

3. **Social Media**
   - Twitter/X for poets
   - TikTok for Gen Z

4. **Referral Program**
   - Invite friends → free Premium month

5. **University Partnerships**
   - B2B licensing for students

**Financial Projections:**
- Year 2: 50k users, 5% Premium conversion
- Revenue: ~$236k/year
- Path to profitability by optimizing costs

**Deliverables:**
- ✅ 50k+ users
- ✅ $20k+ MRR
- ✅ Break-even or profitable
- ✅ Team of 5+ people

---

## 6. Critical Dependencies & Integrations

### 6.1 External Services

| Service | Purpose | Provider Options | Estimated Cost |
|---------|---------|------------------|----------------|
| **Authentication** | OAuth, JWT | Auth0, Supabase, Custom | $0-100/mo |
| **Payment Processing** | Subscriptions | Stripe, Paddle | 2.9% + 30¢/transaction |
| **Email** | Notifications, newsletters | SendGrid, AWS SES | $0-50/mo |
| **Push Notifications** | Mobile alerts | Firebase, OneSignal | Free tier OK |
| **Video Streaming** | Live competitions | Agora, LiveKit | $0.99/1000 min |
| **TTS (Text-to-Speech)** | Audio verses | Google Cloud TTS, ElevenLabs | $4/1M chars |
| **CDN** | Static assets | Cloudflare | Free tier OK |
| **Cloud Storage** | Media files | S3, R2 | $0.023/GB |
| **Error Tracking** | Bug monitoring | Sentry | Free tier OK |
| **Analytics** | User behavior | Mixpanel, PostHog | Free tier OK |

### 6.2 Required Libraries & Tools

**Python (Backend):**
```requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
pydantic==2.5.0
redis==5.0.1
celery==5.3.4
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
transformers==4.35.2
torch==2.1.1
langchain==0.0.340
camel-tools==1.5.2
elasticsearch==8.11.0
reportlab==4.0.7
pytest==7.4.3
httpx==0.25.2
```

**JavaScript (Frontend):**
```package.json
{
  "dependencies": {
    "next": "14.0.4",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "typescript": "5.3.3",
    "tailwindcss": "3.3.6",
    "@tanstack/react-query": "5.12.2",
    "axios": "1.6.2",
    "zustand": "4.4.7",
    "react-hook-form": "7.48.2",
    "zod": "3.22.4",
    "socket.io-client": "4.6.0",
    "framer-motion": "10.16.16",
    "recharts": "2.10.3"
  }
}
```

### 6.3 Configuration Requirements

**Environment Variables (.env):**
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/bahr_db
REDIS_URL=redis://localhost:6379/0
ELASTICSEARCH_URL=http://localhost:9200

# API Keys
JWT_SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-...
STRIPE_SECRET_KEY=sk_test_...

# AWS (if using)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=bahr-media

# Email
SENDGRID_API_KEY=...
FROM_EMAIL=noreply@bahr.app

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# Feature Flags
ENABLE_AI_GENERATION=true
ENABLE_COMPETITIONS=true
```

---

## 7. Key Algorithms & Logic

### 7.1 Prosody Analysis Algorithm (High-Level)

```
INPUT: Arabic verse text
OUTPUT: {taqti3_pattern, bahr, confidence}

STEP 1: Text Normalization
  - Remove diacritics (optional)
  - Normalize hamza and alef variants
  - Clean whitespace

STEP 2: Phonetic Conversion
  - Add default vowels if missing (using context rules)
  - Convert to phoneme sequence
  - Example: "كتب" → /ka/ /ta/ /ba/

STEP 3: Prosodic Pattern Extraction
  - Map phonemes to prosodic units:
    - CV (consonant-vowel) = / (haraka)
    - CVC or CVV = /o (haraka + sukun)
  - Generate pattern string

STEP 4: Tafa'il Matching
  - Sliding window over pattern
  - Match known tafa'il (فعولن, مفاعيلن, etc.)
  - Allow fuzzy matching for zihafat

STEP 5: Bahr Detection
  - Compare tafa'il sequence to 16 bahr templates
  - Calculate confidence score
  - Return best match

STEP 6: Error Detection (optional)
  - Identify deviations from expected pattern
  - Suggest corrections
```

### 7.2 AI Generation with Prosody Constraints

```
INPUT: {bahr, theme, length}
OUTPUT: generated_verses[]

STEP 1: Format Prompt
  prompt = "<|bahr|>{bahr}<|verse|>"

STEP 2: Generate Token-by-Token
  FOR each position:
    - Get top-k candidate tokens from LLM
    - FOR each candidate:
      - Append to current sequence
      - Compute prosodic pattern so far
      - Check if pattern matches expected bahr
    - FILTER OUT tokens that violate meter
    - Sample from remaining valid tokens

STEP 3: Post-Generation Validation
  - Analyze generated verse
  - If meter incorrect: regenerate OR apply correction

STEP 4: Quality Check
  - Coherence check (does it make sense?)
  - Diversity check (not repetitive?)
  - If fails: regenerate with adjusted parameters
```

### 7.3 Competition Scoring Formula

```
INPUT: verse_text, expected_bahr, audience_votes
OUTPUT: total_score (0-100)

COMPONENTS:

1. Meter Score (40 points)
   - Analyze verse
   - IF bahr_detected == expected_bahr:
       meter_score = 40 * confidence
     ELSE:
       meter_score = 0

2. Meaning Quality (30 points)
   - Use GPT-4 or custom model to evaluate:
     - Coherence (does it make sense?)
     - Depth (is there meaning beyond surface?)
     - Creativity (originality)
   - Scale 0-30

3. Beauty Score (20 points)
   - Vocabulary richness (unique words / total words)
   - Figurative language (metaphors, imagery)
   - Emotional impact
   - Scale 0-20

4. Audience Votes (10 points)
   - (num_votes_for / total_votes) * 10

TOTAL = meter_score + meaning_score + beauty_score + audience_score
```

---

## 8. Testing Strategy

### 8.1 Unit Tests

**Prosody Engine:**
- Test all 16 bahrs with known verses
- Test edge cases (very short, very long, non-Arabic)
- Test with and without diacritics
- Target: 90%+ accuracy, 80%+ code coverage

**API Endpoints:**
- Test all endpoints with valid/invalid inputs
- Test authentication and authorization
- Test rate limiting

### 8.2 Integration Tests

- End-to-end flow: user registration → analyze verse → competition
- Database transactions
- Cache invalidation

### 8.3 Performance Tests

- Load testing: 100 concurrent users
- Stress testing: 1000 concurrent users
- Latency: p95 <500ms for API calls
- Database query optimization

### 8.4 User Acceptance Testing (UAT)

- Beta testing with 50-100 users
- Collect feedback via surveys
- Bug tracking in GitHub Issues

---

## 9. Deployment Strategy

### 9.1 Development Environment

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: bahr_db
      POSTGRES_USER: bahr_user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  elasticsearch:
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://bahr_user:password@postgres:5432/bahr_db
      REDIS_URL: redis://redis:6379/0

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000/api/v1

volumes:
  postgres_data:
```

### 9.2 Staging Environment

**Option A: Railway**
- Connect GitHub repo
- Auto-deploy on push to `develop` branch
- Managed PostgreSQL and Redis

**Option B: Render**
- Web service for FastAPI
- Static site for Next.js
- Managed databases

### 9.3 Production Environment

**Cloud Provider:** AWS, GCP, or DigitalOcean

**Infrastructure:**
- Kubernetes cluster (3 nodes minimum)
- Load balancer (NGINX or cloud LB)
- Managed PostgreSQL (RDS, Cloud SQL)
- Managed Redis (ElastiCache, Memorystore)
- Object storage (S3, Cloud Storage)
- CDN (Cloudflare)

**CI/CD Pipeline:**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pytest

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker images
        run: docker build -t bahr-backend:${{ github.sha }} ./backend
      - name: Push to registry
        run: docker push bahr-backend:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: kubectl set image deployment/backend backend=bahr-backend:${{ github.sha }}
```

---

## 10. Security Considerations

### 10.1 Authentication & Authorization

- JWT tokens with expiration (15 min access, 7 day refresh)
- Password hashing: bcrypt with cost factor 12
- OAuth 2.0 for social login
- RBAC (Role-Based Access Control): admin, moderator, user

### 10.2 API Security

- Rate limiting: 100 requests/min per IP
- CORS: whitelist allowed origins
- Input validation: Pydantic schemas
- SQL injection prevention: SQLAlchemy ORM (no raw SQL)
- XSS prevention: sanitize user inputs

### 10.3 Data Protection

- HTTPS only (TLS 1.3)
- Encrypt sensitive data at rest (API keys, passwords)
- Regular backups (daily, retained 30 days)
- GDPR compliance (data export, deletion)

### 10.4 Monitoring & Logging

- Error tracking: Sentry
- Logging: Structured logs to ELK stack
- Alerting: Prometheus alerts for downtime, high latency
- DDoS protection: Cloudflare

---

## 11. Ambiguities & Questions for Human Clarification

### 11.1 Prosody Analysis

❓ **Tashkeel (Diacritics) Handling:**
- Should the analyzer *require* fully diacriticized text, or attempt to infer vowels?
- If inferring, what accuracy is acceptable? (Will introduce errors)
- **Recommendation:** Support both modes (with/without tashkeel), higher accuracy when provided

❓ **Dialect Poetry:**
- The doc mentions support for "شعر شعبي/نبطي" (colloquial/Nabati poetry)
- These don't follow classical prosody rules - how to handle?
- **Recommendation:** Phase 2 feature, requires separate models/rules

❓ **Modern Free Verse (شعر حر):**
- Does not follow traditional bahrs
- Should platform support analysis? If so, what metrics?
- **Recommendation:** Future scope, not MVP

### 11.2 AI Generation

❓ **Training Data Licensing:**
- Is scraping classical poetry (public domain) legally safe?
- Do we need explicit permission from poets for modern works?
- **Recommendation:** Consult legal expert, use only public domain for MVP

❓ **Content Moderation:**
- AI might generate offensive/inappropriate content
- How strict should filtering be?
- **Recommendation:** Implement content filter, allow users to report, human moderators

❓ **Persona-Based Generation:**
- "Write like Al-Mutanabbi" - how to train this?
- Requires fine-tuning on specific poet's corpus
- **Recommendation:** Phase 3 feature, start with generic style only

### 11.3 Competitions

❓ **Judging Fairness:**
- How to prevent bias in AI judging (meaning/beauty scores)?
- Audience votes can be gamed (bots, friends)
- **Recommendation:** Combine AI + audience + expert human judges for high-stakes competitions

❓ **Prize Distribution:**
- Legal implications of monetary prizes?
- Tax reporting requirements?
- **Recommendation:** Consult legal/financial advisor, start with virtual currency (coins) only

❓ **Anti-Cheating:**
- How to detect if user is copying from existing poetry databases?
- **Recommendation:** Fuzzy matching against library, flag high similarity (>80%) for review

### 11.4 Monetization

❓ **Pricing Strategy:**
- Is $4.99/month competitive for Arabic market?
- Purchasing power varies widely across MENA
- **Recommendation:** Market research, consider regional pricing

❓ **API Abuse:**
- How to prevent competitors from scraping our API?
- **Recommendation:** API key rotation, CAPTCHAs for suspicious patterns, legal ToS

❓ **Subscription Management:**
- Which payment gateways work best in MENA?
- Stripe coverage is limited in some countries
- **Recommendation:** Use Stripe + Paddle for broader coverage, consider local gateways (Moyasar, PayTabs)

### 11.5 Technical

❓ **Model Hosting Costs:**
- 13B parameter model (Jais) is expensive to serve
- vLLM helps, but still ~$500-1000/month for GPU
- **Recommendation:** Start with smaller model (AraGPT2), upgrade when revenue supports it, or use API (OpenAI GPT-4 with Arabic prompt)

❓ **Elasticsearch vs. PostgreSQL Full-Text Search:**
- Elasticsearch adds complexity and cost
- PostgreSQL has decent Arabic full-text search
- **Recommendation:** Start with PostgreSQL, migrate to Elasticsearch when library >50k verses

❓ **Mobile: React Native vs. Flutter:**
- React Native: easier code sharing with web (React)
- Flutter: better performance, growing Arabic support
- **Recommendation:** React Native for faster MVP, consider Flutter if performance issues

---

## 12. Success Metrics & KPIs

### Phase 1 (MVP - Analyzer)
- ✅ 90%+ accuracy on common bahrs
- ✅ <200ms API response time (cached)
- ✅ 10+ beta testers provide positive feedback
- ✅ 1000+ verses analyzed in first month

### Phase 2 (AI Poet)
- ✅ 85%+ generated verses follow correct meter
- ✅ 7+/10 average human rating for meaning
- ✅ <5s generation time
- ✅ 500+ generations in first month

### Phase 3 (Competitions)
- ✅ 1000+ matches completed
- ✅ 60%+ user retention (return for 2nd match)
- ✅ 100+ active leaderboard participants
- ✅ 4+/5 user satisfaction

### Phase 4 (Learning)
- ✅ 50%+ course completion rate
- ✅ 100+ enrolled students
- ✅ 80%+ quiz passing rate
- ✅ 100+ questions asked to AI tutor

### Phase 5 (Mobile)
- ✅ 5k+ downloads in first month
- ✅ 4.0+ rating on App Store & Google Play
- ✅ 30%+ of web users install app
- ✅ <1% crash rate

### Phase 6 (Monetization)
- ✅ 50k+ total users
- ✅ 5%+ conversion to Premium
- ✅ $20k+ MRR
- ✅ Break-even or profitable

---

## 13. Codex-Specific Implementation Guidelines

### 13.1 Input/Output Formats

When Codex implements endpoints, use these exact schemas:

**Analyze Endpoint:**
```json
// Request
POST /api/v1/analyze
{
  "text": "إذا غامَرتَ في شَرَفٍ مَرومِ",
  "detect_bahr": true,
  "suggest_corrections": false
}

// Response
{
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
```

**Generate Endpoint:**
```json
// Request
POST /api/v1/generate
{
  "bahr": "الطويل",
  "theme": "الحكمة",
  "length": 2,
  "temperature": 0.7,
  "persona": null
}

// Response
{
  "verses": [
    {
      "text": "...",
      "taqti3": "...",
      "bahr": "الطويل"
    }
  ],
  "generation_time_ms": 3200
}
```

### 13.2 Data Types & Validation

**Pydantic Models (Backend):**
```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=500)
    detect_bahr: bool = True
    suggest_corrections: bool = False

    @validator('text')
    def validate_arabic(cls, v):
        # Check if text contains Arabic characters
        if not any('\u0600' <= c <= '\u06FF' for c in v):
            raise ValueError('Text must contain Arabic characters')
        return v

class BahrInfo(BaseModel):
    name_ar: str
    name_en: str
    confidence: float = Field(..., ge=0.0, le=1.0)

class AnalyzeResponse(BaseModel):
    text: str
    taqti3: str
    bahr: Optional[BahrInfo]
    errors: List[str]
    suggestions: List[str]
    score: int = Field(..., ge=0, le=100)
```

**TypeScript Types (Frontend):**
```typescript
export interface AnalyzeRequest {
  text: string;
  detect_bahr?: boolean;
  suggest_corrections?: boolean;
}

export interface BahrInfo {
  name_ar: string;
  name_en: string;
  confidence: number;
}

export interface AnalyzeResponse {
  text: string;
  taqti3: string;
  bahr: BahrInfo | null;
  errors: string[];
  suggestions: string[];
  score: number;
}
```

### 13.3 Code Style & Conventions

**Python (Backend):**
- Follow PEP 8
- Use Black for formatting
- Type hints for all functions
- Docstrings for public APIs

```python
def perform_taqti3(verse: str) -> str:
    """
    Perform prosodic scansion (taqti3) on an Arabic verse.

    Args:
        verse: The Arabic verse text (with or without diacritics)

    Returns:
        The tafa'il pattern string (e.g., "فعولن مفاعيلن فعولن مفاعيلن")

    Raises:
        ValueError: If verse is empty or contains no Arabic text

    Example:
        >>> perform_taqti3("إذا غامَرتَ في شَرَفٍ مَرومِ")
        "فعولن مفاعيلن فعولن مفاعيلن"
    """
    pass
```

**TypeScript (Frontend):**
- Use ESLint + Prettier
- Functional components (React)
- TypeScript strict mode

```typescript
interface AnalyzeFormProps {
  onSubmit: (text: string) => Promise<void>;
  loading?: boolean;
}

export const AnalyzeForm: React.FC<AnalyzeFormProps> = ({ onSubmit, loading = false }) => {
  // Component implementation
};
```

### 13.4 Error Handling

**Backend:**
```python
from fastapi import HTTPException

@router.post("/analyze")
async def analyze_verse(request: AnalyzeRequest):
    try:
        result = perform_analysis(request.text)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in analyze: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

**Frontend:**
```typescript
try {
  const result = await analyzeVerse(text);
  setResult(result);
} catch (error) {
  if (error.response?.status === 400) {
    toast.error('نص غير صالح');
  } else {
    toast.error('حدث خطأ، يرجى المحاولة مرة أخرى');
  }
}
```

---

## 14. Implementation Checklist for Codex

### Phase 1: MVP Analyzer

**Week 1-2: Prosody Engine**
- [ ] Implement `normalize_arabic_text()` function
- [ ] Implement `text_to_phonemes()` function
- [ ] Implement `perform_taqti3()` algorithm
- [ ] Create `BahrDetector` class
- [ ] Write unit tests for all 16 bahrs
- [ ] Achieve 90%+ accuracy on test dataset

**Week 3-4: API & Database**
- [ ] Create PostgreSQL schema (users, poems, verses, bahrs, tafa3il, analysis_cache)
- [ ] Write Alembic migration scripts
- [ ] Seed database with 16 bahrs data
- [ ] Implement FastAPI `/analyze` endpoint
- [ ] Add Redis caching layer
- [ ] Generate Swagger documentation
- [ ] Write integration tests

**Week 5-6: Frontend**
- [ ] Initialize Next.js project with TypeScript
- [ ] Configure Tailwind CSS with RTL support
- [ ] Add Arabic fonts (Cairo, Amiri)
- [ ] Create Home page component
- [ ] Create Analyze page component
- [ ] Create AnalyzeResults component
- [ ] Implement API client (axios)
- [ ] Test mobile responsiveness

**Week 7-8: Testing & Deployment**
- [ ] Write end-to-end tests
- [ ] Perform load testing (100 concurrent users)
- [ ] Deploy to staging (Railway/Render)
- [ ] Setup production database (Supabase/Railway)
- [ ] Recruit 10 beta testers
- [ ] Fix critical bugs
- [ ] Write API documentation

### Phase 2: AI Poet (Abbreviated - see full roadmap above)
- [ ] Collect 100k+ verses dataset
- [ ] Clean and validate data
- [ ] Fine-tune Arabic LLM (AraGPT2 or Jais)
- [ ] Implement `/generate` endpoint
- [ ] Add rate limiting
- [ ] Integrate in frontend
- [ ] Test generation quality

### Phase 3-6: (Follow detailed roadmap above)

---

## 15. Final Notes for Codex

### Task Interpretation Guidelines

1. **When generating prosody analysis code:**
   - Prioritize accuracy over speed (can optimize later)
   - Handle both diacriticized and non-diacriticized text
   - Return confidence scores, not just binary results
   - Test with verses from all 16 bahrs

2. **When generating API endpoints:**
   - Always validate inputs with Pydantic
   - Return consistent error structures
   - Log errors for debugging
   - Add OpenAPI descriptions

3. **When generating frontend components:**
   - Support RTL (dir="rtl")
   - Use Arabic fonts
   - Mobile-first responsive design
   - Loading states for async operations

4. **When generating database migrations:**
   - Add indexes for foreign keys
   - Add indexes for frequently queried columns (e.g., verse_text_hash)
   - Use JSONB for flexible schemas (e.g., metadata)
   - Include rollback logic

5. **When generating tests:**
   - Unit tests for pure functions (prosody engine)
   - Integration tests for API endpoints
   - Use fixtures for database state
   - Mock external services (OpenAI API, payment gateways)

### Expected Codex Workflow

1. **Receive implementation task** (e.g., "Implement the taqti3 algorithm")
2. **Read relevant specification** from this document
3. **Generate code** following:
   - Correct file path (`app/core/taqti3.py`)
   - Type hints and docstrings
   - Error handling
   - Unit tests (`tests/core/test_taqti3.py`)
4. **Validate against acceptance criteria** (e.g., 90%+ accuracy)
5. **If acceptance not met:** iterate with adjustments

### Common Pitfalls to Avoid

❌ **Don't:**
- Hardcode Arabic text in code (use database/config files)
- Ignore RTL layout (causes UI issues)
- Skip validation (security risk)
- Use blocking I/O in async functions
- Commit secrets to Git

✅ **Do:**
- Use environment variables for config
- Add comprehensive error messages in Arabic for user-facing errors
- Cache expensive operations (prosody analysis, AI generation)
- Version the API (v1, v2) for breaking changes
- Document complex algorithms with comments

---

## 16. Quick Reference

### Project Structure
```
bahr/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/          # Prosody engine
│   │   ├── api/v1/        # API endpoints
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── utils/
│   ├── tests/
│   ├── migrations/        # Alembic
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js pages
│   │   ├── components/
│   │   ├── lib/           # API client, utils
│   │   └── types/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .github/workflows/     # CI/CD
└── README.md
```

### Essential Commands

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Docker
docker-compose up -d

# Tests
pytest backend/tests/
npm test

# Linting
black backend/
flake8 backend/
npm run lint
```

### Key URLs (Local Development)
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **PostgreSQL:** localhost:5432
- **Redis:** localhost:6379
- **Elasticsearch:** localhost:9200

---

## Conclusion

This implementation plan provides Codex (or any AI coding assistant) with:

✅ **Clear technical specifications** for all platform modules
✅ **Detailed API endpoint contracts** with exact input/output formats
✅ **Database schema** with all required tables and relationships
✅ **Phase-by-phase roadmap** with concrete tasks and acceptance criteria
✅ **Code examples** in Python and TypeScript
✅ **Testing strategies** and performance targets
✅ **Deployment guidelines** for development, staging, and production
✅ **Security best practices**
✅ **Highlighted ambiguities** requiring human clarification

**Next Steps:**
1. Review and approve this plan
2. Clarify ambiguities (see Section 11)
3. Begin Phase 0 (setup)
4. Feed individual tasks to Codex with references to relevant sections

**Estimated Timeline:**
- Phase 1 (MVP): 2 months
- Phases 2-3 (AI + Competitions): 6 months
- Phases 4-5 (Learning + Mobile): 7 months
- **Total to market-ready product:** 12-15 months

**Human Oversight Required:**
- Architecture decisions (database choice, cloud provider)
- UI/UX design approval
- Content creation (videos, lessons)
- Legal/compliance (data privacy, payment processing)
- Quality assurance (final testing, user feedback)

This plan is **ready for handoff to Codex** for immediate implementation. 🚀
