# ⚙️ دليل سير العمل والتطوير الشامل
## Git Workflow + Testing + Deployment Pipeline

---

## 📋 نظرة عامة

دليل شامل لسير العمل في مشروع بَحْر من التطوير إلى الإنتاج، مع التركيز على:
- **Git Workflow** منظم وآمن
- **Code Quality** عالية مع المراجعة
- **Testing Strategy** شاملة ومتدرجة
- **CI/CD Pipeline** مؤتمت بالكامل
- **Deployment** آمن ومراقب
- **Team Collaboration** فعّالة

---

## 🌿 Git Workflow Strategy

### Branch Structure

```
Git Branch Strategy (Git Flow):

main (production)
├── develop (integration)
│   ├── feature/user-authentication
│   ├── feature/prosody-analysis-engine
│   ├── feature/competition-system
│   └── feature/arabic-nlp-integration
├── release/v1.0.0
├── hotfix/critical-security-fix
└── docs/api-documentation
```

### Branch Types

```yaml
Branch Types:
  main:
    purpose: "Production-ready code"
    protection: "Required reviews, status checks"
    deployment: "Auto-deploy to production"
    
  develop:
    purpose: "Integration branch for features"
    protection: "Required status checks"
    deployment: "Auto-deploy to staging"
    
  feature/*:
    purpose: "New features and enhancements" 
    naming: "feature/short-description"
    source: "develop"
    target: "develop"
    
  release/*:
    purpose: "Prepare new release"
    naming: "release/v1.2.0"
    source: "develop"
    target: "main"
    
  hotfix/*:
    purpose: "Critical fixes for production"
    naming: "hotfix/issue-description"
    source: "main"
    target: "main + develop"
    
  docs/*:
    purpose: "Documentation updates"
    naming: "docs/topic-name"
    source: "develop"
    target: "develop"
```

---

## 🔄 Development Workflow

### 1. Feature Development Process

```bash
# 1. Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/prosody-analyzer

# 2. Development cycle
# - Write code
# - Write tests  
# - Update documentation

# 3. Regular commits with conventional format
git add .
git commit -m "feat(prosody): add Arabic meter detection algorithm

- Implement pattern matching for classical meters
- Add confidence scoring system
- Include unit tests for meter detection
- Update API documentation

Closes #123"

# 4. Keep feature branch updated
git checkout develop
git pull origin develop
git checkout feature/prosody-analyzer
git merge develop

# 5. Push feature branch
git push -u origin feature/prosody-analyzer

# 6. Create Pull Request
# - Fill PR template
# - Request reviews
# - Link related issues
# - Add labels and milestone
```

### 2. Commit Message Convention

```
Commit Message Format:
<type>(<scope>): <description>

[optional body]

[optional footer]

Types:
  feat: A new feature
  fix: A bug fix
  docs: Documentation only changes
  style: Code style changes (formatting, etc.)
  refactor: Code refactoring
  perf: Performance improvements
  test: Adding or modifying tests
  chore: Build process or auxiliary tool changes

Examples:
  feat(api): add user authentication endpoints
  fix(prosody): resolve meter detection accuracy issue
  docs(readme): update installation instructions
  test(analysis): add unit tests for text normalization
  refactor(database): optimize queries for better performance
```

### 3. Code Review Process

```yaml
Code Review Checklist:
  
  Functionality:
    - ✅ Feature works as expected
    - ✅ Edge cases are handled
    - ✅ Error scenarios covered
    - ✅ Performance considerations
    
  Code Quality:
    - ✅ Follows project conventions
    - ✅ DRY principle applied
    - ✅ Readable and maintainable
    - ✅ Proper error handling
    - ✅ Security considerations
    
  Testing:
    - ✅ Unit tests written
    - ✅ Integration tests included
    - ✅ Test coverage > 80%
    - ✅ Tests pass locally and in CI
    
  Documentation:
    - ✅ API documentation updated
    - ✅ README updated if needed
    - ✅ Code comments for complex logic
    - ✅ Database schema changes documented
```

---

## 🧪 Testing Strategy

### Test Pyramid Structure

```
Testing Pyramid:

           /\
          /  \
         / E2E\ (Few)
        /______\
       /        \
      /Integration\ (Some)
     /____________\
    /              \
   /   Unit Tests   \ (Many)
  /__________________\

E2E (5%): Full user journeys
Integration (15%): API + Database + External services  
---

## 🧪 Testing Strategy (مُحدّثة)

### Test Pyramid Structure

```
Testing Pyramid:

           /\
          /  \
         / E2E\ (5% - Few but Critical)
        /______\
       /        \
      /Integration\ (15% - Key Flows)
     /____________\
    /              \
   /   Unit Tests   \ (80% - Fast & Comprehensive)
  /__________________\

E2E (5%): Full user journeys
Integration (15%): API + Database + External services  
Unit (80%): Individual functions and components
```

### Component-Specific Coverage Targets:

```yaml
Backend Components:

  Normalizer (app/core/prosody/normalizer.py):
    Coverage Target: 95%
    Test Cases: 60+
    Focus Areas:
      - Diacritics removal (10 cases)
      - Hamza normalization (8 cases)
      - Ta Marbuta handling (5 cases)
      - Mixed Arabic/English text (8 cases)
      - Special characters & numbers (10 cases)
      - Edge cases: empty string, very long text, etc. (10 cases)
      - Shadda decomposition (6 cases)
      - Tanwīn pause rules (8 cases)

  Segmenter (app/core/prosody/segmenter.py):
    Coverage Target: 90%
    Test Cases: 40+
    Focus Areas:
      - Syllable type detection (CV, CVV, CVC) (12 cases)
      - Classical poetry verses (10 cases)
      - Modern poetry variations (8 cases)
      - Madd letter handling (6 cases)
      - Sukūn cluster resolution (4 cases)

  Pattern Matcher (app/core/prosody/pattern_matcher.py):
    Coverage Target: 90%
    Test Cases: 50+
    Focus Areas:
      - Each taf'ila pattern (8 × 5 = 40 cases)
      - Zihāfāt variations (10 cases)

  Meter Detector (app/core/prosody/meter_detector.py):
    Coverage Target: 85%
    Test Cases: 170+
    Focus Areas:
      - Each meter (16 meters × 10 examples = 160 cases)
      - Ambiguous cases (10 cases)

  API Endpoints (app/api/v1/endpoints/*.py):
    Coverage Target: 85%
    Test Cases: 50+
    Focus Areas:
      - Happy paths (15 cases)
      - Authentication & authorization (10 cases)
      - Input validation errors (15 cases)
      - Rate limiting (5 cases)
      - Error responses (5 cases)

Frontend Components:

  TextInput Component:
    Coverage Target: 80%
    Test Cases: 15+
    Focus Areas:
      - RTL text handling
      - Character limit enforcement
      - Keyboard shortcuts
      - Copy/paste behavior

  ResultsDisplay Component:
    Coverage Target: 85%
    Test Cases: 20+
    Focus Areas:
      - Rendering with different confidence levels
      - Alternative meters display
      - Export functionality
      - Loading states

  Analysis Hook (useAnalyze):
    Coverage Target: 90%
    Test Cases: 12+
    Focus Areas:
      - API call success
      - Error handling
      - Loading states
      - Cache management
```

### Edge Cases & Critical Test Scenarios:

```yaml
Text Processing Edge Cases:
  1. Empty text: ""
  2. Very long text: 10,000+ characters
  3. Only spaces: "     "
  4. Only punctuation: "،؛!؟"
  5. Mixed Arabic/English: "Poetry is شعر"
  6. Arabic numerals: "الدرس ١٢٣"
  7. Latin numerals: "القصيدة 123"
  8. Special Arabic chars: "ﷲ ﷺ"
  9. Emoji in text: "الشعر 😊"
  10. Repeated characters: "اااااااا"
  11. No vowels: "كتب"
  12. All diacritics: "كُتُبٌ"
  13. Broken Arabic: "أآإئؤء"
  14. Poetry with typos: "قفأ نبڪ"
  15. Half-verse only: "قفا نبك من ذكرى"

Meter Detection Edge Cases:
  1. Perfect classical verse
  2. Verse with one zihāf
  3. Verse with multiple zihāfāt
  4. Modern poetry (free verse)
  5. Sha'bi/nabati poetry
  6. Broken meter (intentional)
  7. Prose mistaken for poetry
  8. Mixed meters in same text
  9. Very short text (< 10 words)
  10. Incomplete verse (missing hemistich)

API Edge Cases:
  1. Concurrent requests from same user
  2. Malformed JSON
  3. Missing required fields
  4. Extra unexpected fields
  5. SQL injection attempts
  6. XSS attempts in text field
  7. Extremely large payload (> 10MB)
  8. Rate limit exceeded (101st request)
  9. Expired authentication token
  10. Invalid authentication token
```

### Performance Regression Tests:

```python
# tests/performance/test_regression.py
import pytest
import time
from app.core.prosody.analyzer import ProsodyAnalyzer

class TestPerformanceRegression:
    """Ensure performance doesn't degrade with changes"""
    
    @pytest.fixture
    def analyzer(self):
        return ProsodyAnalyzer()
    
    @pytest.mark.slow
    def test_normalization_performance(self, analyzer, benchmark):
        """Normalizer should process 1000 chars in < 10ms"""
        text = "قفا نبك من ذكرى حبيب ومنزل " * 50  # ~1500 chars
        
        def normalize():
            return analyzer.normalizer.normalize(text)
        
        result = benchmark(normalize)
        
        # Assert performance target
        assert benchmark.stats['mean'] < 0.010  # < 10ms average
    
    @pytest.mark.slow
    def test_analysis_performance(self, analyzer, benchmark):
        """Full analysis should complete in < 500ms (P95)"""
        verse = "قفا نبك من ذكرى حبيب ومنزل"
        
        def analyze():
            return analyzer.analyze(verse)
        
        result = benchmark(analyze)
        
        # P95 should be under 500ms
        assert benchmark.stats['stddev'] < 0.1  # Low variance
        assert result['processing_time_ms'] < 500
    
    @pytest.mark.slow
    def test_batch_analysis_performance(self, analyzer, benchmark):
        """Batch of 10 verses should complete in < 3 seconds"""
        verses = [
            "قفا نبك من ذكرى حبيب ومنزل",
            "أرى الدهر مختلف الحوادث",
            "على قدر أهل العزم تأتي العزائم"
        ] * 4  # 12 verses
        
        start = time.time()
        results = [analyzer.analyze(v) for v in verses]
        duration = time.time() - start
        
        assert duration < 6.0  # < 6s for 12 verses
        assert all(r['success'] for r in results)
```

### Testing Environment Setup (محدّث)

```yaml
# pytest.ini
[tool:pytest]
minversion = 6.0
addopts = 
    -ra
    -q
    --strict-markers
    --strict-config
    --cov=app
    --cov-report=html
    --cov-report=term-missing:skip-covered
    --cov-fail-under=80
    --maxfail=5
    --tb=short
    -p no:warnings
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers = 
    slow: marks tests as slow (deselect with '-m "not slow"')
    unit: unit tests (fast, isolated)
    integration: integration tests (DB, Redis, API)
    e2e: end-to-end tests (browser-based)
    arabic: tests specific to Arabic text processing
    prosody: prosody engine tests
    performance: performance regression tests
    security: security-focused tests

# Coverage configuration
[coverage:run]
source = app
omit = 
    */tests/*
    */migrations/*
    */__pycache__/*
    */venv/*

[coverage:report]
precision = 2
show_missing = True
skip_covered = False

# Exclude from coverage
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
```

### Unit Testing Framework

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import get_db
from app.models.base import Base

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def test_db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db):
    """Create database session for testing"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):
    """Create test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def sample_arabic_text():
    """Sample Arabic poetry for testing"""
    return {
        "correct_meter": "قفا نبك من ذكرى حبيب ومنزل",
        "incorrect_meter": "هذا نص عادي ليس شعراً",
        "mixed_diacritics": "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ"
    }

@pytest.fixture
def authenticated_user(client, db_session):
    """Create authenticated test user"""
    user_data = {
        "username": "testpoet",
        "email": "poet@test.com", 
        "password": "testpassword123",
        "full_name": "Test Poet"
    }
    
    # Register user
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    
    # Login and get token
    login_data = {"email": user_data["email"], "password": user_data["password"]}
    response = client.post("/api/v1/auth/login", json=login_data)
    token_data = response.json()
    
    # Set authorization header
    client.headers.update({"Authorization": f"Bearer {token_data['access_token']}"})
    
    return {
        "client": client,
        "user_data": user_data,
        "token": token_data["access_token"]
    }
```

### Test Examples

```python
# tests/test_prosody/test_analyzer.py
import pytest
from app.core.prosody.analyzer import ProsodyAnalyzer
from app.core.prosody.normalizer import ArabicNormalizer

class TestProsodyAnalyzer:
    """Test suite for prosody analysis engine"""
    
    @pytest.fixture
    def analyzer(self):
        return ProsodyAnalyzer()
    
    @pytest.fixture 
    def normalizer(self):
        return ArabicNormalizer()
    
    @pytest.mark.unit
    def test_text_normalization(self, normalizer):
        """Test Arabic text normalization"""
        text_with_diacritics = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ"
        expected = "قفا نبك من ذكرى حبيب"
        
        result = normalizer.normalize(text_with_diacritics)
        assert result == expected
    
    @pytest.mark.unit
    def test_syllable_segmentation(self, analyzer):
        """Test syllable segmentation accuracy"""
        text = "قفا نبك من ذكرى حبيب ومنزل"
        
        result = analyzer.segment_syllables(text)
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(syllable, str) for syllable in result)
    
    @pytest.mark.unit
    @pytest.mark.arabic
    def test_meter_detection_taweel(self, analyzer):
        """Test detection of الطويل meter"""
        verse = "قفا نبك من ذكرى حبيب ومنزل"
        
        result = analyzer.detect_meter(verse)
        
        assert result["detected_meter"] == "الطويل"
        assert result["confidence"] > 0.8
    
    @pytest.mark.unit
    def test_quality_scoring(self, analyzer):
        """Test verse quality scoring"""
        good_verse = "قفا نبك من ذكرى حبيب ومنزل"
        poor_verse = "هذا نص عادي غير شعري"
        
        good_score = analyzer.calculate_quality(good_verse)
        poor_score = analyzer.calculate_quality(poor_verse)
        
        assert good_score > poor_score
        assert 0 <= good_score <= 1
        assert 0 <= poor_score <= 1

# tests/test_api/test_analysis.py
import pytest
from fastapi import status

class TestAnalysisAPI:
    """Test suite for analysis API endpoints"""
    
    @pytest.mark.integration
    def test_analyze_poetry_success(self, client, sample_arabic_text):
        """Test successful poetry analysis"""
        request_data = {
            "text": sample_arabic_text["correct_meter"],
            "options": {
                "analysis_mode": "accurate",
                "return_alternatives": True
            }
        }
        
        response = client.post("/api/v1/analyze/", json=request_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["success"] is True
        assert "data" in data
        
        result = data["data"]
        assert "prosodic_analysis" in result
        assert "meter_detection" in result
        assert "quality_score" in result
        assert isinstance(result["processing_time_ms"], int)
    
    @pytest.mark.integration
    def test_analysis_with_authentication(self, authenticated_user, sample_arabic_text):
        """Test analysis with authenticated user"""
        client = authenticated_user["client"]
        
        request_data = {
            "text": sample_arabic_text["correct_meter"],
            "options": {"analysis_mode": "detailed"}
        }
        
        response = client.post("/api/v1/analyze/", json=request_data)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check that analysis is saved to history
        history_response = client.get("/api/v1/analyze/history")
        assert history_response.status_code == status.HTTP_200_OK
        
        history_data = history_response.json()
        assert len(history_data["data"]) > 0
    
    @pytest.mark.integration  
    def test_batch_analysis(self, client, sample_arabic_text):
        """Test batch analysis endpoint"""
        request_data = {
            "texts": [
                sample_arabic_text["correct_meter"],
                "ألا في سبيل المجد ما أنا فاعل"
            ],
            "analysis_options": {"analysis_mode": "fast"}
        }
        
        response = client.post("/api/v1/analyze/batch", json=request_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert len(data) == 2
        assert all(result["success"] for result in data)
    
    @pytest.mark.integration
    def test_invalid_text_analysis(self, client):
        """Test analysis with invalid text"""
        request_data = {
            "text": "",  # Empty text
            "options": {}
        }
        
        response = client.post("/api/v1/analyze/", json=request_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

# tests/test_e2e/test_user_journey.py
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
class TestUserJourney:
    """End-to-end user journey tests"""
    
    def test_complete_user_registration_and_analysis(self, page: Page):
        """Test complete user journey from registration to analysis"""
        # Navigate to homepage
        page.goto("http://localhost:3000")
        
        # Register new user
        page.click("text=تسجيل حساب جديد")
        page.fill('[data-testid="username"]', "testuser123")
        page.fill('[data-testid="email"]', "testuser@example.com")
        page.fill('[data-testid="password"]', "testpass123")
        page.fill('[data-testid="full-name"]', "Test User")
        page.click('[data-testid="register-button"]')
        
        # Verify successful registration
        expect(page.locator("text=تم تسجيل الحساب بنجاح")).to_be_visible()
        
        # Login
        page.fill('[data-testid="login-email"]', "testuser@example.com")
        page.fill('[data-testid="login-password"]', "testpass123")
        page.click('[data-testid="login-button"]')
        
        # Verify successful login
        expect(page.locator("text=مرحباً Test User")).to_be_visible()
        
        # Navigate to analysis page
        page.click("text=تحليل النص")
        
        # Perform poetry analysis
        page.fill('[data-testid="poem-text"]', "قفا نبك من ذكرى حبيب ومنزل")
        page.click('[data-testid="analyze-button"]')
        
        # Verify analysis results
        expect(page.locator('[data-testid="analysis-result"]')).to_be_visible()
        expect(page.locator("text=الطويل")).to_be_visible()
        expect(page.locator('[data-testid="quality-score"]')).to_be_visible()
        
        # Save to history
        page.click('[data-testid="save-analysis"]')
        expect(page.locator("text=تم حفظ التحليل")).to_be_visible()
        
        # Check analysis history
        page.click("text=السجل")
        expect(page.locator('[data-testid="analysis-history"]')).to_be_visible()
        expect(page.locator("text=قفا نبك من ذكرى")).to_be_visible()
```

---

## 🚀 CI/CD Pipeline

### GitHub Actions Configuration

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  release:
    types: [ published ]

env:
  PYTHON_VERSION: "3.11"
  NODE_VERSION: "18"

jobs:
  # Backend Tests
  backend-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: bahr_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements/testing.txt
    
    - name: Run linting
      run: |
        cd backend
        black --check .
        flake8 .
        mypy app/
    
    - name: Run security checks
      run: |
        cd backend
        bandit -r app/
        safety check
    
    - name: Run unit tests
      env:
        DATABASE_URL: postgresql://test:test@localhost:5432/bahr_test
        REDIS_URL: redis://localhost:6379/0
        SECRET_KEY: test-secret-key
      run: |
        cd backend
        pytest tests/ -v --cov=app --cov-report=xml
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml
        flags: backend
        name: backend-coverage
  
  # Frontend Tests  
  frontend-tests:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
    
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run linting
      run: |
        cd frontend
        npm run lint
    
    - name: Run type checking
      run: |
        cd frontend
        npm run type-check
    
    - name: Run unit tests
      run: |
        cd frontend
        npm run test:coverage
    
    - name: Build application
      run: |
        cd frontend
        npm run build
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        directory: ./frontend/coverage
        flags: frontend
        name: frontend-coverage

  # E2E Tests
  e2e-tests:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-tests]
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Docker Compose
      run: |
        docker-compose -f docker-compose.test.yml up -d
        sleep 30  # Wait for services to be ready
    
    - name: Run E2E tests
      run: |
        npm install -g @playwright/test
        playwright install
        npm run test:e2e
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: e2e-test-results
        path: test-results/
    
    - name: Cleanup
      if: always()
      run: docker-compose -f docker-compose.test.yml down

  # Security Scanning
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      if: always()
      with:
        sarif_file: 'trivy-results.sarif'

  # Deploy to Staging
  deploy-staging:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-tests, security-scan]
    if: github.ref == 'refs/heads/develop'
    
    environment:
      name: staging
      url: https://staging.bahr.app
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Login to Amazon ECR
      uses: aws-actions/amazon-ecr-login@v1
    
    - name: Build and push Docker images
      run: |
        # Build backend image
        docker build -t $ECR_REGISTRY/bahr-backend:staging ./backend
        docker push $ECR_REGISTRY/bahr-backend:staging
        
        # Build frontend image  
        docker build -t $ECR_REGISTRY/bahr-frontend:staging ./frontend
        docker push $ECR_REGISTRY/bahr-frontend:staging
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
    
    - name: Deploy to ECS
      run: |
        aws ecs update-service \
          --cluster bahr-staging \
          --service bahr-backend-staging \
          --force-new-deployment
        
        aws ecs update-service \
          --cluster bahr-staging \
          --service bahr-frontend-staging \
          --force-new-deployment
    
    - name: Verify deployment
      run: |
        echo "Waiting for deployment to complete..."
        sleep 60
        
        # Check health endpoints
        curl -f https://staging-api.bahr.app/api/v1/health/ || exit 1
        curl -f https://staging.bahr.app/ || exit 1

  # Deploy to Production
  deploy-production:
    runs-on: ubuntu-latest
    needs: [e2e-tests]
    if: github.event_name == 'release'
    
    environment:
      name: production
      url: https://bahr.app
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Deploy with Blue/Green strategy
      run: |
        # Deploy backend
        aws ecs update-service \
          --cluster bahr-production \
          --service bahr-backend-production \
          --force-new-deployment
        
        # Wait and verify backend health
        sleep 120
        curl -f https://api.bahr.app/api/v1/health/ || exit 1
        
        # Deploy frontend
        aws ecs update-service \
          --cluster bahr-production \
          --service bahr-frontend-production \
          --force-new-deployment
        
        # Final verification
        sleep 60
        curl -f https://bahr.app/ || exit 1
    
    - name: Post-deployment smoke tests
      run: |
        # Run critical path smoke tests
        curl -f https://api.bahr.app/api/v1/health/detailed || exit 1
        
        # Test key API endpoints
        curl -f -X POST https://api.bahr.app/api/v1/analyze/ \
          -H "Content-Type: application/json" \
          -d '{"text": "قفا نبك من ذكرى حبيب ومنزل"}' || exit 1
    
    - name: Notify team
      if: always()
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: |
          Production deployment ${{ job.status }}!
          Version: ${{ github.event.release.tag_name }}
          URL: https://bahr.app
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-merge-conflict
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-added-large-files
      - id: check-case-conflict
      
  # Backend (Python)
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        files: ^backend/
        language_version: python3.11
        
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        files: ^backend/
        args: ["--profile", "black"]
        
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        files: ^backend/
        additional_dependencies: [flake8-docstrings]
        
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        files: ^backend/app/
        additional_dependencies: [types-all]
        
  # Frontend (Node.js)
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.44.0
    hooks:
      - id: eslint
        files: ^frontend/
        additional_dependencies:
          - eslint@8.44.0
          - "@typescript-eslint/eslint-plugin@5.60.0"
          - "@typescript-eslint/parser@5.60.0"
          
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.0
    hooks:
      - id: prettier
        files: ^frontend/
        exclude: ^frontend/node_modules/
        
  # Security
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        files: ^backend/
        args: ["-c", "backend/pyproject.toml"]
        
  # Documentation
  - repo: https://github.com/executablebooks/mdformat
    rev: 0.7.16
    hooks:
      - id: mdformat
        additional_dependencies:
          - mdformat-gfm
          - mdformat-black
```

---

## 📦 Deployment Strategies

### Docker Configuration

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VENV_IN_PROJECT=1
ENV POETRY_CACHE_DIR=/opt/poetry_cache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set work directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --only=main && rm -rf $POETRY_CACHE_DIR

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health/ || exit 1

# Run application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built application
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Database
  postgres:
    image: postgres:15
    container_name: bahr-postgres
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/scripts/init_db.sql:/docker-entrypoint-initdb.d/init_db.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped
    
  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: bahr-redis
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped
    
  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: bahr-backend
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY}
    volumes:
      - ./backend/logs:/app/logs
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health/"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped
    
  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: bahr-frontend
    depends_on:
      backend:
        condition: service_healthy
    ports:
      - "3000:80"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped
    
  # Nginx Load Balancer
  nginx:
    image: nginx:alpine
    container_name: bahr-nginx
    depends_on:
      - frontend
      - backend
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    ports:
      - "80:80"
      - "443:443"
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

---

## 🔍 Monitoring & Logging

### Application Monitoring

```python
# app/core/monitoring.py
import time
import logging
from contextlib import contextmanager
from functools import wraps
from typing import Dict, Any, Optional
import structlog
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_USERS = Gauge('active_users_total', 'Number of active users')
ANALYSIS_COUNT = Counter('poetry_analyses_total', 'Total poetry analyses', ['meter', 'status'])

# Structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(ensure_ascii=False)
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

@contextmanager
def monitor_analysis_performance(meter_name: Optional[str] = None):
    """Context manager to monitor analysis performance"""
    start_time = time.time()
    try:
        yield
        duration = time.time() - start_time
        ANALYSIS_COUNT.labels(meter=meter_name or "unknown", status="success").inc()
        logger.info("Analysis completed", duration=duration, meter=meter_name)
    except Exception as e:
        duration = time.time() - start_time
        ANALYSIS_COUNT.labels(meter=meter_name or "unknown", status="error").inc()
        logger.error("Analysis failed", duration=duration, meter=meter_name, error=str(e))
        raise

def monitor_endpoint(func):
    """Decorator to monitor API endpoint performance"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            REQUEST_COUNT.labels(
                method="POST",  # Assuming POST for simplicity
                endpoint=func.__name__,
                status="success"
            ).inc()
            REQUEST_DURATION.observe(time.time() - start_time)
            return result
        except Exception as e:
            REQUEST_COUNT.labels(
                method="POST",
                endpoint=func.__name__,
                status="error"
            ).inc()
            logger.error("Endpoint error", endpoint=func.__name__, error=str(e))
            raise
    return wrapper

# Start metrics server
def start_metrics_server(port: int = 9090):
    """Start Prometheus metrics server"""
    start_http_server(port)
    logger.info("Metrics server started", port=port)
```

### Error Tracking

```python
# app/core/error_tracking.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from app.config import settings

def setup_error_tracking():
    """Configure Sentry for error tracking"""
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[
                FastApiIntegration(auto_enabling_integrations=False),
                SqlalchemyIntegration(),
            ],
            traces_sample_rate=0.1,
            environment=settings.ENVIRONMENT,
            release=settings.VERSION,
            before_send=filter_sensitive_data
        )

def filter_sensitive_data(event, hint):
    """Filter sensitive data from error reports"""
    # Remove sensitive headers
    if 'request' in event:
        headers = event['request'].get('headers', {})
        headers.pop('authorization', None)
        headers.pop('cookie', None)
    
    # Remove sensitive form data
    if 'request' in event and 'data' in event['request']:
        data = event['request']['data']
        if isinstance(data, dict):
            data.pop('password', None)
            data.pop('token', None)
    
    return event
```

---

## 🔒 Security Best Practices

### Security Configuration

```python
# app/core/security_config.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import secrets

def configure_security(app: FastAPI):
    """Configure security middleware and settings"""
    
    # HTTPS redirect in production
    if not settings.DEBUG:
        app.add_middleware(HTTPSRedirectMiddleware)
    
    # Trusted host protection
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.bahr.app", "bahr.app", "localhost", "127.0.0.1"]
    )
    
    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
        expose_headers=["X-Process-Time"]
    )
    
    # Security headers
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com;"
        )
        return response

# Secrets management
class SecretManager:
    """Secure secrets management"""
    
    @staticmethod
    def generate_secret_key() -> str:
        """Generate cryptographically secure secret key"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash API key for secure storage"""
        import hashlib
        return hashlib.sha256(api_key.encode()).hexdigest()

---

## 🛡️ قائمة أمان الـ MVP (MVP Security Checklist)

هذه القائمة تُنفَّذ تدريجياً بدءاً من Week 1 وتكتمل قبل نهاية Week 4.

### المرحلة 1 (Week 1-2): الأساسيات
- [ ] تفعيل CORS مع origins محددة (localhost + نطاق الإنتاج لاحقاً)
- [ ] إضافة Security Headers (موجودة في `security_config.py`) والتحقق في الاختبارات.
- [ ] توليد SECRET_KEY قوي (32+ bytes) وعدم تخزينه في المستودع.
- [ ] تحديد حجم الجسم (Body) للطلب `/analyze` (100KB) عبر middleware (راجع `BACKEND_API.md`).
- [ ] إضافة معدل الطلبات (Rate limiting) لكل IP (100 طلب/ساعة) باستخدام Redis.
- [ ] تمييز جميع سجلات الأخطاء 5xx بحقل `request_id`.
- [ ] تعطيل أو حماية واجهة Swagger في الإنتاج (`/docs`).

### المرحلة 2 (Week 3-4): التعزيز
- [ ] تفعيل نظام Token Refresh (عمر وصول قصير + Refresh أطول).
- [ ] إضافة فحص بسيط لـ API Key داخلي للمهام الإدارية (ingestion).
- [ ] مراقبة معدل محاولات الدخول الفاشلة (Counter + Alert > 20/10m).
- [ ] دمج تنبيهات فشل متكرر (5xx spike / rate limit abuse) في Grafana.

### المرحلة 3 (Pre-Launch): الصلابة
- [ ] فحص ثغرات الحزم (pip audit / npm audit) بدون تحذيرات حرجة.
- [ ] مراجعة يدوية لـ 10 ملفات حساسة (auth, security, rate limiting, error handling).
- [ ] اختبار اختراق داخلي (سيناريوهات: XSS، SQLi، تجاوز المعدل، رفع الحجم).

مؤشرات القبول للأمان (MVP):
```yaml
No critical dependency vulnerabilities: true
Unauthorized meter access possible: false
Rate-limit bypass attempts logged & alerted: true
Leak of secrets in logs: false
Open API docs publicly in production: false
```

---

## 🧪 الحد الأدنى للاختبارات (Minimum Viable Tests)

يجب توفر هذه المجموعة قبل دمج أول إصدار للمحرك (Week 3) لضمان بناء مستقر.

### Backend Minimum
- [ ] 12 اختبار وحدة للتطبيع (diacritics، shadda، tanwīn، hamza).
- [ ] 8 اختبار وحدة للتقطيع (syllable boundaries الأساسية + madd).
- [ ] 16 اختبار Meter (1 مثال لكل بحر كلاسيكي).
- [ ] 4 اختبارات API (تحليل ناجح، تحليل فشل تحقق، معدل طلبات، حجم زائد).
- [ ] 2 اختبار أداء مبسط (زمن تحليل بيت واحد < 500ms، دفعة 5 أبيات < 2.5s).
- [ ] 4 اختبارات أمن (محاولة XSS، حجم زائد، تجاوز معدل، نص فارغ).

### Frontend Minimum
- [ ] اختبار إدخال النص (RTL + حدود الحروف).
- [ ] اختبار عرض النتائج مع بدائل meter.
- [ ] اختبار حالة تحميل / خطأ.
- [ ] اختبار hook `useAnalyze` (نجاح + خطأ + إعادة طلب).

### CI Minimum Gates
```yaml
coverage: >= 40% (يرتفع تدريجياً إلى 80%)
lint: pass (no error severity findings)
security scan: no critical issues
tests: required (unit + minimal integration)
build: green (frontend + backend docker build)
```

### تصعيد التغطية (Coverage Ramp)
```yaml
Week 3: 40%
Week 5: 55%
Week 7: 65%
Week 10: 75%
Week 12: 80% (Beta)
Week 13: 80% (Launch)
```

ملاحظة: الهدف الأعلى (95% لبعض الوحدات) يبقى في الأقسام التفصيلية أعلاه، لكن هذه الحدود الدنيا تمنع التدهور.

---
```

---

## 📊 Performance Optimization

### Database Query Optimization

```python
# app/db/optimization.py
from sqlalchemy import text
from sqlalchemy.orm import Session
import asyncio
from typing import List, Dict, Any

class QueryOptimizer:
    """Database query optimization utilities"""
    
    @staticmethod
    def explain_query(db: Session, query: str) -> Dict[str, Any]:
        """Analyze query execution plan"""
        explain_query = text(f"EXPLAIN ANALYZE {query}")
        result = db.execute(explain_query).fetchall()
        return {
            "execution_plan": [dict(row) for row in result],
            "optimization_suggestions": QueryOptimizer._analyze_plan(result)
        }
    
    @staticmethod
    def _analyze_plan(execution_plan) -> List[str]:
        """Analyze execution plan and provide optimization suggestions"""
        suggestions = []
        
        for row in execution_plan:
            plan_text = str(row[0])
            
            if "Seq Scan" in plan_text:
                suggestions.append("Consider adding an index for sequential scan")
            
            if "cost=" in plan_text and "rows=" in plan_text:
                # Extract cost and rows information
                import re
                cost_match = re.search(r'cost=([\d.]+)\.\.([\d.]+)', plan_text)
                if cost_match and float(cost_match.group(2)) > 1000:
                    suggestions.append("High cost operation detected - consider query optimization")
        
        return suggestions

# Connection pooling optimization
from sqlalchemy.pool import QueuePool

def create_optimized_engine():
    """Create database engine with optimized settings"""
    return create_engine(
        settings.DATABASE_URL,
        poolclass=QueuePool,
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=settings.DEBUG
    )
```

### Caching Strategy

```python
# app/core/cache_strategy.py
import redis
import json
import pickle
from typing import Any, Optional, Union
from functools import wraps
import hashlib

class CacheManager:
    """Advanced caching with multiple strategies"""
    
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.default_ttl = 3600  # 1 hour
    
    def cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate consistent cache key"""
        key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            data = self.redis.get(key)
            if data:
                return pickle.loads(data)
            return None
        except Exception:
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        try:
            serialized = pickle.dumps(value)
            self.redis.setex(key, ttl or self.default_ttl, serialized)
        except Exception:
            pass  # Fail silently for cache errors
    
    async def delete(self, pattern: str) -> None:
        """Delete keys matching pattern"""
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)
    
    def cached(self, ttl: int = 3600, key_prefix: str = ""):
        """Decorator for caching function results"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                cache_key = self.cache_key(key_prefix or func.__name__, *args, **kwargs)
                
                # Try to get from cache
                cached_result = await self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Execute function and cache result
                result = await func(*args, **kwargs)
                await self.set(cache_key, result, ttl)
                return result
            
            return wrapper
        return decorator

# Usage example
cache_manager = CacheManager(settings.REDIS_URL)

@cache_manager.cached(ttl=1800, key_prefix="analysis")
async def cached_analysis(text: str, options: dict):
    """Cached poetry analysis"""
    # Expensive analysis operation
    return perform_analysis(text, options)
```

---

## 🎯 Next Steps

✅ **Development Workflow Guide مكتمل**

المتبقي في التوثيق:
1. **[Arabic NLP Research](../research/ARABIC_NLP_RESEARCH.md)** - مراجع ومكتبات معالجة العربية
2. **[Project Timeline](../planning/PROJECT_TIMELINE.md)** - الخطة الزمنية والمراحل

---

## 📝 ملخص سير العمل

### 🛠️ Development Excellence:
- **Git Flow** منظم مع branch protection
- **Code Quality** مع pre-commit hooks
- **Testing Pyramid** شاملة ومتدرجة
- **CI/CD Pipeline** مؤتمت بالكامل
- **Security** مدمجة في كل مرحلة

### 🚀 Deployment Ready:
- **Docker** containerization كاملة
- **Multi-environment** staging + production
- **Health checks** وmonitoring شامل
- **Blue/Green deployment** للإنتاج الآمن
- **Error tracking** مع Sentry

### 📊 Quality Assurance:
- **80%+ test coverage** مطلوب
- **Security scanning** تلقائي
- **Performance monitoring** مستمر
- **Code review** إجباري
- **Documentation** مع كل feature

---

**⚙️ هذا يكمل دليل سير العمل والتطوير - الإطار الشامل لإنجاز المشروع بجودة عالية!**