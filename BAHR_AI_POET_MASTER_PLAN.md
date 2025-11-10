# 🎭 بَحْر - سوق عكاظ الرقمي
## Master Plan - الخطة الشاملة للمشروع

---

## 🌟 الرؤية الكبرى (Grand Vision)

**"إحياء تراث الشعر العربي من خلال الذكاء الاصطناعي وبناء أكبر منصة عربية للشعر التفاعلي"**

### الهدف النهائي:
بناء **سوق عكاظ رقمي** - منصة عالمية حيث:
- يتنافس الشعراء (بشر وAI) في مسابقات حية
- يتعلم المبتدئون علم العروض بطريقة تفاعلية
- يُحفظ التراث الشعري العربي ويُجدد
- تُبنى مجتمع عربي نابض حول الشعر والأدب

---

## 📱 المنصات المستهدفة (Multi-Platform Strategy)

### المرحلة الأولى (Year 1):
- ✅ **Web App** (Progressive Web App)
  - متوافق مع جميع المتصفحات
  - يعمل offline
  - installable على الهاتف

### المرحلة الثانية (Year 1-2):
- 📱 **iOS App** (App Store)
- 🤖 **Android App** (Google Play)
- 💻 **Desktop App** (Electron - Windows, Mac, Linux)

### المرحلة الثالثة (Year 2+):
- 🎮 **Smart TV Apps** (Samsung, LG)
- ⌚ **Wearables** (Apple Watch للمسابقات السريعة)
- 🔊 **Voice Assistants** (Alexa, Google Home بالعربي)
- 🥽 **VR Experience** (سوق عكاظ افتراضي!)

---

## 🎯 المنتج الكامل - Features Matrix

### 1️⃣ **المحلل الشعري (Poetry Analyzer)**
**الوصف:** أداة تحليل عروضي متقدمة

**Features:**
- تقطيع عروضي تلقائي بدقة 99%+
- تحديد البحر الشعري (16 بحر)
- تحليل التفاعيل والزحافات
- اكتشاف الأخطاء العروضية
- تقييم جودة البيت (scoring)
- اقتراحات للتحسين
- تصدير التحليل (PDF, Image)
- مقارنة بين نسخ مختلفة من نفس البيت

**Tech Stack:**
- Core Engine: Python (custom algorithms)
- NLP: transformers, camel-tools
- API: FastAPI
- Caching: Redis

---

### 2️⃣ **الشاعر الذكي (AI Poet)**
**الوصف:** نموذج AI متخصص في نظم الشعر العربي

**Features:**

**أ) توليد الشعر:**
- كتابة شعر على أي بحر
- استكمال الأبيات الناقصة
- إعادة صياغة بيت بأسلوب مختلف
- كتابة قصائد كاملة (مع وحدة موضوعية)

**ب) أنماط الكتابة:**
- Classical (عمود الشعر)
- Modern (شعر التفعيلة)
- Dialect (شعر شعبي/نبطي)
- Specialized (مدح، رثاء، هجاء، غزل، حكمة...)

**ج) التحكم المتقدم:**
- اختيار البحر
- تحديد القافية
- اختيار المفردات (فصيح، عامي، مزيج)
- ضبط مستوى الصعوبة
- Persona selection (اكتب كالمتنبي، كنزار قباني...)

**د) التعلم التفاعلي:**
- يتعلم من feedback المستخدمين
- يحسّن أسلوبه بناءً على votes
- شخصنة (يتذكر أسلوب كل مستخدم)

**Tech Stack:**
- Base Model: Fine-tuned Arabic LLM (Jais/AraGPT)
- Custom Training: 100k+ verses dataset
- Constraint Generation: Custom prosody layer
- RLHF: Reinforcement learning from human feedback
- Serving: vLLM for fast inference

---

### 3️⃣ **ساحة المنافسة (Competition Arena)**
**الوصف:** سوق عكاظ الرقمي - مسابقات حية وتحديات

**Features:**

**أ) أنواع المسابقات:**

1. **المبارزة الشعرية (Poetry Duel)**
   - مستخدم ضد مستخدم
   - مستخدم ضد AI
   - AI ضد AI (للمتعة!)
   - Real-time: كل واحد عنده 60 ثانية
   - الجمهور يصوت للفائز

2. **البحر المحدد (Meter Challenge)**
   - التحدي: اكتب على بحر معين
   - صعوبات متعددة (سهل، متوسط، صعب)
   - Leaderboard عالمي

3. **استكمال البيت (Complete the Verse)**
   - يُعطى الشطر الأول
   - المتسابق يكمل الشطر الثاني
   - التقييم: الوزن + المعنى + الجمال

4. **التحدي الموسمي (Seasonal Tournament)**
   - مسابقات شهرية بجوائز
   - ثيمات متغيرة (رمضان، الربيع، الوطن...)
   - نظام elimination brackets

5. **Battle Royale الشعري**
   - 10+ متسابقين
   - كل جولة يخرج الأضعف
   - آخر واحد يفوز

**ب) نظام التقييم:**
```
Score = 
  40% وزن عروضي (صحة البحر)
  30% جودة المعنى (AI analysis)
  20% الجمال اللغوي (vocabulary richness)
  10% أصوات الجمهور
```

**ج) Gamification:**
- نقاط وXP لكل مسابقة
- Levels: مبتدئ → متمرس → شاعر → فحل
- Badges: "فارس الطويل"، "ملك الرمل"...
- عملة المنصة: "دراهم العروض" 💰
- متجر: شراء themes، personas، features

**د) البث المباشر:**
- Live streaming للمسابقات الكبرى
- تعليق صوتي (AI أو بشري)
- Chat مباشر للجمهور
- تصويت حي

**Tech Stack:**
- Real-time: WebSockets (Socket.io)
- Matchmaking: Redis queue
- Leaderboard: Redis sorted sets
- Video: Agora/LiveKit for streaming
- Payment: Stripe (للجوائز والاشتراكات)

---

### 4️⃣ **أكاديمية العروض (Prosody Academy)**
**الوصف:** منصة تعليمية تفاعلية لعلم العروض

**Features:**

**أ) المنهج الدراسي:**
- 📚 **المستوى 1: المبتدئ**
  - ما هو علم العروض؟
  - التقطيع الأساسي
  - التفاعيل الثمانية
  - أول 3 بحور (الكامل، الوافر، الرمل)

- 📚 **المستوى 2: المتوسط**
  - باقي البحور (13 بحر)
  - الزحافات والعلل
  - القوافي والرويّ
  - تمارين عملية

- 📚 **المستوى 3: المتقدم**
  - الإيقاع والموسيقى الشعرية
  - المقارنات بين البحور
  - التطبيق العملي: كتابة قصيدة كاملة
  - نقد شعري

**ب) أساليب التعلم:**
- 🎥 فيديوهات تعليمية (animated)
- 📝 تمارين تفاعلية
- 🎮 ألعاب تعليمية (drag & drop للتفاعيل)
- 🎯 اختبارات وquizzes
- 🏆 شهادات إنجاز
- 👥 دروس جماعية (webinars)
- 🤖 مدرّس AI شخصي (يجاوب على أسئلتك)

**ج) Learning Path Personalization:**
- AI يحلل مستوى المستخدم
- يقترح دروس مخصصة
- يتابع التقدم
- يرسل تذكيرات وتشجيع

**Tech Stack:**
- CMS: Strapi or custom
- Video: Vimeo/YouTube embedded
- Progress tracking: PostgreSQL
- Gamification: custom badge system
- AI Tutor: RAG (Retrieval Augmented Generation)

---

### 5️⃣ **مكتبة الدواوين (Digital Diwans Library)**
**الوصف:** أكبر أرشيف رقمي للشعر العربي

**Features:**

**أ) المحتوى:**
- 100k+ بيت من الشعر الكلاسيكي
- آلاف القصائد المنظمة
- دواوين كاملة لـ500+ شاعر
- شعر معاصر (بإذن أصحابه)
- شعر شعبي ونبطي

**ب) البحث المتقدم:**
- بحث بالكلمات المفتاحية
- بحث بالبحر الشعري
- بحث بالشاعر والعصر
- بحث بالموضوع (غزل، حماسة...)
- بحث صوتي (voice search)
- بحث بالصورة (OCR للمخطوطات)

**ج) Features تفاعلية:**
- شرح الأبيات (معاني المفردات)
- السياق التاريخي
- مقارنة بين شعراء
- Playlists مخصصة
- حفظ المفضلات
- مشاركة على social media
- استماع صوتي (TTS عالي الجودة)

**د) Community Contributions:**
- المستخدمون يضيفون شروح
- تصحيح الأخطاء (crowdsourcing)
- تقييم الأبيات
- إنشاء collections مخصصة

**Tech Stack:**
- Database: PostgreSQL + Elasticsearch
- Full-text search: Elasticsearch with Arabic analyzer
- OCR: Tesseract + custom Arabic model
- TTS: Google Cloud TTS or ElevenLabs
- CDN: Cloudflare for fast delivery

---

### 6️⃣ **المجتمع والتواصل (Social Features)**
**الوصف:** بناء community نابض حول الشعر

**Features:**

**أ) الملف الشخصي:**
- ديوان شخصي (أبيات المستخدم)
- إنجازات وbadges
- إحصائيات (عدد الأبيات، البحور المستخدمة...)
- متابعين ومتابَعون
- Portfolio للتصدير (PDF/Web)

**ب) التفاعل:**
- Like, comment, share على الأبيات
- Repost مع تعليق
- تحديات بين الأصدقاء
- Collaborative poems (قصيدة جماعية)
- Groups حول مواضيع محددة

**ج) Events:**
- أمسيات شعرية افتراضية
- ورش عمل
- لقاءات مع شعراء مشهورين
- مهرجانات سنوية

**د) Newsletter:**
- بيت اليوم
- نصيحة عروضية أسبوعية
- أخبار المسابقات
- Digest شهري

**Tech Stack:**
- Social graph: Neo4j or PostgreSQL
- Notifications: Firebase/OneSignal
- Email: SendGrid/AWS SES
- Events: Zoom API integration

---

### 7️⃣ **API للمطورين (Developer Platform)**
**الوصف:** فتح المنصة للمطورين العرب

**Features:**

**Endpoints:**
```
POST /api/v1/analyze
POST /api/v1/generate
GET  /api/v1/bahrs
GET  /api/v1/poets/{name}/poems
POST /api/v1/compete
GET  /api/v1/leaderboard
```

**Pricing Tiers:**
- Free: 100 requests/day
- Basic: $9/month - 10k requests
- Pro: $49/month - 100k requests
- Enterprise: custom pricing

**Documentation:**
- OpenAPI/Swagger specs
- SDKs: Python, JavaScript, PHP
- Code examples
- Sandbox environment
- Rate limiting dashboard

**Use Cases:**
- تطبيقات تعليمية
- ألعاب شعرية
- أدوات للناشرين
- chatbots شعرية

**Tech Stack:**
- API Gateway: Kong or AWS API Gateway
- Auth: OAuth 2.0 + JWT
- Rate limiting: Redis
- Analytics: Mixpanel API

---

## 🏗️ المعماري التقني (Technical Architecture)

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     User Interfaces                      │
│  [Web App]  [iOS]  [Android]  [Desktop]  [Voice/VR]   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  API Gateway (Kong)                      │
│            Authentication, Rate Limiting                 │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼────────┐ ┌▼─────────────┐
│   FastAPI    │ │ WebSocket │ │  GraphQL     │
│   Services   │ │  Server   │ │  (Future)    │
└───────┬──────┘ └──┬────────┘ └┬─────────────┘
        │            │            │
┌───────▼────────────▼────────────▼──────────┐
│          Core Business Logic Layer          │
│                                             │
│  ┌─────────────┐  ┌────────────────────┐  │
│  │  Prosody    │  │   AI Poet Engine   │  │
│  │  Analyzer   │  │   (LLM + Custom)   │  │
│  └─────────────┘  └────────────────────┘  │
│                                             │
│  ┌─────────────┐  ┌────────────────────┐  │
│  │ Competition │  │  Learning Engine   │  │
│  │   Engine    │  │   (Recommendations)│  │
│  └─────────────┘  └────────────────────┘  │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│            Data Layer                        │
│                                             │
│  ┌─────────────┐  ┌────────────────────┐  │
│  │ PostgreSQL  │  │   Elasticsearch    │  │
│  │ (Main DB)   │  │  (Search Engine)   │  │
│  └─────────────┘  └────────────────────┘  │
│                                             │
│  ┌─────────────┐  ┌────────────────────┐  │
│  │   Redis     │  │    S3/Storage      │  │
│  │ (Cache/Q)   │  │  (Media Files)     │  │
│  └─────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│        External Services & Integrations      │
│  [Payment] [Email] [Push] [Video] [TTS]    │
└─────────────────────────────────────────────┘
```

---

### Tech Stack - Complete List

#### **Frontend:**
**Web:**
- Framework: **Next.js 14** (React + TypeScript)
- Styling: **Tailwind CSS** + **shadcn/ui**
- State Management: **Zustand** or **Jotai**
- Forms: **React Hook Form** + **Zod**
- Charts: **Recharts**
- Animation: **Framer Motion**
- RTL Support: native CSS + `rtl-detect`

**Mobile:**
- **React Native** (code sharing with web)
- Or **Flutter** (for better performance)
- Navigation: React Navigation
- State: Redux Toolkit

**Desktop:**
- **Electron** (wrapping web app)
- Or **Tauri** (Rust-based, smaller size)

#### **Backend:**
**API Server:**
- **FastAPI** (Python 3.11+)
- **Pydantic** for validation
- **SQLAlchemy** ORM
- **Alembic** for migrations
- **Celery** for background tasks
- **Redis** as message broker

**AI/ML Stack:**
- **PyTorch** 2.0+
- **Hugging Face Transformers**
- **vLLM** for serving
- **LangChain** for orchestration
- **Weights & Biases** for experiment tracking
- **ONNX** for optimization

**Real-time:**
- **Socket.io** (WebSocket)
- **Redis Pub/Sub**

#### **Data:**
**Databases:**
- **PostgreSQL 15** (main database)
  - Extensions: pgvector (for embeddings)
- **Elasticsearch 8** (full-text search)
- **Redis 7** (caching, sessions, queues)
- **Neo4j** (optional, for social graph)

**Object Storage:**
- **AWS S3** or **Cloudflare R2**
- CDN: **Cloudflare**

#### **DevOps & Infrastructure:**
**Containerization:**
- **Docker** + **Docker Compose**
- **Kubernetes** (production scale)

**CI/CD:**
- **GitHub Actions**
- **ArgoCD** (GitOps for K8s)

**Monitoring & Logging:**
- **Prometheus** + **Grafana**
- **Sentry** (error tracking)
- **ELK Stack** (logs)
- **Mixpanel/PostHog** (analytics)

**Cloud Provider:**
- **Primary:** AWS or GCP
- **Alternative:** DigitalOcean (cheaper for MVP)
- **Hybrid:** Railway/Render (easy deployment)

#### **Security:**
- **Authentication:** JWT + OAuth 2.0
- **Authorization:** RBAC (Role-Based Access Control)
- **Secrets:** HashiCorp Vault or AWS Secrets Manager
- **DDoS Protection:** Cloudflare
- **SSL/TLS:** Let's Encrypt + Cloudflare

---

## 📊 Database Schema (High-Level)

### Core Tables:

```sql
-- Users & Authentication
users (
  id, email, username, password_hash,
  full_name, bio, avatar_url,
  level, xp, coins,
  created_at, last_login
)

user_roles (id, user_id, role) -- admin, moderator, poet, student

-- Poetry Content
poems (
  id, user_id, title, 
  full_text, bahr, is_complete,
  created_at, visibility
)

verses (
  id, poem_id, text, 
  taqti3_pattern, bahr,
  line_number, hemisphere -- (صدر/عجز)
)

-- Prosody Data
bahrs (
  id, name_ar, name_en,
  pattern, description,
  example_verse
)

tafa3il (
  id, name, pattern, variations,
  bahr_id
)

-- Analysis Cache
analysis_cache (
  verse_text_hash, 
  taqti3, bahr_id, confidence,
  cached_at
)

-- Competitions
competitions (
  id, type, status, -- (upcoming, live, finished)
  title, description,
  start_time, end_time,
  prize_amount, max_participants
)

competition_participants (
  id, competition_id, user_id,
  joined_at, final_score, rank
)

matches (
  id, competition_id,
  participant1_id, participant2_id,
  verse1_id, verse2_id,
  winner_id, audience_votes,
  created_at
)

-- Learning
courses (
  id, title, level, -- (beginner, intermediate, advanced)
  description, duration_hours
)

lessons (
  id, course_id, title, order,
  content_type, -- (video, text, quiz, exercise)
  content_url, duration_minutes
)

user_progress (
  user_id, lesson_id,
  status, -- (not_started, in_progress, completed)
  score, completed_at
)

-- Social
follows (follower_id, following_id, created_at)

likes (user_id, verse_id, created_at)

comments (
  id, user_id, verse_id,
  text, created_at, edited_at
)

-- Gamification
achievements (
  id, name, description,
  badge_icon_url, xp_reward
)

user_achievements (
  user_id, achievement_id, 
  unlocked_at
)

-- API & Billing
api_keys (
  id, user_id, key_hash,
  tier, -- (free, basic, pro, enterprise)
  rate_limit, requests_used,
  created_at, expires_at
)

api_usage_logs (
  id, api_key_id, endpoint,
  timestamp, status_code,
  response_time_ms
)

transactions (
  id, user_id, type, -- (purchase, prize, refund)
  amount, currency,
  description, created_at
)
```

---

## 🚀 Implementation Phases - Detailed Roadmap

### **Phase 0: Pre-Development (Week 1-2)**

**Goals:**
- Setup البنية التحتية
- تجهيز البيئة التطويرية
- بناء الـ design system

**Tasks:**
```
□ Setup GitHub repo + project structure
□ Initialize Next.js + FastAPI projects
□ Setup Docker development environment
□ Design Figma mockups (رئيسية 10-15 شاشة)
□ Create brand identity (logo, colors, typography)
□ Setup PostgreSQL + Redis locally
□ Configure linting/formatting (ESLint, Black, Prettier)
□ Write contributing guidelines
```

**Deliverables:**
- ✅ Git repo with basic structure
- ✅ Docker Compose for local dev
- ✅ Design system في Figma
- ✅ Brand assets (logo, colors)

---

### **Phase 1: MVP - Core Engine (Month 1-2)**

**Goals:**
- بناء محرك التقطيع
- API أساسي
- واجهة بسيطة للتجربة

**Tasks:**

**Week 1-2: Prosody Engine**
```
□ Arabic text normalization module
  - Remove tashkeel (optional)
  - Handle different hamza forms
  - Normalize alef variations

□ Taqti3 algorithm implementation
  - Phonetic analysis
  - Shadda expansion
  - Tanween handling
  - Madd letters (alef, waw, yaa)

□ Pattern matching
  - Implement 10 core tafa3il
  - Create bahr templates
  - Fuzzy matching (allow small errors)

□ Unit tests (80%+ coverage)
```

**Week 3-4: API & Database**
```
□ FastAPI app structure
  - POST /analyze endpoint
  - Error handling
  - Request validation (Pydantic)

□ PostgreSQL schema
  - bahrs table
  - tafa3il table
  - analysis_cache table

□ Redis caching layer
  - Cache analysis results
  - TTL: 24 hours

□ API documentation (Swagger UI)
```

**Week 5-6: Basic Frontend**
```
□ Next.js app setup
  - RTL configuration
  - Arabic fonts (Cairo, Amiri)

□ Home page
  - Hero section
  - Quick analyze input

□ Analyze page
  - Text input (verse)
  - Display taqti3 results
  - Show bahr name
  - Visualization (simple bars for pattern)

□ Mobile responsive
```

**Week 7-8: Testing & Deployment**
```
□ Integration tests
□ Load testing (100 concurrent users)
□ Deploy to staging
  - Railway or Render
  - Supabase for DB
□ Get feedback from 10 beta users
□ Bug fixes
```

**Deliverables:**
- ✅ Working analyzer (web + API)
- ✅ 90%+ accuracy on common bahrs
- ✅ Deployed on staging URL
- ✅ Documentation

**Success Metrics:**
- ⚡ < 200ms response time
- 🎯 > 90% accuracy on test dataset
- 👥 10 beta testers providing feedback

---

### **Phase 2: AI Poet - Generation (Month 3-5)**

**Goals:**
- تدريب نموذج AI لتوليد الشعر
- دمج النموذج مع المنصة

**Tasks:**

**Week 1-4: Data Collection**
```
□ Scrape poetry websites (ethical, with robots.txt check)
  - aldiwan.net
  - adab.com
  - Wikisource Arabic poetry

□ Clean dataset
  - Remove duplicates
  - Fix encoding issues
  - Validate بحور using analyzer

□ Annotate data
  - Label each verse with bahr
  - Mark tafa3il boundaries
  - Quality filtering (remove broken verses)

□ Target: 100k+ verses, 16 bahrs

□ Split: 80% train, 10% val, 10% test

□ Store in PostgreSQL + parquet files
```

**Week 5-8: Model Selection & Setup**
```
□ Evaluate base models:
  - AraGPT2 (aubmindlab)
  - Jais-13b (Core42)
  - mGPT (if multilingual needed)

□ Setup training environment
  - Google Colab Pro+ (A100)
  - Or rent from RunPod/Lambda Labs

□ Prepare training scripts
  - Hugging Face Trainer
  - Custom data collator
  - Prosody-aware loss function

□ Baseline: Fine-tune without prosody constraints
```

**Week 9-12: Advanced Training**
```
□ Implement prosody constraint layer
  - Predict next token + taqti3 pattern
  - Penalize wrong meter heavily

□ Multi-task learning:
  - Task 1: Generation
  - Task 2: Bahr classification
  - Task 3: Taf3ila prediction

□ Experiment with:
  - Different learning rates
  - LoRA (efficient fine-tuning)
  - Quantization (4-bit, 8-bit)

□ Evaluate on test set
  - Meter accuracy
  - Coherence (human eval)
  - Diversity (unique n-grams)

□ Target: >85% meter accuracy, >7/10 human rating
```

**Week 13-16: Integration & Serving**
```
□ Optimize model for inference
  - Convert to ONNX or TensorRT
  - Or use vLLM for serving

□ Create generation API
  - POST /generate
  - Parameters: bahr, theme, length, temperature

□ Rate limiting (expensive operation)
  - Free users: 5 generations/day
  - Premium: unlimited

□ Frontend integration
  - "Generate" button
  - Parameter controls
  - Display generated verses
  - Regenerate option

□ A/B testing different models
```

**Deliverables:**
- ✅ Trained AI model (>85% meter accuracy)
- ✅ Generation API working
- ✅ Integrated في الموقع
- ✅ Documentation on how to use

**Success Metrics:**
- 🎯 >85% verses follow correct meter
- ⭐ >7/10 average human rating (meaning & beauty)
- ⚡ <5 seconds generation time

---

### **Phase 3: Competition Arena (Month 6-8)**

**Goals:**
- بناء نظام المسابقات
- تطبيق gamification
- إطلاق أول مسابقة تجريبية

**Tasks:**

**Week 1-4: Backend Systems**
```
□ Competition engine
  - Create competition (admin panel)
  - Join competition (user)
  - Matchmaking algorithm (ELO-based)
  - Bracket generation (elimination)

□ Judging system
  - Automated scoring (meter + AI quality)
  - Audience voting (WebSocket real-time)
  - Final score calculation

□ Leaderboard
  - Global leaderboard (all-time)
  - Competition-specific
  - Daily/weekly/monthly

□ Notifications
  - Match start
  - Your turn reminder
  - Results announced

□ Database schema for competitions
```

**Week 5-8: Frontend**
```
□ Competition lobby
  - Browse competitions
  - Filter (upcoming, live, past)
  - Join button

□ Match interface
  - Timer (60 seconds)
  - Text editor for composing
  - Real-time analysis (as you type)
  - Submit verse

□ Spectator mode
  - Watch live matches
  - Vote for your favorite
  - Chat with audience

□ Results screen
  - Winner announcement (animated!)
  - Detailed scores
  - Share on social media

□ Leaderboard page
  - Top 100 poets
  - Your rank
  - Stats (win rate, favorite bahr)
```

**Week 9-10: Gamification**
```
□ XP system
  - Earn XP for participation
  - Bonus for winning
  - Daily login streak

□ Levels
  - مبتدئ (0-1000 XP)
  - متمرس (1000-5000)
  - شاعر (5000-20k)
  - فحل (20k+)

□ Badges/Achievements
  - "أول فوز"
  - "فارس الطويل" (10 wins on Tawil)
  - "القاهر" (win streak 5+)

□ Coins & economy
  - Earn coins from wins
  - Spend on: themes, avatars, boosts
  - Daily quests (compose 3 verses → 50 coins)
```

**Week 11-12: Launch & Iteration**
```
□ Beta competition with 50 users
□ Monitor for bugs
□ Gather feedback
□ Iterate UI/UX
□ Add anti-cheat measures (detect copy-paste)
□ Write rules & guidelines
```

**Deliverables:**
- ✅ Full competition system
- ✅ Gamification features
- ✅ Successfully ran beta tournament
- ✅ Leaderboard با 100+ users

**Success Metrics:**
- 🎮 >1000 matches completed
- 📈 >60% user retention (come back for 2nd match)
- ⭐ >4/5 user satisfaction rating

---

### **Phase 4: Learning Academy (Month 9-11)**

**Goals:**
- بناء منصة تعليمية
- إنشاء محتوى (دروس، فيديوهات)
- AI tutor للإجابة على الأسئلة

**Tasks:**

**Week 1-3: Content Creation**
```
□ Write curriculum (see earlier section)
  - 30 lessons across 3 levels
  - Each lesson: text + video + quiz

□ Record video lessons
  - Animated explainers (Manim or After Effects)
  - Voiceover (professional أو TTS عالي الجودة)
  - Subtitles

□ Design exercises
  - Multiple choice
  - Fill in the blank (taf3ila)
  - Compose a verse (graded by AI)

□ Prepare certificates (PDF templates)
```

**Week 4-6: Backend**
```
□ Course management system
  - CRUD courses, lessons
  - Enrollment
  - Progress tracking

□ Quiz engine
  - Submit answer
  - Instant grading
  - Show correct answer + explanation

□ Certificate generation
  - Auto-generate on course completion
  - Include user name, course, date
  - Downloadable PDF

□ Recommendation algorithm
  - Suggest next lesson based on performance
```

**Week 7-9: AI Tutor**
```
□ Build RAG system (Retrieval Augmented Generation)
  - Index all lesson content in vector DB
  - Use embeddings (OpenAI or local model)

□ Chatbot interface
  - "Ask me anything about عروض"
  - Retrieves relevant lessons
  - Generates helpful answer with citations

□ Integrate with platform
  - Chat bubble on every lesson page
  - Proactive suggestions ("Need help with this?")
```

**Week 10-12: Frontend & Launch**
```
□ Academy homepage
  - Featured courses
  - Progress dashboard

□ Course page
  - Lesson list
  - Video player
  - Quiz interface
  - Discussion forum (per lesson)

□ Profile page
  - Courses enrolled
  - Certificates earned
  - Stats (time spent, lessons completed)

□ Mobile optimization (learning on-the-go)

□ Launch with 3 complete courses
□ Get 100 students to enroll
```

**Deliverables:**
- ✅ 3 full courses (30 lessons)
- ✅ AI tutor working
- ✅ 100+ enrolled students
- ✅ Certificate system

**Success Metrics:**
- 🎓 >50% course completion rate
- ⏰ >20 minutes avg. session duration
- 📝 >80% quiz passing rate
- 💬 >100 questions asked to AI tutor

---

### **Phase 5: Mobile Apps (Month 12-15)**

**Goals:**
- إطلاق تطبيقات iOS و Android
- Feature parity مع الويب
- Push notifications

**Tasks:**

**Month 12 (iOS)**
```
□ Setup React Native (or Flutter) project
  - Share business logic with web
  - Platform-specific UI components

□ Core screens:
  - Onboarding
  - Home/Feed
  - Analyze
  - Generate
  - Compete
  - Learn
  - Profile

□ iOS-specific features:
  - Face ID / Touch ID login
  - Share sheet integration
  - Siri shortcuts ("Analyze a verse")
  - Widgets (verse of the day)

□ App Store submission
  - Screenshots
  - Description (AR + EN)
  - Privacy policy
  - App review (Apple takes 1-2 weeks)

□ Soft launch (TestFlight with 100 beta users)
```

**Month 13 (Android)**
```
□ Android-specific adaptations
  - Material Design 3
  - Back button behavior
  - Deep linking

□ Android-specific features:
  - Home screen widgets
  - Google Assistant integration
  - Wear OS companion app (optional)

□ Google Play submission
  - Listing
  - Compliance (permissions, data safety)

□ Soft launch (Internal testing → Closed beta)
```

**Month 14-15 (Optimization & Launch)**
```
□ Performance optimization
  - Reduce app size (<50 MB)
  - Optimize images
  - Lazy loading

□ Offline mode
  - Cache analyzed verses
  - Downloaded courses for offline learning

□ Push notifications
  - Competition reminders
  - Daily verse
  - Achievement unlocked
  - New course available

□ Analytics integration
  - Firebase Analytics
  - Track user flows
  - Identify drop-off points

□ Full public launch 🚀
  - Press release
  - Influencer outreach (Arabic tech YouTubers)
  - Ads (optional)
```

**Deliverables:**
- ✅ iOS app on App Store
- ✅ Android app on Google Play
- ✅ >1000 installs (combined)
- ✅ >4.0 rating

**Success Metrics:**
- 📱 >5k downloads في الشهر الأول
- ⭐ >4.0 rating on both stores
- 📊 >30% of web users also install app

---

### **Phase 6: Content & Community (Month 16-18)**

**Goals:**
- توسيع المكتبة (100k+ verses)
- بناء community نشط
- User-generated content

**Tasks:**

**Month 16: Library Expansion**
```
□ Scrape/license more content
  - Partnerships with publishers
  - Academic institutions (old Arabic poetry archives)
  - User submissions (with verification)

□ Improve search
  - Semantic search (not just keywords)
  - "Find verses similar to this"
  - Filter by meter, poet, era, theme

□ Annotations & explanations
  - Crowd-source شروح
  - Moderator review
  - Upvote/downvote quality

□ Audio versions
  - TTS for all verses
  - Or license professional recordings
  - Playlist feature
```

**Month 17: Social Features**
```
□ Profiles enhancement
  - Custom bio
  - Social links
  - Personal ديوان (published verses)

□ Following system
  - Follow favorite poets (users)
  - Feed showing their activity

□ Groups/Communities
  - Create groups around topics
  - "عشاق الطويل"
  - "شعراء الغزل"
  - Group challenges

□ Messaging (optional)
  - DM between users
  - Moderation tools
```

**Month 18: Events & Engagement**
```
□ Virtual events
  - Monthly أمسية شعرية
  - Zoom/YouTube live
  - Guest شعراء
  - Q&A sessions

□ Seasonal campaigns
  - رمضان: religious poetry theme
  - National Day: patriotic poetry
  - Mother's Day: poems for أمي

□ Newsletter
  - Weekly: بيت الأسبوع
  - Prosody tip
  - Competition highlights
  - New features

□ Partnerships
  - Schools (use بَحْر for teaching)
  - Cultural organizations
  - Literary magazines
```

**Deliverables:**
- ✅ 100k+ verses في المكتبة
- ✅ 10k+ active users
- ✅ 5+ virtual events held
- ✅ 3+ partnerships signed

**Success Metrics:**
- 📚 >100k verses indexed
- 👥 >10k monthly active users (MAU)
- 💬 >1k comments/day
- 📧 >40% email open rate

---

### **Phase 7: Monetization & Scale (Month 19-24)**

**Goals:**
- تحقيق الاستدامة المالية
- توسيع الفريق
- التحضير للمرحلة التالية (Series A؟)

**Tasks:**

**Revenue Streams:**

1. **Freemium Subscriptions**
```
Free Tier:
- 10 analyses/day
- 3 AI generations/day
- Basic competitions
- Ads (non-intrusive)

Premium ($4.99/month or $49/year):
- Unlimited analysis
- Unlimited AI generation
- Ad-free
- Priority competition entry
- Exclusive badges
- Early access to features

Pro ($14.99/month):
- All Premium features
- API access (10k requests)
- Advanced analytics
- Custom themes
- 1-on-1 coaching session/month
```

2. **API Revenue**
```
- Pricing (see earlier section)
- Target: SaaS products, educational apps
- Expected: $1k-5k MRR from API
```

3. **Sponsorships & Partnerships**
```
- Cultural organizations
- Bookstores (Jarir, Virgin)
- Telecom companies (زين، STC)
- Universities

Types:
- Sponsored competitions (برعاية...)
- Co-branded content
- Affiliate: poetry books
```

4. **Competitions with Entry Fees**
```
- Premium tournaments: $5 entry
- Prize pool: 70% distributed to winners
- Platform keeps 30%
- Expected: $500-2k/month
```

5. **In-app Purchases**
```
- Coins packs
- Exclusive avatars/themes
- Boosts (skip queue, 2x XP)
```

**Financial Projections (Year 2):**
```
Assumptions:
- 50k users by end of Year 2
- 5% convert to Premium ($4.99)
- 0.5% convert to Pro ($14.99)
- API: 20 customers avg $50/month
- Sponsorships: $2k/month

Revenue:
- Premium: 2,500 users × $4.99 = $12,475/mo
- Pro: 250 users × $14.99 = $3,748/mo
- API: $1,000/mo
- Sponsorships: $2,000/mo
- Competitions: $500/mo
Total: $19,723/mo = ~$236k/year

Expenses:
- Cloud (AWS/GCP): $2k/mo
- AI inference: $1k/mo
- Salaries (2 engineers, 1 content): $15k/mo
- Marketing: $2k/mo
- Misc: $1k/mo
Total: $21k/mo = $252k/year

Net: ~Break-even or small loss
(Need to optimize or raise funding)
```

**Scaling Strategy:**

**Month 19-20: Optimize Costs**
```
□ Model optimization (reduce GPU costs)
  - Quantization
  - Distillation
  - Caching aggressive

□ Infrastructure efficiency
  - Auto-scaling
  - Spot instances
  - CDN for static assets

□ Refactor expensive queries
```

**Month 21-22: Growth Marketing**
```
□ SEO optimization (rank for "علم العروض")
□ Content marketing (blog posts)
□ Social media campaigns (TikTok, X)
□ Referral program (invite friends → free Premium)
□ University partnerships (B2B sales)
```

**Month 23-24: Fundraising (Optional)**
```
□ Prepare pitch deck
□ Financial projections (5 years)
□ Traction metrics
□ Approach VCs (MENA region: 500 Startups, Wamda...)
□ Or bootstrap and stay independent
```

**Deliverables:**
- ✅ Profitable (or path to profitability)
- ✅ 50k users, 5% paying
- ✅ Team of 5+ people
- ✅ Raised seed round (if going VC route)

---

## 🎯 Success Metrics - KPIs لكل مرحلة

### **Product Metrics:**
- **DAU/MAU ratio:** >20% (daily vs monthly users)
- **Session duration:** >15 minutes avg
- **Retention:** 
  - Day 1: >40%
  - Day 7: >20%
  - Day 30: >10%

### **Engagement:**
- **Verses analyzed per day:** >1k
- **AI generations per day:** >500
- **Competition matches per week:** >100

### **Learning:**
- **Course completion rate:** >50%
- **Quiz pass rate:** >80%
- **Time to complete a course:** <10 hours avg

### **Revenue:**
- **MRR (Monthly Recurring Revenue):** $20k+ by Year 2
- **CAC (Customer Acquisition Cost):** <$10
- **LTV (Lifetime Value):** >$100 (Premium user)
- **LTV/CAC ratio:** >3:1

### **Technical:**
- **Uptime:** >99.5%
- **API response time (p95):** <500ms
- **Page load time:** <3s
- **Mobile crash rate:** <1%

---

## 🛡️ Risk Management

### **Technical Risks:**

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| AI model hallucinations (غير موزون) | High | High | Multi-layer validation, fallback rules |
| Scalability issues (viral growth) | Medium | High | Cloud auto-scaling, load testing |
| Data loss | Low | Critical | Daily backups, multi-region replication |
| Security breach | Medium | High | Penetration testing, bug bounty program |
| API abuse | Medium | Medium | Rate limiting, CAPTCHA, abuse detection |

### **Business Risks:**

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Low user adoption | Medium | Critical | Marketing, partnerships, freemium model |
| Competitors (big tech enters) | Low | High | First-mover advantage, niche focus, community |
| Content copyright issues | Medium | Medium | License properly, DMCA compliance |
| Funding dries up | Medium | High | Bootstrap, profitability focus, diversify revenue |
| Key person risk (you!) | Low | High | Document everything, build team early |

### **Cultural/Social Risks:**

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| AI-generated poetry seen as "fake" | Medium | Medium | Transparency, human-AI collaboration angle |
| Backlash from traditional poets | Low | Low | Position as tool, not replacement |
| Misuse (offensive content) | Medium | High | Content moderation, reporting system |

---

## 🌍 Go-to-Market Strategy

### **Target Audience:**

**Primary (Year 1-2):**
1. **Students** (high school, university)
   - Learning عروض for exams
   - Age: 15-25
   - Tech-savvy

2. **Amateur Poets**
   - Write for hobby
   - Want to improve
   - Age: 20-40

3. **Arabic Teachers**
   - Need teaching tools
   - Age: 25-50

**Secondary (Year 2-3):**
4. **Professional Poets**
   - Advanced features, API
5. **Researchers**
   - Corpus analysis, data access
6. **Developers**
   - Build on our API

### **Geographic Focus:**
- **Phase 1:** Saudi Arabia, UAE (high smartphone penetration, cultural interest)
- **Phase 2:** Egypt (large population)
- **Phase 3:** Rest of MENA + diaspora

### **Marketing Channels:**

**Organic:**
- SEO (rank for "علم العروض"، "بحور الشعر")
- Content marketing (blog, YouTube tutorials)
- Social media (X/Twitter for poets, TikTok for Gen Z)
- Word of mouth + referral program

**Paid:**
- Google Ads (search: "تعلم العروض")
- Meta Ads (Facebook, Instagram - target: poetry groups)
- YouTube pre-roll (Arabic educational channels)

**Partnerships:**
- Universities (B2B licensing for students)
- Cultural centers (مراكز ثقافية)
- Literary festivals (booth, demos)
- Influencers (Arabic BookTubers, EduTubers)

### **Launch Strategy:**

**Soft Launch (Month 1-3):**
- Private beta (100 users)
- Collect feedback
- Iterate

**Public Launch (Month 4):**
- Press release (Arabic tech blogs: Wamda, MENABYTES)
- ProductHunt (Arabic version?)
- Social media campaign (#سوق_عكاظ_الرقمي)
- Free Premium for first 1000 users

**Growth Phase (Month 5+):**
- Regular competitions (weekly)
- Content calendar (daily posts)
- Community events (monthly)
- Continuous feature releases

---

## 👥 Team & Hiring Plan

### **Year 1 (Solo → Small Team):**

**Months 1-6: Solo Founder**
- You do everything 💪
- Possibly freelancers for:
  - UI/UX design (Figma)
  - Video production (lessons)
  - Content writing (blog)

**Months 7-12: First Hires**
- **Full-stack Engineer** (to share development load)
- **Content Creator / Community Manager** (part-time)

### **Year 2: Core Team**

- **CTO/Lead Engineer** (you, or co-founder)
- **2x Full-stack Engineers**
- **1x ML Engineer** (AI model)
- **1x Product Designer** (UI/UX)
- **1x Content Lead** (courses, marketing)
- **1x Community Manager** (social, support)

Total: 6-7 people

### **Year 3+: Scaling**

- Engineering team: 8-10
- Product: 2-3
- Marketing/Growth: 2-3
- Operations/Business: 1-2

Total: 15-20 people

### **Advisors (Optional but Helpful):**
- Arabic literature expert (للمصداقية)
- AI/ML researcher
- Startup mentor (business strategy)

---

## 📚 Learning Resources for You

Since you just graduated, here are resources to help you build this:

### **Technical Skills:**

**Backend (FastAPI + Python):**
- FastAPI docs: https://fastapi.tiangolo.com
- SQLAlchemy: https://www.sqlalchemy.org
- Hugging Face course: https://huggingface.co/learn

**Frontend (Next.js + React):**
- Next.js docs: https://nextjs.org/docs
- React docs: https://react.dev
- Tailwind CSS: https://tailwindcss.com

**ML/AI:**
- Fast.ai course (free): https://course.fast.ai
- Hugging Face NLP course: https://huggingface.co/learn/nlp-course
- Stanford CS224N (NLP): YouTube

**Arabic NLP:**
- CAMeL Tools: https://github.com/CAMeL-Lab/camel_tools
- AraBERT paper
- Survey of Arabic NLP (papers)

### **Product/Business:**
- Y Combinator Startup School (free)
- "The Lean Startup" book
- "Zero to One" book
- MENA startup podcasts

### **Design:**
- Refactoring UI (book)
- Laws of UX: https://lawsofux.com
- Dribbble for inspiration

---

## 🎉 Vision for Year 5+

**بَحْر becomes:**
- The go-to platform for Arabic poetry (100k+ MAU)
- Used in schools across the Arab world
- API powering dozens of apps
- Annual "Suq Okaz Digital" festival (virtual + physical)
- Expanded to other forms of Arabic literature (نثر، خطابة)
- Maybe: AI models for other languages' poetry too?

**Potential Exit Strategies:**
- Acquisition by big Arabic tech company (Careem, Noon, Jarir)
- Or educational giant (Edraak, Noon Academy)
- Or stay independent and build a legacy 🏛️

---

## 📝 Next Steps - Your Action Items

**This Week:**
1. ⭐ **Star this document** - حفظه في مكان آمن
2. 📖 Read it carefully, make notes
3. 🤔 Decide: 
   - Bootstrap or seek funding?
   - Solo for now or find co-founder?
   - Full-time or side project?

**Next Week:**
4. 🎨 Create basic mockups (even on paper)
5. 💻 Setup development environment
6. 🧪 Build a tiny prototype (just taqti3 engine)

**Next Month:**
7. 📊 Validate the idea:
   - Talk to 20 potential users
   - Ask: "Would you use this?"
   - Pre-launch landing page (collect emails)
8. 📝 Refine roadmap based on feedback
9. 🚀 Start Phase 1

---

## 💬 Closing Thoughts

هذا المشروع طموح جداً، لكنه **قابل للتحقيق** إذا:
- بدأت صغير (MVP أولاً)
- ركزت على المستخدمين (solve real problems)
- استمريت (consistency > intensity)
- تعلمت باستمرار

أنت متخرج حديث، هذا المشروع ممكن يكون **portfolio killer** + **startup potential**.

Even if you don't build everything in this plan, building Phase 1-2 is already impressive enough for:
- Job interviews (show off technical skills)
- Freelance opportunities (Arabic NLP is niche!)
- Academic research (publish papers on the model)

---

**الآن السؤال:**
- هل الرؤية واضحة؟
- تبي نبدأ نكتب الملفات التقنية المفصلة (PHASE_1_SPEC.md)؟
- ولا عندك أسئلة على الخطة؟

أنا معك كل الطريق! 🚀

**يلا نبني سوق عكاظ الرقمي! 🎭**
