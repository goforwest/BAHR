# 🎯 Phase 1: MVP - المواصفات التقنية المفصلة
## محرك تحليل الشعر العربي (Poetry Analysis Engine)

---

## 📋 نظرة عامة

**الهدف:** بناء MVP لمحرك تحليل الشعر العربي يشمل:
- تقطيع عروضي تلقائي (Automatic Prosodic Analysis)  
- تحديد البحر الشعري (Meter Detection)
- واجهة ويب تفاعلية (Interactive Web Interface)
- API للتكامل مع تطبيقات أخرى

**المدة:** 6-8 أسابيع  
**الأولوية:** عالية جداً (Foundation للمشروع كله)

## ⚠️ حدود النطاق (Scope Constraints - MVP)

- خارج النطاق: المسابقات (competitions)، التفاعل الاجتماعي (follows/comments/likes)، التحليلات المتقدمة، والملفات الصوتية. هذه مؤجلة لما بعد الإطلاق.  
- داخل النطاق: محرك العروض (قواعد فقط في هذه المرحلة)، واجهة تحليل أساسية، API التحليل، ذاكرة مؤقتة Redis، وتوثيق كامل.

## ✅ معايير القبول (Acceptance Criteria)

- دقة كشف البحر على مجموعة تحقق 100–200 بيت كلاسيكي: ≥ 70% (نهاية Week 6).  
- زمن الاستجابة لبيت واحد (P95): ≤ 500ms على جهاز مطوّر M1/8GB.  
- رسائل الأخطاء ثنائية اللغة وفق `ERROR_HANDLING_STRATEGY.md` مع 429 عند تجاوز الحد.  
- عرض بدائل للبحور عندما تكون الثقة < 0.85.  
- تغطية اختبار ≥ 70% في وحدات المحرك الأساسية (Normalizer/Segmenter/Matcher/Meter).

## 🧩 متطلبات البيانات (Dataset Target)

- مستهدف MVP: 100–200 بيت مُعنّون (نص، بحر، تقطيع/نمط إن أمكن، مصدر، عصر).  
- مواصفات الحقول في `docs/research/DATASET_SPEC.md`.  
- تجميع تدريجي وتوسعة لاحقة إلى ≥ 500 بيت قبل Week 12.

---

## 🎯 المتطلبات الوظيفية (Functional Requirements)

### 1️⃣ **محرك التقطيع العروضي**

#### Input:
- نص عربي (بيت شعر أو أكثر)
- خيارات اختيارية:
  - إزالة التشكيل (تلقائي/يدوي)
  - نوع التحليل (دقيق/سريع)

#### Processing:
- تطبيع النص العربي (Arabic Text Normalization)
- تقطيع صوتي (Phonetic Segmentation) 
- تحليل التفاعيل (Prosodic Pattern Analysis)
- مطابقة مع البحور الشعرية (Meter Matching)

#### Output:
```json
{
  "input_text": "أَلا في سَبيلِ المَجدِ ما أَنا فاعِلُ",
  "normalized_text": "الا في سبيل المجد ما انا فاعل",
  "prosodic_analysis": {
    "taqti3": "مُسْتَفْعِلُنْ فَاعِلُنْ مُسْتَفْعِلُنْ فَاعِلُنْ",
    "pattern": "- u - - | - u - | - u - - | - u -",
    "syllable_count": 14
  },
  "meter_detection": {
    "detected_meter": "الرجز",
    "confidence": 0.95,
    "alternative_meters": [
      {"name": "الرجز المشطور", "confidence": 0.12}
    ]
  },
  "quality_score": 0.92,
  "suggestions": [
    "البيت يتبع بحر الرجز بدقة عالية"
  ]
}
```

### 2️⃣ **واجهة المستخدم (Web Interface)**

#### الصفحة الرئيسية:
- **Hero Section:** مقدمة عن بَحْر
- **Quick Analyzer:** حقل إدخال سريع للتجربة
- **Features Overview:** شرح الميزات الأساسية
- **Examples:** أمثلة تفاعلية

#### صفحة التحليل:
- **Input Area:** محرر نص عربي مع دعم RTL
- **Settings Panel:** خيارات التحليل
- **Results Section:** عرض النتائج بطريقة جذابة
- **Visual Representation:** تمثيل بصري للتقطيع

#### عناصر UI مطلوبة:
```
Components:
├── TextAnalyzer
│   ├── InputArea (RTL text editor)
│   ├── SettingsPanel (analysis options)
│   ├── AnalyzeButton (loading states)
│   └── ResultsDisplay
│
├── Results  
│   ├── ProsodyVisualization
│   ├── MeterInfo
│   ├── QualityScore
│   └── Suggestions
│
├── Examples
│   ├── PresetVerses
│   └── QuickDemo
│
└── Layout
    ├── Header (navigation)
    ├── Footer (links)
    └── Sidebar (optional)
```

### 3️⃣ **REST API**

#### Core Endpoints:

```
POST /api/v1/analyze
GET  /api/v1/meters
GET  /api/v1/examples
GET  /api/v1/health
POST /api/v1/datasets/verses   # (Admin-only) إدخال/استيراد بيانات مُعنونة
```

#### Detailed Specifications:

**POST /api/v1/analyze**
```json
// Request
{
  "text": "أَلا في سَبيلِ المَجدِ ما أَنا فاعِلُ",
  "options": {
    "remove_diacritics": true,
    "analysis_mode": "accurate", // "accurate" | "fast"
    "return_alternatives": true
  }
}

// Response
{
  "success": true,
  "data": {
    // ... (same as processing output above)
  },
  "processing_time_ms": 156,
  "request_id": "abc123"
}
```

**GET /api/v1/meters**
**POST /api/v1/datasets/verses** (Admin-only)
```json
// Request (JSONL batch supported)
{
  "records": [
    {
      "text": "قفا نبك من ذكرى حبيب ومنزل",
      "meter": "الطويل",
      "era": "classical",
      "source": "المعلقات",
      "notes": ""
    }
  ]
}

// Response
{
  "success": true,
  "data": {"inserted": 1, "duplicates": 0},
  "request_id": "abc123"
}
```

Rate Limiting (MVP): 100 طلب/الساعة لكل IP (429 عند التجاوز).
```json
// Response
{
  "success": true,
  "data": [
    {
      "id": "rajaz",
      "name_ar": "الرجز", 
      "name_en": "Rajaz",
      "pattern": "مُسْتَفْعِلُنْ مُسْتَفْعِلُنْ مُسْتَفْعِلُنْ",
      "description": "من أبسط البحور وأكثرها استعمالاً",
      "example": "قِفا نَبْكِ مِنْ ذِكْرى حَبيبٍ وَمَنْزِلِ"
    }
    // ... other meters
  ]
}
```

---

## 🏗️ التصميم المعماري (System Architecture)

### High-Level Architecture:

```
┌─────────────────────────────────────────────┐
│              Frontend (Next.js)              │
│  ┌─────────────┐ ┌─────────────┐           │
│  │ UI Components│ │ State Mgmt  │           │
│  └─────────────┘ └─────────────┘           │
└─────────────────┬───────────────────────────┘
                  │ HTTP/REST
┌─────────────────▼───────────────────────────┐
│              API Gateway                     │
│           (FastAPI + Middleware)            │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           Business Logic Layer              │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │      Prosody Analysis Engine        │   │
│  │  ┌─────────────┐ ┌─────────────┐   │   │
│  │  │ Normalizer  │ │  Pattern    │   │   │
│  │  │             │ │  Matcher    │   │   │
│  │  └─────────────┘ └─────────────┘   │   │
│  │  ┌─────────────┐ ┌─────────────┐   │   │
│  │  │ Segmenter   │ │   Meter     │   │   │
│  │  │             │ │  Detector   │   │   │
│  │  └─────────────┘ └─────────────┘   │   │
│  └─────────────────────────────────────┘   │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│              Data Layer                     │
│  ┌─────────────┐ ┌─────────────┐           │
│  │ PostgreSQL  │ │   Redis     │           │
│  │ (Metadata)  │ │  (Cache)    │           │
│  └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────┘
```

---

## 🗄️ تصميم قاعدة البيانات (Database Design)

### PostgreSQL Schema:

```sql
-- Prosodic Meters (البحور)
CREATE TABLE meters (
    id SERIAL PRIMARY KEY,
    name_ar VARCHAR(50) NOT NULL UNIQUE,
    name_en VARCHAR(50) NOT NULL,
    pattern TEXT NOT NULL,
    description TEXT,
    example_verse TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Prosodic Patterns (التفاعيل)
CREATE TABLE tafa3il (
    id SERIAL PRIMARY KEY,
    name_ar VARCHAR(50) NOT NULL,
    name_en VARCHAR(50),
    symbol VARCHAR(20) NOT NULL, -- مُسْتَفْعِلُنْ
    pattern VARCHAR(20) NOT NULL, -- - u - -
    meter_id INTEGER REFERENCES meters(id),
    position_in_meter INTEGER, -- موقع التفعيلة في البحر
    variations TEXT[], -- الزحافات المختلفة
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analysis Cache (تخزين نتائج التحليل)
CREATE TABLE analysis_cache (
    id SERIAL PRIMARY KEY,
    text_hash VARCHAR(64) NOT NULL UNIQUE, -- MD5 of normalized text
    original_text TEXT NOT NULL,
    normalized_text TEXT NOT NULL,
    taqti3_result JSONB NOT NULL,
    detected_meter_id INTEGER REFERENCES meters(id),
    confidence_score DECIMAL(3,2),
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_count INTEGER DEFAULT 1,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Request Logs (لمراقبة الاستخدام)
CREATE TABLE api_requests (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(100) NOT NULL,
    method VARCHAR(10) NOT NULL,
    request_body JSONB,
    response_status INTEGER NOT NULL,
    processing_time_ms INTEGER,
    client_ip INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_meters_name_ar ON meters(name_ar);
CREATE INDEX idx_analysis_cache_text_hash ON analysis_cache(text_hash);
CREATE INDEX idx_analysis_cache_meter ON analysis_cache(detected_meter_id);
CREATE INDEX idx_analysis_cache_created_at ON analysis_cache(created_at);
CREATE INDEX idx_api_requests_created_at ON api_requests(created_at);
CREATE INDEX idx_api_requests_endpoint ON api_requests(endpoint);
```

### Redis Cache Structure:

```
Keys:
├── analysis:{text_hash}     # كاش نتائج التحليل
├── meters:all              # كاش جميع البحور  
├── stats:daily:{date}      # إحصائيات يومية
└── rate_limit:{ip}         # حد الطلبات حسب IP
```

---

## 💻 تفاصيل التطوير (Development Details)

### Backend Structure (FastAPI):

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app setup
│   ├── config.py               # Configuration settings
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── analyze.py      # Analysis endpoints
│   │   │   ├── meters.py       # Meters endpoints
│   │   │   └── health.py       # Health check
│   │   └── middleware.py       # Custom middleware
│   │
│   ├── core/                   # Core business logic
│   │   ├── __init__.py
│   │   ├── prosody/
│   │   │   ├── __init__.py
│   │   │   ├── normalizer.py   # Text normalization
│   │   │   ├── segmenter.py    # Syllable segmentation  
│   │   │   ├── analyzer.py     # Prosodic analysis
│   │   │   └── detector.py     # Meter detection
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── arabic.py       # Arabic text utilities
│   │       └── cache.py        # Caching utilities
│   │
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   ├── base.py             # Base model class
│   │   ├── meter.py            # Meter model
│   │   ├── analysis.py         # Analysis cache model
│   │   └── request_log.py      # Request log model
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── analyze.py          # Analysis request/response
│   │   ├── meter.py            # Meter schemas
│   │   └── common.py           # Common schemas
│   │
│   └── database/
│       ├── __init__.py
│       ├── connection.py       # Database connection
│       ├── migrations/         # Alembic migrations
│       └── seeds/              # Initial data
│
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── pytest.ini
└── tests/
    ├── __init__.py
    ├── test_api/
    ├── test_core/
    └── test_models/
```

### Frontend Structure (Next.js):

```
frontend/
├── src/
│   ├── app/                    # App Router (Next.js 13+)
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── analyze/
│   │   │   └── page.tsx        # Analysis page
│   │   └── globals.css         # Global styles
│   │
│   ├── components/             # Reusable components
│   │   ├── ui/                 # Basic UI components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── card.tsx
│   │   │   └── loading.tsx
│   │   ├── analyzer/
│   │   │   ├── TextInput.tsx   # Arabic text input
│   │   │   ├── AnalysisSettings.tsx
│   │   │   ├── ResultsDisplay.tsx
│   │   │   └── ProsodyVisualization.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Navigation.tsx
│   │   └── examples/
│   │       ├── PresetVerses.tsx
│   │       └── QuickDemo.tsx
│   │
│   ├── lib/                    # Utilities & configuration
│   │   ├── api.ts              # API client
│   │   ├── utils.ts            # Helper functions
│   │   ├── constants.ts        # App constants
│   │   └── types.ts            # TypeScript types
│   │
│   ├── hooks/                  # Custom React hooks
│   │   ├── useAnalyze.ts       # Analysis hook
│   │   ├── useMeters.ts        # Meters data hook
│   │   └── useLocalStorage.ts  # Local storage hook
│   │
│   └── styles/                 # Styling
│       ├── globals.css         # Global styles
│       ├── arabic.css          # Arabic typography
│       └── components.css      # Component styles
│
├── public/
│   ├── images/
│   ├── icons/
│   └── favicon.ico
│
├── package.json
├── next.config.js              # Next.js configuration
├── tailwind.config.js          # Tailwind CSS config
├── tsconfig.json               # TypeScript config
├── Dockerfile
└── __tests__/
    ├── components/
    ├── pages/
    └── utils/
```

---

## 🔧 التقنيات والمكتبات (Tech Stack)

### Backend Dependencies:

```python
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
alembic==1.13.0
psycopg2-binary==2.9.9
redis==5.0.1

# Arabic NLP
camel-tools==1.5.4
pyarabic==0.6.15
arabic-reshaper==3.0.0

# Data Processing
pydantic==2.5.0
numpy==1.25.2
pandas==2.1.3

# Utilities
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
httpx==0.25.2

# Monitoring & Logging
structlog==23.2.0
sentry-sdk[fastapi]==1.38.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2
```

### Frontend Dependencies:

```json
{
  "dependencies": {
    "next": "14.0.3",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "typescript": "^5.0.0",
    
    "tailwindcss": "^3.3.0",
    "@tailwindcss/typography": "^0.5.10",
    "clsx": "^2.0.0",
    "class-variance-authority": "^0.7.0",
    
    "zustand": "^4.4.7",
    "react-hook-form": "^7.48.0",
    "zod": "^3.22.4",
    
    "axios": "^1.6.0",
    "react-query": "^3.39.3",
    
    "framer-motion": "^10.16.0",
    "lucide-react": "^0.294.0",
    
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-select": "^2.0.0",
    
    "recharts": "^2.8.0"
  },
  
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    
    "eslint": "^8.0.0",
    "eslint-config-next": "14.0.3",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    
    "prettier": "^3.0.0",
    "prettier-plugin-tailwindcss": "^0.5.0",
    
    "@testing-library/react": "^13.0.0",
    "@testing-library/jest-dom": "^6.0.0",
    "jest": "^29.0.0",
    "jest-environment-jsdom": "^29.0.0"
  }
}
```

---

## 🧪 استراتيجية الاختبار (Testing Strategy)

### Backend Testing:

```python
# tests/test_core/test_analyzer.py
import pytest
from app.core.prosody.analyzer import ProsodyAnalyzer

class TestProsodyAnalyzer:
    def setup_method(self):
        self.analyzer = ProsodyAnalyzer()
    
    def test_basic_analysis(self):
        text = "أَلا في سَبيلِ المَجدِ ما أَنا فاعِلُ"
        result = self.analyzer.analyze(text)
        
        assert result.success is True
        assert result.detected_meter == "الرجز"
        assert result.confidence > 0.8
    
    def test_normalization(self):
        text_with_diacritics = "أَلا في سَبيلِ"
        text_normalized = "الا في سبيل"
        
        result = self.analyzer.normalize_text(text_with_diacritics)
        assert result == text_normalized
    
    @pytest.mark.parametrize("meter,example", [
        ("الطويل", "طَويلٌ لَهُ ما بَينَ السَماءِ وَأَرضِها"),
        ("الكامل", "كَمَلَ الجَمالُ مِنَ البَهاءِ وَالحُسنِ"),
    ])
    def test_meter_detection(self, meter, example):
        result = self.analyzer.analyze(example)
        assert result.detected_meter == meter
```

### Frontend Testing:

```typescript
// __tests__/components/TextInput.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import TextInput from '@/components/analyzer/TextInput'

describe('TextInput Component', () => {
  test('renders text input with RTL support', () => {
    render(<TextInput onAnalyze={jest.fn()} />)
    
    const textArea = screen.getByRole('textbox')
    expect(textArea).toBeInTheDocument()
    expect(textArea).toHaveAttribute('dir', 'rtl')
  })
  
  test('calls onAnalyze when analyze button is clicked', () => {
    const mockAnalyze = jest.fn()
    render(<TextInput onAnalyze={mockAnalyze} />)
    
    const textArea = screen.getByRole('textbox')
    const analyzeButton = screen.getByText('تحليل')
    
    fireEvent.change(textArea, { 
      target: { value: 'أَلا في سَبيلِ المَجدِ ما أَنا فاعِلُ' } 
    })
    fireEvent.click(analyzeButton)
    
    expect(mockAnalyze).toHaveBeenCalledWith(
      'أَلا في سَبيلِ المَجدِ ما أَنا فاعِلُ'
    )
  })
})
```

### Integration Testing:

```python
# tests/test_api/test_analyze.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_analyze_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/analyze", json={
            "text": "أَلا في سَبيلِ المَجدِ ما أَنا فاعِلُ",
            "options": {"remove_diacritics": True}
        })
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "prosodic_analysis" in data["data"]
    assert "meter_detection" in data["data"]
    assert data["data"]["meter_detection"]["confidence"] > 0.5
```

---

## 📊 المقاييس والمراقبة (Metrics & Monitoring)

### Key Performance Indicators (KPIs):

```python
# Metrics to track
METRICS = {
    # Performance
    "response_time_p95": "< 500ms",
    "response_time_avg": "< 200ms", 
    "accuracy_rate": "> 90%",
    
    # Availability
    "uptime": "> 99%",
    "error_rate": "< 1%",
    
    # Usage
    "requests_per_day": "target: 1000+",
    "unique_users_daily": "target: 50+",
    "cache_hit_rate": "> 70%"
}
```

### Logging Strategy:

```python
# app/core/logger.py
import structlog
import logging

def setup_logging():
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
logger = structlog.get_logger()

# Usage in code:
logger.info("Analysis completed", 
           text_length=len(text), 
           detected_meter=result.meter,
           confidence=result.confidence,
           processing_time_ms=duration)
```

---

## 🚀 خطة النشر (Deployment Strategy)

### Development Environment:
```bash
# Local development with Docker Compose
make setup  # Setup environment
make start  # Start all services
make test   # Run tests
```

### Staging Environment:
```bash
# Deploy to Railway/Render for testing
railway up  # Deploy to Railway
```

### Production Environment:
```bash
# Deploy to cloud provider (AWS/GCP/Digital Ocean)
# Using Docker containers + managed databases
```

---

## ✅ تعريف الإنجاز (Definition of Done)

### Backend:
- [ ] جميع endpoints تعمل وموثقة
- [ ] تغطية الاختبارات > 80%
- [ ] محرك التقطيع يحقق > 90% دقة
- [ ] زمن الاستجابة < 200ms متوسط
- [ ] كاش Redis يعمل بكفاءة
- [ ] لوائح المراقبة مفعلة

### Frontend:  
- [ ] جميع الصفحات تعمل وتدعم RTL
- [ ] تصميم responsive على جميع الأحجام
- [ ] اختبارات المكونات تمر
- [ ] تجربة المستخدم سلسة وبديهية
- [ ] دعم الأمثلة التفاعلية
- [ ] معالجة الأخطاء واضحة

### Integration:
- [ ] API و Frontend متكاملان
- [ ] Docker Compose يعمل للتطوير
- [ ] نشر تجريبي ناجح
- [ ] توثيق شامل للاستخدام
- [ ] feedback من 10 مستخدمين تجريبيين

---

## 🎯 الخطوة التالية

عند إكمال Phase 1 بنجاح، انتقل إلى:
**[Phase 2: AI Poet Development](PHASE_2_AI_POET.md)**

---

## 📝 ملاحظات مهمة

1. **ابدأ بسيط:** MVP يعني الحد الأدنى القابل للحياة
2. **اختبر مبكراً:** كل feature يجب يتاختبر فور الانتهاء منه
3. **وثّق كل شيء:** كود، قرارات، مشاكل، حلول
4. **اطلب feedback:** من مستخدمين حقيقيين في أسرع وقت
5. **لا تتوقف عند مشكلة:** اطلب مساعدة إذا احتجت

---

**🏆 النجاح في Phase 1 = أساس قوي لباقي المشروع!**