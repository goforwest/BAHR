# BAHR CI/CD Pipeline Architecture

```mermaid
graph TB
    subgraph "Development"
        A[Developer] -->|git push| B[GitHub Repository]
        A -->|Create PR| B
    end

    subgraph "GitHub Actions - Backend CI"
        B -->|backend/** changes| C[Backend Workflow]
        C --> D[Setup Python 3.11/3.12]
        D --> E[Install Dependencies]
        E --> F[Flake8 Lint]
        F --> G[Black Format Check]
        G --> H[isort Import Check]
        H --> I[mypy Type Check]
        I --> J[pytest + Coverage]
        J --> K[Upload to Codecov]
    end

    subgraph "GitHub Actions - Frontend CI"
        B -->|frontend/** changes| L[Frontend Workflow]
        L --> M[Setup Node 20.x/22.x]
        M --> N[Install Dependencies]
        N --> O[ESLint]
        O --> P[TypeScript Check]
        P --> Q[Prettier Check]
        Q --> R[Next.js Build]
        R --> S[Run Tests]
    end

    subgraph "GitHub Actions - Deploy"
        B -->|push to main| T[Deploy Workflow]
        T --> U{All CI Passed?}
        U -->|Yes| V[Deploy Backend]
        U -->|Yes| W[Deploy Frontend]
        U -->|No| X[❌ Block Deploy]
    end

    subgraph "Railway Platform"
        V --> Y[Backend Service]
        W --> Z[Frontend Service]
        Y --> AA[PostgreSQL]
        Y --> AB[Redis]
        Z --> AC[CDN/Edge]
    end

    subgraph "Production"
        AA --> AD[🚀 Live Backend API]
        AC --> AE[🌐 Live Frontend App]
    end

    K -.->|Coverage Report| AF[Codecov Dashboard]
    J -.->|Test Results| AG[GitHub Checks]
    S -.->|Build Status| AG

    style C fill:#e1f5e1
    style L fill:#e1f5e1
    style T fill:#fff3cd
    style AD fill:#d4edda
    style AE fill:#d4edda
    style X fill:#f8d7da
```

---

## Workflow Stages

### 1️⃣ Code Push / PR Creation
- Developer pushes code or creates pull request
- GitHub triggers appropriate workflows based on file paths

### 2️⃣ Backend CI Pipeline
```
┌─────────────────────────────────────────┐
│  Backend CI (Python 3.11, 3.12)        │
├─────────────────────────────────────────┤
│  1. Install dependencies (cached)       │
│  2. Flake8: Syntax & style check       │
│  3. Black: Format validation           │
│  4. isort: Import organization         │
│  5. mypy: Static type checking         │
│  6. pytest: Run test suite             │
│  7. Coverage: Generate report          │
│  8. Upload: Send to Codecov            │
└─────────────────────────────────────────┘
```

**Duration:** ~3-5 minutes  
**Parallel:** Yes (Python 3.11 + 3.12)

### 3️⃣ Frontend CI Pipeline
```
┌─────────────────────────────────────────┐
│  Frontend CI (Node 20.x, 22.x)         │
├─────────────────────────────────────────┤
│  1. Install dependencies (cached)       │
│  2. ESLint: Code quality check         │
│  3. TypeScript: Type validation        │
│  4. Prettier: Format check             │
│  5. Next.js: Production build          │
│  6. Jest: Run test suite               │
└─────────────────────────────────────────┘
```

**Duration:** ~4-6 minutes  
**Parallel:** Yes (Node 20.x + 22.x)

### 4️⃣ Deployment Pipeline
```
┌─────────────────────────────────────────┐
│  Deploy (main branch only)             │
├─────────────────────────────────────────┤
│  1. Check all CI passed                │
│  2. Deploy backend to Railway          │
│  3. Deploy frontend to Railway         │
│  4. Health check endpoints             │
│  5. Report deployment status           │
└─────────────────────────────────────────┘
```

**Duration:** ~2-4 minutes  
**Triggers:** Push to main, Manual dispatch

---

## Decision Flow

```mermaid
flowchart TD
    A[Code Changed] --> B{Which Files?}
    
    B -->|backend/**| C[Run Backend CI]
    B -->|frontend/**| D[Run Frontend CI]
    B -->|Both| E[Run Both CIs]
    
    C --> F{All Checks Pass?}
    D --> F
    E --> F
    
    F -->|Yes ✅| G{Branch = main?}
    F -->|No ❌| H[❌ Block Merge]
    
    G -->|Yes| I[Trigger Deployment]
    G -->|No| J[✅ Ready to Merge]
    
    I --> K[Deploy Backend]
    I --> L[Deploy Frontend]
    
    K --> M{Health Check?}
    L --> M
    
    M -->|Pass ✅| N[🚀 Production Live]
    M -->|Fail ❌| O[🔴 Rollback]
```

---

## Status Badges Flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant CI as CI Workflow
    participant Badge as README Badge
    participant User as Visitor

    Dev->>GH: Push Code
    GH->>CI: Trigger Workflow
    CI->>CI: Run Tests
    CI-->>Badge: Update Status (pending)
    User->>Badge: View README
    Badge-->>User: Show "pending" 🟡
    
    CI->>CI: Complete Tests
    alt Tests Pass
        CI-->>Badge: Update Status (passing)
        Badge-->>User: Show "passing" 🟢
    else Tests Fail
        CI-->>Badge: Update Status (failing)
        Badge-->>User: Show "failing" 🔴
    end
```

---

## Environment Flow

```mermaid
graph LR
    A[Local Dev] -->|git push| B[develop branch]
    B -->|CI passes| C[Pull Request]
    C -->|Review + Approve| D[Merge to develop]
    D -->|Integration tests| E[Create PR to main]
    E -->|Final review| F[Merge to main]
    F -->|Auto-deploy| G[Railway Production]
    
    style A fill:#e3f2fd
    style B fill:#fff9c4
    style D fill:#fff9c4
    style F fill:#ffecb3
    style G fill:#c8e6c9
```

---

## Caching Strategy

```mermaid
graph TD
    A[Workflow Starts] --> B{Cache Exists?}
    
    subgraph Backend
        B -->|Yes| C[Restore pip cache]
        B -->|No| D[Download all packages]
        C --> E[Install only new deps]
        D --> F[Install all deps]
        E --> G[Save cache]
        F --> G
    end
    
    subgraph Frontend
        B -->|Yes| H[Restore npm cache]
        B -->|No| I[Download all packages]
        H --> J[Install only new deps]
        I --> K[Install all deps]
        J --> L[Save cache]
        K --> L
    end
    
    G --> M[Run Tests]
    L --> M
    
    style C fill:#d4edda
    style H fill:#d4edda
    style D fill:#f8d7da
    style I fill:#f8d7da
```

**Cache Keys:**
- Backend: Hash of `requirements.txt`
- Frontend: Hash of `package-lock.json`

**Speed Improvement:**
- With cache: ~30 seconds install
- Without cache: ~3-5 minutes install
- **5-10x faster** with cache hits

---

## Branch Protection Rules

```mermaid
graph TD
    A[Pull Request Created] --> B{Required Checks}
    
    B --> C[Backend CI]
    B --> D[Frontend CI]
    B --> E[Code Review]
    
    C --> F{All Pass?}
    D --> F
    E --> F
    
    F -->|Yes ✅| G[Enable Merge Button]
    F -->|No ❌| H[Block Merge]
    
    G --> I[Merge to main]
    I --> J[Auto-deploy]
    
    style G fill:#d4edda
    style H fill:#f8d7da
    style J fill:#cfe2ff
```

**Recommended Settings:**
- ✅ Require status checks before merge
- ✅ Require branches to be up to date
- ✅ Require pull request reviews (1+)
- ✅ Dismiss stale reviews on new commits
- ✅ Restrict push to main branch

---

## Deployment Architecture

```mermaid
graph TB
    subgraph "GitHub"
        A[main branch]
    end
    
    subgraph "Railway Services"
        A --> B[Backend Trigger]
        A --> C[Frontend Trigger]
        
        B --> D[Build Backend]
        C --> E[Build Frontend]
        
        D --> F[Docker Image]
        E --> G[Node.js Build]
        
        F --> H[Deploy Backend Pod]
        G --> I[Deploy Frontend Pod]
    end
    
    subgraph "Data Layer"
        J[(PostgreSQL)]
        K[(Redis)]
    end
    
    subgraph "Production URLs"
        L[api.bahr.app]
        M[bahr.app]
    end
    
    H --> J
    H --> K
    H --> L
    I --> M
    
    M -.->|API calls| L
    
    style H fill:#4caf50
    style I fill:#2196f3
    style L fill:#ff9800
    style M fill:#9c27b0
```

---

## Monitoring & Observability

```mermaid
graph TD
    A[Production Services] --> B[Logs]
    A --> C[Metrics]
    A --> D[Errors]
    
    B --> E[Railway Logs]
    C --> F[Railway Metrics]
    D --> G[Error Tracking]
    
    E --> H[Developer Dashboard]
    F --> H
    G --> H
    
    H --> I{Issue Detected?}
    I -->|Yes| J[Alert Team]
    I -->|No| K[Continue Monitoring]
    
    J --> L[Create Issue]
    L --> M[Fix & Deploy]
    M --> A
    
    style I fill:#fff3cd
    style J fill:#f8d7da
    style M fill:#d4edda
```

---

## Success Metrics

### CI/CD Performance
| Metric | Target | Current |
|--------|--------|---------|
| Backend CI Duration | < 5 min | ~3-4 min ✅ |
| Frontend CI Duration | < 6 min | ~4-5 min ✅ |
| Deploy Duration | < 5 min | ~2-3 min ✅ |
| Cache Hit Rate | > 80% | ~90% ✅ |
| Test Coverage | > 70% | TBD 📊 |

### Quality Gates
| Check | Status |
|-------|--------|
| Syntax Errors | ✅ Blocked |
| Format Issues | ✅ Blocked |
| Type Errors | ✅ Blocked |
| Failing Tests | ✅ Blocked |
| Build Failures | ✅ Blocked |

---

## Quick Commands Reference

```bash
# Check workflow status
gh run list

# Watch latest run
gh run watch

# View specific workflow
gh run view <run-id>

# Trigger manual deploy
gh workflow run deploy.yml

# View deployment logs
railway logs --service=backend
railway logs --service=frontend
```

---

**Last Updated:** November 9, 2025  
**Status:** ✅ Production Ready  
**Next Review:** Week 2 Sprint Review
