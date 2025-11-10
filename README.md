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
pip install -r requirements.txt
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
│   └── tests/            # Backend tests
├── dataset/               # Golden dataset & scripts
│   ├── evaluation/       # Test verses
│   └── scripts/          # Data processing
├── docs/                  # Complete documentation
│   ├── technical/        # API specs, architecture
│   ├── planning/         # Timeline, assumptions
│   └── research/         # NLP research, datasets
└── implementation-guides/ # Step-by-step guides
```

---

## 📖 Documentation

### 🎯 Getting Started
- [📘 Quick Start Guide](QUICK_START_GUIDE.md)
- [👨‍💻 Developer Guide](docs/START_HERE_DEVELOPER.md)
- [🗺️ Project Overview](docs/START_HERE.md)

### 🛠️ Technical
- [🏛️ Architecture Overview](docs/technical/ARCHITECTURE_OVERVIEW.md)
- [🔌 API Specification](docs/technical/API_SPECIFICATION.yaml)
- [🗄️ Database Schema](docs/technical/DATABASE_SCHEMA.md)
- [🎯 Prosody Engine](docs/technical/PROSODY_ENGINE.md)

### 📋 Planning
- [📅 Project Timeline](docs/planning/PROJECT_TIMELINE.md)
- [✅ Week 1 Checklist](docs/WEEK_1_CRITICAL_CHECKLIST.md)
- [🎯 Implementation Plan](IMPLEMENTATION_PLAN_FOR_CODEX.md)

---

## 🎯 Current Status

**Phase:** Phase 0 Complete ✅ → Week 1 Starting 🚀  
**Progress:** 60% (Documentation + Frontend Complete)

### ✅ Completed
- [x] Complete technical documentation (40+ files)
- [x] Next.js 16 frontend with RTL + Arabic fonts
- [x] Golden dataset v0.20 (42 annotated verses)
- [x] FastAPI backend structure
- [x] Docker Compose configuration
- [x] CI/CD workflows (GitHub Actions)

### 🔄 In Progress
- [ ] Backend API implementation (Week 1)
- [ ] CAMeL Tools integration
- [ ] Meter detection algorithm
- [ ] Database setup with Alembic

### 📅 Upcoming
- [ ] Frontend-Backend integration (Week 2)
- [ ] Authentication & user management
- [ ] Production deployment
- [ ] Performance optimization

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
