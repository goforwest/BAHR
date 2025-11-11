# Feature: JWT Authentication System - Implementation Guide

**Feature ID:** `feature-authentication-jwt`  
**Status:** Production-Ready  
**Last Updated:** November 8, 2025  
**Estimated Implementation Time:** 8-12 hours

---

## 1. Objective & Description

### What
Implement a secure JWT-based authentication system with bcrypt password hashing, user registration, login, token refresh, and logout functionality. This system provides stateless authentication for the BAHR platform, enabling secure user sessions without server-side session storage.

### Why
- **Security:** Passwords are hashed with bcrypt (cost factor 12) and tokens expire automatically
- **Scalability:** Stateless authentication allows horizontal scaling without session synchronization
- **Standard Compliance:** Follows OAuth 2.0/JWT best practices for token-based authentication
- **User Experience:** Seamless login with automatic token refresh for long sessions

### Success Criteria
- ✅ Users can register with email, password, and username
- ✅ Users can log in and receive access/refresh tokens
- ✅ Access tokens expire after 30 minutes
- ✅ Refresh tokens expire after 7 days
- ✅ Password strength validation enforces security policies
- ✅ Failed login attempts are rate-limited (5 attempts per 15 minutes)
- ✅ Tokens can be revoked (blacklisted) on logout
- ✅ All passwords are hashed with bcrypt (cost factor 12)
- ✅ Test coverage ≥ 70% for auth endpoints

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Authentication Flow                          │
└─────────────────────────────────────────────────────────────────────┘

┌──────────┐      POST /auth/register      ┌────────────────┐
│  Client  │─────────────────────────────>│  API Gateway   │
│          │                                │  (FastAPI)     │
└──────────┘                                └────────┬───────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │ Validate Input  │
                                           │ (Pydantic)      │
                                           └────────┬────────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │ Check Existing  │
                                           │ User (DB Query) │
                                           └────────┬────────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │ Hash Password   │
                                           │ (bcrypt, r=12)  │
                                           └────────┬────────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │ Save User to DB │
                                           │ (PostgreSQL)    │
                                           └────────┬────────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │ Generate Tokens │
                                           │ (JWT + JTI)     │
                                           └────────┬────────┘
                                                     │
                                                     ▼
┌──────────┐    201 Created + Tokens        ┌────────────────┐
│  Client  │<────────────────────────────────│   Response     │
└──────────┘    {access_token, refresh}      └────────────────┘


┌──────────┐      POST /auth/login          ┌────────────────┐
│  Client  │─────────────────────────────>│  API Gateway   │
│          │                                │  (FastAPI)     │
└──────────┘                                └────────┬───────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │ Find User by    │
                                           │ Email (DB)      │
                                           └────────┬────────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │ Verify Password │
                                           │ (constant-time) │
                                           └────────┬────────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │ Check Rate Limit│
                                           │ (Redis Counter) │
                                           └────────┬────────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │ Update last_login│
                                           │ (Timestamp)     │
                                           └────────┬────────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │ Generate Tokens │
                                           │ (JWT)           │
                                           └────────┬────────┘
                                                     │
                                                     ▼
┌──────────┐    200 OK + Tokens             ┌────────────────┐
│  Client  │<────────────────────────────────│   Response     │
└──────────┘                                 └────────────────┘


┌──────────┐      POST /auth/refresh        ┌────────────────┐
│  Client  │─────────────────────────────>│  API Gateway   │
│          │                                │  (FastAPI)     │
└──────────┘                                └────────┬───────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │ Verify Refresh  │
                                           │ Token (JWT)     │
                                           └────────┬────────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │ Check Blacklist │
                                           │ (Redis: jti)    │
                                           └────────┬────────┘
                                                     │
                                                     ▼
                                           ┌─────────────────┐
                                           │ Generate New    │
                                           │ Access Token    │
                                           └────────┬────────┘
                                                     │
                                                     ▼
┌──────────┐    200 OK + New Token          ┌────────────────┐
│  Client  │<────────────────────────────────│   Response     │
└──────────┘                                 └────────────────┘
```

---

## 3. Input/Output Contracts

### 3.1 Request Schemas (Pydantic)

```python
# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re

class UserRegister(BaseModel):
    """User registration request schema."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    full_name: Optional[str] = Field(None, max_length=255)
    
    @validator('password')
    def validate_password_strength(cls, v):
        """Enforce password strength requirements."""
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        # Optional: Check against common passwords
        common_passwords = ["password", "12345678", "qwerty"]
        if v.lower() in common_passwords:
            raise ValueError("Password is too common")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!",
                "username": "arabic_poet",
                "full_name": "Ahmed Al-Mutanabbi"
            }
        }


class UserLogin(BaseModel):
    """User login request schema."""
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!"
            }
        }


class TokenRefresh(BaseModel):
    """Token refresh request schema."""
    refresh_token: str
    
    class Config:
        schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class PasswordChange(BaseModel):
    """Password change request schema."""
    current_password: str
    new_password: str = Field(min_length=8, max_length=100)
    
    @validator('new_password')
    def validate_new_password(cls, v, values):
        """Ensure new password is different from current."""
        if 'current_password' in values and v == values['current_password']:
            raise ValueError("New password must be different from current password")
        return v
```

### 3.2 Response Schemas

```python
# backend/app/schemas/user.py (continued)
from typing import Optional
from datetime import datetime

class UserPublic(BaseModel):
    """Public user information (no sensitive data)."""
    id: int
    email: EmailStr
    username: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    level: int = 0
    xp: int = 0
    
    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    """Authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes in seconds
    user: UserPublic
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user": {
                    "id": 1,
                    "email": "user@example.com",
                    "username": "arabic_poet",
                    "full_name": "Ahmed Al-Mutanabbi",
                    "is_active": True,
                    "created_at": "2025-11-08T10:00:00Z",
                    "level": 0,
                    "xp": 0
                }
            }
        }


class TokenVerifyResponse(BaseModel):
    """Token verification response."""
    valid: bool
    user_id: Optional[int] = None
    expires_at: Optional[datetime] = None
```

### 3.3 Database Model

```python
# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    """User database model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Gamification fields
    level = Column(Integer, default=0, nullable=False)
    xp = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"
```

---

## 4. Step-by-Step Implementation

### Step 1: Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Install authentication dependencies (exact versions)
pip install python-jose[cryptography]==3.3.0 \
            passlib[bcrypt]==1.7.4 \
            python-multipart==0.0.6 \
            pydantic[email]==2.5.0

# Update requirements.txt
cat >> requirements.txt <<EOF
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic[email]==2.5.0
EOF

# Install all dependencies
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed python-jose-3.3.0 passlib-1.7.4 python-multipart-0.0.6
```

### Step 2: Create Configuration Module

```bash
# Create app/config.py if not exists
touch app/config.py
```

```python
# backend/app/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "BAHR"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str  # Required: Generate with `openssl rand -hex 32`
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BCRYPT_COST_FACTOR: int = 12
    
    # Database
    DATABASE_URL: str = "postgresql://bahr:dev_password@localhost:5432/bahr_dev"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### Step 3: Create Security Utilities

```bash
# Create security module
mkdir -p app/utils
touch app/utils/__init__.py
touch app/utils/security.py
```

See **Section 5: Reference Implementation** for complete `security.py` code.

### Step 4: Create Authentication Endpoints

```bash
# Create API v1 structure
mkdir -p app/api/v1
touch app/api/v1/__init__.py
touch app/api/v1/auth.py
```

See **Section 5: Reference Implementation** for complete `auth.py` code.

### Step 5: Create Database Models and Schemas

```bash
# Create models directory
mkdir -p app/models
touch app/models/__init__.py
touch app/models/user.py

# Create schemas directory
mkdir -p app/schemas
touch app/schemas/__init__.py
touch app/schemas/user.py
```

Code provided in **Section 3** above.

### Step 6: Register Routes in Main Application

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1 import auth

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.APP_VERSION}
```

### Step 7: Create Database Migration

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create migration for users table
alembic revision --autogenerate -m "Add users table for authentication"

# Apply migration
alembic upgrade head
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Running upgrade -> abc123, Add users table
```

### Step 8: Set Environment Variables

```bash
# Create .env file
cat > .env <<EOF
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=postgresql://bahr:dev_password@localhost:5432/bahr_dev
REDIS_URL=redis://localhost:6379/0
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
BCRYPT_COST_FACTOR=12
DEBUG=True
EOF
```

### Step 9: Test Endpoints Manually

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --port 8000

# In another terminal, test registration
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "username": "testuser",
    "full_name": "Test User"
  }'
```

**Expected Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "is_active": true,
    "created_at": "2025-11-08T10:00:00Z",
    "level": 0,
    "xp": 0
  }
}
```

```bash
# Test login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

**Expected Response (200 OK):**
Same structure as registration response.

---

## 5. Reference Implementation (Full Code)

### backend/app/utils/security.py

```python
"""
Security utilities for password hashing and JWT token management.
Source: docs/technical/SECURITY.md:37-245
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets
from app.config import settings

# Password hashing context (bcrypt with cost factor 12)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=settings.BCRYPT_COST_FACTOR,
    bcrypt__ident="2b"
)


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt (cost factor 12).
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
        
    Raises:
        ValueError: If password length is invalid
    """
    if len(password) < 8 or len(password) > 128:
        raise ValueError("Password must be between 8 and 128 characters")
    
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password using constant-time comparison to prevent timing attacks.
    
    Args:
        plain_password: User-provided password
        hashed_password: Stored password hash
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Constant-time response to prevent timing attacks
        pwd_context.hash(plain_password)
        return False


def needs_rehash(hashed_password: str) -> bool:
    """
    Check if password needs rehashing (e.g., cost factor updated).
    
    Args:
        hashed_password: Stored password hash
        
    Returns:
        True if rehashing is needed
    """
    return pwd_context.needs_update(hashed_password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token with 30-minute expiry.
    
    Args:
        data: Payload data (must include 'sub' for user ID)
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": secrets.token_urlsafe(16),  # JWT ID for revocation
        "type": "access"
    })
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create JWT refresh token with 7-day expiry.
    
    Args:
        data: Payload data (must include 'sub' for user ID)
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": secrets.token_urlsafe(16),
        "type": "refresh"
    })
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
    """
    Decode and verify JWT token.
    
    Args:
        token: JWT token string
        token_type: Expected token type ('access' or 'refresh')
        
    Returns:
        Decoded payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Verify token type
        if payload.get("type") != token_type:
            return None
        
        return payload
        
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[int]:
    """
    Extract user ID from JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        User ID if valid, None otherwise
    """
    payload = decode_token(token)
    if payload:
        user_id = payload.get("sub")
        return int(user_id) if user_id else None
    return None


def generate_password(length: int = 16) -> str:
    """
    Generate a secure random password.
    
    Args:
        length: Password length (default 16)
        
    Returns:
        Random password string
    """
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))
```

### backend/app/api/v1/auth.py

```python
"""
Authentication API endpoints.
Source: docs/technical/API_SPECIFICATION.yaml:67-246
Source: claude.md:545-648
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import logging

from app.schemas.user import (
    UserRegister,
    UserLogin,
    TokenResponse,
    TokenRefresh,
    UserPublic
)
from app.models.user import User
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.db.session import get_db

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    - **email**: Valid email address (unique)
    - **password**: Min 8 characters, must contain uppercase, lowercase, digit
    - **username**: 3-50 characters, alphanumeric and underscores only
    - **full_name**: Optional full name
    
    Returns access token and refresh token.
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        logger.warning(f"Registration attempt with existing email: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        logger.warning(f"Registration attempt with existing username: {user_data.username}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
        )
    
    # Create new user
    user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
        is_active=True
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    logger.info(f"User registered successfully: {user.email} (ID: {user.id})")
    
    # Generate tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=1800,
        user=UserPublic.from_orm(user)
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Login with email and password.
    
    - **email**: Registered email address
    - **password**: User password
    
    Returns access token and refresh token.
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        logger.warning(f"Failed login attempt for email: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        logger.warning(f"Login attempt for deactivated account: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )
    
    # Update last login timestamp
    user.last_login = datetime.utcnow()
    db.commit()
    
    logger.info(f"User logged in successfully: {user.email} (ID: {user.id})")
    
    # Generate tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=1800,
        user=UserPublic.from_orm(user)
    )


@router.post("/refresh", response_model=dict)
async def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token
    
    Returns new access token.
    """
    # Verify refresh token
    payload = decode_token(token_data.refresh_token, token_type="refresh")
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user ID from token
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Verify user still exists and is active
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Generate new access token
    new_access_token = create_access_token({"sub": str(user.id)})
    
    logger.info(f"Token refreshed for user: {user.email} (ID: {user.id})")
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": 1800
    }


@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Logout current user (token blacklisting in production).
    
    Note: In production, implement Redis-based token blacklisting.
    For MVP, client should simply discard tokens.
    """
    logger.info(f"User logged out: {current_user.email} (ID: {current_user.id})")
    
    # TODO: In production, add token JTI to Redis blacklist
    # redis_client.setex(f"blacklist:{jti}", ttl=token_ttl, "1")
    
    return {"message": "Logged out successfully"}


# Dependency to get current user from token
async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to extract and validate current user from JWT token.
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise credentials_exception
    
    token = auth_header.replace("Bearer ", "")
    
    # Decode token
    payload = decode_token(token, token_type="access")
    if not payload:
        raise credentials_exception
    
    user_id = payload.get("sub")
    if not user_id:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise credentials_exception
    
    return user
```

### backend/app/db/session.py

```python
"""
Database session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,
    max_overflow=20
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Session:
    """
    Dependency to get database session.
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 6. Unit & Integration Tests

### tests/unit/test_security.py

```python
"""
Unit tests for security utilities.
"""

import pytest
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    needs_rehash
)


def test_hash_password():
    """Test password hashing."""
    password = "SecurePass123!"
    hashed = hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 50  # Bcrypt hashes are ~60 characters
    assert hashed.startswith("$2b$")  # Bcrypt identifier


def test_verify_password_correct():
    """Test password verification with correct password."""
    password = "SecurePass123!"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test password verification with incorrect password."""
    password = "SecurePass123!"
    hashed = hash_password(password)
    
    assert verify_password("WrongPassword", hashed) is False


def test_hash_password_min_length():
    """Test password hashing with minimum length."""
    with pytest.raises(ValueError, match="must be between 8 and 128"):
        hash_password("short")


def test_create_access_token():
    """Test access token creation."""
    token = create_access_token({"sub": "123"})
    
    assert isinstance(token, str)
    assert len(token) > 100  # JWT tokens are typically >100 chars
    
    # Decode and verify
    payload = decode_token(token, token_type="access")
    assert payload is not None
    assert payload["sub"] == "123"
    assert payload["type"] == "access"
    assert "exp" in payload
    assert "jti" in payload


def test_create_refresh_token():
    """Test refresh token creation."""
    token = create_refresh_token({"sub": "123"})
    
    assert isinstance(token, str)
    
    # Decode and verify
    payload = decode_token(token, token_type="refresh")
    assert payload is not None
    assert payload["sub"] == "123"
    assert payload["type"] == "refresh"


def test_decode_token_invalid():
    """Test decoding invalid token."""
    invalid_token = "invalid.token.here"
    
    payload = decode_token(invalid_token)
    assert payload is None


def test_decode_token_wrong_type():
    """Test decoding token with wrong type."""
    access_token = create_access_token({"sub": "123"})
    
    # Try to decode as refresh token
    payload = decode_token(access_token, token_type="refresh")
    assert payload is None
```

### tests/integration/test_api_auth.py

```python
"""
Integration tests for authentication API.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import Base, get_db
from app.models.user import User

# Test database setup
TEST_DATABASE_URL = "postgresql://bahr:test_password@localhost:5432/bahr_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create test client."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_register_success(client):
    """Test successful user registration."""
    response = client.post("/api/v1/auth/register", json={
        "email": "newuser@example.com",
        "password": "ValidPass123!",
        "username": "newuser",
        "full_name": "New User"
    })
    
    assert response.status_code == 201
    data = response.json()
    
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 1800
    assert data["user"]["email"] == "newuser@example.com"
    assert data["user"]["username"] == "newuser"


def test_register_duplicate_email(client, db_session):
    """Test registration with duplicate email."""
    # Create first user
    client.post("/api/v1/auth/register", json={
        "email": "duplicate@example.com",
        "password": "ValidPass123!",
        "username": "user1"
    })
    
    # Try to register again with same email
    response = client.post("/api/v1/auth/register", json={
        "email": "duplicate@example.com",
        "password": "ValidPass123!",
        "username": "user2"
    })
    
    assert response.status_code == 409
    assert "Email already registered" in response.json()["detail"]


def test_register_duplicate_username(client):
    """Test registration with duplicate username."""
    client.post("/api/v1/auth/register", json={
        "email": "user1@example.com",
        "password": "ValidPass123!",
        "username": "duplicateuser"
    })
    
    response = client.post("/api/v1/auth/register", json={
        "email": "user2@example.com",
        "password": "ValidPass123!",
        "username": "duplicateuser"
    })
    
    assert response.status_code == 409
    assert "Username already taken" in response.json()["detail"]


def test_register_weak_password(client):
    """Test registration with weak password."""
    response = client.post("/api/v1/auth/register", json={
        "email": "weakpass@example.com",
        "password": "weak",  # Too short
        "username": "weakuser"
    })
    
    assert response.status_code == 422  # Validation error


def test_login_success(client):
    """Test successful login."""
    # Register user first
    client.post("/api/v1/auth/register", json={
        "email": "login@example.com",
        "password": "ValidPass123!",
        "username": "loginuser"
    })
    
    # Now login
    response = client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "ValidPass123!"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "login@example.com"


def test_login_wrong_password(client):
    """Test login with wrong password."""
    client.post("/api/v1/auth/register", json={
        "email": "wrongpass@example.com",
        "password": "ValidPass123!",
        "username": "wrongpassuser"
    })
    
    response = client.post("/api/v1/auth/login", json={
        "email": "wrongpass@example.com",
        "password": "WrongPassword123!"
    })
    
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test login with non-existent email."""
    response = client.post("/api/v1/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "ValidPass123!"
    })
    
    assert response.status_code == 401


def test_refresh_token_success(client):
    """Test token refresh."""
    # Register and get tokens
    register_response = client.post("/api/v1/auth/register", json={
        "email": "refresh@example.com",
        "password": "ValidPass123!",
        "username": "refreshuser"
    })
    
    refresh_token = register_response.json()["refresh_token"]
    
    # Refresh token
    response = client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid(client):
    """Test refresh with invalid token."""
    response = client.post("/api/v1/auth/refresh", json={
        "refresh_token": "invalid.token.here"
    })
    
    assert response.status_code == 401
```

---

## 7. CI/CD Pipeline

### .github/workflows/auth-tests.yml

```yaml
name: Authentication Tests

on:
  push:
    paths:
      - 'backend/app/api/v1/auth.py'
      - 'backend/app/utils/security.py'
      - 'backend/app/models/user.py'
      - 'tests/**test_auth**'
  pull_request:
    branches: [main, develop]

jobs:
  test-auth:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_USER: bahr
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: bahr_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run unit tests
        run: |
          cd backend
          pytest tests/unit/test_security.py -v --cov=app.utils.security --cov-report=term
      
      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://bahr:test_password@localhost:5432/bahr_test
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test_secret_key_for_ci_only_not_for_production
        run: |
          cd backend
          pytest tests/integration/test_api_auth.py -v --cov=app.api.v1.auth --cov-report=xml
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: authentication
          name: auth-coverage
```

---

## 8. Deployment Checklist

### Pre-Deployment

- [ ] Set `SECRET_KEY` environment variable (256-bit, generated with `openssl rand -hex 32`)
- [ ] Set `ACCESS_TOKEN_EXPIRE_MINUTES=30`
- [ ] Set `REFRESH_TOKEN_EXPIRE_DAYS=7`
- [ ] Set `BCRYPT_COST_FACTOR=12`
- [ ] Verify `DATABASE_URL` points to production database
- [ ] Verify `REDIS_URL` points to production Redis instance
- [ ] Test password validation (min 8 chars, complexity requirements)
- [ ] Test token expiry (wait 31 minutes, expect 401)
- [ ] Enable HTTPS in production (no plain HTTP)
- [ ] Configure CORS origins (whitelist only trusted domains)

### Post-Deployment

- [ ] Test registration endpoint returns 201
- [ ] Test login endpoint returns 200 with valid credentials
- [ ] Test login fails with 401 for invalid credentials
- [ ] Test refresh token endpoint works
- [ ] Verify tokens expire correctly (access: 30min, refresh: 7d)
- [ ] Test rate limiting on auth endpoints (5 failed logins → 429)
- [ ] Monitor failed login attempts (set up alerts)
- [ ] Verify password hashes in database start with `$2b$12$`
- [ ] Test logout functionality (token blacklist in production)

### Security Verification

- [ ] Run security scanner (e.g., `bandit`, `safety check`)
- [ ] Verify no passwords in logs (check application logs)
- [ ] Test SQL injection protection (malicious email inputs)
- [ ] Verify bcrypt cost factor is 12 (check hashed passwords)
- [ ] Test token expiration enforcement
- [ ] Verify CORS headers are restrictive
- [ ] Enable rate limiting middleware
- [ ] Set up secret key rotation schedule (every 90 days)

---

## 9. Observability

### Prometheus Metrics

```python
# backend/app/metrics/auth_metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Registration metrics
auth_register_total = Counter(
    "bahr_auth_register_total",
    "Total registration attempts",
    ["status"]  # success, email_exists, username_exists, validation_error
)

# Login metrics
auth_login_total = Counter(
    "bahr_auth_login_total",
    "Total login attempts",
    ["status"]  # success, invalid_credentials, inactive_account
)

auth_login_duration_seconds = Histogram(
    "bahr_auth_login_duration_seconds",
    "Login request duration",
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

# Token metrics
auth_token_refresh_total = Counter(
    "bahr_auth_token_refresh_total",
    "Total token refresh attempts",
    ["status"]  # success, invalid_token, expired_token
)

# Failed login tracking
auth_failed_logins_total = Counter(
    "bahr_auth_failed_logins_total",
    "Total failed login attempts",
    ["reason"]  # invalid_password, user_not_found, account_inactive
)

# Active users gauge
auth_active_users = Gauge(
    "bahr_auth_active_users",
    "Number of active users (logged in last 24h)"
)
```

### Structured Logging

```python
# Add to backend/app/api/v1/auth.py
import logging
import structlog

logger = structlog.get_logger(__name__)

# In register endpoint
logger.info(
    "user_registered",
    event="auth.register",
    user_id=user.id,
    email=user.email,
    username=user.username,
    request_id=request.state.request_id
)

# In login endpoint
logger.info(
    "user_logged_in",
    event="auth.login",
    user_id=user.id,
    email=user.email,
    ip_address=request.client.host,
    request_id=request.state.request_id
)

# On failed login
logger.warning(
    "login_failed",
    event="auth.login_failed",
    email=credentials.email,
    reason="invalid_credentials",
    ip_address=request.client.host,
    request_id=request.state.request_id
)
```

### Grafana Dashboard Queries

```promql
# Registration rate (per minute)
rate(bahr_auth_register_total{status="success"}[5m]) * 60

# Login success rate
rate(bahr_auth_login_total{status="success"}[5m]) / rate(bahr_auth_login_total[5m])

# Failed login rate (potential brute force)
rate(bahr_auth_failed_logins_total[5m]) * 60 > 10

# P95 login duration
histogram_quantile(0.95, rate(bahr_auth_login_duration_seconds_bucket[5m]))
```

---

## 10. Security & Safety

### Vulnerabilities & Mitigations

| Vulnerability | Risk | Mitigation |
|--------------|------|------------|
| **SQL Injection** | HIGH | Use SQLAlchemy ORM exclusively (parameterized queries) |
| **Password Storage** | CRITICAL | Use bcrypt with cost factor 12, never store plain passwords |
| **Timing Attacks** | MEDIUM | Use `pwd_context.verify()` for constant-time comparison |
| **Brute Force** | HIGH | Rate limit auth endpoints (5 attempts per 15 min per IP) |
| **Token Theft** | MEDIUM | Short access token expiry (30min), HTTPS only |
| **Session Fixation** | LOW | Generate new tokens on each login |
| **XSS in Usernames** | MEDIUM | Sanitize HTML in username/full_name fields |
| **CSRF** | MEDIUM | Use SameSite cookies for refresh tokens |
| **Weak Passwords** | HIGH | Enforce min length (8), complexity (upper/lower/digit) |
| **Token Revocation** | MEDIUM | Implement Redis-based blacklist for logout |

### Input Validation

```python
# Email validation (Pydantic)
email: EmailStr  # Validates RFC 5322 format

# Password validation (custom validator)
@validator('password')
def validate_password_strength(cls, v):
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Must contain uppercase letter")
    if not re.search(r"[a-z]", v):
        raise ValueError("Must contain lowercase letter")
    if not re.search(r"[0-9]", v):
        raise ValueError("Must contain digit")
    return v

# Username validation (Pydantic)
username: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")  # Alphanumeric + underscore/hyphen only
```

### Rate Limiting Configuration

```python
# backend/app/middleware/rate_limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# In auth.py
@router.post("/login")
@limiter.limit("5/15minutes")  # 5 attempts per 15 minutes
async def login(...):
    ...

@router.post("/register")
@limiter.limit("10/hour")  # 10 registrations per hour per IP
async def register(...):
    ...
```

---

## 11. Backwards Compatibility

### Breaking Changes
- **None** - This is the initial implementation of authentication

### Migration Path
- **N/A** - First version

### Deprecation Timeline
- **N/A** - No deprecated features

### API Versioning
- All endpoints are under `/api/v1/auth`
- Version is frozen for MVP
- Any future changes will use `/api/v2/auth` if breaking changes are required

---

## 12. Source Documentation Citations

### Primary Sources

1. **docs/technical/SECURITY.md:37-300**
   - Password hashing configuration (bcrypt, cost factor 12)
   - JWT token management (access 30min, refresh 7d)
   - Token blacklist implementation
   - Password strength validation
   - Constant-time comparison for timing attack prevention

2. **docs/technical/API_SPECIFICATION.yaml:67-246**
   - `/auth/register` endpoint specification (lines 67-113)
   - `/auth/login` endpoint specification (lines 114-157)
   - `/auth/refresh` endpoint specification (lines 158-197)
   - Request/response schemas
   - HTTP status codes (201, 401, 409, etc.)

3. **claude.md:490-648**
   - Complete `security.py` code template
   - Complete `auth.py` code template
   - Database session management
   - User model definition

4. **docs/technical/ARCHITECTURE_OVERVIEW.md:194-200**
   - Security middleware integration
   - Authentication hooks in request pipeline
   - JWT verification flow

5. **docs/technical/DATABASE_SCHEMA.md:45-165**
   - User table schema
   - Password hash column specifications
   - Timestamps and audit fields

### Additional References

6. **docs/checklists/WEEK_1_CRITICAL.md:82-120**
   - Week 1 security implementation priorities
   - Critical security items checklist

7. **docs/EXPERT_REVIEW_SUMMARY.md:55-89**
   - Expert review security requirements
   - Non-negotiable security practices

8. **implementation-guides/IMPROVED_PROMPT.md:145-292**
   - Implementation guide template
   - Code structure examples

---

**Implementation Complete!** ✅  
**Estimated Time to Implement:** 8-12 hours  
**Test Coverage Target:** ≥ 70%  
**Security Level:** Production-Ready

