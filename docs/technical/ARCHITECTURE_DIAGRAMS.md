# 🏗️ Architecture Diagrams
## Visual System Design for BAHR Arabic Poetry Platform

---

**Document Type:** Architecture Visualization (C4 Model)  
**Last Updated:** November 8, 2025  
**Diagram Format:** PlantUML (text) + Mermaid (rendered in GitHub)  
**Audience:** Developers, Architects, Stakeholders

---

## 📋 Overview

This document provides **visual representations** of the BAHR system architecture using the C4 Model:
- **Level 1:** System Context (how BAHR fits in the world)
- **Level 2:** Container Diagram (high-level technical components)
- **Level 3:** Component Diagram (internal structure)
- **Level 4:** Sequence Diagrams (detailed interactions)

**Rendering:**
- GitHub Markdown auto-renders Mermaid diagrams
- PlantUML source provided for customization
- Export to PNG/SVG: https://plantuml.com/ or Mermaid Live Editor

---

## 1. System Context Diagram (C4 Level 1)

**Purpose:** Shows BAHR's place in the broader ecosystem.

### Mermaid Diagram:

```mermaid
C4Context
    title System Context - BAHR Arabic Poetry Platform (MVP)

    Person(user, "Poetry Enthusiast", "Student, poet, or researcher analyzing Arabic poetry")
    
    System(bahr, "BAHR Platform", "Analyzes Arabic poetry prosody, detects meters, assesses quality")
    
    System_Ext(postgres, "PostgreSQL", "Stores user data, analyses, meters")
    System_Ext(redis, "Redis", "Caches analysis results, rate limiting")
    System_Ext(sentry, "Sentry", "Error tracking and monitoring (optional)")
    System_Ext(email, "Email Service", "SendGrid for notifications (Phase 2)")
    
    Rel(user, bahr, "Analyzes verses, views history", "HTTPS/JSON")
    Rel(bahr, postgres, "Reads/writes data", "PostgreSQL protocol")
    Rel(bahr, redis, "Caches results, rate limits", "Redis protocol")
    Rel(bahr, sentry, "Sends errors", "HTTPS")
    Rel(bahr, email, "Sends notifications (Phase 2)", "SMTP/API")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

### Key Actors:
- **User:** Interacts with BAHR via web browser (Next.js frontend)
- **BAHR Platform:** Core system (FastAPI backend + Prosody Engine)
- **External Systems:** Database, cache, monitoring, email (future)

---

## 2. Container Diagram (C4 Level 2)

**Purpose:** Shows the major technical containers that make up BAHR.

### Mermaid Diagram:

```mermaid
C4Container
    title Container Diagram - BAHR Platform (MVP)

    Person(user, "User", "Poetry enthusiast")

    Container_Boundary(bahr, "BAHR Platform") {
        Container(web, "Web Application", "Next.js 14, TypeScript", "Provides poetry analysis UI in browser")
        Container(api, "API Application", "FastAPI, Python 3.11", "Handles API requests, orchestrates analysis")
        Container(prosody, "Prosody Engine", "Python 3.11", "Normalizes text, detects meters, scores quality")
    }

    ContainerDb(postgres, "Database", "PostgreSQL 15", "Stores users, analyses, meters")
    ContainerDb(redis, "Cache", "Redis 7", "Caches analysis results, rate limiting")
    
    System_Ext(monitoring, "Monitoring", "Prometheus + Grafana (partial)")

    Rel(user, web, "Uses", "HTTPS")
    Rel(web, api, "Makes API calls", "JSON/HTTPS")
    Rel(api, prosody, "Calls analysis functions", "Direct Python calls")
    Rel(api, postgres, "Reads/writes", "SQLAlchemy ORM")
    Rel(api, redis, "Caches, rate limits", "Redis client")
    Rel(api, monitoring, "Exports metrics", "Prometheus scrape")

    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
```

### Container Responsibilities:

| Container | Technology | Purpose | Scaling Strategy |
|-----------|-----------|---------|------------------|
| **Web Application** | Next.js 14 (App Router) | User interface, form validation | Serverless (Vercel) |
| **API Application** | FastAPI + Uvicorn | Request handling, auth, routing | Horizontal (Docker containers) |
| **Prosody Engine** | Python 3.11 (CAMeL Tools) | Text analysis, meter detection | In-process (no separate deployment) |
| **Database** | PostgreSQL 15 | Persistent data storage | Vertical (managed service: Supabase/Neon) |
| **Cache** | Redis 7 | Ephemeral data, rate limiting | Managed service (Railway Redis) |

---

## 3. Component Diagram (C4 Level 3)

**Purpose:** Internal structure of the API Application container.

### Mermaid Diagram:

```mermaid
C4Component
    title Component Diagram - API Application (FastAPI Backend)

    Container_Boundary(api, "API Application") {
        Component(router, "API Router", "FastAPI Router", "Routes requests to endpoints")
        Component(middleware, "Middleware Stack", "FastAPI Middleware", "Auth, rate limiting, logging, CORS")
        Component(auth, "Auth Service", "JWT Handler", "Validates tokens, manages sessions")
        Component(analysis_svc, "Analysis Service", "Business Logic", "Orchestrates prosody analysis")
        Component(user_svc, "User Service", "Business Logic", "User management operations")
        Component(normalizer, "Text Normalizer", "Prosody Engine", "Removes diacritics, unifies characters")
        Component(segmenter, "Syllable Segmenter", "Prosody Engine", "Breaks text into syllables")
        Component(detector, "Meter Detector", "Prosody Engine", "Matches patterns to meters")
        Component(scorer, "Quality Scorer", "Prosody Engine", "Assesses verse quality")
        Component(cache, "Cache Manager", "Redis Client", "Get/set cached results")
        Component(repo, "Repositories", "SQLAlchemy", "Database access layer")
    }

    ContainerDb(postgres, "PostgreSQL", "Database")
    ContainerDb(redis, "Redis", "Cache")

    Rel(router, middleware, "Passes request through")
    Rel(middleware, auth, "Validates JWT")
    Rel(middleware, analysis_svc, "Routes to service")
    Rel(analysis_svc, cache, "Check cache")
    Rel(analysis_svc, normalizer, "Normalize text")
    Rel(normalizer, segmenter, "Segment syllables")
    Rel(segmenter, detector, "Detect meter")
    Rel(detector, scorer, "Score quality")
    Rel(analysis_svc, repo, "Persist result")
    Rel(user_svc, repo, "User CRUD")
    Rel(repo, postgres, "SQL queries")
    Rel(cache, redis, "Redis commands")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

### Component Interaction:

**Request Path:**
1. Router receives `/api/v1/analyze` POST
2. Middleware validates JWT, checks rate limit
3. Analysis Service checks cache (Redis)
4. If cache miss: Normalizer → Segmenter → Detector → Scorer
5. Analysis Service persists result (PostgreSQL via Repository)
6. Response returned with envelope

---

## 4. Sequence Diagrams

### 4.1 Verse Analysis Flow (Happy Path)

```mermaid
sequenceDiagram
    actor User
    participant Web as Web App (Next.js)
    participant API as FastAPI Backend
    participant Cache as Redis Cache
    participant Engine as Prosody Engine
    participant DB as PostgreSQL

    User->>Web: Enter verse text
    Web->>API: POST /api/v1/analyze {text: "..."}
    
    API->>API: Validate JWT (middleware)
    API->>API: Check rate limit (middleware)
    
    API->>Cache: GET analysis:{hash(text)}
    alt Cache Hit
        Cache-->>API: Cached result
        API-->>Web: 200 OK {meter, confidence, ...}
    else Cache Miss
        Cache-->>API: null
        API->>Engine: normalize(text)
        Engine-->>API: normalized_text
        API->>Engine: segment(normalized_text)
        Engine-->>API: syllables[]
        API->>Engine: detect_meter(syllables)
        Engine-->>API: {meter, confidence, alternatives}
        API->>Engine: assess_quality(...)
        Engine-->>API: quality_score
        
        API->>DB: INSERT INTO analyses (...)
        DB-->>API: analysis_id
        
        API->>Cache: SET analysis:{hash} {result} EX 3600
        Cache-->>API: OK
        
        API-->>Web: 200 OK {meter, confidence, ...}
    end
    
    Web-->>User: Display result
```

**Key Points:**
- Cache reduces latency from ~500ms to ~30ms
- Normalization is idempotent (same input → same output)
- All steps logged with request_id for tracing

---

### 4.2 User Registration Flow

```mermaid
sequenceDiagram
    actor User
    participant Web as Web App
    participant API as FastAPI Backend
    participant Auth as Auth Service
    participant DB as PostgreSQL

    User->>Web: Fill registration form
    Web->>API: POST /api/v1/auth/register {username, email, password}
    
    API->>API: Validate input (Pydantic)
    
    API->>DB: SELECT * FROM users WHERE email=?
    alt User exists
        DB-->>API: User record
        API-->>Web: 409 Conflict {error: "Email already registered"}
        Web-->>User: Show error message
    else User does not exist
        DB-->>API: null
        
        API->>Auth: hash_password(password)
        Auth-->>API: password_hash
        
        API->>DB: INSERT INTO users (username, email, password_hash, ...)
        DB-->>API: user_id
        
        API->>Auth: create_access_token(user_id)
        Auth-->>API: access_token
        
        API->>Auth: create_refresh_token(user_id)
        Auth-->>API: refresh_token
        
        API-->>Web: 201 Created {user_id, access_token, refresh_token}
        Web->>Web: Store tokens in localStorage
        Web-->>User: Redirect to dashboard
    end
```

**Security Notes:**
- Password hashed with bcrypt (cost factor 12)
- JWT includes jti (JWT ID) for revocation
- Refresh token valid for 7 days, access token 30 minutes

---

### 4.3 Error Handling Flow (Graceful Degradation)

```mermaid
sequenceDiagram
    actor User
    participant API as FastAPI Backend
    participant Engine as Prosody Engine
    participant Cache as Redis
    participant DB as PostgreSQL
    participant Monitoring as Sentry

    User->>API: POST /api/v1/analyze {text: "..."}
    
    API->>Engine: analyze(text)
    
    alt NLP Library Error
        Engine->>Engine: CAMeL Tools fails
        Engine->>Monitoring: Log error (ERR_NLP_001)
        Engine->>Engine: Fallback to rule-based only
        Engine-->>API: result (with fallback=true)
        API-->>User: 200 OK {data, meta: {fallback: true}}
    else Database Timeout
        API->>DB: INSERT INTO analyses
        DB-->>API: Timeout (5 seconds)
        API->>Monitoring: Log critical error (ERR_DB_001)
        API-->>User: 500 Internal Server Error {error: {code: "ERR_DB_001", message: "..."}}
    else Redis Unavailable
        API->>Cache: SET analysis:{hash}
        Cache-->>API: Connection refused
        API->>Monitoring: Log warning (ERR_CACHE_001)
        Note over API: Continue without caching
        API-->>User: 200 OK {data, meta: {cached: false}}
    else Input Too Long
        API->>API: Validate text length
        Note over API: Length > 2000 characters
        API-->>User: 413 Payload Too Large {error: {code: "ERR_INPUT_003", suggestion: "..."}}
    else Rate Limit Exceeded
        API->>Cache: INCR ratelimit:{user_id}
        Cache-->>API: count > 100
        API-->>User: 429 Too Many Requests {error: {code: "ERR_RATE_001", wait_time: 60}}
    end
```

**Fallback Strategy:**
1. CAMeL Tools fails → Use simple regex-based normalization
2. Database unavailable → Return result without persisting (log error)
3. Redis unavailable → Continue without cache (performance hit, but functional)
4. All external systems down → Return basic analysis with warnings

---

## 5. Data Flow Diagrams

### 5.1 Analysis Request Data Flow

```mermaid
flowchart TB
    Start([User submits verse]) --> Input[/"Raw Arabic text\n(with diacritics)"/]
    
    Input --> Normalize["Normalize Text\n- Remove diacritics\n- Unify Alif variants\n- Clean punctuation"]
    
    Normalize --> Normalized[/"Normalized text\n(plain Arabic)"/]
    
    Normalized --> Segment["Syllable Segmentation\n- CV pattern detection\n- Long/short classification"]
    
    Segment --> Syllables[/"Syllable array\n[{text, long}, ...]"/]
    
    Syllables --> Pattern["Build Pattern\n- Convert to '-' (long) and 'u' (short)\n- Group into feet"]
    
    Pattern --> PatternStr[/"Pattern string\n'- u - - | - u u - | ...'"/]
    
    PatternStr --> Match["Meter Matching\n- Compare to 16 meter signatures\n- Calculate similarity scores"]
    
    Match --> Candidates[/"Meter candidates\n[{name, conf}, ...]"/]
    
    Candidates --> Calibrate["Confidence Calibration\n- Adjust for verse length\n- Consider zihafat\n- Factor in era"]
    
    Calibrate --> FinalMeter[/"Final meter\n{name, confidence, alternatives}"/]
    
    FinalMeter --> Quality["Quality Assessment\n- Meter adherence\n- Syllable balance\n- Vocabulary richness"]
    
    Quality --> Result[/"Analysis result\n{meter, quality_score, suggestions}"/]
    
    Result --> Cache{Cache?}
    Cache -->|Yes| Redis[("Redis\nTTL: 3600s")]
    Cache -->|If authenticated| DB[("PostgreSQL\nPermanent")]
    
    Redis --> End([Return to user])
    DB --> End
    
    style Start fill:#d4edda
    style End fill:#d4edda
    style Input fill:#fff3cd
    style Normalized fill:#fff3cd
    style Syllables fill:#fff3cd
    style PatternStr fill:#fff3cd
    style Candidates fill:#fff3cd
    style FinalMeter fill:#cfe2ff
    style Result fill:#cfe2ff
    style Redis fill:#f8d7da
    style DB fill:#f8d7da
```

**Data Transformations:**

| Stage | Input Example | Output Example | Transformation |
|-------|--------------|----------------|----------------|
| Raw Input | `قِفَا نَبْكِ` | (same) | User provides |
| Normalize | `قِفَا نَبْكِ` | `قفا نبك` | Remove diacritics, clean |
| Segment | `قفا نبك` | `[{text:"قفا", long:true}, {text:"نبك", long:false}]` | Syllable detection |
| Pattern | Syllables | `"- u - -"` | Map long/short |
| Meter Detect | `"- u - -"` | `{name:"الطويل", conf:0.92}` | Pattern matching |
| Quality | All above | `{score:0.85, suggestions:[...]}` | Multi-factor assessment |

---

### 5.2 Cache Decision Flow

```mermaid
flowchart TB
    Request[Analysis Request] --> HashText["Hash normalized text\nMD5(normalize(text))"]
    
    HashText --> CacheKey["Cache key:\nanalysis:{hash}"]
    
    CacheKey --> CheckRedis{Redis available?}
    
    CheckRedis -->|No| SkipCache[Skip caching\nmeta.cached = false]
    CheckRedis -->|Yes| GetCache[GET from Redis]
    
    GetCache --> CacheHit{Hit?}
    
    CacheHit -->|Yes| ReturnCached["Return cached result\nmeta.cached = true\nlatency < 50ms"]
    
    CacheHit -->|No| PerformAnalysis["Perform full analysis\nlatency ~ 300-500ms"]
    
    PerformAnalysis --> SetCache["SET in Redis\nTTL: 3600s"]
    
    SetCache --> ReturnNew["Return new result\nmeta.cached = false"]
    
    SkipCache --> PerformAnalysis2["Perform full analysis\n(no caching)"]
    PerformAnalysis2 --> ReturnNoCached["Return result\nmeta.cached = false"]
    
    ReturnCached --> End([Response])
    ReturnNew --> End
    ReturnNoCached --> End
    
    style ReturnCached fill:#d4edda
    style ReturnNew fill:#fff3cd
    style ReturnNoCached fill:#f8d7da
```

**Cache Strategy:**
- **TTL:** 3600 seconds (1 hour)
- **Key Format:** `analysis:{md5(normalized_text)}`
- **Eviction:** LRU (Least Recently Used)
- **Target Hit Rate:** >40%

**Benefits:**
- Cache hit: ~30ms latency (10x faster)
- Reduced database load
- Improved user experience
- Lower infrastructure costs

---

## 6. Deployment Architecture

### 6.1 MVP Deployment (Railway)

```mermaid
graph TB
    subgraph Internet
        User[👤 User Browser]
    end
    
    subgraph Railway Platform
        subgraph Frontend Service
            Vercel[Vercel CDN<br/>Next.js Static]
        end
        
        subgraph Backend Service
            API1[FastAPI Container 1<br/>2 Workers]
            API2[FastAPI Container 2<br/>2 Workers]
            LB[Load Balancer]
        end
        
        subgraph Data Services
            PG[(PostgreSQL<br/>Managed DB)]
            RD[(Redis<br/>Managed Cache)]
        end
        
        subgraph Monitoring Optional
            Prom[Prometheus]
            Graf[Grafana]
        end
    end
    
    User -->|HTTPS| Vercel
    Vercel -->|API Calls| LB
    LB --> API1
    LB --> API2
    
    API1 --> PG
    API1 --> RD
    API2 --> PG
    API2 --> RD
    
    API1 -.->|Metrics| Prom
    API2 -.->|Metrics| Prom
    Prom --> Graf
    
    style User fill:#e1f5ff
    style Vercel fill:#d4edda
    style LB fill:#fff3cd
    style API1 fill:#cfe2ff
    style API2 fill:#cfe2ff
    style PG fill:#f8d7da
    style RD fill:#f8d7da
    style Prom fill:#e2e3e5
    style Graf fill:#e2e3e5
```

**Infrastructure:**
- **Frontend:** Vercel (serverless, global CDN)
- **Backend:** Railway containers (2x, auto-scaling)
- **Database:** Railway PostgreSQL (managed)
- **Cache:** Railway Redis (managed)
- **Monitoring:** Partial (Prometheus + Grafana)

**Scaling Triggers:**
- CPU > 70% → Add backend container
- Memory > 80% → Vertical scale database
- Request rate > 100/sec → Add container

---

### 6.2 Production Deployment (DigitalOcean - Week 13+)

```mermaid
graph TB
    subgraph Internet
        User[👤 Users]
        CDN[Cloudflare CDN<br/>Global Edge Network]
    end
    
    subgraph DigitalOcean
        subgraph Load Balancing
            LB[DO Load Balancer<br/>SSL Termination]
        end
        
        subgraph App Platform
            API1[Backend Droplet 1<br/>4 vCPU, 8GB RAM]
            API2[Backend Droplet 2<br/>4 vCPU, 8GB RAM]
            API3[Backend Droplet 3<br/>Standby]
        end
        
        subgraph Database Cluster
            PG_Primary[(PostgreSQL Primary<br/>8GB RAM)]
            PG_Replica[(PostgreSQL Replica<br/>Read-only)]
        end
        
        subgraph Redis Cluster
            Redis_Master[(Redis Master<br/>4GB RAM)]
            Redis_Replica[(Redis Replica)]
        end
        
        subgraph Monitoring
            Prom[Prometheus]
            Graf[Grafana]
            Alert[AlertManager]
        end
        
        subgraph Backup
            S3[Spaces Object Storage<br/>Daily Backups]
        end
    end
    
    subgraph External
        Sentry[Sentry<br/>Error Tracking]
        Email[SendGrid<br/>Email Service]
    end
    
    User --> CDN
    CDN --> LB
    LB --> API1
    LB --> API2
    LB --> API3
    
    API1 --> PG_Primary
    API1 --> Redis_Master
    API2 --> PG_Primary
    API2 --> Redis_Master
    API3 --> PG_Primary
    API3 --> Redis_Master
    
    PG_Primary -.->|Replication| PG_Replica
    Redis_Master -.->|Replication| Redis_Replica
    
    API1 --> Prom
    API2 --> Prom
    API3 --> Prom
    Prom --> Graf
    Prom --> Alert
    
    PG_Primary -.->|Backup| S3
    
    API1 -.->|Errors| Sentry
    API2 -.->|Errors| Sentry
    API1 -.->|Emails| Email
    
    style User fill:#e1f5ff
    style CDN fill:#d4edda
    style LB fill:#fff3cd
    style API1 fill:#cfe2ff
    style API2 fill:#cfe2ff
    style API3 fill:#e2e3e5
    style PG_Primary fill:#f8d7da
    style PG_Replica fill:#f8d7da
    style Redis_Master fill:#f8d7da
    style Redis_Replica fill:#f8d7da
    style S3 fill:#d1ecf1
```

**Production Features:**
- **High Availability:** 3 backend instances (2 active, 1 standby)
- **Database Replication:** Read replica for analytics/reports
- **Redis Replication:** Failover support
- **Automated Backups:** Daily PostgreSQL dumps to S3-compatible storage
- **SSL/TLS:** Cloudflare edge certificates
- **DDoS Protection:** Cloudflare WAF
- **Monitoring:** Full Prometheus + Grafana + AlertManager
- **Error Tracking:** Sentry integration

---

## 7. Integration Points

### 7.1 External System Dependencies

```mermaid
graph LR
    subgraph BAHR System
        API[FastAPI Backend]
    end
    
    subgraph Data Layer
        API --> PG[(PostgreSQL<br/>Port 5432)]
        API --> Redis[(Redis<br/>Port 6379)]
    end
    
    subgraph NLP Libraries
        API --> CAMeL[CAMeL Tools<br/>Morphology DB]
        API --> PyArabic[PyArabic<br/>Utilities]
    end
    
    subgraph Monitoring Optional
        API -.-> Prometheus[Prometheus<br/>Port 9090]
        API -.-> Sentry[Sentry SaaS<br/>HTTPS]
    end
    
    subgraph Phase 2 Future
        API -.-> AI[AI Model Service<br/>gRPC/HTTP]
        API -.-> Email[Email Service<br/>SMTP/API]
    end
    
    style API fill:#cfe2ff
    style PG fill:#f8d7da
    style Redis fill:#f8d7da
    style CAMeL fill:#fff3cd
    style PyArabic fill:#fff3cd
    style Prometheus fill:#e2e3e5
    style Sentry fill:#e2e3e5
    style AI fill:#d1ecf1,stroke-dasharray: 5 5
    style Email fill:#d1ecf1,stroke-dasharray: 5 5
```

**Dependency Matrix:**

| System | Purpose | Protocol | Failure Impact | Mitigation |
|--------|---------|----------|----------------|------------|
| PostgreSQL | Persistent storage | TCP 5432 | Cannot save analyses | Circuit breaker, return error |
| Redis | Cache + rate limit | TCP 6379 | Slow responses | Continue without cache |
| CAMeL Tools | Arabic NLP | In-process | Lower accuracy | Fallback to rule-based |
| Prometheus | Metrics | HTTP scrape | No monitoring | Non-critical |
| Sentry | Error tracking | HTTPS | No alerts | Non-critical |

---

## 8. Security Architecture

### 8.1 Defense in Depth

```mermaid
graph TB
    User[User] --> Edge[Edge Layer<br/>Cloudflare WAF + DDoS]
    
    Edge --> TLS[TLS Termination<br/>SSL Certificate]
    
    TLS --> LB[Load Balancer<br/>Health Checks]
    
    LB --> CORS[CORS Middleware<br/>Allowed Origins]
    
    CORS --> RateLimit[Rate Limiting<br/>Redis-based]
    
    RateLimit --> Auth[JWT Authentication<br/>Bearer Token]
    
    Auth --> InputVal[Input Validation<br/>Pydantic Schemas]
    
    InputVal --> Sanitize[Input Sanitization<br/>SQL Injection Prevention]
    
    Sanitize --> Business[Business Logic<br/>Authorization Checks]
    
    Business --> ORM[ORM Layer<br/>Parameterized Queries]
    
    ORM --> DB[(Encrypted Database<br/>PostgreSQL)]
    
    style Edge fill:#d4edda
    style TLS fill:#d4edda
    style RateLimit fill:#fff3cd
    style Auth fill:#fff3cd
    style InputVal fill:#cfe2ff
    style Sanitize fill:#cfe2ff
    style DB fill:#f8d7da
```

**Security Layers:**

1. **Edge Protection:** WAF, DDoS mitigation (Cloudflare)
2. **Transport Security:** TLS 1.3, HTTPS enforced
3. **Network Security:** Firewall rules, VPC isolation
4. **Application Security:** CORS, rate limiting, JWT
5. **Input Security:** Validation, sanitization, XSS prevention
6. **Data Security:** Encrypted at rest, encrypted in transit
7. **Access Control:** RBAC (Role-Based Access Control)

---

## 9. Diagram Sources (PlantUML)

### 9.1 System Context (PlantUML Source)

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

LAYOUT_WITH_LEGEND()

title System Context - BAHR Arabic Poetry Platform

Person(user, "Poetry Enthusiast", "Analyzes Arabic poetry")

System(bahr, "BAHR Platform", "Provides prosodic analysis of Arabic verses")

System_Ext(postgres, "PostgreSQL", "Database")
System_Ext(redis, "Redis", "Cache")

Rel(user, bahr, "Uses", "HTTPS")
Rel(bahr, postgres, "Stores data", "TCP")
Rel(bahr, redis, "Caches results", "TCP")

@enduml
```

### 9.2 Container Diagram (PlantUML Source)

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

title Container Diagram - BAHR Platform

Person(user, "User")

System_Boundary(bahr, "BAHR Platform") {
    Container(web, "Web Application", "Next.js", "UI")
    Container(api, "API", "FastAPI", "Backend")
    Container(engine, "Prosody Engine", "Python", "Analysis")
}

ContainerDb(postgres, "Database", "PostgreSQL")
ContainerDb(redis, "Cache", "Redis")

Rel(user, web, "Uses")
Rel(web, api, "API calls")
Rel(api, engine, "Analyzes")
Rel(api, postgres, "R/W")
Rel(api, redis, "Cache")

@enduml
```

---

## 10. How to Update Diagrams

### Method 1: GitHub Markdown (Recommended)
1. Edit this file directly in GitHub
2. Mermaid diagrams render automatically
3. Commit changes

### Method 2: PlantUML
1. Copy PlantUML source (Section 9)
2. Paste into https://plantuml.com/
3. Export as PNG/SVG
4. Add to `docs/diagrams/` folder

### Method 3: Mermaid Live Editor
1. Copy Mermaid source
2. Paste into https://mermaid.live/
3. Export as PNG/SVG
4. Add to documentation

### Diagram Versioning:
- Include version in diagram title: `v1.0 - MVP`
- Date updates in commit messages
- Archive old versions in `docs/diagrams/archive/`

---

## 11. Additional Diagrams Needed (Future Work)

### Phase 2 Additions:
- [ ] AI Model Architecture (inference flow)
- [ ] Competition System (matchmaking, scoring)
- [ ] Social Features (following, notifications)
- [ ] Admin Dashboard (moderation workflow)
- [ ] Analytics Pipeline (data warehousing)

### Operational Diagrams:
- [ ] CI/CD Pipeline (GitHub Actions flow)
- [ ] Backup & Recovery (disaster recovery)
- [ ] Scaling Strategy (auto-scaling triggers)
- [ ] Cost Optimization (resource allocation)

---

**Document Maintained By:** Architecture Team  
**Last Updated:** November 8, 2025  
**Next Review:** December 1, 2025 (after MVP launch)  
**Tools Used:** Mermaid.js, PlantUML, C4 Model

**References:**
- C4 Model: https://c4model.com/
- Mermaid Docs: https://mermaid.js.org/
- PlantUML: https://plantuml.com/
