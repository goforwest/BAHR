# 🛡️ OWASP Top 10 Compliance Mapping
## Security Controls for BAHR Platform (2021 Edition)

**Last Updated:** November 9, 2025  
**OWASP Version:** Top 10 - 2021  
**Purpose:** Map BAHR security controls to OWASP Top 10 vulnerabilities  
**Related:** `SECURITY.md`, `SECURITY_AUDIT_CHECKLIST.md`

---

## 📋 Overview

This document maps each OWASP Top 10 (2021) vulnerability to BAHR's security controls, showing:
- **Risk Level** for BAHR specifically
- **Implemented Controls** (what we do)
- **Testing Procedures** (how we verify)
- **Code References** (where to find it)
- **Residual Risk** (what remains)

**Risk Levels:**
- 🔴 **Critical** - Immediate attention required
- 🟠 **High** - Address before production
- 🟡 **Medium** - Address within sprint
- 🟢 **Low** - Monitor and improve

---

## A01:2021 – Broken Access Control
### Risk Level: 🟠 High

### Description
Restrictions on what authenticated users can do are not properly enforced. Attackers can access unauthorized data or perform actions beyond their privileges.

### BAHR-Specific Risks
- Users accessing other users' analysis history
- Unauthorized meter pattern modifications
- Bypassing rate limits via token manipulation
- Privilege escalation in admin endpoints

### Implemented Controls

#### 1. JWT-Based Authentication
**Location:** `backend/app/auth/`

```python
# Example: Protected endpoint
@router.get("/api/v1/users/me")
async def get_current_user(
    current_user: User = Depends(get_current_user)
):
    """Returns authenticated user's profile"""
    return current_user

# Dependency enforces JWT validation
async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return await get_user(user_id)
    except JWTError:
        raise credentials_exception
```

#### 2. Resource Ownership Checks
**Location:** `backend/app/api/v1/analyses.py`

```python
@router.get("/api/v1/analyses/{analysis_id}")
async def get_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id
    ).first()
    
    # Ownership check
    if analysis.user_id != current_user.id:
        if current_user.role not in ["admin", "moderator"]:
            raise HTTPException(403, "Not authorized")
    
    return analysis
```

#### 3. Role-Based Access Control (RBAC)
**Location:** `backend/app/auth/rbac.py`

```python
# Role hierarchy
ROLES = {
    "student": 1,
    "poet": 2,
    "teacher": 3,
    "moderator": 4,
    "admin": 5
}

def require_role(min_role: str):
    """Decorator to enforce minimum role"""
    def decorator(func):
        async def wrapper(*args, current_user: User, **kwargs):
            if ROLES[current_user.role] < ROLES[min_role]:
                raise HTTPException(403, "Insufficient privileges")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Usage
@router.delete("/api/v1/users/{user_id}")
@require_role("admin")
async def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    # Only admins can delete users
    pass
```

### Testing Procedures

```bash
# Test 1: Access other user's resource
TOKEN_USER1=$(get_token user1@test.com)
TOKEN_USER2=$(get_token user2@test.com)
ANALYSIS_ID=$(create_analysis $TOKEN_USER1)

# Should fail with 403
curl -H "Authorization: Bearer $TOKEN_USER2" \
  http://localhost:8000/api/v1/analyses/$ANALYSIS_ID

# Test 2: Privilege escalation attempt
curl -X POST http://localhost:8000/api/v1/admin/settings \
  -H "Authorization: Bearer $TOKEN_USER1" \
  -d '{"key":"value"}'
# Should fail with 403 for non-admin user

# Test 3: Missing JWT token
curl http://localhost:8000/api/v1/analyses/123
# Should fail with 401
```

### Residual Risk: 🟡 Medium
- Future feature: Share analysis with other users (needs permission model)
- Admin actions not fully logged (Week 2 enhancement)

---

## A02:2021 – Cryptographic Failures
### Risk Level: 🟡 Medium

### Description
Failures related to cryptography which often lead to sensitive data exposure.

### BAHR-Specific Risks
- Password storage (if weak hashing)
- JWT secret exposure
- Unencrypted database backups
- Secrets in git history

### Implemented Controls

#### 1. Password Hashing (bcrypt)
**Location:** `backend/app/core/security/password.py`

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Cost factor
)

def hash_password(password: str) -> str:
    """Hash password with bcrypt (cost=12)"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Constant-time password verification"""
    try:
        return pwd_context.verify(plain, hashed)
    except Exception:
        # Constant-time failure to prevent timing attacks
        pwd_context.hash(plain)
        return False
```

#### 2. TLS/HTTPS Enforcement
**Location:** `backend/app/middleware/security.py`

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Production only
if settings.environment == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["api.bahr.app", "*.bahr.app"]
    )
```

#### 3. Secure Headers
**Location:** `backend/app/middleware/security.py`

```python
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = \
        "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

#### 4. Secret Management
**Location:** `.env` (not in git)

```bash
# .gitignore
.env
.env.local
.env.*.local
*.key
*.pem

# Environment variables
SECRET_KEY=<generated-with-openssl-rand-hex-32>
DATABASE_PASSWORD=<strong-password>
REDIS_PASSWORD=<strong-password>
```

### Testing Procedures

```bash
# Test 1: Verify bcrypt cost factor
python -c "from app.core.security.password import pwd_context; \
  hashed = pwd_context.hash('test'); \
  assert hashed.startswith('\$2b\$12\$'), 'Bcrypt cost factor not 12'"

# Test 2: Check HSTS header
curl -I https://api.bahr.app | grep -i strict-transport-security

# Test 3: Verify no secrets in git
git log -p | grep -i "SECRET_KEY.*=" | grep -v ".example"
# Should return nothing

# Test 4: Check TLS version
nmap --script ssl-enum-ciphers -p 443 api.bahr.app | grep TLSv1.2
```

### Residual Risk: 🟢 Low
- Database encryption at rest (optional, cloud provider handles)
- Backup encryption (to be implemented Week 2)

---

## A03:2021 – Injection
### Risk Level: 🟡 Medium

### Description
User-supplied data is not validated, filtered, or sanitized. Includes SQL, NoSQL, OS command, and LDAP injection.

### BAHR-Specific Risks
- SQL injection in analysis queries
- NoSQL injection in Redis cache keys
- Arabic text injection attacks (RTL override)
- Command injection if using external tools

### Implemented Controls

#### 1. SQL Injection Prevention (ORM)
**Location:** `backend/app/db/repositories/analysis.py`

```python
from sqlalchemy.orm import Session

# ✅ SAFE: Using ORM with parameterized queries
def get_analyses_by_meter(db: Session, meter_name: str):
    return db.query(Analysis).filter(
        Analysis.detected_meter == meter_name  # Parameterized
    ).all()

# ❌ UNSAFE: Never do this
# query = f"SELECT * FROM analyses WHERE meter = '{meter_name}'"
# db.execute(query)
```

#### 2. Input Validation (Pydantic)
**Location:** `backend/app/schemas/analysis.py`

```python
from pydantic import BaseModel, Field, validator
import re

class AnalysisRequest(BaseModel):
    text: str = Field(
        min_length=10,
        max_length=2000,
        description="Arabic verse text"
    )
    
    @validator('text')
    def validate_arabic_text(cls, v):
        # Remove dangerous characters
        dangerous_chars = [
            '\u202E',  # RTL override
            '\u202D',  # LTR override
            '\u200B',  # Zero-width space
        ]
        for char in dangerous_chars:
            v = v.replace(char, '')
        
        # Validate Arabic percentage
        arabic_chars = sum(1 for c in v if '\u0600' <= c <= '\u06FF')
        total_chars = len(v.replace(' ', ''))
        if total_chars > 0 and arabic_chars / total_chars < 0.7:
            raise ValueError("Text must be at least 70% Arabic")
        
        return v
```

#### 3. Redis Key Sanitization
**Location:** `backend/app/core/cache/keys.py`

```python
import hashlib
import re

def generate_cache_key(prefix: str, data: str) -> str:
    """Generate safe Redis key"""
    # Use hash instead of user input directly
    data_hash = hashlib.md5(data.encode()).hexdigest()
    
    # Sanitize prefix (alphanumeric + underscore only)
    safe_prefix = re.sub(r'[^a-zA-Z0-9_]', '', prefix)
    
    return f"{safe_prefix}:{data_hash}"

# ✅ SAFE
cache_key = generate_cache_key("analysis", normalized_text)

# ❌ UNSAFE: Never use user input directly
# cache_key = f"analysis:{user_input}"
```

#### 4. HTML/XSS Prevention
**Location:** `backend/app/api/responses.py`

```python
import html

def sanitize_html(text: str) -> str:
    """Escape HTML entities"""
    return html.escape(text)

# Usage
response_data = {
    "text": sanitize_html(user_input),
    "meter": sanitize_html(meter_name)
}
```

### Testing Procedures

```bash
# Test 1: SQL injection attempt
curl -X POST http://localhost:8000/api/v1/analyze \
  -d '{"text":"قفا نبك' OR 1=1--"}' | \
  jq '.success'
# Should return false with validation error

# Test 2: XSS attempt
curl -X POST http://localhost:8000/api/v1/analyze \
  -d '{"text":"<script>alert('xss')</script>قفا نبك"}' | \
  jq '.data.normalized_text'
# Should not contain script tags

# Test 3: RTL override injection
python -c "
import requests
text = 'قفا\u202Eنبك'  # RTL override
r = requests.post('http://localhost:8000/api/v1/analyze', 
                  json={'text': text})
assert '\u202E' not in r.json()['data']['normalized_text']
"

# Test 4: NoSQL injection (Redis)
# Try cache poisoning with special characters
curl -X POST http://localhost:8000/api/v1/analyze \
  -d '{"text":"قفا نبك; FLUSHALL;"}' | \
  jq '.data'
# Should hash the input, not execute Redis command
```

### Residual Risk: 🟢 Low
- No direct SQL queries used
- All user input validated via Pydantic
- Arabic-specific sanitization in place

---

## A04:2021 – Insecure Design
### Risk Level: 🟢 Low

### Description
Missing or ineffective control design. Focus on risks inherent to the business logic.

### BAHR-Specific Risks
- Meter detection algorithm manipulation
- Analysis result tampering
- Abuse of free tier limits
- Data poisoning through fake analyses

### Implemented Controls

#### 1. Rate Limiting
**Location:** `backend/app/middleware/rate_limit.py`

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/analyze")
@limiter.limit("100/hour")
async def analyze_verse(request: Request, ...):
    # Limited to 100 requests per hour per IP
    pass
```

#### 2. Analysis Integrity
**Location:** `backend/app/prosody/engine.py`

```python
from hashlib import sha256
import json

def sign_analysis(result: AnalysisResult) -> str:
    """Generate integrity signature for analysis"""
    canonical = json.dumps({
        'text': result.normalized_text,
        'meter': result.detected_meter,
        'confidence': result.confidence,
        'timestamp': result.created_at.isoformat()
    }, sort_keys=True)
    
    signature = sha256(
        (canonical + settings.SECRET_KEY).encode()
    ).hexdigest()
    
    return signature

def verify_analysis(result: AnalysisResult, signature: str) -> bool:
    """Verify analysis hasn't been tampered with"""
    expected = sign_analysis(result)
    return expected == signature
```

#### 3. Abuse Detection
**Location:** `backend/app/core/abuse_detection.py`

```python
async def detect_abuse(user_id: int, db: Session) -> bool:
    """Detect potential abuse patterns"""
    # Check for rapid repeated requests
    recent_analyses = db.query(Analysis).filter(
        Analysis.user_id == user_id,
        Analysis.created_at > datetime.now() - timedelta(minutes=5)
    ).count()
    
    if recent_analyses > 50:
        logger.warning(f"Abuse detected: user {user_id}, {recent_analyses} requests in 5min")
        return True
    
    # Check for identical text spam
    duplicate_count = db.query(Analysis).filter(
        Analysis.user_id == user_id,
        Analysis.normalized_text == current_text
    ).count()
    
    if duplicate_count > 10:
        logger.warning(f"Spam detected: user {user_id}, {duplicate_count} duplicates")
        return True
    
    return False
```

### Testing Procedures

```bash
# Test 1: Rate limit enforcement
for i in {1..101}; do
  curl -s http://localhost:8000/api/v1/analyze \
    -d '{"text":"قفا نبك"}' -o /dev/null -w "%{http_code}\n"
done | tail -1
# Should return 429 after 100 requests

# Test 2: Abuse detection
# Create 51 analyses in 5 minutes
# Should trigger abuse warning in logs
```

### Residual Risk: 🟢 Low
- Threat modeling completed during design
- Security requirements in `SECURITY.md`
- Regular security reviews planned

---

## A05:2021 – Security Misconfiguration
### Risk Level: 🟡 Medium

### Description
Missing hardening, improperly configured permissions, default configurations, overly verbose error messages.

### BAHR-Specific Risks
- Debug mode enabled in production
- Default credentials in Docker
- Verbose error messages exposing internals
- CORS misconfiguration

### Implemented Controls

#### 1. Environment-Based Configuration
**Location:** `backend/app/config.py`

```python
class Settings(BaseSettings):
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Usage
if settings.debug and settings.is_production:
    raise RuntimeError("Debug mode cannot be enabled in production")
```

#### 2. Error Message Sanitization
**Location:** `backend/app/middleware/error_handler.py`

```python
@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    # Log full error internally
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    # Return sanitized error to client
    if settings.is_production:
        message = "An internal error occurred"
        details = None
    else:
        message = str(exc)
        details = {"traceback": traceback.format_exc()}
    
    return JSONResponse(
        status_code=500,
        content={
            "success": false,
            "error": {
                "code": "ERR_UNKNOWN_001",
                "message": message,
                "details": details
            }
        }
    )
```

#### 3. CORS Configuration
**Location:** `backend/app/main.py`

```python
from fastapi.middleware.cors import CORSMiddleware

# Production: Specific origins only
if settings.is_production:
    allowed_origins = [
        "https://bahr.app",
        "https://www.bahr.app"
    ]
else:
    # Development: Allow localhost
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # NOT ["*"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

#### 4. Default Credentials Prevention
**Location:** `docker-compose.yml`

```yaml
services:
  postgres:
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}  # From .env, not hardcoded
      # NOT: POSTGRES_PASSWORD: admin123
```

### Testing Procedures

```bash
# Test 1: Verify debug mode is off
curl http://localhost:8000/docs
# Should return 404 in production

# Test 2: Check error messages
curl http://localhost:8000/api/v1/trigger-error
# Should return generic message in production

# Test 3: CORS configuration
curl -H "Origin: http://evil.com" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS http://localhost:8000/api/v1/analyze
# Should not include evil.com in Access-Control-Allow-Origin

# Test 4: Default credentials
docker exec bahr_postgres psql -U postgres -c "\du"
# Should not have default passwords
```

### Residual Risk: 🟡 Medium
- Need security headers verification in CI
- Need automated config audit tool

---

## A06:2021 – Vulnerable and Outdated Components
### Risk Level: 🟡 Medium

### Description
Using components with known vulnerabilities, outdated software, or not knowing component versions.

### BAHR-Specific Risks
- Vulnerable Python dependencies (FastAPI, SQLAlchemy, etc.)
- Outdated NLP libraries (CAMeL Tools, PyArabic)
- Docker base images with CVEs
- Node.js frontend dependencies

### Implemented Controls

#### 1. Dependency Pinning
**Location:** `backend/requirements/base.txt`

```txt
# Exact versions pinned
fastapi==0.115.0
sqlalchemy==2.0.23
pydantic==2.5.0

# NOT: fastapi>=0.100.0
```

#### 2. Automated Scanning (CI/CD)
**Location:** `.github/workflows/security.yml`

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run pip-audit
        run: |
          pip install pip-audit
          pip-audit -r requirements/base.txt
      
      - name: Run Safety
        run: |
          pip install safety
          safety check --json -r requirements/base.txt
      
      - name: Scan Docker image
        run: |
          docker build -t bahr-api:test .
          docker scan bahr-api:test
```

#### 3. Update Policy
**Location:** `docs/workflows/DEPENDENCY_MANAGEMENT.md`

```markdown
## Update Schedule

### Critical Security Patches
- Timeline: Within 24-48 hours
- Process: Emergency PR → Review → Deploy

### High/Medium Vulnerabilities
- Timeline: Within 1 week
- Process: Regular PR → Testing → Deploy

### Dependency Updates
- Monthly: Patch versions (0.0.X)
- Quarterly: Minor versions (0.X.0)
- Annually: Major versions (X.0.0)
```

### Testing Procedures

```bash
# Test 1: Check for known vulnerabilities
pip install pip-audit
pip-audit

# Test 2: Check dependency freshness
pip list --outdated

# Test 3: Scan Docker image
docker scan bahr-api:latest --severity high

# Test 4: Check for CVEs
curl https://nvd.nist.gov/vuln/search/results?form_type=Advanced&cves=on&cpe_vendor=cpe:/:python
```

### Residual Risk: 🟡 Medium
- Automated dependency updates (Dependabot) not yet configured
- Need SCA (Software Composition Analysis) tool integration

---

## A07:2021 – Identification and Authentication Failures
### Risk Level: 🟠 High

### Description
Confirmation of the user's identity, authentication, and session management is critical.

### BAHR-Specific Risks
- Weak password policy
- Missing rate limiting on login
- Session fixation
- No account lockout
- Credential stuffing attacks

### Implemented Controls

#### 1. Strong Password Requirements
**Location:** `backend/app/core/security/password.py`

```python
class PasswordValidator:
    MIN_LENGTH = 8
    MAX_LENGTH = 128
    
    @staticmethod
    def validate(password: str) -> tuple[bool, list[str]]:
        issues = []
        
        if len(password) < PasswordValidator.MIN_LENGTH:
            issues.append(f"Minimum {PasswordValidator.MIN_LENGTH} characters")
        
        if len(password) > PasswordValidator.MAX_LENGTH:
            issues.append(f"Maximum {PasswordValidator.MAX_LENGTH} characters")
        
        if not re.search(r'[a-z]', password):
            issues.append("At least one lowercase letter")
        
        if not re.search(r'[A-Z]', password):
            issues.append("At least one uppercase letter")
        
        if not re.search(r'\d', password):
            issues.append("At least one number")
        
        # Check against common passwords
        if password.lower() in COMMON_PASSWORDS:
            issues.append("Password is too common")
        
        return len(issues) == 0, issues
```

#### 2. Login Rate Limiting
**Location:** `backend/app/api/v1/auth.py`

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@router.post("/auth/login")
@limiter.limit("5/minute")  # 5 attempts per minute
async def login(credentials: LoginRequest, request: Request):
    user = await authenticate_user(credentials.email, credentials.password)
    
    if not user:
        # Log failed attempt
        await log_failed_login(
            email=credentials.email,
            ip=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        raise HTTPException(401, "Invalid credentials")
    
    return create_tokens(user)
```

#### 3. Account Lockout
**Location:** `backend/app/core/security/lockout.py`

```python
async def check_lockout(email: str, db: Session) -> bool:
    """Check if account is locked"""
    failed_attempts = await get_failed_login_attempts(email, db)
    
    if len(failed_attempts) >= 5:
        last_attempt = max(failed_attempts, key=lambda x: x.timestamp)
        lockout_until = last_attempt.timestamp + timedelta(minutes=15)
        
        if datetime.now() < lockout_until:
            raise HTTPException(
                429,
                f"Account locked until {lockout_until.isoformat()}"
            )
        else:
            # Clear old attempts
            await clear_failed_attempts(email, db)
    
    return False
```

#### 4. Session Security
**Location:** `backend/app/middleware/session.py`

```python
# JWT with short expiration
ACCESS_TOKEN_EXPIRE = 30  # minutes
REFRESH_TOKEN_EXPIRE = 7  # days

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4())  # Token ID for revocation
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

### Testing Procedures

```bash
# Test 1: Weak password rejection
curl -X POST http://localhost:8000/api/v1/auth/register \
  -d '{"email":"test@test.com","password":"123"}' | \
  jq '.error.message'
# Should reject weak password

# Test 2: Login rate limiting
for i in {1..6}; do
  curl -X POST http://localhost:8000/api/v1/auth/login \
    -d '{"email":"test@test.com","password":"wrong"}' \
    -w "%{http_code}\n"
done | tail -1
# Should return 429 after 5 attempts

# Test 3: Account lockout
# Make 5 failed login attempts
# Should lock account for 15 minutes

# Test 4: Token expiration
# Wait 31 minutes, try using access token
# Should return 401 unauthorized
```

### Residual Risk: 🟠 High
- Multi-factor authentication not implemented (Phase 2)
- Password breach database check not integrated
- Biometric authentication not supported (future)

---

## A08:2021 – Software and Data Integrity Failures
### Risk Level: 🟢 Low

### Description
Code and infrastructure that does not protect against integrity violations.

### BAHR-Specific Risks
- Unsigned analysis results
- Tampering with meter patterns
- Malicious updates to NLP models
- CI/CD pipeline compromise

### Implemented Controls

#### 1. Data Integrity (Analysis Results)
**Location:** `backend/app/core/integrity.py`

```python
import hmac
import hashlib

def sign_data(data: dict, secret: str) -> str:
    """Create HMAC signature for data"""
    canonical = json.dumps(data, sort_keys=True)
    signature = hmac.new(
        secret.encode(),
        canonical.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature

def verify_signature(data: dict, signature: str, secret: str) -> bool:
    """Verify data hasn't been tampered"""
    expected = sign_data(data, secret)
    return hmac.compare_digest(expected, signature)
```

#### 2. CI/CD Security
**Location:** `.github/workflows/ci.yml`

```yaml
# Verify dependencies haven't been tampered
- name: Verify checksums
  run: |
    pip install pip-tools
    pip-compile --generate-hashes requirements/base.txt
    pip-sync --require-hashes requirements/base.txt

# Code signing (future)
- name: Sign artifacts
  run: |
    gpg --sign dist/bahr-api-1.0.0.tar.gz
```

### Testing Procedures

```bash
# Test 1: Verify analysis signature
python -c "
from app.core.integrity import sign_data, verify_signature
data = {'meter': 'الطويل', 'confidence': 0.92}
sig = sign_data(data, 'secret')
assert verify_signature(data, sig, 'secret')

# Tampered data should fail
data['confidence'] = 0.99
assert not verify_signature(data, sig, 'secret')
"

# Test 2: Check Docker image signature
docker trust inspect bahr-api:latest
```

### Residual Risk: 🟢 Low
- Code signing for releases (to be implemented)
- Supply chain security (Dependabot integration pending)

---

## A09:2021 – Security Logging and Monitoring Failures
### Risk Level: 🟡 Medium

### Description
Without logging and monitoring, breaches cannot be detected.

### BAHR-Specific Risks
- Failed login attempts not logged
- Unusual analysis patterns not detected
- No alerting on security events
- Log data not retained

### Implemented Controls

#### 1. Security Event Logging
**Location:** `backend/app/core/logging/security.py`

```python
import logging
import json

security_logger = logging.getLogger("security")

async def log_security_event(
    event_type: str,
    user_id: int = None,
    ip_address: str = None,
    details: dict = None
):
    """Log security-relevant events"""
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "ip_address": ip_address,
        "details": details
    }
    
    security_logger.warning(json.dumps(event))
    
    # Also store in database for analysis
    await db.security_events.create(event)

# Usage
await log_security_event(
    event_type="failed_login",
    ip_address=request.client.host,
    details={"email": email, "reason": "invalid_password"}
)
```

#### 2. Metrics and Alerting
**Location:** `backend/app/metrics/security.py`

```python
from prometheus_client import Counter, Gauge

failed_login_total = Counter(
    'bahr_failed_logins_total',
    'Total failed login attempts',
    ['reason']
)

suspicious_activity_total = Counter(
    'bahr_suspicious_activity_total',
    'Suspicious activity detected',
    ['activity_type']
)

# Alert rules (Prometheus)
# Alert if > 10 failed logins per minute
# Alert if unusual traffic pattern
```

#### 3. Log Retention
**Location:** `backend/app/core/logging/config.py`

```python
LOGGING_CONFIG = {
    "handlers": {
        "security_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/bahr/security.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 90,  # 90 days retention
            "formatter": "json"
        }
    }
}
```

### Testing Procedures

```bash
# Test 1: Verify failed login is logged
tail -f /var/log/bahr/security.log &
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d '{"email":"test@test.com","password":"wrong"}'
# Should see entry in security.log

# Test 2: Check Prometheus metrics
curl http://localhost:8000/metrics | grep failed_login
# Should show counter

# Test 3: Trigger alert (simulate 20 failed logins)
# Check if alert fires in Alertmanager
```

### Residual Risk: 🟡 Medium
- SIEM integration not yet implemented
- Automated incident response not configured
- Log analysis automation pending

---

## A10:2021 – Server-Side Request Forgery (SSRF)
### Risk Level: 🟢 Low

### BAHR-Specific Risks
- Future feature: Import verse from URL
- Webhook integrations (future)
- External API calls for NLP

### Implemented Controls

#### 1. URL Validation
**Location:** `backend/app/core/security/url.py`

```python
from urllib.parse import urlparse
import ipaddress

ALLOWED_DOMAINS = [
    "aldiwan.net",
    "adab.com"
]

BLOCKED_IP_RANGES = [
    ipaddress.ip_network("127.0.0.0/8"),    # Localhost
    ipaddress.ip_network("10.0.0.0/8"),     # Private
    ipaddress.ip_network("172.16.0.0/12"),  # Private
    ipaddress.ip_network("192.168.0.0/16"), # Private
    ipaddress.ip_network("169.254.0.0/16"), # Link-local
]

async def validate_url(url: str) -> bool:
    """Validate URL is safe for SSRF"""
    parsed = urlparse(url)
    
    # Check protocol
    if parsed.scheme not in ["http", "https"]:
        raise ValueError("Only HTTP/HTTPS allowed")
    
    # Check domain whitelist
    if parsed.netloc not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain {parsed.netloc} not allowed")
    
    # Resolve and check IP
    import socket
    try:
        ip = socket.gethostbyname(parsed.netloc)
        ip_obj = ipaddress.ip_address(ip)
        
        for blocked_range in BLOCKED_IP_RANGES:
            if ip_obj in blocked_range:
                raise ValueError(f"IP {ip} is in blocked range")
    except socket.gaierror:
        raise ValueError("Cannot resolve domain")
    
    return True
```

### Testing Procedures

```bash
# Test 1: Block private IP access
curl -X POST http://localhost:8000/api/v1/import \
  -d '{"url":"http://127.0.0.1:8080/admin"}' | \
  jq '.success'
# Should fail

# Test 2: Block metadata endpoints
curl -X POST http://localhost:8000/api/v1/import \
  -d '{"url":"http://169.254.169.254/latest/meta-data/"}' | \
  jq '.success'
# Should fail

# Test 3: Allow whitelisted domain
curl -X POST http://localhost:8000/api/v1/import \
  -d '{"url":"https://aldiwan.net/poem/123"}' | \
  jq '.success'
# Should succeed
```

### Residual Risk: 🟢 Low
- Feature not yet implemented (future)
- When implemented, follow validation above

---

## 📊 Overall Risk Summary

| OWASP Category | Risk Level | Status | Priority |
|----------------|-----------|--------|----------|
| A01: Broken Access Control | 🟠 High | ⚠️ Partial | P1 |
| A02: Cryptographic Failures | 🟡 Medium | ✅ Good | P2 |
| A03: Injection | 🟡 Medium | ✅ Good | P2 |
| A04: Insecure Design | 🟢 Low | ✅ Good | P3 |
| A05: Security Misconfiguration | 🟡 Medium | ⚠️ Partial | P2 |
| A06: Vulnerable Components | 🟡 Medium | ⚠️ Partial | P1 |
| A07: Auth Failures | 🟠 High | ⚠️ Partial | P1 |
| A08: Integrity Failures | 🟢 Low | ✅ Good | P3 |
| A09: Logging Failures | 🟡 Medium | ⚠️ Partial | P2 |
| A10: SSRF | 🟢 Low | ✅ Good | P3 |

**Overall Security Posture:** 🟡 **Medium** (Acceptable for MVP launch)

---

## 🎯 Week 1 Action Items

### Critical (Before Production)
1. ✅ Implement JWT authentication
2. ✅ Enable rate limiting
3. ✅ Add security headers
4. ✅ Configure CORS properly
5. ⚠️ Add failed login logging

### Important (Week 1-2)
6. Set up dependency scanning
7. Configure log retention
8. Add abuse detection
9. Implement account lockout
10. Create security runbook

### Nice to Have (Week 2+)
11. MFA (multi-factor auth)
12. SIEM integration
13. Automated incident response
14. Penetration testing

---

## 🔗 Related Documentation

- `SECURITY.md` - Main security guide
- `SECURITY_AUDIT_CHECKLIST.md` - Detailed checklist
- `ERROR_HANDLING_STRATEGY.md` - Error handling
- `API_VERSIONING.md` - API security lifecycle

---

**Document Version:** 1.0  
**Last Updated:** November 9, 2025  
**Next Review:** December 9, 2025  
**Maintained By:** Security Team
