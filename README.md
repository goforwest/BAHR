# بَحْر (BAHR) - Arabic Poetry Analysis Platform

<div align="center">

![BAHR Logo](https://img.shields.io/badge/بَحْر-BAHR-blue?style=for-the-badge)

**نظام ذكي لتحليل الشعر العربي**  
*Intelligent Arabic Poetry Analysis System*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Backend CI](https://github.com/goforwest/BAHR/actions/workflows/backend.yml/badge.svg)](https://github.com/goforwest/BAHR/actions/workflows/backend.yml)
[![Frontend CI](https://github.com/goforwest/BAHR/actions/workflows/frontend.yml/badge.svg)](https://github.com/goforwest/BAHR/actions/workflows/frontend.yml)
[![Deploy](https://github.com/goforwest/BAHR/actions/workflows/deploy.yml/badge.svg)](https://github.com/goforwest/BAHR/actions/workflows/deploy.yml)

[![Next.js](https://img.shields.io/badge/Next.js-16.0-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?logo=typescript)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-v4-38B2AC?logo=tailwind-css)](https://tailwindcss.com/)

[English](#english) | [العربية](#arabic)

</div>

---

## 🌟 Overview

**BAHR** (بَحْر, meaning "sea" or "meter" in Arabic) is a comprehensive platform for analyzing and understanding Arabic classical poetry through advanced NLP techniques and prosodic analysis.

### ✨ Key Features

- 🎼 **Meter Detection** - Automatic identification of Arabic poetic meters (البحور)
- 📊 **Syllable Segmentation** - Precise prosodic analysis using CAMeL Tools
- ✨ **Rhyme Analysis** - Pattern extraction and validation
- 🌐 **RTL-First UI** - Beautiful Arabic-first interface with Next.js 16
- 🔍 **Real-time Analysis** - Instant feedback on poetry structure
- 📚 **Golden Dataset** - 42 annotated classical verses for testing

---

## 🚀 Quick Start

### Frontend (Next.js 16)

```bash
cd frontend
npm install
npm run dev
```

Visit: http://localhost:3000

### Backend (FastAPI) - Coming Week 1

```bash
cd backend
# Development environment (includes testing tools)
pip install -r requirements/development.txt

# Or for production
pip install -r requirements/production.txt

# Start server
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

---

## 🏗️ Tech Stack

### Frontend
- **Framework:** Next.js 16.0.1 with App Router
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS v4
- **Components:** shadcn/ui (New York style)
- **Fonts:** Cairo (UI) + Amiri (poetry) via `next/font/google`
- **RTL:** Native `dir="rtl"` support

### Backend
- **Framework:** FastAPI 0.115+
- **Language:** Python 3.11+
- **NLP:** CAMeL Tools for Arabic processing
- **Database:** PostgreSQL 15+ with SQLAlchemy
- **Cache:** Redis 7+
- **Migration:** Alembic

### DevOps
- **Containerization:** Docker + Docker Compose
- **CI/CD:** GitHub Actions
- **Deployment:** Railway (backend) + Vercel (frontend)

---

## 📂 Project Structure

```
BAHR/
├── frontend/              # Next.js 16 frontend
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   └── lib/          # Utilities
│   └── components/        # React components
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # Database models
│   │   ├── prosody/      # Prosody engine
│   │   └── nlp/          # NLP utilities
│   ├── database/
│   │   └── migrations/   # Alembic migrations
│   ├── scripts/          # Database seeding
│   └── tests/            # Backend tests
├── dataset/               # Golden dataset & scripts
│   ├── evaluation/       # Test verses
│   └── scripts/          # Data processing
├── infrastructure/        # Deployment & DevOps
│   ├── docker/           # Docker configs
│   └── railway/          # Railway configs
├── docs/                  # Complete documentation
│   ├── architecture/     # Architecture decisions
│   ├── features/         # Implementation guides
│   ├── technical/        # API specs
│   └── planning/         # Timeline, roadmap
└── scripts/               # Development scripts
    ├── setup/            # Environment setup
    ├── health/           # Health checks
    └── testing/          # Test utilities
```

---

## 📖 Documentation

> **Note:** Documentation was reorganized on November 10, 2025 for better organization. See [Documentation Guide](docs/README.md) for the complete structure.

### 🎯 Quick Links
- 🌟 **Vision & Strategy:** [Master Plan](docs/vision/MASTER_PLAN.md) - Long-term vision and product roadmap
- 🚀 **Get Started:** [Developer Onboarding](docs/onboarding/docs/onboarding/GETTING_STARTED.md) - **START HERE!** Complete setup guide
- 📋 **Current Progress:** [Progress Log](docs/project-management/PROGRESS_LOG_CURRENT.md) - Recent updates and achievements
- 🎯 **Implementation Plan:** [Roadmap](docs/planning/IMPLEMENTATION_ROADMAP.md) - Current implementation plan (v2.0)
- �️ **Architecture:** [Technical Docs](docs/technical/) - API specs, database schema, architecture decisions
- 📖 **Feature Guides:** [Implementation Guides](docs/features/) - Step-by-step feature implementation

### 📂 Documentation Categories
- **Vision:** Long-term goals, product strategy ([/docs/vision/](docs/vision/))
- **Onboarding:** Getting started, development setup ([/docs/onboarding/](docs/onboarding/))
- **Guides:** Quick reference, how-to guides ([/docs/guides/](docs/guides/))
- **Planning:** Timeline, roadmap, assumptions ([/docs/planning/](docs/planning/))
- **Technical:** Architecture, API, database ([/docs/technical/](docs/technical/))
- **Checklists:** Week/phase task lists ([/docs/checklists/](docs/checklists/))
- **DevOps:** CI/CD, deployment guides ([/docs/devops/](docs/devops/))
- **Archive:** Historical milestones, reviews ([/archive/](archive/))

> **📋 November 10, 2025 Update:** Documentation reorganized for better structure.  
> See [DOCUMENTATION_REORGANIZATION_CHANGELOG.md](docs/DOCUMENTATION_REORGANIZATION_CHANGELOG.md) for file migration map.

### 📚 Key Resources
- [📖 Complete Documentation Index](docs/README.md) - Full navigation guide
- [🔍 Quick Start: Analyze Endpoint](docs/guides/ANALYZE_ENDPOINT_QUICKSTART.md) - API usage guide
- [✅ Week 1 Critical Checklist](docs/checklists/WEEK_1_CRITICAL.md) - Week 1 tasks
- [🗂️ Historical Archive](archive/README.md) - Past milestones and reports

---

## 🎯 Current Status

**Phase:** Phase 0 ✅ COMPLETE + Phase 1 Week 1-2 ✅ COMPLETE  
**Progress:** 95% (All core components implemented and tested)

### ✅ Completed
- [x] Complete technical documentation (40+ files)
- [x] Next.js 16 frontend with RTL + Arabic fonts
- [x] Golden dataset v0.20 (52 annotated verses)
- [x] FastAPI backend with CORS middleware
- [x] Docker Compose configuration (PostgreSQL + Redis)
- [x] CI/CD workflows (GitHub Actions)
- [x] **Prosody Engine Core (Week 1-2)**
  - [x] Text normalization with CAMeL Tools
  - [x] Phonetic analysis (CV pattern extraction)
  - [x] Taqti3 algorithm (syllable segmentation)
  - [x] Bahr detection (4 meters: الطويل، الكامل، الرمل، الوافر)
  - [x] **98.1% accuracy on test dataset** ✅ (exceeds 90% target)
- [x] **Database & Infrastructure**
  - [x] Alembic migrations with 8 performance indexes
  - [x] 16 Arabic meters + 8 prosodic feet seeded
  - [x] PostgreSQL 15 running in Docker
- [x] **Testing & Quality**
  - [x] 220 passing tests
  - [x] 99% code coverage
  - [x] Accuracy test suite with golden dataset
- [x] **Production Readiness (Week 0)**
  - [x] Railway CLI installed
  - [x] CORS policy configured
  - [x] Database indexes documented (ADR-002)

### � In Progress
- [ ] Railway project setup (CLI ready, need to create project)
- [ ] API endpoints implementation (Week 2)
- [ ] Frontend-Backend integration

### 📅 Upcoming
- [ ] Production deployment to Railway + Vercel
- [ ] Authentication & user management
- [ ] Performance optimization

---

## 🛠️ Developer Productivity

### Shell Aliases (Optional but Recommended)

BAHR includes a comprehensive set of shell aliases for common development tasks. To use them:

```bash
# Add to your ~/.zshrc
source /Users/YOUR_USERNAME/Desktop/Personal/BAHR/.bahr_aliases.sh

# Reload shell
source ~/.zshrc
```

**Available commands:**
- `bahr-help` - Show all available commands
- `bahr-setup` - Complete environment setup
- `bahr-start/stop/restart` - Manage Docker services
- `bahr-migrate` - Run database migrations
- `bahr-test` - Run tests with coverage
- `bahr-backend/frontend` - Start development servers
- Plus 30+ more utilities for navigation, testing, and database management

See the full command list by running `bahr-help` after sourcing the aliases file.

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/BAHR.git
cd BAHR

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make changes and test
npm test          # Frontend tests
pytest            # Backend tests

# 4. Commit and push
git commit -m "feat: add your feature"
git push origin feature/your-feature-name

# 5. Create Pull Request
```

---

## 📊 Dataset

The project includes a **Golden Dataset** of 42 manually annotated classical Arabic verses:

- ✅ Schema-validated JSONL format
- ✅ Prosodic annotations (meters, feet, rhymes)
- ✅ Metadata (poet, era, source)
- ✅ Quality assurance reports

See [dataset/evaluation/README.md](dataset/evaluation/README.md)

---

## 🔐 Security

- 🔒 JWT-based authentication
- 🛡️ OWASP Top 10 compliance
- 🔐 Secrets management via Railway/Vercel
- 🚫 Rate limiting & DDoS protection

See [docs/technical/SECURITY.md](docs/technical/SECURITY.md)

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **CAMeL Tools** - Arabic NLP toolkit
- **shadcn/ui** - Beautiful UI components
- **Next.js Team** - Amazing React framework
- **FastAPI** - High-performance Python framework

---

## 📞 Contact & Support

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/goforwest/BAHR/issues)
- **Discussions:** [GitHub Discussions](https://github.com/goforwest/BAHR/discussions)

---

<div align="center">

**Built with ❤️ for Arabic Poetry Enthusiasts**

[⭐ Star us on GitHub](https://github.com/goforwest/BAHR) | [📖 Read the Docs](docs/) | [🐛 Report Bug](https://github.com/goforwest/BAHR/issues)

</div>

---

<div id="arabic"></div>

## 🇸🇦 النسخة العربية

### نظرة عامة

**بَحْر** هو منصة شاملة لتحليل وفهم الشعر العربي الكلاسيكي من خلال تقنيات معالجة اللغات الطبيعية المتقدمة والتحليل العروضي.

### المميزات الرئيسية

- 🎼 **كشف البحور الشعرية** - تحديد تلقائي للأوزان العروضية
- 📊 **التقطيع العروضي** - تحليل دقيق للمقاطع الصوتية
- ✨ **تحليل القوافي** - استخراج والتحقق من أنماط القافية
- 🌐 **واجهة عربية أصيلة** - تصميم جميل يدعم العربية بالكامل
- 🔍 **تحليل فوري** - ردود فعل مباشرة على بنية القصيدة
- 📚 **مجموعة بيانات ذهبية** - 42 بيتًا كلاسيكيًا مُشَرَّحًا

### البدء السريع

```bash
# الواجهة الأمامية
cd frontend && npm install && npm run dev

# الخلفية (قريبًا)
cd backend && pip install -r requirements.txt
```

### الحالة الحالية

**المرحلة:** المرحلة 0 مكتملة ✅  
**التقدم:** 60%

- ✅ التوثيق الكامل
- ✅ الواجهة الأمامية (Next.js 16)
- ✅ مجموعة البيانات الذهبية
- 🔄 تطوير الخلفية (الأسبوع 1)

---

**صُنع بحب ❤️ لعشاق الشعر العربي**
