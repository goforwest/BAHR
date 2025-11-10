# 🗄️ تصميم قاعدة البيانات الشامل
## PostgreSQL Schema for بَحْر Poetry Platform

---

## 📋 نظرة عامة

تصميم شامل لقاعدة البيانات الخاصة بمنصة بَحْر لتحليل الشعر العربي، مع التركيز على:
- **أداء عالي** للبحث والاستعلامات
- **دعم النصوص العربية** كاملاً
- **مقياس قابل للتوسع** مع نمو البيانات  
- **سلامة البيانات** والعلاقات
- **فهرسة ذكية** لتحليل الأشعار
- **دعم التحليلات المتقدمة** والإحصائيات

### ⚠️ ملاحظة نطاق (Scope Notice - MVP)
الجداول الخاصة بالمسابقات والتفاعل الاجتماعي والتحليلات المتقدمة (Competitions, Submissions, Follows, Comments, Likes, Daily Stats, User Activity) **مؤجلة لما بعد الإطلاق** للحفاظ على سرعة الإنجاز والتركيز على المحرك العروضي. لا تُنشأ في المهاجرات الأولى؛ يُحتفظ بها هنا كتصميم مستقبلي.

---

## 🏗️ معمارية قاعدة البيانات

```
Database Architecture:
┌─────────────────────────────────────────────────────────────────┐
│                     Application Layer                          │
│         ┌─────────────────┐    ┌─────────────────┐             │
│         │     FastAPI     │    │   Background    │             │
│         │   Application   │    │     Jobs        │             │
│         └─────────────────┘    └─────────────────┘             │
└─────────────────┬───────────────────────┬───────────────────────┘
                  │                       │
┌─────────────────▼───────────────────────▼───────────────────────┐
│                    Connection Pool                              │
│     ┌─────────────────┐              ┌─────────────────┐        │
│     │   Read Pool     │              │  Write Pool     │        │
│     │   (5 conns)     │              │   (3 conns)     │        │
│     └─────────────────┘              └─────────────────┘        │
└─────────────────┬───────────────────────┬───────────────────────┘
                  │                       │
┌─────────────────▼───────────────────────▼───────────────────────┐
│                 PostgreSQL 15 Database                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │    Core     │ │  Analysis   │ │   Social    │               │
│  │   Tables    │ │   Tables    │ │   Tables    │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
│                                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │ Indexes &   │ │ Full-Text   │ │   Cache     │               │
│  │Constraints  │ │   Search    │ │   Tables    │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 ERD - Entity Relationship Diagram

```
ERD Overview:

┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│    Users    │◄────────┤  Analyses   │────────►│   Meters    │
│             │   1:N   │             │   N:1   │             │
│ - id (PK)   │         │ - id (PK)   │         │ - id (PK)   │
│ - username  │         │ - user_id   │         │ - name      │
│ - email     │         │ - text      │         │ - pattern   │
│ - role      │         │ - result    │         │ - type      │
└─────────────┘         └─────────────┘         └─────────────┘
       │                                              │
       │ 1:N                                          │ 1:N
       ▼                                              ▼
┌─────────────┐                                ┌─────────────┐
│ UserProfiles│                                │MeterVariants│
│             │                                │             │
│ - user_id   │                                │ - meter_id  │
│ - bio       │                                │ - variant   │
│ - level     │                                │ - examples  │
└─────────────┘                                └─────────────┘

┌─────────────┐    N:M    ┌─────────────┐    N:M    ┌─────────────┐
│Competitions │◄────────►│Participants │◄────────►│ Submissions │
│             │          │             │          │             │
│ - id (PK)   │          │ - comp_id   │          │ - id (PK)   │
│ - title     │          │ - user_id   │          │ - user_id   │
│ - deadline  │          │ - joined_at │          │ - poem_text │
└─────────────┘          └─────────────┘          └─────────────┘
```

---

## 🗂️ Core Tables

### 1. Users Table

```sql
-- Users table with comprehensive user management
CREATE TABLE users (
    id                  SERIAL PRIMARY KEY,
    username           VARCHAR(50) UNIQUE NOT NULL,
    email              VARCHAR(255) UNIQUE NOT NULL,
    password_hash      VARCHAR(255) NOT NULL,
    full_name          VARCHAR(100) NOT NULL,
    role               user_role_enum NOT NULL DEFAULT 'student',
    
    -- Profile fields
    bio                TEXT,
    avatar_url         VARCHAR(500),
    birth_date         DATE,
    location           VARCHAR(100),
    website            VARCHAR(255),
    
    -- Gamification
    level              INTEGER DEFAULT 1,
    xp                 INTEGER DEFAULT 0,
    coins              INTEGER DEFAULT 0,
    
    -- Account status
    is_active          BOOLEAN DEFAULT TRUE,
    is_verified        BOOLEAN DEFAULT FALSE,
    email_verified_at  TIMESTAMP WITH TIME ZONE,
    last_login         TIMESTAMP WITH TIME ZONE,
    
    -- Preferences
    preferred_language VARCHAR(5) DEFAULT 'ar',
    theme             VARCHAR(10) DEFAULT 'light',
    notifications     JSONB DEFAULT '{"email": true, "push": true}',
    
    -- Privacy
    profile_visibility privacy_enum DEFAULT 'public',
    analysis_privacy   privacy_enum DEFAULT 'private',
    
    -- Timestamps
    created_at         TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at         TIMESTAMP WITH TIME ZONE
);

-- Custom ENUMs
CREATE TYPE user_role_enum AS ENUM (
    'student', 'poet', 'teacher', 'moderator', 'admin'
);

CREATE TYPE privacy_enum AS ENUM (
    'public', 'friends', 'private'
);

-- Indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_level ON users(level DESC);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- Full-text search on user profiles
CREATE INDEX idx_users_search ON users 
    USING GIN(to_tsvector('arabic', full_name || ' ' || COALESCE(bio, '')));

-- Triggers for updated_at
CREATE TRIGGER set_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

### 2. Analyses Table

```sql
-- Poetry analysis results
CREATE TABLE analyses (
    id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id               INTEGER REFERENCES users(id) ON DELETE SET NULL,
    
    -- Input data
    original_text         TEXT NOT NULL,
    normalized_text       TEXT NOT NULL,
    language              VARCHAR(5) DEFAULT 'ar',
    dialect               VARCHAR(20),
    
    -- Analysis metadata
    analysis_mode         analysis_mode_enum NOT NULL DEFAULT 'accurate',
    processing_time_ms    INTEGER,
    algorithm_version     VARCHAR(20) NOT NULL DEFAULT '1.0',
    
    -- Prosodic analysis
    prosodic_pattern      JSONB NOT NULL,
    syllable_count        INTEGER,
    stress_pattern        TEXT,
    taqti3               TEXT,  -- التقطيع العروضي
    
    -- Meter detection
    detected_meter        VARCHAR(50),
    meter_confidence      DECIMAL(5,4) CHECK (meter_confidence >= 0 AND meter_confidence <= 1),
    alternative_meters    JSONB DEFAULT '[]',
    
    -- Quality assessment
    quality_score         DECIMAL(5,4) CHECK (quality_score >= 0 AND quality_score <= 1),
    quality_breakdown     JSONB,  -- Detailed quality metrics
    
    -- Results and suggestions
    analysis_result       JSONB NOT NULL,
    suggestions          JSONB DEFAULT '[]',
    corrections          JSONB DEFAULT '[]',
    
    -- Metadata
    is_public            BOOLEAN DEFAULT FALSE,
    view_count           INTEGER DEFAULT 0,
    share_count          INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at           TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at           TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Analysis mode enum
CREATE TYPE analysis_mode_enum AS ENUM (
    'fast', 'accurate', 'detailed'
);

-- Indexes
CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_meter ON analyses(detected_meter) WHERE detected_meter IS NOT NULL;
CREATE INDEX idx_analyses_quality ON analyses(quality_score DESC) WHERE quality_score IS NOT NULL;
CREATE INDEX idx_analyses_created_at ON analyses(created_at DESC);
CREATE INDEX idx_analyses_public ON analyses(is_public) WHERE is_public = TRUE;
CREATE INDEX idx_analyses_confidence ON analyses(meter_confidence DESC);

-- JSONB indexes for complex queries
CREATE INDEX idx_analyses_result_gin ON analyses USING GIN(analysis_result);
CREATE INDEX idx_analyses_pattern_gin ON analyses USING GIN(prosodic_pattern);

-- Full-text search on text content
CREATE INDEX idx_analyses_text_search ON analyses 
    USING GIN(to_tsvector('arabic', original_text));

-- Composite index for user's recent analyses
CREATE INDEX idx_analyses_user_recent ON analyses(user_id, created_at DESC);

-- Partial index for high-quality analyses
CREATE INDEX idx_analyses_high_quality ON analyses(quality_score, created_at DESC) 
    WHERE quality_score >= 0.8 AND is_public = TRUE;
```

### 3. Meters Table

```sql
-- Arabic prosodic meters reference
CREATE TABLE meters (
    id                  SERIAL PRIMARY KEY,
    name               VARCHAR(100) UNIQUE NOT NULL,  -- اسم البحر
    english_name       VARCHAR(100),
    
    -- Pattern information
    base_pattern       TEXT NOT NULL,  -- النمط الأساسي
    pattern_type       meter_type_enum NOT NULL,
    complexity_level   INTEGER CHECK (complexity_level >= 1 AND complexity_level <= 5),
    
    -- Characteristics
    syllable_count     INTEGER,
    foot_pattern       TEXT[],  -- تفعيلات البحر
    common_variations  JSONB DEFAULT '[]',
    
    -- Usage statistics
    frequency_rank     INTEGER,
    usage_count       INTEGER DEFAULT 0,
    difficulty_score  DECIMAL(3,2) CHECK (difficulty_score >= 1 AND difficulty_score <= 5),
    
    -- Historical and cultural info
    origin_period     VARCHAR(50),
    famous_poets      TEXT[],
    description_ar    TEXT,
    description_en    TEXT,
    
    -- Examples
    example_verses    JSONB DEFAULT '[]',
    audio_samples     JSONB DEFAULT '[]',
    
    -- Status
    is_active         BOOLEAN DEFAULT TRUE,
    is_classical      BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at        TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Meter type enum
CREATE TYPE meter_type_enum AS ENUM (
    'classical',      -- البحور الخليلية
    'modern',         -- البحور الحديثة  
    'folk',           -- الشعبية
    'experimental'    -- التجريبية
);

-- Indexes
CREATE INDEX idx_meters_name ON meters(name);
CREATE INDEX idx_meters_type ON meters(pattern_type);
CREATE INDEX idx_meters_difficulty ON meters(difficulty_score);
CREATE INDEX idx_meters_frequency ON meters(frequency_rank);
CREATE INDEX idx_meters_active ON meters(is_active) WHERE is_active = TRUE;

-- Full-text search on meter descriptions
CREATE INDEX idx_meters_search ON meters 
    USING GIN(to_tsvector('arabic', name || ' ' || COALESCE(description_ar, '')));
```

### 4. Meter Variants Table

```sql
-- Variations and alternative patterns for each meter
CREATE TABLE meter_variants (
    id              SERIAL PRIMARY KEY,
    meter_id        INTEGER NOT NULL REFERENCES meters(id) ON DELETE CASCADE,
    
    variant_name    VARCHAR(100) NOT NULL,
    variant_pattern TEXT NOT NULL,
    
    -- Characteristics
    confidence_weight DECIMAL(3,2) DEFAULT 1.0,
    usage_frequency   DECIMAL(5,4),  -- How often this variant appears
    region           VARCHAR(50),    -- Geographic usage
    time_period      VARCHAR(50),    -- Historical period
    
    -- Examples
    example_verses   JSONB DEFAULT '[]',
    notable_poets    TEXT[],
    
    -- Metadata
    is_active       BOOLEAN DEFAULT TRUE,
    notes           TEXT,
    
    -- Timestamps  
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_meter_variants_meter_id ON meter_variants(meter_id);
CREATE INDEX idx_meter_variants_frequency ON meter_variants(usage_frequency DESC);
CREATE INDEX idx_meter_variants_active ON meter_variants(is_active) WHERE is_active = TRUE;

-- Unique constraint
ALTER TABLE meter_variants 
    ADD CONSTRAINT uq_meter_variant UNIQUE(meter_id, variant_name);
```

---

## 🏆 Competition & Social Tables

### 5. Competitions Table (Deferred Post-MVP)

```sql
-- Poetry competitions and challenges
CREATE TABLE competitions (
    id                  SERIAL PRIMARY KEY,
    title              VARCHAR(200) NOT NULL,
    slug               VARCHAR(100) UNIQUE NOT NULL,
    description        TEXT,
    
    -- Competition details
    competition_type   competition_type_enum NOT NULL,
    theme             VARCHAR(100),
    required_meter    INTEGER REFERENCES meters(id),
    min_verses        INTEGER DEFAULT 1,
    max_verses        INTEGER DEFAULT 10,
    
    -- Timing
    start_date        TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date          TIMESTAMP WITH TIME ZONE NOT NULL,
    voting_end_date   TIMESTAMP WITH TIME ZONE,
    
    -- Prizes and rewards
    prize_pool        JSONB DEFAULT '{}',  -- {first: {coins: 1000, xp: 500}, ...}
    winner_benefits   JSONB DEFAULT '[]',
    
    -- Status and visibility
    status            competition_status_enum DEFAULT 'draft',
    is_public         BOOLEAN DEFAULT TRUE,
    requires_approval BOOLEAN DEFAULT FALSE,
    
    -- Participation
    max_participants  INTEGER,
    entry_fee_coins   INTEGER DEFAULT 0,
    
    -- Judging
    judging_criteria  JSONB DEFAULT '[]',
    auto_judging      BOOLEAN DEFAULT FALSE,
    
    -- Organizer
    created_by        INTEGER NOT NULL REFERENCES users(id),
    
    -- Statistics
    participant_count INTEGER DEFAULT 0,
    submission_count  INTEGER DEFAULT 0,
    view_count       INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Competition ENUMs
CREATE TYPE competition_type_enum AS ENUM (
    'weekly_challenge',
    'monthly_contest', 
    'meter_challenge',
    'theme_contest',
    'collaboration',
    'learning_challenge'
);

CREATE TYPE competition_status_enum AS ENUM (
    'draft',
    'published',
    'active',
    'judging', 
    'completed',
    'cancelled'
);

-- Indexes
CREATE INDEX idx_competitions_status ON competitions(status);
CREATE INDEX idx_competitions_dates ON competitions(start_date, end_date);
CREATE INDEX idx_competitions_type ON competitions(competition_type);
CREATE INDEX idx_competitions_creator ON competitions(created_by);
CREATE INDEX idx_competitions_public ON competitions(is_public) WHERE is_public = TRUE;

-- Full-text search
CREATE INDEX idx_competitions_search ON competitions 
    USING GIN(to_tsvector('arabic', title || ' ' || COALESCE(description, '')));
```

### 6. Competition Participants Table (Deferred Post-MVP)

```sql
-- Users participating in competitions
CREATE TABLE competition_participants (
    id              SERIAL PRIMARY KEY,
    competition_id  INTEGER NOT NULL REFERENCES competitions(id) ON DELETE CASCADE,
    user_id        INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Participation details
    registration_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status          participant_status_enum DEFAULT 'registered',
    
    -- Entry details
    entry_fee_paid  BOOLEAN DEFAULT FALSE,
    payment_amount  INTEGER DEFAULT 0,
    payment_date    TIMESTAMP WITH TIME ZONE,
    
    -- Performance
    submission_count INTEGER DEFAULT 0,
    best_score      DECIMAL(5,4),
    ranking         INTEGER,
    
    -- Notifications
    notify_updates  BOOLEAN DEFAULT TRUE,
    notify_results  BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at     TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Participant status enum
CREATE TYPE participant_status_enum AS ENUM (
    'registered',
    'active',
    'submitted',
    'disqualified',
    'withdrawn'
);

-- Indexes
CREATE INDEX idx_participants_competition ON competition_participants(competition_id);
CREATE INDEX idx_participants_user ON competition_participants(user_id);
CREATE INDEX idx_participants_status ON competition_participants(status);
CREATE INDEX idx_participants_ranking ON competition_participants(ranking) WHERE ranking IS NOT NULL;

-- Unique constraint
ALTER TABLE competition_participants 
    ADD CONSTRAINT uq_competition_participant UNIQUE(competition_id, user_id);
```

### 7. Submissions Table (Deferred Post-MVP)

```sql
-- Poetry submissions to competitions
CREATE TABLE submissions (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    competition_id    INTEGER NOT NULL REFERENCES competitions(id) ON DELETE CASCADE,
    user_id          INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Submission content
    title            VARCHAR(200),
    poem_text        TEXT NOT NULL,
    meter_used       INTEGER REFERENCES meters(id),
    
    -- Analysis results (cached from analyses table)
    analysis_id      UUID REFERENCES analyses(id),
    quality_score    DECIMAL(5,4),
    meter_accuracy   DECIMAL(5,4),
    
    -- Judging and scoring
    judge_scores     JSONB DEFAULT '{}',  -- {judge_id: {score: 8.5, notes: "..."}}
    auto_score       DECIMAL(5,4),
    final_score      DECIMAL(5,4),
    ranking          INTEGER,
    
    -- Public interaction
    vote_count       INTEGER DEFAULT 0,
    view_count       INTEGER DEFAULT 0,
    comment_count    INTEGER DEFAULT 0,
    
    -- Status
    status           submission_status_enum DEFAULT 'draft',
    is_public        BOOLEAN DEFAULT FALSE,
    
    -- Feedback
    judge_feedback   TEXT,
    ai_suggestions   JSONB DEFAULT '[]',
    
    -- Timestamps
    submitted_at     TIMESTAMP WITH TIME ZONE,
    created_at       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Submission status enum
CREATE TYPE submission_status_enum AS ENUM (
    'draft',
    'submitted',
    'under_review',
    'judged',
    'winner',
    'disqualified'
);

-- Indexes  
CREATE INDEX idx_submissions_competition ON submissions(competition_id);
CREATE INDEX idx_submissions_user ON submissions(user_id);
CREATE INDEX idx_submissions_status ON submissions(status);
CREATE INDEX idx_submissions_score ON submissions(final_score DESC) WHERE final_score IS NOT NULL;
CREATE INDEX idx_submissions_ranking ON submissions(ranking) WHERE ranking IS NOT NULL;
CREATE INDEX idx_submissions_public ON submissions(is_public) WHERE is_public = TRUE;

-- Full-text search on submission content
CREATE INDEX idx_submissions_search ON submissions 
    USING GIN(to_tsvector('arabic', title || ' ' || poem_text));
```

---

## 👥 Social & Interaction Tables

### 8. User Follows Table (Deferred Post-MVP)

```sql
-- User following relationships
CREATE TABLE user_follows (
    id          SERIAL PRIMARY KEY,
    follower_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    following_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Follow metadata
    status      follow_status_enum DEFAULT 'active',
    notes       TEXT,  -- Personal notes about this user
    
    -- Interaction settings
    notify_posts BOOLEAN DEFAULT TRUE,
    notify_competitions BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Follow status enum
CREATE TYPE follow_status_enum AS ENUM (
    'active',
    'muted',
    'blocked'
);

-- Indexes
CREATE INDEX idx_user_follows_follower ON user_follows(follower_id);
CREATE INDEX idx_user_follows_following ON user_follows(following_id);
CREATE INDEX idx_user_follows_status ON user_follows(status);

-- Constraints
ALTER TABLE user_follows 
    ADD CONSTRAINT uq_user_follow UNIQUE(follower_id, following_id);
ALTER TABLE user_follows 
    ADD CONSTRAINT chk_no_self_follow CHECK(follower_id != following_id);
```

### 9. Comments Table (Deferred Post-MVP)

```sql
-- Comments on submissions and analyses
CREATE TABLE comments (
    id            SERIAL PRIMARY KEY,
    user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Polymorphic relationships (could be submission, analysis, etc.)
    commentable_type VARCHAR(50) NOT NULL,  -- 'submission', 'analysis', etc.
    commentable_id   UUID NOT NULL,         -- ID of the commented object
    
    -- Comment content
    content       TEXT NOT NULL,
    language      VARCHAR(5) DEFAULT 'ar',
    
    -- Threading (replies)
    parent_id     INTEGER REFERENCES comments(id) ON DELETE CASCADE,
    thread_depth  INTEGER DEFAULT 0,
    
    -- Interaction
    like_count    INTEGER DEFAULT 0,
    reply_count   INTEGER DEFAULT 0,
    
    -- Moderation
    is_approved   BOOLEAN DEFAULT TRUE,
    is_flagged    BOOLEAN DEFAULT FALSE,
    flag_reason   TEXT,
    
    -- Timestamps
    created_at    TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at    TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE INDEX idx_comments_user ON comments(user_id);
CREATE INDEX idx_comments_commentable ON comments(commentable_type, commentable_id);
CREATE INDEX idx_comments_parent ON comments(parent_id) WHERE parent_id IS NOT NULL;
CREATE INDEX idx_comments_approved ON comments(is_approved) WHERE is_approved = TRUE;
CREATE INDEX idx_comments_created_at ON comments(created_at DESC);

-- Full-text search
CREATE INDEX idx_comments_search ON comments 
    USING GIN(to_tsvector('arabic', content));
```

### 10. Likes Table (Deferred Post-MVP)

```sql
-- Likes/reactions system
CREATE TABLE likes (
    id           SERIAL PRIMARY KEY,
    user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Polymorphic target (submission, analysis, comment, etc.)
    likeable_type VARCHAR(50) NOT NULL,
    likeable_id   UUID NOT NULL,
    
    -- Reaction type
    reaction     reaction_type_enum DEFAULT 'like',
    
    -- Timestamps
    created_at   TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Reaction types enum
CREATE TYPE reaction_type_enum AS ENUM (
    'like',
    'love', 
    'amazing',
    'insightful',
    'funny'
);

-- Indexes
CREATE INDEX idx_likes_user ON likes(user_id);
CREATE INDEX idx_likes_target ON likes(likeable_type, likeable_id);
CREATE INDEX idx_likes_reaction ON likes(reaction);

-- Unique constraint (one reaction per user per target)
ALTER TABLE likes 
    ADD CONSTRAINT uq_user_like UNIQUE(user_id, likeable_type, likeable_id);
```

---

## 📊 Analytics & Statistics Tables

### 11. Daily Stats Table (Deferred Post-MVP)

```sql
-- Daily aggregated statistics
CREATE TABLE daily_stats (
    id                  SERIAL PRIMARY KEY,
    date               DATE NOT NULL,
    
    -- User statistics  
    new_users          INTEGER DEFAULT 0,
    active_users       INTEGER DEFAULT 0,
    returning_users    INTEGER DEFAULT 0,
    
    -- Analysis statistics
    total_analyses     INTEGER DEFAULT 0,
    successful_analyses INTEGER DEFAULT 0,
    avg_processing_time INTEGER,  -- milliseconds
    
    -- Competition statistics
    active_competitions INTEGER DEFAULT 0,
    new_submissions    INTEGER DEFAULT 0,
    
    -- Content statistics
    public_submissions INTEGER DEFAULT 0,
    total_comments     INTEGER DEFAULT 0,
    total_likes        INTEGER DEFAULT 0,
    
    -- Meter usage statistics
    popular_meters     JSONB DEFAULT '{}',  -- {meter_name: count}
    
    -- Performance metrics
    avg_quality_score  DECIMAL(5,4),
    system_uptime     DECIMAL(5,4),  -- percentage
    
    -- Timestamps
    created_at        TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE UNIQUE INDEX idx_daily_stats_date ON daily_stats(date);
CREATE INDEX idx_daily_stats_created ON daily_stats(created_at DESC);
```

### 12. User Activity Logs Table (Deferred Post-MVP)

```sql
-- Detailed user activity tracking
CREATE TABLE user_activity_logs (
    id            BIGSERIAL PRIMARY KEY,  -- Use BIGSERIAL for high volume
    user_id       INTEGER REFERENCES users(id) ON DELETE SET NULL,
    
    -- Activity details
    activity_type activity_type_enum NOT NULL,
    activity_data JSONB,  -- Flexible data storage
    
    -- Context
    ip_address    INET,
    user_agent    TEXT,
    session_id    VARCHAR(255),
    
    -- Tracking
    page_path     VARCHAR(500),
    referrer      VARCHAR(500),
    
    -- Performance
    response_time INTEGER,  -- milliseconds
    
    -- Timestamp
    created_at    TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Activity types enum
CREATE TYPE activity_type_enum AS ENUM (
    'login',
    'logout',
    'analysis_performed',
    'submission_created',
    'competition_joined',
    'profile_updated',
    'comment_posted',
    'like_given',
    'follow_action',
    'page_view'
);

-- Indexes
CREATE INDEX idx_activity_user ON user_activity_logs(user_id);
CREATE INDEX idx_activity_type ON user_activity_logs(activity_type);
CREATE INDEX idx_activity_created ON user_activity_logs(created_at DESC);

-- Partial index for active users
CREATE INDEX idx_activity_recent_users ON user_activity_logs(user_id, created_at) 
    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days';

-- JSONB index for activity data
CREATE INDEX idx_activity_data_gin ON user_activity_logs USING GIN(activity_data);
```

---

## 🔧 Utility Tables

### 13. System Settings Table
---

## 🧩 اختصار مخطط المهاجرات (Migration Phasing)

Phase MVP Migrations (Weeks 1-2):
- users
- meters (+ meter_variants optional)
- analyses (core fields only: remove social counters for initial)
- system_settings (minimal config)

ملاحظات مهمة للـ MVP:
- ❌ لا تُنشئ فهارس أو تهيئات Full-Text Search عربية في هذه المرحلة.
- ✅ استخدم فهارس بسيطة على الأعمدة الأساسية (meter, created_at, user_id).
- ✅ أجّل أي Views/Materialized Views مرتبطة بالبحث حتى Post-MVP.

Deferred (Post-Launch):
- competitions, competition_participants, submissions
- user_follows, comments, likes
- daily_stats, user_activity_logs (replace with lightweight log streaming initially)

Rationale: تقليل التعقيد، تسريع التطوير، تجنب تكاليف صيانة جداول غير مستخدمة.

---

## 🧪 تبسيط جدول analyses (MVP Variant)

الحقلــان المقترح حذفهما مؤقتاً:
- share_count, view_count (يُحصيان لاحقاً عبر analytics layer)
- corrections (يُضاف بعد توافر واجهة تحرير)

الحقلــان يبقيان:
- alternative_meters
- quality_score (يُحسب بنسخة مبسطة في Week 7+)

Migration Override Example:
```sql
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    original_text TEXT NOT NULL,
    normalized_text TEXT NOT NULL,
    analysis_mode analysis_mode_enum NOT NULL DEFAULT 'accurate',
    prosodic_pattern JSONB NOT NULL,
    taqti3 TEXT,
    detected_meter VARCHAR(50),
    meter_confidence DECIMAL(5,4) CHECK (meter_confidence >= 0 AND meter_confidence <= 1),
    alternative_meters JSONB DEFAULT '[]',
    quality_score DECIMAL(5,4) CHECK (quality_score >= 0 AND quality_score <= 1),
    analysis_result JSONB NOT NULL,
    suggestions JSONB DEFAULT '[]',
    processing_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

## ✅ Checklist قبل إنشاء كل جدول (Migration Hygiene)
- فهرسة الحقول الأكثر استعمالاً (meter, created_at)
- تجنب الحقول غير المطلوبة أول 8 أسابيع
- توثيق السبب لكل إضافة جديدة في CHANGELOG / CRITICAL_CHANGES.md
- تأكيد أن الحجم التقديري < 50MB قبل الإطلاق (قياس عبر pg_class)


```sql
-- Application configuration settings
CREATE TABLE system_settings (
    id              SERIAL PRIMARY KEY,
    setting_key     VARCHAR(100) UNIQUE NOT NULL,
    setting_value   TEXT,
    setting_type    setting_type_enum NOT NULL,
    
    -- Metadata
    category        VARCHAR(50),
    description     TEXT,
    is_public       BOOLEAN DEFAULT FALSE,  -- Can be exposed to frontend
    is_readonly     BOOLEAN DEFAULT FALSE,  -- Cannot be modified via UI
    
    -- Validation
    validation_rule TEXT,  -- JSON schema or regex for validation
    default_value   TEXT,
    
    -- Timestamps
    created_at     TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Setting types enum
CREATE TYPE setting_type_enum AS ENUM (
    'string',
    'integer', 
    'boolean',
    'json',
    'array'
);

-- Indexes
CREATE INDEX idx_settings_category ON system_settings(category);
CREATE INDEX idx_settings_public ON system_settings(is_public) WHERE is_public = TRUE;

-- Sample settings
INSERT INTO system_settings (setting_key, setting_value, setting_type, category, description) VALUES
    ('max_analysis_per_day', '100', 'integer', 'limits', 'Maximum analyses per user per day'),
    ('competition_entry_fee', '10', 'integer', 'competition', 'Default entry fee in coins'),
    ('maintenance_mode', 'false', 'boolean', 'system', 'Enable maintenance mode'),
    ('featured_meters', '["الطويل", "البسيط", "الكامل"]', 'json', 'content', 'Featured meters on homepage');
```

### 14. Error Logs Table

```sql
-- Application error logging
CREATE TABLE error_logs (
    id              BIGSERIAL PRIMARY KEY,
    
    -- Error details
    error_type      VARCHAR(100) NOT NULL,
    error_message   TEXT NOT NULL,
    error_stack     TEXT,
    
    -- Request context
    user_id         INTEGER REFERENCES users(id) ON DELETE SET NULL,
    request_path    VARCHAR(500),
    request_method  VARCHAR(10),
    request_params  JSONB,
    
    -- Environment
    environment     VARCHAR(20) DEFAULT 'production',
    server_name     VARCHAR(100),
    
    -- Tracking
    session_id      VARCHAR(255),
    ip_address      INET,
    user_agent      TEXT,
    
    -- Status
    is_resolved     BOOLEAN DEFAULT FALSE,
    resolution_note TEXT,
    
    -- Timestamps  
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at     TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE INDEX idx_error_logs_type ON error_logs(error_type);
CREATE INDEX idx_error_logs_user ON error_logs(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_error_logs_unresolved ON error_logs(is_resolved, created_at) WHERE is_resolved = FALSE;
CREATE INDEX idx_error_logs_recent ON error_logs(created_at DESC);

-- Partition by month for better performance
-- (PostgreSQL 10+ feature for high-volume logging)
```

---

## 🔍 Advanced Database Features

### Full-Text Search Configuration (Deferred)

⚠️ ملاحظة هامة: **الفهرسة والبحث بالنص الكامل العربي (Full-Text Search)** مؤجلة إلى ما بعد الـ MVP.

**السبب:**
- تنفيذ FTS عربي عالي الجودة يحتاج ضبط مُخصص (stemming، normalizing، stopwords) وتجريب دقيق.
- لا توجد حاجة فورية بحث نصي معقد في أول 12 أسبوع؛ التركيز الآن على تحليل البيت وإرجاع نتائجه.
- يقلل التعقيد في المهاجرات الأولى ويحافظ على سرعة التطوير.

**نطاق الـ MVP:**
- الاكتفاء باسترجاع التحليلات حسب المستخدم أو المعرّف أو البحر.
- عدم إنشاء تهيئة نص عربي مخصصة الآن (arabic_config) في قاعدة الإنتاج الأولى.
- حذف/تعليق أية Materialized Views تعتمد على FTS حتى مرحلة Post-MVP.

**يُفعَّل لاحقاً (Phase Post-MVP):**
- إنشاء TEXT SEARCH CONFIGURATION مخصص.
- إضافة جداول/أعمدة مساعدة للفهرسة (normalized_text المخزنة مسبقاً).
- اختبار دقة البحث مقابل مجموعة 2000+ بيت.

عند التفعيل لاحقاً، يُستخدم المثال التالي (مُدرج كمرجع فقط الآن):

```sql
-- Create Arabic text search configuration
CREATE TEXT SEARCH CONFIGURATION arabic_config (COPY = simple);

-- Add Arabic-specific dictionaries and rules
ALTER TEXT SEARCH CONFIGURATION arabic_config
    ALTER MAPPING FOR word WITH arabic_stem, simple;

-- Create custom search functions
CREATE OR REPLACE FUNCTION search_poems(search_query TEXT)
RETURNS TABLE(
    id UUID,
    title VARCHAR(200),
    poem_text TEXT,
    user_name VARCHAR(100),
    quality_score DECIMAL(5,4),
    rank REAL
)
LANGUAGE SQL
AS $$
    SELECT 
        s.id,
        s.title,
        s.poem_text,
        u.full_name,
        s.quality_score,
        ts_rank(
            to_tsvector('arabic_config', s.title || ' ' || s.poem_text),
            plainto_tsquery('arabic_config', search_query)
        ) as rank
    FROM submissions s
    JOIN users u ON s.user_id = u.id
    WHERE s.is_public = TRUE
    AND to_tsvector('arabic_config', s.title || ' ' || s.poem_text) @@ 
        plainto_tsquery('arabic_config', search_query)
    ORDER BY rank DESC, s.quality_score DESC
    LIMIT 50;
$$;
```

### Materialized Views for Performance

```sql
-- Materialized view for user statistics
CREATE MATERIALIZED VIEW user_stats_mv AS
SELECT 
    u.id as user_id,
    u.username,
    u.level,
    u.xp,
    COUNT(a.id) as total_analyses,
    COUNT(s.id) as total_submissions,
    AVG(a.quality_score) as avg_quality,
    COUNT(cp.id) as competitions_joined,
    MAX(a.created_at) as last_analysis_date
FROM users u
LEFT JOIN analyses a ON u.id = a.user_id
LEFT JOIN submissions s ON u.id = s.user_id  
LEFT JOIN competition_participants cp ON u.id = cp.user_id
WHERE u.is_active = TRUE
GROUP BY u.id, u.username, u.level, u.xp;

-- Index on materialized view
CREATE UNIQUE INDEX idx_user_stats_mv_user_id ON user_stats_mv(user_id);
CREATE INDEX idx_user_stats_mv_level ON user_stats_mv(level DESC);

-- Refresh function
CREATE OR REPLACE FUNCTION refresh_user_stats()
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats_mv;
END;
$$;
```

### Partitioning Strategy

```sql
-- Partition large tables by date for better performance
CREATE TABLE analyses_partitioned (
    LIKE analyses INCLUDING ALL
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE analyses_2024_01 PARTITION OF analyses_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE analyses_2024_02 PARTITION OF analyses_partitioned  
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Auto-partition function
CREATE OR REPLACE FUNCTION create_monthly_partition(table_name TEXT, start_date DATE)
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
    partition_name TEXT;
    end_date DATE;
BEGIN
    partition_name := table_name || '_' || to_char(start_date, 'YYYY_MM');
    end_date := start_date + INTERVAL '1 month';
    
    EXECUTE format('CREATE TABLE %I PARTITION OF %I 
                   FOR VALUES FROM (%L) TO (%L)',
                   partition_name, table_name, start_date, end_date);
END;
$$;
```

---

## ⚡ Performance Optimization

### Essential Functions

```sql
-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Cache meter usage statistics
CREATE OR REPLACE FUNCTION update_meter_usage_stats()
RETURNS TRIGGER AS $$
BEGIN
    -- Update meter usage count
    UPDATE meters 
    SET usage_count = usage_count + 1 
    WHERE id = NEW.detected_meter;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_update_meter_usage 
    AFTER INSERT ON analyses 
    FOR EACH ROW 
    WHEN (NEW.detected_meter IS NOT NULL)
    EXECUTE FUNCTION update_meter_usage_stats();

-- Automatic user level calculation
CREATE OR REPLACE FUNCTION calculate_user_level(user_xp INTEGER)
RETURNS INTEGER AS $$
BEGIN
    -- Simple level calculation: level = floor(sqrt(xp/100)) + 1
    RETURN FLOOR(SQRT(user_xp::FLOAT / 100.0)) + 1;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Update user level when XP changes
CREATE OR REPLACE FUNCTION update_user_level()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.xp != OLD.xp THEN
        NEW.level = calculate_user_level(NEW.xp);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_update_user_level 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_user_level();
```

### Database Maintenance

```sql
-- Cleanup old logs and temporary data
CREATE OR REPLACE FUNCTION cleanup_old_data()
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    -- Delete old activity logs (older than 90 days)
    DELETE FROM user_activity_logs 
    WHERE created_at < CURRENT_DATE - INTERVAL '90 days';
    
    -- Delete old error logs (older than 30 days and resolved)
    DELETE FROM error_logs 
    WHERE created_at < CURRENT_DATE - INTERVAL '30 days'
    AND is_resolved = TRUE;
    
    -- Clean up orphaned records
    DELETE FROM comments 
    WHERE commentable_type = 'submission' 
    AND commentable_id::TEXT NOT IN (SELECT id::TEXT FROM submissions);
    
    -- Update statistics
    INSERT INTO daily_stats (date, total_analyses, total_comments)
    SELECT 
        CURRENT_DATE,
        COUNT(*) FILTER (WHERE created_at::date = CURRENT_DATE),
        (SELECT COUNT(*) FROM comments WHERE created_at::date = CURRENT_DATE)
    FROM analyses
    ON CONFLICT (date) DO UPDATE SET
        total_analyses = EXCLUDED.total_analyses,
        total_comments = EXCLUDED.total_comments;
        
    -- Vacuum and analyze critical tables
    VACUUM ANALYZE analyses;
    VACUUM ANALYZE submissions;
    VACUUM ANALYZE user_activity_logs;
END;
$$;

-- Schedule daily cleanup (requires pg_cron extension)
-- SELECT cron.schedule('cleanup-job', '0 2 * * *', 'SELECT cleanup_old_data();');
```

---

## 🔐 Security & Constraints

### Row Level Security (RLS)

```sql
-- Enable RLS on sensitive tables
ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_activity_logs ENABLE ROW LEVEL SECURITY;

-- Policy for analyses - users can only see their own private analyses
CREATE POLICY analyses_select_policy ON analyses
    FOR SELECT
    USING (
        user_id = current_user_id() 
        OR is_public = TRUE
        OR current_user_role() = 'admin'
    );

-- Policy for submissions - based on competition and privacy settings
CREATE POLICY submissions_select_policy ON submissions
    FOR SELECT  
    USING (
        user_id = current_user_id()
        OR is_public = TRUE
        OR EXISTS (
            SELECT 1 FROM competition_participants cp
            WHERE cp.competition_id = submissions.competition_id
            AND cp.user_id = current_user_id()
        )
        OR current_user_role() IN ('moderator', 'admin')
    );

-- Helper functions for RLS
CREATE OR REPLACE FUNCTION current_user_id()
RETURNS INTEGER AS $$
BEGIN
    RETURN COALESCE(current_setting('app.user_id', true)::INTEGER, 0);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION current_user_role()
RETURNS TEXT AS $$
BEGIN
    RETURN COALESCE(current_setting('app.user_role', true), 'anonymous');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### Data Validation

```sql
-- Check constraints for data integrity
ALTER TABLE analyses ADD CONSTRAINT chk_quality_score_range 
    CHECK (quality_score IS NULL OR (quality_score >= 0 AND quality_score <= 1));

ALTER TABLE analyses ADD CONSTRAINT chk_confidence_range
    CHECK (meter_confidence IS NULL OR (meter_confidence >= 0 AND meter_confidence <= 1));

ALTER TABLE users ADD CONSTRAINT chk_level_positive
    CHECK (level > 0);

ALTER TABLE users ADD CONSTRAINT chk_xp_non_negative
    CHECK (xp >= 0);

ALTER TABLE competitions ADD CONSTRAINT chk_competition_dates
    CHECK (end_date > start_date);

-- Custom domain for email validation
CREATE DOMAIN email_address AS VARCHAR(255)
    CHECK (VALUE ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Use domain in users table
ALTER TABLE users ALTER COLUMN email TYPE email_address;
```

---

## 📈 Sample Data & Seeding

### Initial Data

```sql
-- Insert default meters
INSERT INTO meters (name, english_name, base_pattern, pattern_type, complexity_level, syllable_count, foot_pattern) VALUES
    ('الطويل', 'At-Taweel', 'فعولن مفاعيلن فعولن مفاعيلن', 'classical', 2, 16, ARRAY['فعولن', 'مفاعيلن']),
    ('البسيط', 'Al-Baseet', 'مستفعلن فاعلن مستفعلن فاعلن', 'classical', 2, 16, ARRAY['مستفعلن', 'فاعلن']),
    ('الكامل', 'Al-Kamil', 'متفاعلن متفاعلن متفاعلن', 'classical', 1, 15, ARRAY['متفاعلن']),
    ('الوافر', 'Al-Wafir', 'مفاعلتن مفاعلتن فعولن', 'classical', 3, 14, ARRAY['مفاعلتن', 'فعولن']),
    ('الرجز', 'Ar-Rajaz', 'مستفعلن مستفعلن مستفعلن', 'classical', 1, 15, ARRAY['مستفعلن']);

-- Insert meter variants
INSERT INTO meter_variants (meter_id, variant_name, variant_pattern, usage_frequency) VALUES
    (1, 'الطويل المحذوف', 'فعولن مفاعيلن فعولن مفاعيل', 0.3),
    (2, 'البسيط المطوي', 'مفتعلن فاعلن مفتعلن فاعلن', 0.2),
    (3, 'الكامل المحذذف', 'متفاعلن متفاعلن متفاعل', 0.4);

-- Insert system settings
INSERT INTO system_settings (setting_key, setting_value, setting_type, category, description, is_public) VALUES
    ('app_name', 'بَحْر - منصة تحليل الشعر العربي', 'string', 'general', 'Application name', true),
    ('max_daily_analyses', '50', 'integer', 'limits', 'Max analyses per user per day', false),
    ('competition_announcement', 'مسابقة أفضل قصيدة هذا الشهر', 'string', 'announcements', 'Current competition announcement', true),
    ('featured_poets', '["امرؤ القيس", "الفرزدق", "جرير"]', 'json', 'content', 'Featured classical poets', true);

-- Create admin user
INSERT INTO users (username, email, password_hash, full_name, role, level, xp, is_verified) VALUES
    ('admin', 'admin@bahr.app', '$2b$12$encrypted_password_hash', 'مدير النظام', 'admin', 10, 5000, true);
```

---

---

## 🔄 Database Migration Safety Best Practices

### Critical Migration Rules

**Never do these in production:**
```sql
-- ❌ DANGEROUS: Dropping columns (data loss)
ALTER TABLE users DROP COLUMN old_field;

-- ❌ DANGEROUS: Changing column types (can fail with data)
ALTER TABLE analyses ALTER COLUMN meter_confidence TYPE VARCHAR;

-- ❌ DANGEROUS: Adding NOT NULL without default (breaks existing rows)
ALTER TABLE users ADD COLUMN required_field VARCHAR(50) NOT NULL;

-- ❌ DANGEROUS: Renaming columns (breaks running code)
ALTER TABLE meters RENAME COLUMN name_ar TO arabic_name;
```

**Do this instead:**
```sql
-- ✅ SAFE: Mark column as deprecated (soft delete)
ALTER TABLE users ADD COLUMN old_field_deprecated BOOLEAN DEFAULT TRUE;
COMMENT ON COLUMN users.old_field IS 'DEPRECATED: Use new_field instead. Remove in v2.0';

-- ✅ SAFE: Add new column, migrate data, then drop old (3-step process)
-- Step 1 (migration 001): Add new column
ALTER TABLE analyses ADD COLUMN meter_confidence_new DECIMAL(5,4);

-- Step 2 (migration 002): Backfill data
UPDATE analyses SET meter_confidence_new = meter_confidence::DECIMAL WHERE meter_confidence IS NOT NULL;

-- Step 3 (migration 003 - after deploy): Drop old column
ALTER TABLE analyses DROP COLUMN meter_confidence;

-- ✅ SAFE: Add NOT NULL in 2 steps
-- Step 1: Add nullable column with default
ALTER TABLE users ADD COLUMN required_field VARCHAR(50) DEFAULT 'default_value';

-- Step 2 (after backfill): Make it NOT NULL
ALTER TABLE users ALTER COLUMN required_field SET NOT NULL;

-- ✅ SAFE: Rename via alias (keep both for transition period)
ALTER TABLE meters ADD COLUMN arabic_name VARCHAR(50);
UPDATE meters SET arabic_name = name_ar;
-- Deploy code that uses arabic_name
-- Later: DROP COLUMN name_ar (migration 005)
```

### Migration File Template

```python
# alembic/versions/001_safe_migration_template.py

"""
Safe migration template

Revision ID: 001_safe_migration
Revises: 
Create Date: 2025-11-08 20:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_safe_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    """
    Apply migration
    
    SAFETY CHECKLIST:
    - [ ] Tested on copy of production database
    - [ ] Rollback procedure documented
    - [ ] No data loss risk
    - [ ] Backwards compatible with running code
    - [ ] Can be applied with zero downtime
    - [ ] Estimated duration: < 30 seconds
    """
    # Example: Add new column (safe)
    op.add_column(
        'users',
        sa.Column('phone_number', sa.String(20), nullable=True)  # nullable = safe
    )
    
    # Example: Create index concurrently (safe, no locks)
    op.create_index(
        'idx_users_phone',
        'users',
        ['phone_number'],
        unique=False,
        postgresql_concurrently=True  # CRITICAL: No table locks
    )
    
    # Example: Add constraint (after backfill data)
    op.create_check_constraint(
        'ck_users_phone_format',
        'users',
        "phone_number ~ '^[+]?[0-9]{10,15}$'"  # Regex validation
    )

def downgrade() -> None:
    """
    Rollback migration
    
    IMPORTANT: Test rollback procedure!
    """
    op.drop_constraint('ck_users_phone_format', 'users', type_='check')
    op.drop_index('idx_users_phone', table_name='users', postgresql_concurrently=True)
    op.drop_column('users', 'phone_number')
```

### Safe Migration Patterns

```python
# Pattern 1: Add column with default value
def upgrade():
    op.add_column('users', sa.Column('is_premium', sa.Boolean(), server_default='false'))

def downgrade():
    op.drop_column('users', 'is_premium')

# Pattern 2: Create index concurrently (no table lock)
def upgrade():
    # Use raw SQL for CONCURRENTLY (not supported in op.create_index)
    op.execute(
        "CREATE INDEX CONCURRENTLY idx_analyses_meter_confidence "
        "ON analyses(meter_confidence DESC) "
        "WHERE meter_confidence >= 0.65"
    )

def downgrade():
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS idx_analyses_meter_confidence")

# Pattern 3: Backfill data safely (batched updates)
def upgrade():
    # Add new column
    op.add_column('analyses', sa.Column('era', sa.String(20)))
    
    # Backfill in batches to avoid long transactions
    connection = op.get_bind()
    connection.execute(
        sa.text("""
            UPDATE analyses 
            SET era = 'classical' 
            WHERE created_at < '2000-01-01' 
              AND era IS NULL
            LIMIT 1000  -- Process in chunks
        """)
    )
    # Repeat until all rows updated
    # Or use background job for large tables

def downgrade():
    op.drop_column('analyses', 'era')

# Pattern 4: Column deprecation (3-phase approach)
# Phase 1 (Week 1): Add new column, keep old
def upgrade_phase1():
    op.add_column('users', sa.Column('email_verified_new', sa.Boolean(), server_default='false'))
    op.execute("UPDATE users SET email_verified_new = email_verified WHERE email_verified IS NOT NULL")

# Phase 2 (Week 2): Deploy code using new column (both columns exist)
# No migration, just code deployment

# Phase 3 (Week 3): Drop old column
def upgrade_phase3():
    op.drop_column('users', 'email_verified')  # Safe now, code doesn't use it
```

### Rollback Procedure Documentation

```yaml
# migration_rollback_plan.yml

migration_id: 005_add_user_preferences
date: 2025-11-15
estimated_duration: 45 seconds
risk_level: low

changes_applied:
  - Added column: users.preferences (JSONB)
  - Created index: idx_users_preferences_gin
  - Updated 1,234 existing rows with default value

rollback_steps:
  1. Stop application deployments
  2. Run downgrade migration:
     $ alembic downgrade -1
  3. Verify rollback:
     $ psql -c "SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name='preferences';"
     # Should return 0 rows
  4. Check index:
     $ psql -c "\d users"
     # idx_users_preferences_gin should not appear
  5. Resume deployments

rollback_risks:
  - Data added to 'preferences' column will be lost (if any)
  - Application code expecting 'preferences' will fail

mitigation:
  - Take database snapshot before migration
  - Test rollback on staging first
  - Coordinate with code deployment (deploy old code first, then rollback migration)

estimated_rollback_duration: 30 seconds

emergency_contact:
  - DBA: dba@bahr-platform.com
  - DevOps: devops@bahr-platform.com
```

### Pre-Migration Checklist

```markdown
## Before Running Migration in Production

### Testing
- [ ] Applied migration to exact copy of production database
- [ ] Verified migration completes successfully
- [ ] Tested rollback procedure
- [ ] Checked migration duration (< 30 seconds for tables < 1M rows)
- [ ] Verified no table locks with `SELECT * FROM pg_locks WHERE NOT granted`

### Safety
- [ ] Migration is backwards compatible (old code still works)
- [ ] No DROP COLUMN or DROP TABLE statements
- [ ] No ALTER COLUMN TYPE without explicit USING clause
- [ ] All new NOT NULL columns have DEFAULT values
- [ ] All indexes created with CONCURRENTLY keyword

### Documentation
- [ ] Rollback procedure documented
- [ ] Estimated duration documented
- [ ] Risk assessment completed
- [ ] Stakeholders notified (if high-risk migration)

### Monitoring
- [ ] Grafana dashboard ready to monitor migration impact
- [ ] Alert rules configured for:
  - High database CPU usage
  - Long-running queries
  - Connection pool exhaustion
  - Replication lag (if applicable)

### Backup
- [ ] Recent database backup verified (< 24 hours old)
- [ ] Backup restoration tested recently
- [ ] Snapshot created immediately before migration

### Execution Plan
- [ ] Migration scheduled during low-traffic window
- [ ] Team available for support (DBA, DevOps, Backend dev)
- [ ] Communication channel open (Slack #deployments)
- [ ] Rollback decision threshold defined (e.g., if duration > 2 minutes, rollback)
```

### Common Migration Anti-Patterns to Avoid

```sql
-- ❌ Anti-Pattern 1: Locking table for long time
ALTER TABLE large_table ADD COLUMN new_field TEXT NOT NULL DEFAULT 'value';
-- Problem: Locks table during backfill of millions of rows

-- ✅ Solution: 2-step approach
ALTER TABLE large_table ADD COLUMN new_field TEXT;  -- Fast, no default
UPDATE large_table SET new_field = 'value' WHERE new_field IS NULL;  -- Background job
ALTER TABLE large_table ALTER COLUMN new_field SET DEFAULT 'value';
ALTER TABLE large_table ALTER COLUMN new_field SET NOT NULL;

-- ❌ Anti-Pattern 2: Creating index without CONCURRENTLY
CREATE INDEX idx_analyses_meter ON analyses(detected_meter);
-- Problem: Locks table, blocks writes

-- ✅ Solution: Use CONCURRENTLY
CREATE INDEX CONCURRENTLY idx_analyses_meter ON analyses(detected_meter);

-- ❌ Anti-Pattern 3: Dropping constraint immediately
ALTER TABLE users DROP CONSTRAINT ck_email_format;
-- Problem: Running code may rely on this constraint

-- ✅ Solution: 2-phase removal
-- Phase 1: Remove constraint validation in code
-- Phase 2 (1 week later): Drop constraint in migration

-- ❌ Anti-Pattern 4: Complex data transformations in migration
UPDATE users SET metadata = jsonb_set(metadata, '{legacy}', 'true') WHERE created_at < '2020-01-01';
-- Problem: Slow, can timeout

-- ✅ Solution: Background job
-- Create migration that adds column
-- Separate Python script/Celery task to backfill data in batches
```

### Migration Monitoring Queries

```sql
-- Check migration progress (run in separate session)
SELECT 
  pid,
  usename,
  application_name,
  state,
  query_start,
  now() - query_start AS duration,
  query
FROM pg_stat_activity
WHERE query LIKE '%alembic%' OR query LIKE '%ALTER TABLE%'
ORDER BY query_start DESC;

-- Check for blocked queries
SELECT 
  blocked_locks.pid AS blocked_pid,
  blocked_activity.usename AS blocked_user,
  blocking_locks.pid AS blocking_pid,
  blocking_activity.usename AS blocking_user,
  blocked_activity.query AS blocked_statement,
  blocking_activity.query AS current_statement_in_blocking_process
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- Check table bloat after migration
SELECT 
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
  n_live_tup,
  n_dead_tup,
  round(n_dead_tup::numeric / NULLIF(n_live_tup, 0), 4) AS dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

---

## 🎯 Migration Strategy

### Alembic Configuration

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.models import Base  # Import all models
from app.config import settings

# Alembic Config object
config = context.config

# Override sqlalchemy.url from app settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

## 📊 Performance Monitoring

### Essential Indexes Summary

```sql
-- Critical indexes for performance
-- Users table
CREATE INDEX CONCURRENTLY idx_users_performance ON users(is_active, level DESC, created_at);

-- Analyses table  
CREATE INDEX CONCURRENTLY idx_analyses_performance ON analyses(user_id, created_at DESC) WHERE quality_score >= 0.7;

-- Submissions table
CREATE INDEX CONCURRENTLY idx_submissions_performance ON submissions(competition_id, final_score DESC) WHERE status = 'submitted';

-- Comments table
CREATE INDEX CONCURRENTLY idx_comments_performance ON comments(commentable_type, commentable_id, created_at DESC) WHERE is_approved = TRUE;

-- Activity logs (for reporting)
CREATE INDEX CONCURRENTLY idx_activity_reporting ON user_activity_logs(activity_type, created_at) WHERE created_at >= CURRENT_DATE - INTERVAL '7 days';
```

### Database Size Estimates

```sql
-- Monitor table sizes
SELECT 
    schemaname,
    tablename,
    pg_total_relation_size(schemaname||'.'||tablename) AS size_bytes,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size_pretty,
    n_tup_ins + n_tup_upd + n_tup_del AS total_operations
FROM pg_tables t
JOIN pg_stat_user_tables s ON t.tablename = s.relname
WHERE schemaname = 'public'
ORDER BY size_bytes DESC;
```

---

## 🎯 Next Steps

✅ **Database Design Document مكتمل**

التالي في القائمة:
1. **[Development Workflow Guide](../workflows/DEVELOPMENT_WORKFLOW.md)** - Git وسير العمل 
2. **[Arabic NLP Research](../research/ARABIC_NLP_RESEARCH.md)** - مراجع المكتبات العربية
3. **[Project Timeline](../planning/PROJECT_TIMELINE.md)** - الخطة الزمنية المفصلة

---

## 📝 ملخص المميزات

### 🔧 Technical Excellence:
- **PostgreSQL 15** مع دعم كامل للنصوص العربية
- **Indexing استراتيجي** للاستعلامات السريعة  
- **Row Level Security** لحماية البيانات
- **Partitioning** للجداول الكبيرة
- **Full-text search** باللغة العربية

### 📊 Scalability Ready:
- **Materialized Views** للإحصائيات 
- **Connection Pooling** للأداء
- **Background Jobs** للمعالجة الثقيلة
- **Cleanup Functions** للصيانة التلقائية
- **Migration Strategy** للتطوير المستمر

---

**🗄️ هذا يكمل تصميم قاعدة البيانات الشامل - الأساس القوي لحفظ وإدارة بيانات المشروع!**