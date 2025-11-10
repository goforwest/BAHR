# 🔒 Security Audit Checklist
## Comprehensive Security Assessment for BAHR Platform

**Last Updated:** November 9, 2025  
**Purpose:** Security verification before production deployment  
**Frequency:** Pre-deployment + Quarterly reviews  
**Related:** `SECURITY.md`, `API_VERSIONING.md`, `ERROR_HANDLING_STRATEGY.md`

---

## 📋 Overview

This checklist ensures BAHR meets security standards across:
- Authentication & Authorization
- Data Protection
- Input Validation
- Infrastructure Security
- OWASP Top 10 Compliance
- Arabic-specific Security Concerns

**Scoring:**
- ✅ Implemented and verified
- ⚠️ Partially implemented
- ❌ Not implemented
- 📝 Not applicable

---

## 🔐 1. Authentication & Authorization

### 1.1 Password Security

- [ ] **Password Hashing**
  - [ ] Bcrypt with cost factor ≥ 12 implemented
  - [ ] Password hashing verified in unit tests
  - [ ] No plaintext passwords in logs or database
  - [ ] Timing-safe password comparison used

- [ ] **Password Policy**
  - [ ] Minimum length: 8 characters enforced
  - [ ] Maximum length: 128 characters (prevent DoS)
  - [ ] Complexity requirements documented
  - [ ] Password strength meter in UI
  - [ ] Common password blacklist implemented

- [ ] **Password Reset**
  - [ ] Secure token generation (crypto-random)
  - [ ] Token expiration: ≤ 1 hour
  - [ ] One-time use tokens
  - [ ] Rate limiting on reset requests
  - [ ] No username enumeration in reset flow

**Verification Commands:**
```python
# Test password hashing
python -c "from app.core.security.password import PasswordManager; \
  hashed = PasswordManager.hash_password('TestPass123'); \
  assert PasswordManager.verify_password('TestPass123', hashed); \
  print('✅ Password hashing works')"

# Check bcrypt cost factor
python -c "from passlib.context import CryptContext; \
  ctx = CryptContext(schemes=['bcrypt']); \
  print(f'Bcrypt rounds: {ctx.identify(hashed).split(\"$\")[2]}')"
```

---

### 1.2 JWT Tokens

- [ ] **Token Security**
  - [ ] HS256 or RS256 algorithm (not 'none')
  - [ ] Secret key ≥ 256 bits
  - [ ] Secret key stored in env var (not code)
  - [ ] Token signing verified
  - [ ] Algorithm verification enforced

- [ ] **Token Expiration**
  - [ ] Access token: ≤ 30 minutes
  - [ ] Refresh token: ≤ 7 days
  - [ ] `exp` claim validated
  - [ ] `nbf` (not before) claim used
  - [ ] Token refresh rotation implemented

- [ ] **Token Revocation**
  - [ ] Blacklist for revoked tokens (Redis)
  - [ ] Logout invalidates tokens
  - [ ] JTI (token ID) for tracking
  - [ ] Admin can revoke user tokens

**Verification Commands:**
```bash
# Decode JWT to verify claims
curl http://localhost:8000/api/v1/auth/login \
  -d '{"email":"test@test.com","password":"pass"}' | \
  jq -r '.data.access_token' | \
  python -c "import sys, jwt; \
    token = sys.stdin.read().strip(); \
    decoded = jwt.decode(token, options={'verify_signature': False}); \
    print(f'Expires: {decoded[\"exp\"]}'); \
    assert decoded['exp'] - decoded['iat'] <= 1800"
```

---

### 1.3 Session Management

- [ ] **Session Security**
  - [ ] Secure cookie flags: HttpOnly, Secure, SameSite
  - [ ] Session timeout: ≤ 30 minutes idle
  - [ ] Session rotation on privilege change
  - [ ] Concurrent session limit per user
  - [ ] Session invalidation on logout

- [ ] **CSRF Protection**
  - [ ] CSRF tokens for state-changing operations
  - [ ] SameSite cookie attribute set
  - [ ] Double-submit cookie pattern
  - [ ] Origin header validation

---

## 🛡️ 2. Input Validation & Sanitization

### 2.1 Arabic Text Input

- [ ] **Text Validation**
  - [ ] Minimum/maximum length enforced
  - [ ] Arabic character percentage ≥ 70% validated
  - [ ] Unicode normalization (NFC) applied
  - [ ] Control characters stripped
  - [ ] Null bytes removed

- [ ] **Security Characters**
  - [ ] RTL override (U+202E) removed
  - [ ] LTR override (U+202D) removed
  - [ ] Zero-width space (U+200B) removed
  - [ ] Zero-width non-joiner removed
  - [ ] Byte order mark (U+FEFF) removed

**Test Cases:**
```python
# Test RTL override attack
test_input = "قفا\u202Eنبك"  # Contains RTL override
response = normalize(test_input)
assert "\u202E" not in response, "RTL override not removed"

# Test zero-width characters
test_input = "قفا\u200Bنبك"
response = normalize(test_input)
assert "\u200B" not in response, "Zero-width not removed"
```

---

### 2.2 API Input Validation

- [ ] **Request Validation**
  - [ ] Pydantic models for all inputs
  - [ ] Field type validation enforced
  - [ ] Min/max constraints defined
  - [ ] Regex patterns for strings
  - [ ] Enum validation for fixed values

- [ ] **SQL Injection Prevention**
  - [ ] Parameterized queries only (SQLAlchemy ORM)
  - [ ] No raw SQL with string concatenation
  - [ ] Input escaping for dynamic queries
  - [ ] Whitelist for table/column names

- [ ] **NoSQL Injection Prevention**
  - [ ] Redis commands parameterized
  - [ ] No user input in EVAL commands
  - [ ] Input validation for cache keys

**Verification:**
```bash
# Test SQL injection attempt
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"قفا نبك' OR 1=1--"}' | \
  jq '.success'
# Should return false with ERR_INPUT_* error
```

---

### 2.3 XSS Prevention

- [ ] **Output Encoding**
  - [ ] HTML escaping for user content
  - [ ] JSON encoding for API responses
  - [ ] Content-Type headers set correctly
  - [ ] X-Content-Type-Options: nosniff header

- [ ] **Content Security Policy**
  - [ ] CSP header configured
  - [ ] Script sources whitelisted
  - [ ] Unsafe-inline/eval disabled
  - [ ] Frame ancestors restricted

**Test:**
```bash
# Test XSS attempt
curl -X POST http://localhost:8000/api/v1/analyze \
  -d '{"text":"<script>alert('xss')</script>قفا نبك"}' | \
  jq '.data.normalized_text'
# Should not contain script tags
```

---

## 🔒 3. Data Protection

### 3.1 Encryption

- [ ] **Data in Transit**
  - [ ] HTTPS enforced (TLS 1.2+)
  - [ ] HTTP → HTTPS redirect
  - [ ] HSTS header set (max-age ≥ 1 year)
  - [ ] Certificate valid and not self-signed
  - [ ] Strong cipher suites only

- [ ] **Data at Rest**
  - [ ] Database encryption enabled (if applicable)
  - [ ] Backup encryption enabled
  - [ ] Secrets encrypted in environment
  - [ ] API keys encrypted in database

**Verification:**
```bash
# Check TLS version
curl -I https://api.bahr.app | grep -i strict-transport-security

# Test SSL configuration
nmap --script ssl-enum-ciphers -p 443 api.bahr.app
```

---

### 3.2 Sensitive Data Handling

- [ ] **PII Protection**
  - [ ] Email addresses hashed in logs
  - [ ] No passwords in logs (even hashed)
  - [ ] User IDs anonymized in analytics
  - [ ] GDPR compliance for EU users

- [ ] **Secret Management**
  - [ ] No secrets in git history
  - [ ] .env files in .gitignore
  - [ ] Secret rotation policy defined
  - [ ] Secrets stored in secure vault (production)

**Check:**
```bash
# Verify no secrets in git
git grep -i "password.*=" | grep -v ".md" | grep -v "example"
git log -p | grep -i "password.*="

# Check .gitignore
cat .gitignore | grep -E "\.env$|\.env\.local$"
```

---

## 🚦 4. Rate Limiting & DoS Protection

### 4.1 Rate Limiting

- [ ] **API Rate Limits**
  - [ ] 100 requests/hour for unauthenticated
  - [ ] 500 requests/hour for authenticated
  - [ ] 10 requests/hour for batch endpoints
  - [ ] Rate limit headers returned (X-RateLimit-*)
  - [ ] 429 status code on limit exceeded

- [ ] **Login Rate Limiting**
  - [ ] 5 failed attempts → account lockout
  - [ ] Lockout duration: 15 minutes
  - [ ] CAPTCHA after 3 failed attempts
  - [ ] Email notification on lockout

**Test:**
```bash
# Test rate limiting
for i in {1..101}; do
  curl -s http://localhost:8000/api/v1/analyze \
    -d '{"text":"قفا نبك"}' \
    -o /dev/null -w "%{http_code}\n"
done | tail -1
# Should return 429 after 100 requests
```

---

### 4.2 Resource Limits

- [ ] **Request Size Limits**
  - [ ] Max request body: 1 MB
  - [ ] Max JSON depth: 10 levels
  - [ ] Max array length: 1000 items
  - [ ] Max string length: 10,000 chars

- [ ] **Timeout Protection**
  - [ ] Request timeout: 30 seconds
  - [ ] Database query timeout: 10 seconds
  - [ ] Redis timeout: 5 seconds
  - [ ] Graceful timeout handling

---

## 🌐 5. Infrastructure Security

### 5.1 Network Security

- [ ] **Firewall Configuration**
  - [ ] Only ports 80, 443 exposed publicly
  - [ ] Database port (5432) internal only
  - [ ] Redis port (6379) internal only
  - [ ] SSH port changed from 22 (if applicable)

- [ ] **CORS Configuration**
  - [ ] Specific origins whitelisted (no *)
  - [ ] Credentials allowed only for trusted origins
  - [ ] Preflight requests handled
  - [ ] OPTIONS method secured

**Test:**
```python
# Test CORS configuration
from fastapi.middleware.cors import CORSMiddleware
# Verify allow_origins != ["*"]
# Verify allow_credentials = True only with specific origins
```

---

### 5.2 Container Security

- [ ] **Docker Security**
  - [ ] Non-root user in containers
  - [ ] Read-only filesystem where possible
  - [ ] Minimal base images (alpine)
  - [ ] No secrets in Dockerfile
  - [ ] Regular image updates

- [ ] **Container Scanning**
  - [ ] Vulnerability scanning enabled
  - [ ] Critical CVEs addressed
  - [ ] Image signing implemented
  - [ ] Security policy defined

**Commands:**
```bash
# Scan Docker image
docker scan bahr-api:latest

# Check running as non-root
docker inspect bahr_api | jq '.[0].Config.User'
# Should not be "root" or empty
```

---

### 5.3 Dependency Security

- [ ] **Dependency Scanning**
  - [ ] pip-audit or safety installed
  - [ ] Regular dependency updates
  - [ ] Known vulnerabilities tracked
  - [ ] Automated alerts configured

- [ ] **Supply Chain Security**
  - [ ] Dependencies pinned to exact versions
  - [ ] Hash verification for packages
  - [ ] Private PyPI mirror (optional)
  - [ ] Dependency review in PRs

**Commands:**
```bash
# Check for vulnerable dependencies
pip install pip-audit
pip-audit

# Or use safety
pip install safety
safety check --json
```

---

## 📊 6. Logging & Monitoring

### 6.1 Security Logging

- [ ] **Audit Logging**
  - [ ] Failed login attempts logged
  - [ ] Privilege escalation logged
  - [ ] Password changes logged
  - [ ] Account deletion logged
  - [ ] API key usage logged

- [ ] **Log Security**
  - [ ] No sensitive data in logs
  - [ ] Structured logging (JSON)
  - [ ] Log rotation configured
  - [ ] Log retention: 90 days minimum
  - [ ] Logs encrypted at rest

**Sample Log Entry:**
```json
{
  "timestamp": "2025-11-09T10:30:00Z",
  "event": "failed_login",
  "severity": "warning",
  "user_id": "***redacted***",
  "email": "u***@example.com",  // Partially masked
  "ip_address": "192.168.1.***",  // Partially masked
  "reason": "invalid_password",
  "attempt_count": 3
}
```

---

### 6.2 Security Monitoring

- [ ] **Alerting**
  - [ ] Alert on 10+ failed logins/minute
  - [ ] Alert on SQL injection attempts
  - [ ] Alert on rate limit violations
  - [ ] Alert on unauthorized access attempts
  - [ ] Alert on unusual traffic patterns

- [ ] **Metrics**
  - [ ] Authentication success/failure rate
  - [ ] API error rate by code
  - [ ] Rate limit hit frequency
  - [ ] Average response time
  - [ ] Concurrent user count

---

## 🔍 7. OWASP Top 10 Compliance

See `OWASP_MAPPING.md` for detailed mapping.

- [ ] **A01: Broken Access Control**
  - [ ] JWT verification on protected endpoints
  - [ ] Resource ownership checks
  - [ ] Role-based access control (RBAC)

- [ ] **A02: Cryptographic Failures**
  - [ ] TLS 1.2+ enforced
  - [ ] Strong password hashing (bcrypt)
  - [ ] Secrets not in code

- [ ] **A03: Injection**
  - [ ] Parameterized queries only
  - [ ] Input validation on all endpoints
  - [ ] Output encoding

- [ ] **A04: Insecure Design**
  - [ ] Threat modeling completed
  - [ ] Secure development lifecycle
  - [ ] Security requirements defined

- [ ] **A05: Security Misconfiguration**
  - [ ] Default credentials changed
  - [ ] Debug mode disabled in production
  - [ ] Security headers configured

- [ ] **A06: Vulnerable Components**
  - [ ] Dependencies up to date
  - [ ] Vulnerability scanning automated
  - [ ] Patch management process

- [ ] **A07: Authentication Failures**
  - [ ] Strong password policy
  - [ ] Multi-factor authentication (future)
  - [ ] Session management secure

- [ ] **A08: Software/Data Integrity**
  - [ ] Code signing
  - [ ] Integrity checks for updates
  - [ ] CI/CD pipeline secured

- [ ] **A09: Logging/Monitoring Failures**
  - [ ] Comprehensive audit logs
  - [ ] Real-time monitoring
  - [ ] Incident response plan

- [ ] **A10: Server-Side Request Forgery**
  - [ ] URL validation for external requests
  - [ ] Whitelist for allowed domains
  - [ ] Network segmentation

---

## 🌍 8. Arabic-Specific Security

### 8.1 Unicode Security

- [ ] **Unicode Attacks**
  - [ ] Homograph attacks prevented
  - [ ] Bidirectional text attacks blocked
  - [ ] Zero-width character filtering
  - [ ] Unicode normalization enforced

- [ ] **RTL Injection**
  - [ ] RTL override characters stripped
  - [ ] Consistent text direction enforcement
  - [ ] Safe rendering in UI

**Test Cases:**
```python
# Homograph attack (Arabic + Latin lookalikes)
test_input = "аdmin"  # Cyrillic 'a' + Latin 'dmin'
# Should be rejected or normalized

# RTL injection
test_input = "admin\u202Enimda"  # Displays as "adminadmin"
# Should strip RTL override
```

---

### 8.2 Content Validation

- [ ] **Arabic Poetry Validation**
  - [ ] Verse length validation
  - [ ] Character set validation
  - [ ] Suspicious pattern detection
  - [ ] Spam/abuse detection

---

## ✅ Pre-Production Checklist

### Week Before Launch

- [ ] Full security audit completed
- [ ] Penetration testing conducted
- [ ] Vulnerability scan passed
- [ ] Security headers verified
- [ ] SSL/TLS configuration tested
- [ ] Rate limiting tested
- [ ] Incident response plan ready
- [ ] Security contacts documented
- [ ] Backup/restore tested
- [ ] Disaster recovery plan ready

### Launch Day

- [ ] Monitor error rates
- [ ] Monitor authentication failures
- [ ] Check security logs
- [ ] Verify rate limiting working
- [ ] Test rollback procedure
- [ ] Security team on standby

### Post-Launch (Week 1)

- [ ] Review security logs daily
- [ ] Monitor for anomalies
- [ ] Update security documentation
- [ ] Address any findings
- [ ] Schedule first security review

---

## 📅 Ongoing Security Maintenance

### Weekly
- [ ] Review failed authentication logs
- [ ] Check for unusual traffic patterns
- [ ] Monitor error rates

### Monthly
- [ ] Dependency updates
- [ ] Security patch review
- [ ] Access control review
- [ ] Log analysis

### Quarterly
- [ ] Full security audit
- [ ] Penetration testing
- [ ] Security training
- [ ] Policy review
- [ ] Incident response drill

### Annually
- [ ] Comprehensive security assessment
- [ ] Third-party security audit
- [ ] Compliance review
- [ ] Security roadmap update

---

## 🔗 Related Documentation

- `docs/technical/SECURITY.md` - Main security guide
- `docs/technical/OWASP_MAPPING.md` - OWASP Top 10 mapping
- `docs/technical/ERROR_HANDLING_STRATEGY.md` - Error codes
- `docs/technical/API_VERSIONING.md` - API security lifecycle
- `docs/workflows/DEVELOPMENT_WORKFLOW.md` - Secure development

---

## 📞 Security Contact

**For security issues:**
- Email: security@bahr.app
- PGP Key: [Link to public key]
- Bug Bounty: [If applicable]
- Response Time: 24-48 hours

**For emergencies:**
- On-call: [Phone number]
- Escalation: [Manager contact]

---

**Checklist Version:** 1.0  
**Last Updated:** November 9, 2025  
**Next Review:** December 9, 2025  
**Owner:** Security Team
