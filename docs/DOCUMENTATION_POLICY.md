# 📖 Documentation Policy

**BAHR Project Documentation Standards & Guidelines**  
**Version:** 1.0  
**Status:** 🎯 Active  
**Last Updated:** 2025-11-10  
**Audience:** All Contributors

---

## Purpose

This document establishes standards, guidelines, and requirements for all documentation in the BAHR project to ensure:
- **Consistency** across all documentation
- **Discoverability** of information
- **Maintainability** over time
- **Quality** that serves users effectively

---

## Documentation Principles

### 1. Single Source of Truth
- Each topic should be documented in **exactly one place**
- Cross-reference rather than duplicate
- When consolidating, archive the old version

### 2. Documentation as Code
- Documentation lives with the code
- Documentation changes require pull requests
- Documentation is versioned alongside code
- Documentation is reviewed like code

### 3. Accuracy Over Perfection
- **Better to have accurate draft docs** than perfect but outdated docs
- Update documentation immediately when code changes
- Mark uncertain information with "TODO" or "VERIFY"

### 4. User-Centric Writing
- Write for the **audience** (new developers, architects, operators)
- Provide **context** before details
- Include **examples** and **use cases**
- Answer "why" not just "what"

---

## Metadata Standards

### Required Frontmatter

All documentation files MUST include YAML frontmatter with these fields:

```yaml
---
title: "Document Title"
category: "vision|architecture|implementation|technical|operations|planning|research"
status: "active|draft|deprecated|archived"
version: "X.Y"
last_updated: "YYYY-MM-DD"
audience: "developers|architects|stakeholders|operators|all"
---
```

### Optional Frontmatter

```yaml
---
author: "Team Name or Person"
related_docs:
  - ../path/to/related1.md
  - ../path/to/related2.md
supersedes: "../path/to/old-doc.md"
tags: ["api", "security", "deployment"]
---
```

### Metadata Definitions

#### Category
- **vision:** Strategic direction, long-term plans, product vision
- **architecture:** System design, architectural decisions, diagrams
- **implementation:** How-to guides, feature documentation
- **technical:** Technical specifications, API references
- **operations:** Deployment, DevOps, monitoring, troubleshooting
- **planning:** Roadmaps, timelines, project management
- **research:** Research findings, external resources, datasets

#### Status
- **active:** Current, maintained, authoritative
- **draft:** Work in progress, not yet complete
- **deprecated:** Superseded but not yet archived
- **archived:** Historical, read-only, no longer maintained

#### Audience
- **developers:** Software engineers implementing features
- **architects:** Technical leads making architectural decisions
- **stakeholders:** Project managers, product owners
- **operators:** DevOps, SRE, production support
- **all:** General audience, onboarding documentation

---

## File Naming Conventions

### General Rules
- Use **SCREAMING_SNAKE_CASE** for documentation files
- Use **kebab-case** for subdirectories
- Be descriptive but concise
- Avoid abbreviations unless widely understood

### Examples
✅ **Good:**
- `DEPLOYMENT_STRATEGY.md`
- `API_CONVENTIONS.md`
- `GETTING_STARTED.md`
- `feature-authentication-jwt.md`

❌ **Avoid:**
- `deploy.md` (too generic)
- `api_stuff.md` (vague)
- `GettingStarted.md` (wrong case)
- `feat-auth.md` (unclear abbreviation)

### Special Files
- `README.md` - Folder index/overview (every subdirectory should have one)
- `CHANGELOG.md` - Version history (root only)
- `INDEX.md` - Cross-reference index (when needed)

---

## Document Structure

### Required Sections

Every documentation file SHOULD include:

1. **Title** (H1 - one per document)
2. **Metadata** (YAML frontmatter)
3. **Purpose/Overview** - What this doc covers
4. **Table of Contents** (for docs >300 lines)
5. **Main Content**
6. **Related Documentation** - Links to related docs
7. **Last Updated Footer** (if not in metadata)

### Optional Sections
- Prerequisites
- Quick Start / TL;DR
- Examples
- Troubleshooting
- FAQ
- Contributing
- License/Copyright

### Document Template

```markdown
---
title: "Your Document Title"
category: "technical"
status: "active"
version: "1.0"
last_updated: "YYYY-MM-DD"
audience: "developers"
---

# Document Title

**Brief Description:** One-sentence summary of what this document covers.

---

## Purpose

Explain why this documentation exists and what problem it solves.

---

## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)

---

## Section 1

Main content here...

---

## Related Documentation

- [Related Doc 1](../path/to/doc1.md)
- [Related Doc 2](../path/to/doc2.md)

---

**Last Updated:** YYYY-MM-DD  
**Maintained By:** Team Name
```

---

## Content Guidelines

### Writing Style

#### Tone
- **Professional** but approachable
- **Clear** and concise
- **Active voice** preferred over passive
- **Direct** second-person ("you") for guides

#### Language
- **English** for all technical documentation
- **Arabic** for user-facing content and vision documents (with English translations)
- Consistent terminology across all docs
- Define acronyms on first use

### Formatting

#### Headings
- Use **semantic heading hierarchy**
- Don't skip levels (H1 → H2 → H3, not H1 → H3)
- Keep headings descriptive and scannable
- Use sentence case, not title case

```markdown
✅ Good:
# Main title (H1)
## Major section (H2)
### Subsection (H3)

❌ Bad:
# Main Title (Title Case - avoid)
### Subsection (skipped H2)
```

#### Lists
- Use **numbered lists** for sequential steps
- Use **bullet lists** for non-sequential items
- Keep list items parallel in structure
- Use sub-lists sparingly

#### Code Blocks
- Always specify **language** for syntax highlighting
- Include **context** before code (what it does)
- Keep examples **minimal** but complete
- Use **comments** to explain complex parts

```markdown
✅ Good:
The following Python code detects meter:

\`\`\`python
def detect_meter(verse: str) -> str:
    """Detect Arabic poetry meter."""
    # Normalize and segment first
    syllables = segment(normalize(verse))
    return match_meter(syllables)
\`\`\`

❌ Bad:
\`\`\`
code here with no language specified
\`\`\`
```

#### Tables
- Use tables for **structured data** (comparisons, specs, matrices)
- Keep tables **simple** (avoid complex merged cells)
- Always include **header row**
- Consider alternatives for very wide tables

#### Links
- Use **descriptive link text** (not "click here")
- Prefer **relative paths** for internal links
- Verify links work before committing
- Link to **specific sections** with anchors when helpful

```markdown
✅ Good:
See the [deployment guide](../deployment/RAILWAY_COMPLETE_GUIDE.md) for details.

❌ Bad:
Click [here](../deployment/RAILWAY_COMPLETE_GUIDE.md) to learn more.
```

#### Emphasis
- **Bold** for important terms, UI elements
- *Italic* for emphasis, first use of terms
- `Code font` for code, filenames, commands
- Avoid ALL CAPS except for acronyms

---

## Documentation Requirements

### For Code Changes

When submitting a pull request that changes code:

#### MUST Update
- API documentation if endpoints change
- Configuration documentation if settings change
- Deployment documentation if deployment process changes
- Feature documentation if feature behavior changes

#### SHOULD Update
- Architecture documentation if design changes
- Performance documentation if benchmarks change
- Security documentation if security model changes
- Examples if code examples become outdated

### For New Features

When adding a new feature:

#### MUST Create
- Feature implementation guide in `/docs/features/`
- API documentation if adds endpoints
- User-facing documentation for how to use the feature

#### SHOULD Create
- Architecture Decision Record (ADR) for significant design choices
- Testing documentation for test strategy
- Migration guide if requires user action

### For Deprecations

When deprecating features:

#### MUST Do
- Mark documentation as `deprecated` in metadata
- Add deprecation notice to top of document
- Link to replacement/alternative
- Update CHANGELOG.md

#### Example Deprecation Notice
```markdown
> **⚠️ DEPRECATED:** This feature is deprecated as of v0.5.0 and will be removed in v1.0.0.  
> Please use [New Feature](./NEW_FEATURE.md) instead.
```

---

## Review Process

### Documentation Pull Requests

All documentation changes MUST:
1. **Pass automated checks:**
   - Link validation
   - Metadata validation
   - Spell check (if enabled)

2. **Include:**
   - Clear description of changes
   - Reason for changes
   - Update to relevant changelogs

3. **Be reviewed for:**
   - Accuracy (does it match the code?)
   - Clarity (will readers understand?)
   - Completeness (covers all necessary information?)
   - Consistency (follows documentation standards?)

### Review Checklist

Reviewers should verify:
- [ ] Metadata is present and correct
- [ ] Links work and point to correct targets
- [ ] Code examples are accurate and runnable
- [ ] Grammar and spelling are correct
- [ ] Formatting follows guidelines
- [ ] Content is appropriate for audience
- [ ] Related documentation is updated
- [ ] Changelog is updated (if appropriate)

---

## Changelog Requirements

### When to Update CHANGELOG.md

Update `/CHANGELOG.md` when:
- **Adding** a new feature
- **Changing** existing functionality
- **Deprecating** a feature
- **Removing** a feature
- **Fixing** a significant bug
- **Updating** a dependency with user impact

### Changelog Format

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [Version] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Features marked for removal

### Removed
- Features that were removed

### Fixed
- Bug fixes

### Security
- Security fixes or improvements
```

### Documentation Changelogs

For documentation-specific changes:
- **Structure changes** → `/docs/tracking/DOCUMENTATION_CHANGELOG.md`
- **Content improvements** → `/docs/tracking/REVIEW_INTEGRATION_CHANGELOG.md`

---

## Archival Policy

### When to Archive

Archive documentation when:
- **Superseded** by newer version
- **Feature removed** from codebase
- **Project phase complete** (e.g., restructuring docs)
- **No longer referenced** by active docs
- **Historical value** but not actively maintained

### Archival Process

1. **Move** file to appropriate `/archive/` subfolder
2. **Add notice** to top of archived file:
   ```markdown
   > **🗄️ ARCHIVED:** This document is archived and no longer maintained.  
   > For current information, see [Current Doc](../docs/current-doc.md).  
   > **Archived:** YYYY-MM-DD
   ```
3. **Update** archive folder README
4. **Update** any references to point to current alternative
5. **Update** metadata:
   - `status: "archived"`
   - Add `archived_date: "YYYY-MM-DD"`

### Archive Organization

```
archive/
├── milestones/       # Completed milestone summaries
├── progress/         # Historical progress logs
├── implementation/   # Feature implementation summaries
├── reviews/          # Audit and review reports
├── deployment/       # Old deployment guides
├── restructuring/    # Repository restructuring docs
└── [other]/          # Category-specific archives
```

---

## Maintenance Schedule

### Daily
- Fix broken links reported by automation
- Update progress logs

### Weekly
- Review pull requests for documentation
- Automated link validation (GitHub Actions)

### Monthly
- Complete [Maintenance Checklist](./MAINTENANCE_CHECKLIST.md)
- Archive old progress log entries
- Update navigation and indexes

### Quarterly
- Documentation mini-audit
- Team feedback survey
- Update documentation standards if needed

### Annually
- Comprehensive documentation audit
- Archive previous year's progress logs
- Update multi-year vision documents

---

## Quality Metrics

### Documentation Health Indicators

Track these metrics:
- **Coverage:** % of features with documentation
- **Freshness:** % of docs updated in last 3 months
- **Accuracy:** Number of documentation bugs reported
- **Usefulness:** Team satisfaction with documentation
- **Discoverability:** Time to find needed information

### Target Metrics
- Coverage: >90%
- Freshness: >75%
- Broken Links: 0
- Documentation Debt: <10 outdated docs

---

## Tools & Automation

### Recommended Tools
- **Linter:** markdownlint for formatting
- **Link Checker:** markdown-link-check
- **Spell Checker:** cspell or aspell
- **Diagram Tool:** Mermaid.js (embedded in markdown)
- **API Docs:** OpenAPI/Swagger for REST APIs

### GitHub Actions
- Weekly link validation
- PR metadata validation
- Spell checking on PR (future)
- Documentation coverage reporting (future)

---

## Exceptions & Flexibility

### When to Deviate

This policy provides **guidelines, not rigid rules**. Deviate when:
- **Specific context** requires it
- **User needs** are better served differently
- **Standards evolve** and policy hasn't caught up

### How to Request Exception
1. Discuss in pull request or issue
2. Document reason for deviation
3. Update policy if pattern emerges

---

## Related Resources

- [Maintenance Checklist](./MAINTENANCE_CHECKLIST.md)
- [Documentation Quick Reference](./DOCUMENTATION_QUICK_REFERENCE.md)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Write the Docs](https://www.writethedocs.org/)

---

## Policy Updates

This policy is a living document. Updates should:
1. Be proposed via pull request
2. Include rationale for change
3. Be reviewed by team
4. Be announced to all contributors
5. Update `last_updated` and `version`

---

**Created:** November 10, 2025  
**Last Updated:** November 10, 2025  
**Version:** 1.0  
**Maintained By:** BAHR Documentation Team  
**Review Cycle:** Quarterly
