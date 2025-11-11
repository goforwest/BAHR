# Feature: Database ORM (PostgreSQL + SQLAlchemy) - Implementation Guide

**Feature ID:** `feature-database-orm`  
**Status:** Production-Ready  
**Last Updated:** November 8, 2025  
**Estimated Implementation Time:** 14-18 hours

---

## 1. Objective & Description

### What
Implement PostgreSQL database schema with SQLAlchemy ORM models and Alembic migrations. Define tables for users, analyses, meters, and relationships with proper indexing, constraints, and Arabic text support.

### Why
- **Data Persistence:** Store analysis results and user data
- **Relational Integrity:** Enforce foreign keys and constraints
- **Performance:** Optimized indexes for Arabic full-text search
- **Migration Management:** Track schema changes with Alembic
- **Type Safety:** Pydantic integration for validation

### Success Criteria
- ✅ Define 5 core tables (users, analyses, meters, user_profiles, analysis_history)
- ✅ Implement SQLAlchemy models with proper relationships
- ✅ Create Alembic migration scripts
- ✅ Add indexes for performance (username, email, created_at)
- ✅ Support Arabic text with proper collation
- ✅ Test CRUD operations for all models
- ✅ Test coverage ≥75% with database integration tests

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                  Database Architecture                               │
└─────────────────────────────────────────────────────────────────────┘

Application Layer (FastAPI)
    │
    │  SQLAlchemy Session
    ▼
┌──────────────────────────────────────┐
│ SQLAlchemy ORM Models                │
│ - User                               │
│ - Analysis                           │
│ - Meter                              │
│ - UserProfile                        │
└──────────┬───────────────────────────┘
           │
           │  SQL Queries
           ▼
┌──────────────────────────────────────┐
│ PostgreSQL 15 Database               │
│                                      │
│ Tables:                              │
│ ┌─────────────┐  ┌─────────────┐   │
│ │   users     │  │  analyses   │   │
│ │ - id (PK)   │  │ - id (PK)   │   │
│ │ - username  │  │ - user_id   │   │
│ │ - email     │  │ - text      │   │
│ └──────┬──────┘  └──────┬──────┘   │
│        │ 1:N            │ N:1       │
│        │                │           │
│ ┌──────▼──────┐  ┌──────▼──────┐   │
│ │user_profiles│  │   meters    │   │
│ │ - user_id   │  │ - id (PK)   │   │
│ │ - bio       │  │ - name      │   │
│ └─────────────┘  └─────────────┘   │
│                                     │
│ Indexes:                            │
│ - idx_users_email (UNIQUE)          │
│ - idx_analyses_user_id              │
│ - idx_analyses_created_at           │
│ - idx_analyses_text_search (GIN)    │
└─────────────────────────────────────┘

Schema Design:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
users
├── id (SERIAL PRIMARY KEY)
├── username (VARCHAR(50) UNIQUE NOT NULL)
├── email (VARCHAR(255) UNIQUE NOT NULL)
├── password_hash (VARCHAR(255) NOT NULL)
├── full_name (VARCHAR(100) NOT NULL)
├── role (ENUM: student, poet, teacher, admin)
├── created_at (TIMESTAMP WITH TIME ZONE)
└── updated_at (TIMESTAMP WITH TIME ZONE)

analyses
├── id (UUID PRIMARY KEY DEFAULT gen_random_uuid())
├── user_id (INTEGER REFERENCES users(id))
├── original_text (TEXT NOT NULL)
├── normalized_text (TEXT NOT NULL)
├── pattern (TEXT NOT NULL)
├── detected_meter (VARCHAR(50))
├── confidence (DECIMAL(5,4))
├── syllable_count (INTEGER)
├── processing_time_ms (INTEGER)
├── created_at (TIMESTAMP WITH TIME ZONE)
└── metadata (JSONB)

meters
├── id (SERIAL PRIMARY KEY)
├── name_arabic (VARCHAR(50) UNIQUE NOT NULL)
├── name_english (VARCHAR(50))
├── pattern (TEXT NOT NULL)
├── description (TEXT)
└── examples (JSONB)
```

---

## 3. Input/Output Contracts

### 3.1 SQLAlchemy Models

```python
# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class UserRole(enum.Enum):
    """User role enumeration."""
    STUDENT = "student"
    POET = "poet"
    TEACHER = "teacher"
    ADMIN = "admin"


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    analyses = relationship("Analysis", back_populates="user")
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
```

```python
# backend/app/models/analysis.py
from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class Analysis(Base):
    """Analysis result model."""
    __tablename__ = "analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Input data
    original_text = Column(Text, nullable=False)
    normalized_text = Column(Text, nullable=False)
    
    # Analysis results
    pattern = Column(Text, nullable=False)
    detected_meter = Column(String(50))
    confidence = Column(Numeric(5, 4))
    syllable_count = Column(Integer)
    
    # Performance metrics
    processing_time_ms = Column(Integer)
    
    # Additional data
    metadata = Column(JSONB, default={})
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="analyses")
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, meter='{self.detected_meter}')>"
```

### 3.2 Alembic Migration Template

```python
# backend/alembic/versions/001_initial_schema.py
"""Initial schema

Revision ID: 001
Create Date: 2025-11-08 12:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(100), nullable=False),
        sa.Column('role', sa.Enum('student', 'poet', 'teacher', 'admin', name='user_role'), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_verified', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('idx_users_username', 'users', ['username'], unique=True)
    op.create_index('idx_users_email', 'users', ['email'], unique=True)


def downgrade():
    op.drop_table('users')
```

---

## 4. Step-by-Step Implementation

### Step 1: Install Dependencies

```bash
# Add to requirements.txt
cat >> backend/requirements.txt <<EOF
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
EOF

pip install sqlalchemy==2.0.23 alembic==1.12.1 psycopg2-binary==2.9.9
```

### Step 2: Create Database Base Class

```python
# backend/app/db/base.py
"""
SQLAlchemy declarative base and session management.

Source: docs/technical/DATABASE_SCHEMA.md:1-200
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://bahr_user:bahr_password@localhost:5432/bahr_db"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=False  # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create declarative base
Base = declarative_base()


def get_db():
    """
    Dependency for FastAPI to get database session.
    
    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Step 3: Create User Model

```python
# backend/app/models/user.py
"""
User model with authentication and profile fields.

Source: docs/technical/DATABASE_SCHEMA.md:37-86
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class UserRole(enum.Enum):
    """User role enumeration."""
    STUDENT = "student"
    POET = "poet"
    TEACHER = "teacher"
    ADMIN = "admin"


class User(Base):
    """
    User account model.
    
    Attributes:
        id: Primary key
        username: Unique username (3-50 chars)
        email: Unique email address
        password_hash: Bcrypt hashed password
        full_name: User's full name
        role: User role (student, poet, teacher, admin)
        is_active: Account active status
        is_verified: Email verification status
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    full_name = Column(String(100), nullable=False)
    role = Column(
        SQLEnum(UserRole),
        default=UserRole.STUDENT,
        nullable=False,
        index=True
    )
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
    
    # Relationships
    analyses = relationship(
        "Analysis",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role.value}')>"


class UserProfile(Base):
    """
    Extended user profile information.
    
    Separate table to avoid bloating users table.
    """
    __tablename__ = "user_profiles"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    bio = Column(Text)
    avatar_url = Column(String(500))
    location = Column(String(100))
    website = Column(String(255))
    
    # Gamification
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    
    # Preferences
    preferred_language = Column(String(5), default="ar")
    theme = Column(String(10), default="light")
    
    # Relationship
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, level={self.level})>"
```

### Step 4: Create Analysis Model

```python
# backend/app/models/analysis.py
"""
Analysis result model.

Source: docs/technical/DATABASE_SCHEMA.md:88-150
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class Analysis(Base):
    """
    Poetry analysis result model.
    
    Stores complete analysis results including:
    - Original and normalized text
    - Prosodic pattern and syllables
    - Detected meter with confidence
    - Processing metrics
    """
    __tablename__ = "analyses"
    
    # Primary key (UUID for distributed systems)
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    # Foreign key (nullable for guest analyses)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Input data
    original_text = Column(Text, nullable=False)
    normalized_text = Column(Text, nullable=False, index=True)
    
    # Analysis results
    pattern = Column(Text, nullable=False)
    detected_meter = Column(String(50), index=True)
    confidence = Column(Numeric(5, 4))  # 0.0000 - 1.0000
    syllable_count = Column(Integer)
    
    # Performance metrics
    processing_time_ms = Column(Integer)
    
    # Additional structured data
    metadata = Column(JSONB, default={})
    
    # Timestamp
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    
    # Relationships
    user = relationship("User", back_populates="analyses")
    
    def __repr__(self):
        return (
            f"<Analysis(id={self.id}, "
            f"meter='{self.detected_meter}', "
            f"confidence={self.confidence})>"
        )


class Meter(Base):
    """
    Prosodic meter reference data.
    
    Stores the 16 classical Arabic meters with patterns.
    """
    __tablename__ = "meters"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Names
    name_arabic = Column(String(50), unique=True, nullable=False, index=True)
    name_english = Column(String(50))
    
    # Pattern
    pattern = Column(Text, nullable=False)
    description = Column(Text)
    
    # Examples and metadata
    examples = Column(JSONB, default=[])
    metadata = Column(JSONB, default={})
    
    def __repr__(self):
        return f"<Meter(id={self.id}, name='{self.name_arabic}')>"
```

### Step 5: Initialize Alembic

```bash
# Initialize Alembic
cd backend
alembic init alembic

# Configure Alembic
cat > alembic.ini <<EOF
[alembic]
script_location = alembic
sqlalchemy.url = postgresql://bahr_user:bahr_password@localhost:5432/bahr_db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
EOF
```

### Step 6: Create Initial Migration

```python
# backend/alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.db.base import Base
from app.models.user import User, UserProfile
from app.models.analysis import Analysis, Meter

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

```bash
# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

### Step 7: Create Database Repository

```python
# backend/app/repositories/user_repository.py
"""User repository for database operations."""

from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User, UserRole


class UserRepository:
    """Repository for user CRUD operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    def create(self, user: User) -> User:
        """Create new user."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user: User) -> User:
        """Update existing user."""
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        """Delete user by ID."""
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
```

### Step 8: Test Database Operations

```python
# tests/integration/test_database.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository


@pytest.fixture
def test_db():
    """Create test database."""
    engine = create_engine("postgresql://test:test@localhost:5432/test_db")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)


def test_create_user(test_db):
    """Test user creation."""
    repo = UserRepository(test_db)
    
    user = User(
        username="test_user",
        email="test@example.com",
        password_hash="hashed_password",
        full_name="Test User",
        role=UserRole.STUDENT
    )
    
    created_user = repo.create(user)
    
    assert created_user.id is not None
    assert created_user.username == "test_user"
    assert created_user.email == "test@example.com"


def test_get_user_by_email(test_db):
    """Test retrieving user by email."""
    repo = UserRepository(test_db)
    
    # Create user
    user = User(
        username="test_user",
        email="test@example.com",
        password_hash="hashed",
        full_name="Test User"
    )
    repo.create(user)
    
    # Retrieve
    found_user = repo.get_by_email("test@example.com")
    
    assert found_user is not None
    assert found_user.email == "test@example.com"
```

---

## 5. Reference Implementation (Full Code)

See Step-by-Step Implementation sections above for complete code.

---

## 6. Unit & Integration Tests

```python
# tests/unit/models/test_user_model.py
import pytest
from app.models.user import User, UserRole


def test_user_model_creation():
    """Test User model instantiation."""
    user = User(
        username="ahmad",
        email="ahmad@example.com",
        password_hash="hashed_password",
        full_name="أحمد محمد",
        role=UserRole.POET
    )
    
    assert user.username == "ahmad"
    assert user.role == UserRole.POET
    assert user.is_active is True
    assert user.is_verified is False


def test_user_repr():
    """Test User string representation."""
    user = User(id=1, username="test", role=UserRole.STUDENT)
    
    assert "User(id=1" in repr(user)
    assert "username='test'" in repr(user)
```

---

## 7. CI/CD Pipeline

```yaml
# .github/workflows/database-tests.yml
name: Database Tests

on:
  push:
    paths:
      - 'backend/app/models/**'
      - 'backend/app/repositories/**'
      - 'backend/alembic/**'

jobs:
  test-database:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run Alembic migrations
        run: |
          cd backend
          alembic upgrade head
        env:
          DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
      
      - name: Run database tests
        run: |
          cd backend
          pytest tests/integration/test_database.py -v \
            --cov=app.models \
            --cov=app.repositories
        env:
          DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
```

---

## 8. Deployment Checklist

- [ ] PostgreSQL 15 installed and running
- [ ] Database created with proper encoding (UTF8)
- [ ] Database user created with appropriate permissions
- [ ] Alembic migrations applied (`alembic upgrade head`)
- [ ] Indexes created for performance
- [ ] Test CRUD operations for all models
- [ ] Verify foreign key constraints
- [ ] Test connection pooling (5 connections)
- [ ] Configure backup strategy
- [ ] Set up monitoring for slow queries

---

## 9. Observability

```python
# backend/app/metrics/database_metrics.py
from prometheus_client import Counter, Histogram

database_queries_total = Counter(
    "bahr_database_queries_total",
    "Total database queries",
    ["operation", "table"]
)

database_query_duration_seconds = Histogram(
    "bahr_database_query_duration_seconds",
    "Database query duration",
    ["operation", "table"],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)
```

---

## 10. Security & Safety

- **Password Storage:** Never store plain passwords (use bcrypt)
- **SQL Injection:** Protected by SQLAlchemy ORM
- **Connection Pooling:** Limit to 5 connections
- **Foreign Keys:** Enforce referential integrity
- **Soft Deletes:** Consider adding deleted_at column

---

## 11. Backwards Compatibility

- **None** - Initial implementation
- **Migration Strategy:** Use Alembic for all schema changes

---

## 12. Source Documentation Citations

1. **docs/technical/DATABASE_SCHEMA.md:1-200** - Database schema design
2. **implementation-guides/IMPROVED_PROMPT.md:661-690** - Feature specification

---

**Implementation Complete!** ✅  
**Estimated Time:** 14-18 hours  
**Test Coverage Target:** ≥ 75%  
**Performance Target:** <10ms per simple query
