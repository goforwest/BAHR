# 📘 API Versioning & Deprecation Policy
## Maintaining Backward Compatibility for BAHR API

**Last Updated:** November 9, 2025  
**Status:** Active Policy  
**Applies to:** All public API endpoints

---

## 📋 Overview

This document defines how the BAHR API handles versioning, breaking changes, and deprecations to ensure:
- **Stability** for existing clients
- **Forward compatibility** for new features
- **Clear migration paths** during deprecations
- **Transparent communication** of changes

---

## 🔢 Versioning Strategy

### URL-Based Versioning

All API endpoints include version in the URL path:

```
https://api.bahr.app/api/v1/analyze
                        ^^^
                      Version
```

**Format:** `/api/v{major}/...`

**Current version:** `v1`

---

### Version Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    API Version Lifecycle                    │
└─────────────────────────────────────────────────────────────┘

v1 (Current)
├── 📅 Released: November 2025
├── 🟢 Status: Stable
├── 🔒 Support: Minimum 24 months
└── 📆 EOL: November 2027 (earliest)

v2 (Future)
├── 📅 Planned: Q3 2026
├── 🟡 Status: Draft
├── 🔄 Changes: Breaking changes from v1
└── 📝 Migration guide: To be published

Deprecation Timeline:
v1 → v2 migration period: 6 months minimum
```

---

## 📏 Versioning Rules

### What Requires a New Major Version (v1 → v2)?

**Breaking changes:**
- ❌ Removing endpoints
- ❌ Removing request/response fields
- ❌ Changing field types (string → number)
- ❌ Changing authentication mechanisms
- ❌ Changing URL structure (beyond `/api/v1/`)
- ❌ Changing response envelope structure
- ❌ Renaming fields (without aliases)

**Example:**
```json
// v1 Response
{
  "data": {
    "detected_meter": "الطويل"
  }
}

// v2 Response (Breaking - field renamed)
{
  "data": {
    "meter": "الطويل"  // ❌ Breaking change
  }
}
```

---

### What Can Be Done Without New Version?

**Non-breaking changes:**
- ✅ Adding new endpoints
- ✅ Adding optional fields to requests
- ✅ Adding new fields to responses
- ✅ Adding new optional query parameters
- ✅ Expanding enum values
- ✅ Making required fields optional
- ✅ Relaxing validation rules

**Example:**
```json
// v1 Response (original)
{
  "data": {
    "detected_meter": "الطويل",
    "confidence": 0.92
  }
}

// v1 Response (enhanced - not breaking)
{
  "data": {
    "detected_meter": "الطويل",
    "confidence": 0.92,
    "quality_score": 0.88  // ✅ New field added
  }
}
```

---

## 🗓️ Deprecation Process

### Deprecation Timeline

```
Month 0: Deprecation Announced
  ↓
  ├── Add deprecation headers
  ├── Update documentation
  └── Notify users via email/blog

Month 1-3: Warning Period
  ↓
  ├── Deprecation warnings in responses
  ├── Dashboard notifications
  └── Migration guide published

Month 4-6: Sunset Period
  ↓
  ├── Increase warning frequency
  ├── Direct outreach to heavy users
  └── Final reminder (30 days before EOL)

Month 6: End of Life (EOL)
  ↓
  └── Feature/endpoint removed
```

---

### Deprecation Headers

Deprecated endpoints will include special headers:

```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 01 Jun 2026 00:00:00 GMT
Link: <https://docs.bahr.app/api/migration-v2>; rel="alternate"
X-API-Warn: This endpoint is deprecated and will be removed on 2026-06-01
```

**Header Definitions:**
- `Deprecation`: Indicates the feature is deprecated
- `Sunset`: RFC 8594 header with exact EOL date
- `Link`: URL to migration guide
- `X-API-Warn`: Human-readable warning message

---

### Deprecation Response Format

Deprecated endpoints also include warnings in the response body:

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "request_id": "abc-123",
    "timestamp": "2026-01-15T10:30:00Z"
  },
  "warnings": [
    {
      "code": "DEPRECATED_ENDPOINT",
      "message": "This endpoint is deprecated and will be removed on 2026-06-01",
      "severity": "warning",
      "details": {
        "sunset_date": "2026-06-01",
        "replacement": "/api/v2/analyze",
        "migration_guide": "https://docs.bahr.app/api/migration-v2"
      }
    }
  ]
}
```

---

## 📝 Change Categories

### 1. Backward Compatible (Patch/Minor)

**Can be deployed immediately:**
- Bug fixes
- Performance improvements
- New optional features
- Documentation updates
- Internal refactoring

**Versioning:** No version bump required (v1 stays v1)

---

### 2. Backward Incompatible (Major)

**Requires new major version:**
- Removing endpoints
- Changing response structures
- Modifying authentication
- Altering error codes

**Versioning:** v1 → v2

---

### 3. Experimental Features

**Beta endpoints:**
- Prefix: `/api/beta/...`
- No stability guarantees
- Can change without notice
- Not recommended for production use

```http
GET /api/beta/ai-generate
X-Beta-Feature: true
```

**Example use case:** AI poetry generation (Phase 2)

---

## 🔔 Communication Channels

### How Users Are Notified

1. **API Response Headers** (immediate, every request)
   - `Deprecation` header
   - `X-API-Warn` messages

2. **Developer Dashboard** (login required)
   - Usage analytics
   - Deprecation warnings
   - Migration checklist

3. **Email Notifications** (to registered users)
   - 6 months before EOL
   - 3 months before EOL
   - 1 month before EOL
   - 1 week before EOL

4. **Documentation** (public)
   - Changelog: `https://docs.bahr.app/changelog`
   - Migration guides
   - API status page

5. **Blog Posts** (major changes only)
   - Announcement of new versions
   - Deprecation notices
   - Migration tutorials

---

## 📚 Migration Guides

### Structure of Migration Guides

Each major version migration will include:

```markdown
# Migration Guide: v1 → v2

## Overview
- Timeline: 6 months (Jan 2026 - Jun 2026)
- Breaking changes: 5 endpoints affected
- Effort: ~2-4 hours for typical integration

## Breaking Changes

### 1. Meter Detection Response Structure
**Old (v1):**
{
  "detected_meter": "الطويل",
  "meter_confidence": 0.92
}

**New (v2):**
{
  "meter": {
    "name": "الطويل",
    "confidence": 0.92,
    "alternatives": [...]
  }
}

**Migration:**
- Update field reference: `detected_meter` → `meter.name`
- Update confidence: `meter_confidence` → `meter.confidence`

## Code Examples
[Python, JavaScript, etc.]

## Testing Checklist
- [ ] Update API base URL
- [ ] Run integration tests
- [ ] Verify error handling
```

---

## 🔍 API Status Page

### Public Status Dashboard

**URL:** `https://status.bahr.app/api`

**Shows:**
- Current API version
- Uptime statistics
- Planned deprecations
- Incident history

**Example:**
```
API Status Dashboard

Current Version: v1
Status: ✅ Operational
Uptime (30d): 99.95%

Upcoming Changes:
⚠️ /api/v1/analyze - Deprecated (EOL: 2026-06-01)
   Replacement: /api/v2/analyze
   Migration guide: [Link]

Recent Incidents:
None in the past 30 days
```

---

## 🛡️ Versioning for Error Codes

Error codes remain stable within a major version:

```json
// v1 Errors
{
  "error": {
    "code": "ERR_INPUT_001",  // Stable in v1
    "message": "..."
  }
}

// v2 Errors (can add new codes, but not change existing)
{
  "error": {
    "code": "ERR_INPUT_001",  // Same meaning as v1
    "message": "..."
  }
}
```

**Rule:** Error codes are part of the API contract and cannot change meaning within a version.

---

## 📊 Version Support Matrix

| Version | Released | Support Status | EOL Date | Recommended For |
|---------|----------|----------------|----------|-----------------|
| v1 | Nov 2025 | ✅ Full Support | Nov 2027+ | Production |
| v2 | (Planned Q3 2026) | 🚧 Development | TBD | Future |
| beta | N/A | ⚠️ Experimental | N/A | Testing only |

**Support levels:**
- **Full Support:** Bug fixes, security patches, new features
- **Security Only:** Critical security patches only
- **Deprecated:** No updates, EOL announced
- **EOL:** Removed from service

---

## 🔐 Security Patches

Security vulnerabilities are patched across **all supported versions**:

```
v1.0.0 → v1.0.1 (security patch)
v1.1.0 → v1.1.1 (security patch)

Timeline:
- Critical: 24-48 hours
- High: 1 week
- Medium/Low: Next release cycle
```

Users are notified via:
- Security advisory email
- Status page notification
- GitHub security advisory

---

## ✅ Checklist for Version Changes

### Before Releasing v2:

- [ ] Document all breaking changes
- [ ] Create comprehensive migration guide
- [ ] Announce deprecation 6 months in advance
- [ ] Add deprecation headers to v1 endpoints
- [ ] Set up v1 → v2 redirect support (optional)
- [ ] Update API documentation
- [ ] Create code examples for v2
- [ ] Test backward compatibility tools
- [ ] Prepare customer communication
- [ ] Update SDKs and client libraries

### During Migration Period:

- [ ] Monitor v1 usage analytics
- [ ] Reach out to high-volume users
- [ ] Provide migration assistance
- [ ] Update deprecation timeline if needed
- [ ] Send reminder emails (3 months, 1 month, 1 week)

### After v2 Launch:

- [ ] Monitor v2 adoption rate
- [ ] Address v2 bug reports promptly
- [ ] Continue supporting v1 until EOL
- [ ] Archive v1 documentation (don't delete)
- [ ] Celebrate! 🎉

---

## 🔗 Related Documentation

- `API_SPECIFICATION.yaml` - Full API reference
- `ERROR_HANDLING_STRATEGY.md` - Error code taxonomy
- `ARCHITECTURE_OVERVIEW.md` - System design
- `API_CONVENTIONS.md` - Response envelope standards

---

## 📞 Questions?

**For API versioning questions:**
- Email: api-support@bahr.app
- Documentation: https://docs.bahr.app/api/versioning
- GitHub Discussions: https://github.com/your-org/BAHR/discussions

---

**Policy Version:** 1.0  
**Last Reviewed:** November 9, 2025  
**Next Review:** May 2026
