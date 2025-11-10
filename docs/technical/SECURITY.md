# 🔒 دليل الأمان (Security Guide)
## استراتيجية الأمان الشاملة لمنصة بَحْر

---

## 📋 نظرة عامة

دليل شامل لتأمين منصة بَحْر من التهديدات الأمنية الشائعة، مع التركيز على:
- **Authentication & Authorization** - المصادقة والتفويض
- **Data Protection** - حماية البيانات
- **Input Validation** - التحقق من المدخلات
- **Arabic-Specific Security** - أمان خاص بالعربية
- **Infrastructure Security** - أمان البنية التحتية

**تاريخ الإنشاء:** November 8, 2025  
**الأولوية:** حرجة (يجب تطبيقها من Week 1)

---

## 🎯 المبادئ الأساسية

```yaml
Security Principles:
  1. Defense in Depth: طبقات أمان متعددة
  2. Principle of Least Privilege: أقل صلاحيات ممكنة
  3. Fail Securely: الفشل الآمن (لا تكشف معلومات حساسة)
  4. Security by Design: الأمان من التصميم، ليس إضافة لاحقة
  5. Regular Updates: تحديثات أمنية منتظمة
```

---

## 🔐 Week 1: Critical Security Items

### 1️⃣ **Password Security**

```python
# app/core/security/password.py
from passlib.context import CryptContext
import secrets
import string

# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Cost factor (balance security vs performance)
    bcrypt__ident="2b"   # Bcrypt version
)

class PasswordManager:
    """Secure password handling"""
    
    MIN_LENGTH = 8
    MAX_LENGTH = 128
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storing"""
        if len(password) < PasswordManager.MIN_LENGTH:
            raise ValueError(f"Password must be at least {PasswordManager.MIN_LENGTH} characters")
        if len(password) > PasswordManager.MAX_LENGTH:
            raise ValueError(f"Password must be at most {PasswordManager.MAX_LENGTH} characters")
        
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a stored password against one provided by user"""
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            # Constant-time response to prevent timing attacks
            pwd_context.hash(plain_password)
            return False
    
    @staticmethod
    def needs_rehash(hashed_password: str) -> bool:
        """Check if password needs rehashing (e.g., cost factor updated)"""
        return pwd_context.needs_update(hashed_password)
    
    @staticmethod
    def generate_password(length: int = 16) -> str:
        """Generate a secure random password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))

# Password strength validation
class PasswordValidator:
    """Validate password strength"""
    
    @staticmethod
    def validate(password: str) -> tuple[bool, list[str]]:
        """
        Returns: (is_valid, list_of_issues)
        """
        issues = []
        
        if len(password) < 8:
            issues.append("Password must be at least 8 characters")
        
        if not any(c.isupper() for c in password):
            issues.append("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in password):
            issues.append("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in password):
            issues.append("Password must contain at least one digit")
        
        # Check against common passwords (implement blocklist)
        common_passwords = ["password", "12345678", "qwerty", "admin"]
        if password.lower() in common_passwords:
            issues.append("Password is too common")
        
        return (len(issues) == 0, issues)
```

**Week 1 Implementation Checklist:**
```yaml
Password Security:
  - ✅ Use bcrypt with cost factor 12
  - ✅ Implement password strength validation
  - ✅ Constant-time comparison (prevent timing attacks)
  - ✅ Add password rehashing check (update old hashes)
  - ✅ Limit password length (prevent DoS via long inputs)
  - ✅ No password hints or recovery questions
  - ✅ Rate limit password attempts (5 tries per 15 minutes)
```

---

### 2️⃣ **JWT Token Security**

```python
# app/core/security/jwt_handler.py
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from jwt.exceptions import InvalidTokenError
import secrets

class JWTHandler:
    """Secure JWT token management"""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7
        
        # Token blacklist (in production, use Redis)
        self.blacklist: set[str] = set()
    
    def create_access_token(
        self, 
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(16),  # JWT ID for revocation
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(16),
            "type": "refresh"
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check token type
            if payload.get("type") != token_type:
                return None
            
            # Check if token is blacklisted
            jti = payload.get("jti")
            if jti and jti in self.blacklist:
                return None
            
            return payload
            
        except InvalidTokenError:
            return None
    
    def revoke_token(self, token: str):
        """Add token to blacklist"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            jti = payload.get("jti")
            if jti:
                self.blacklist.add(jti)
                # In production: redis.setex(f"blacklist:{jti}", ttl, "1")
        except InvalidTokenError:
            pass

# Token rotation strategy
class TokenRotationManager:
    """Manage token rotation for enhanced security"""
    
    @staticmethod
    def rotate_on_usage(refresh_token: str, jwt_handler: JWTHandler) -> tuple[str, str]:
        """
        Rotate tokens on refresh (optional but recommended)
        Returns: (new_access_token, new_refresh_token)
        """
        payload = jwt_handler.verify_token(refresh_token, token_type="refresh")
        if not payload:
            raise ValueError("Invalid refresh token")
        
        # Revoke old refresh token
        jwt_handler.revoke_token(refresh_token)
        
        # Create new tokens
        user_data = {"sub": payload["sub"], "role": payload.get("role")}
        new_access = jwt_handler.create_access_token(user_data)
        new_refresh = jwt_handler.create_refresh_token(user_data)
        
        return new_access, new_refresh
```

**JWT Security Checklist:**
```yaml
JWT Configuration:
  - ✅ Use strong secret key (min 256 bits)
  - ✅ Rotate secret keys every 90 days (have key rotation plan)
  - ✅ Short access token lifetime (30 minutes)
  - ✅ Longer refresh token lifetime (7 days)
  - ✅ Include jti (JWT ID) for revocation
  - ✅ Token blacklist (Redis-backed in production)
  - ✅ Token rotation on refresh (optional but recommended)
  - ✅ Validate token type (access vs refresh)
  - ✅ Check token expiration
  - ✅ Store refresh tokens securely (httpOnly cookies)
```

**Secret Key Rotation Strategy:**
```yaml
Key Rotation Schedule:
  Development: No rotation (use fixed key from .env)
  
  Production:
    - Primary secret key in environment variable
    - Rotate every 90 days
    - Grace period: Support 2 keys simultaneously during rotation
    - Process:
      1. Generate new key: openssl rand -hex 32
      2. Add as SECONDARY_SECRET_KEY
      3. Accept tokens signed with either key (7 days)
      4. Promote secondary to primary
      5. Remove old key
```

---

### 3️⃣ **SQL Injection Prevention**

```python
# app/db/repositories/base.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any

class SecureRepository:
    """Base repository with SQL injection prevention"""
    
    def __init__(self, session: Session):
        self.session = session
    
    # ✅ SAFE: Using SQLAlchemy ORM (parameterized automatically)
    def get_user_by_email_safe(self, email: str):
        """Safe query using ORM"""
        from app.models.user import User
        return self.session.query(User).filter(User.email == email).first()
    
    # ✅ SAFE: Using parameterized raw SQL
    def search_poems_safe(self, search_term: str):
        """Safe raw SQL with parameters"""
        query = text("""
            SELECT * FROM analyses 
            WHERE original_text LIKE :search_term
            LIMIT 100
        """)
        result = self.session.execute(query, {"search_term": f"%{search_term}%"})
        return result.fetchall()
    
    # ❌ UNSAFE: String concatenation (NEVER DO THIS!)
    def search_poems_unsafe(self, search_term: str):
        """
        DANGEROUS! Vulnerable to SQL injection
        Example attack: search_term = "'; DROP TABLE users; --"
        """
        query = f"SELECT * FROM analyses WHERE original_text LIKE '%{search_term}%'"
        # This will execute the SQL injection!
        return self.session.execute(text(query)).fetchall()
    
    # ✅ SAFE: Dynamic table/column names (whitelist approach)
    def sort_by_column_safe(self, table: str, column: str, direction: str):
        """Safe dynamic sorting with whitelist"""
        # Whitelist allowed values
        ALLOWED_TABLES = ["analyses", "users", "meters"]
        ALLOWED_COLUMNS = ["created_at", "quality_score", "username"]
        ALLOWED_DIRECTIONS = ["ASC", "DESC"]
        
        if table not in ALLOWED_TABLES:
            raise ValueError(f"Invalid table: {table}")
        if column not in ALLOWED_COLUMNS:
            raise ValueError(f"Invalid column: {column}")
        if direction.upper() not in ALLOWED_DIRECTIONS:
            raise ValueError(f"Invalid direction: {direction}")
        
        # Now safe to use in query (values are whitelisted)
        query = text(f"SELECT * FROM {table} ORDER BY {column} {direction}")
        return self.session.execute(query).fetchall()
```

**SQL Injection Prevention Checklist:**
```yaml
SQL Security:
  - ✅ Always use SQLAlchemy ORM (parameterized by default)
  - ✅ If raw SQL needed, use text() with parameters
  - ✅ NEVER concatenate user input into SQL strings
  - ✅ Whitelist dynamic table/column names
  - ✅ Validate and sanitize all input
  - ✅ Use principle of least privilege (DB user has minimal permissions)
  - ✅ Disable dangerous SQL features (e.g., xp_cmdshell in MSSQL)
  - ✅ Log and monitor suspicious queries
```

---

### 4️⃣ **XSS Protection (Arabic-Specific)**

```python
# app/core/security/xss_protection.py
import html
import bleach
from typing import Optional

class ArabicXSSProtector:
    """XSS protection with Arabic text support"""
    
    # Allowed HTML tags for rich text (e.g., in user bios)
    ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 'a']
    ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}
    ALLOWED_PROTOCOLS = ['http', 'https']
    
    @staticmethod
    def sanitize_html(content: str) -> str:
        """
        Sanitize HTML content while preserving Arabic text
        Uses bleach library (more robust than basic html.escape)
        """
        if not content:
            return ""
        
        # Bleach handles Arabic text correctly
        cleaned = bleach.clean(
            content,
            tags=ArabicXSSProtector.ALLOWED_TAGS,
            attributes=ArabicXSSProtector.ALLOWED_ATTRIBUTES,
            protocols=ArabicXSSProtector.ALLOWED_PROTOCOLS,
            strip=True  # Strip disallowed tags instead of escaping
        )
        
        return cleaned
    
    @staticmethod
    def escape_for_html(text: str) -> str:
        """
        Basic HTML escaping (for plain text display)
        Handles Arabic characters correctly
        """
        if not text:
            return ""
        
        # html.escape handles Unicode (Arabic) correctly
        return html.escape(text, quote=True)
    
    @staticmethod
    def sanitize_arabic_poem(poem_text: str) -> str:
        """
        Sanitize poem text (no HTML allowed)
        Preserve newlines and Arabic diacritics
        """
        if not poem_text:
            return ""
        
        # Remove any HTML tags
        cleaned = bleach.clean(poem_text, tags=[], strip=True)
        
        # Preserve only allowed characters:
        # - Arabic letters (U+0600-U+06FF)
        # - Arabic diacritics (U+064B-U+0652)
        # - Whitespace and newlines
        # - Basic punctuation
        
        return cleaned.strip()
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL to prevent javascript: and data: URLs"""
        if not url:
            return False
        
        url_lower = url.lower().strip()
        
        # Block dangerous protocols
        dangerous_protocols = ['javascript:', 'data:', 'vbscript:', 'file:']
        if any(url_lower.startswith(proto) for proto in dangerous_protocols):
            return False
        
        # Only allow http(s)
        if not (url_lower.startswith('http://') or url_lower.startswith('https://')):
            return False
        
        return True

# Response headers configuration
SECURITY_HEADERS = {
    # Prevent XSS attacks
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    
    # Content Security Policy (strict for MVP)
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "  # Will tighten in production
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https://api.bahr.com; "  # Your API domain
        "frame-ancestors 'none';"
    ),
    
    # HTTPS enforcement (production only)
    # "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
}
```

**XSS Prevention Checklist:**
```yaml
XSS Protection:
  - ✅ Escape all user input before rendering in HTML
  - ✅ Use bleach for HTML sanitization (Arabic-safe)
  - ✅ Never use dangerouslySetInnerHTML in React (or sanitize first)
  - ✅ Validate URLs to block javascript: and data: protocols
  - ✅ Set Content-Security-Policy header
  - ✅ Set X-Content-Type-Options: nosniff
  - ✅ Set X-Frame-Options: DENY
  - ✅ Test with Arabic text containing HTML tags
  - ✅ Test with RTL override characters (potential UI manipulation)
```

**Arabic-Specific XSS Risks:**
```yaml
Arabic Text Vulnerabilities:
  1. RTL Override Characters:
     - U+202E (RIGHT-TO-LEFT OVERRIDE)
     - Can manipulate text display (e.g., hide malicious content)
     - Solution: Strip or escape these characters
  
  2. Diacritics Overflow:
     - Stacking many diacritics can overflow containers
     - Solution: Limit diacritics per character (max 2)
  
  3. Homograph Attacks:
     - Arabic letters that look similar to Latin (e.g., و vs v)
     - Solution: Display warning for mixed scripts in URLs
```

---

### 5️⃣ **Rate Limiting**

```python
# app/api/middleware/rate_limit.py
from fastapi import Request, HTTPException, status
from datetime import datetime, timedelta
from typing import Optional
import redis.asyncio as redis
import hashlib

class RateLimiter:
    """Rate limiting middleware with Redis backend"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        # Development mode bypass (configured via environment variable)
        self.dev_mode = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "false"
        self.localhost_whitelist = ["127.0.0.1", "localhost", "::1"]
    
    async def check_rate_limit(
        self,
        request: Request,
        limit: int = 100,  # requests
        window: int = 3600,  # seconds (1 hour)
        scope: str = "global"
    ) -> bool:
        """
        Check if request should be rate limited
        Returns: True if allowed, raises HTTPException if rate limited
        """
        # Development mode bypass
        if self.dev_mode:
            return True
        
        # Get identifier (IP + User ID if authenticated)
        identifier = self._get_identifier(request)
        
        # Localhost whitelist (for development and testing)
        client_ip = request.client.host
        if client_ip in self.localhost_whitelist:
            return True
        
        # Create Redis key
        key = f"rate_limit:{scope}:{identifier}"
        
        # Get current count
        current = await self.redis.get(key)
        
        if current is None:
            # First request in window
            await self.redis.setex(key, window, 1)
            return True
        
        current_count = int(current)
        
        if current_count >= limit:
            # Rate limit exceeded
            ttl = await self.redis.ttl(key)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "rate_limit_exceeded",
                    "message": f"Too many requests. Try again in {ttl} seconds.",
                    "message_ar": f"طلبات كثيرة جداً. حاول مرة أخرى بعد {ttl} ثانية.",
                    "retry_after": ttl
                },
                headers={"Retry-After": str(ttl)}
            )
        
        # Increment counter
        await self.redis.incr(key)
        return True
    
    def _get_identifier(self, request: Request) -> str:
        """Get unique identifier for rate limiting"""
        # Prefer user ID if authenticated
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user:{user_id}"
        
        # Fall back to IP address
        # Handle proxies (check X-Forwarded-For)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            ip = forwarded_for.split(",")[0].strip()
        else:
            ip = request.client.host
        
        return f"ip:{ip}"

# Rate limit configurations for different endpoints
RATE_LIMITS = {
    "analysis": {"limit": 50, "window": 3600},  # 50 analyses per hour
    "authentication": {"limit": 5, "window": 900},  # 5 login attempts per 15 min
    "registration": {"limit": 3, "window": 3600},  # 3 registrations per hour per IP
    "password_reset": {"limit": 3, "window": 3600},  # 3 resets per hour
    "api_global": {"limit": 100, "window": 3600},  # 100 requests per hour (default)
}

# Usage in FastAPI
"""
from fastapi import Depends

async def rate_limit_dependency(
    request: Request,
    limiter: RateLimiter = Depends(get_rate_limiter)
):
    await limiter.check_rate_limit(request, **RATE_LIMITS["analysis"])

@router.post("/analyze", dependencies=[Depends(rate_limit_dependency)])
async def analyze_poetry(poem: PoemInput):
    ...
"""
```

**Rate Limiting Checklist:**
```yaml
Rate Limiting:
  - ✅ Implement rate limiting from Week 1
  - ✅ Different limits per endpoint type
  - ✅ Per-IP rate limiting for unauthenticated requests
  - ✅ Per-user rate limiting for authenticated requests
  - ✅ Redis-backed counters (sliding window)
  - ✅ Return 429 status code with Retry-After header
  - ✅ Bilingual error messages (AR + EN)
  - ✅ Stricter limits for authentication endpoints (prevent brute force)
  - ✅ Monitor and adjust limits based on usage patterns
```

---

## 🛡️ Week 6-7: Advanced Security

### 6️⃣ **Content Security Policy (CSP)**

```typescript
// frontend/middleware.ts (Next.js middleware)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  
  // Content Security Policy (tighten for production)
  const cspHeader = `
    default-src 'self';
    script-src 'self' 'unsafe-eval' 'unsafe-inline' https://vercel.live;
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    font-src 'self' https://fonts.gstatic.com;
    img-src 'self' data: https: blob:;
    connect-src 'self' ${process.env.NEXT_PUBLIC_API_URL};
    frame-ancestors 'none';
    base-uri 'self';
    form-action 'self';
  `.replace(/\s{2,}/g, ' ').trim();
  
  response.headers.set('Content-Security-Policy', cspHeader);
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-XSS-Protection', '1; mode=block');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  
  // HSTS (production only - DO NOT enable in development)
  if (process.env.NODE_ENV === 'production') {
    response.headers.set(
      'Strict-Transport-Security',
      'max-age=31536000; includeSubDomains'
    );
  }
  
  return response;
}
```

---

### 7️⃣ **Backup Security**

```yaml
Backup Strategy:
  Database Backups:
    - Frequency: Daily automated backups
    - Retention: 7 days (MVP), 30 days (production)
    - Encryption: AES-256 encryption at rest
    - Storage: Separate cloud bucket (AWS S3 / DO Spaces)
    - Access: Restricted to admin only
    
  Backup Testing:
    - Monthly restore test (ensure backups are valid)
    - Document restore procedure
    - Test RTO (Recovery Time Objective): 4 hours
    - Test RPO (Recovery Point Objective): 24 hours
  
  Secrets Backup:
    - Store in secure vault (1Password / AWS Secrets Manager)
    - NEVER commit secrets to Git
    - Rotate secrets regularly
    - Document secret rotation procedure
```

---

## 🔍 Security Monitoring & Logging

```python
# app/core/security/audit_log.py
from datetime import datetime
from enum import Enum
import logging

class SecurityEventType(Enum):
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    PASSWORD_RESET = "password_reset"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    ADMIN_ACTION = "admin_action"

class SecurityLogger:
    """Log security-related events"""
    
    def __init__(self):
        self.logger = logging.getLogger("security")
    
    def log_event(
        self,
        event_type: SecurityEventType,
        user_id: Optional[int],
        ip_address: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log security event"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type.value,
            "user_id": user_id,
            "ip_address": ip_address,
            "details": details or {}
        }
        
        # Log to file/service
        self.logger.warning(log_data)
        
        # In production: Send to monitoring service (Sentry, DataDog)
        # sentry_sdk.capture_message(f"Security event: {event_type.value}", level="warning")
```

---

## 📋 Security Checklist for Launch

```yaml
Pre-Launch Security Checklist:

✅ Authentication & Authorization:
  - [ ] Password hashing with bcrypt (cost 12+)
  - [ ] JWT tokens with expiration
  - [ ] Token blacklist for logout
  - [ ] Rate limiting on auth endpoints

✅ Input Validation:
  - [ ] All user input validated
  - [ ] SQL injection prevention
  - [ ] XSS protection (HTML escaping)
  - [ ] Arabic text sanitization

✅ Data Protection:
  - [ ] HTTPS enforced (production)
  - [ ] Secure cookies (httpOnly, secure, sameSite)
  - [ ] Encrypted database backups
  - [ ] No secrets in code/Git

✅ Infrastructure:
  - [ ] Security headers set (CSP, X-Frame-Options, etc.)
  - [ ] Rate limiting per IP and per user
  - [ ] CORS properly configured
  - [ ] Database user has minimal permissions

✅ Monitoring:
  - [ ] Security event logging
  - [ ] Failed login attempt monitoring
  - [ ] Rate limit breach alerts
  - [ ] Error monitoring (Sentry)

✅ Compliance:
  - [ ] Privacy policy (if collecting PII)
  - [ ] Terms of service
  - [ ] Cookie consent (EU users)
  - [ ] Data retention policy
```

---

## 🚨 Incident Response Plan

```yaml
Security Incident Response:
  
  1. Detection:
     - Monitor logs for suspicious activity
     - Set up alerts for rate limit breaches
     - Monitor failed login attempts
  
  2. Containment:
     - Immediately revoke compromised tokens
     - Block malicious IP addresses
     - Disable affected user accounts
  
  3. Investigation:
     - Review audit logs
     - Identify attack vector
     - Assess damage scope
  
  4. Recovery:
     - Restore from backup if needed
     - Reset compromised passwords
     - Patch vulnerability
  
  5. Post-Incident:
     - Document incident
     - Update security measures
     - Notify affected users (if required)
```

---

## 📚 Security Resources

```yaml
Security Best Practices:
  - OWASP Top 10: https://owasp.org/www-project-top-ten/
  - OWASP API Security: https://owasp.org/www-project-api-security/
  - FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
  - Next.js Security: https://nextjs.org/docs/app/building-your-application/configuring/content-security-policy

Security Tools:
  - Dependency scanning: Snyk, Dependabot
  - SAST: Bandit (Python), ESLint security plugin (JS)
  - Penetration testing: OWASP ZAP
  - Secret scanning: GitGuardian, TruffleHog
```

---

## ⚠️ Final Notes

**Critical Reminders:**
1. **Security is not optional** - implement from Day 1
2. **Don't reinvent the wheel** - use proven libraries (passlib, bleach, etc.)
3. **Assume all input is malicious** - validate everything
4. **Arabic text needs special attention** - test XSS with Arabic characters
5. **Keep dependencies updated** - security patches are critical
6. **Monitor and log** - you can't fix what you can't see

**Week 1 Priority:**
Focus on items 1-5 above (Password, JWT, SQL Injection, XSS, Rate Limiting). These are the foundations. Advanced items (CSP, monitoring) can be added in Week 6-7.
