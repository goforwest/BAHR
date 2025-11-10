INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Generating static SQL
INFO  [alembic.runtime.migration] Will assume transactional DDL.
BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

INFO  [alembic.runtime.migration] Running upgrade  -> a8bdbba834b3, initial schema
-- Running upgrade  -> a8bdbba834b3

CREATE TYPE userrole AS ENUM ('student', 'poet', 'teacher', 'moderator', 'admin');

CREATE TYPE privacylevel AS ENUM ('public', 'friends', 'private');

CREATE TYPE metertype AS ENUM ('classical', 'modern', 'folk', 'experimental');

CREATE TYPE analysismode AS ENUM ('fast', 'accurate', 'detailed');

CREATE TYPE userrole AS ENUM ('student', 'poet', 'teacher', 'moderator', 'admin');

CREATE TYPE privacylevel AS ENUM ('public', 'friends', 'private');

CREATE TABLE users (
    id SERIAL NOT NULL, 
    username VARCHAR(50) NOT NULL, 
    email VARCHAR(255) NOT NULL, 
    password_hash VARCHAR(255) NOT NULL, 
    full_name VARCHAR(100) NOT NULL, 
    bio TEXT, 
    avatar_url VARCHAR(500), 
    birth_date DATE, 
    location VARCHAR(100), 
    website VARCHAR(255), 
    role userrole DEFAULT 'student' NOT NULL, 
    level INTEGER DEFAULT '1', 
    xp INTEGER DEFAULT '0', 
    coins INTEGER DEFAULT '0', 
    is_active BOOLEAN DEFAULT 'true', 
    is_verified BOOLEAN DEFAULT 'false', 
    email_verified_at TIMESTAMP WITH TIME ZONE, 
    last_login TIMESTAMP WITH TIME ZONE, 
    preferred_language VARCHAR(5) DEFAULT 'ar', 
    theme VARCHAR(10) DEFAULT 'light', 
    notifications JSONB, 
    profile_visibility privacylevel DEFAULT 'public', 
    analysis_privacy privacylevel DEFAULT 'private', 
    deleted_at TIMESTAMP WITH TIME ZONE, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_users_id ON users (id);

CREATE UNIQUE INDEX ix_users_username ON users (username);

CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE INDEX ix_users_role ON users (role);

CREATE INDEX ix_users_level ON users (level);

CREATE INDEX ix_users_is_active ON users (is_active);

CREATE TYPE metertype AS ENUM ('classical', 'modern', 'folk', 'experimental');

CREATE TABLE meters (
    id SERIAL NOT NULL, 
    name VARCHAR(100) NOT NULL, 
    english_name VARCHAR(100), 
    base_pattern TEXT NOT NULL, 
    pattern_type metertype DEFAULT 'classical' NOT NULL, 
    complexity_level INTEGER, 
    syllable_count INTEGER, 
    foot_pattern VARCHAR[], 
    common_variations JSONB, 
    frequency_rank INTEGER, 
    usage_count INTEGER DEFAULT '0', 
    difficulty_score DECIMAL(3, 2), 
    origin_period VARCHAR(50), 
    famous_poets VARCHAR[], 
    description_ar TEXT, 
    description_en TEXT, 
    example_verses JSONB, 
    audio_samples JSONB, 
    is_active BOOLEAN DEFAULT 'true', 
    is_classical BOOLEAN DEFAULT 'true', 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_meters_id ON meters (id);

CREATE UNIQUE INDEX ix_meters_name ON meters (name);

CREATE INDEX ix_meters_pattern_type ON meters (pattern_type);

CREATE INDEX ix_meters_frequency_rank ON meters (frequency_rank);

CREATE INDEX ix_meters_is_active ON meters (is_active);

CREATE TABLE tafail (
    id SERIAL NOT NULL, 
    name_ar VARCHAR(50) NOT NULL, 
    name_en VARCHAR(50), 
    pattern VARCHAR(50) NOT NULL, 
    arabic_notation VARCHAR(50), 
    syllable_structure VARCHAR(50), 
    syllable_count INTEGER NOT NULL, 
    long_syllables INTEGER DEFAULT '0', 
    short_syllables INTEGER DEFAULT '0', 
    common_variations JSONB, 
    alternative_forms VARCHAR[], 
    used_in_meters VARCHAR[], 
    usage_frequency DECIMAL(5, 4), 
    example_words JSONB, 
    description TEXT, 
    is_active BOOLEAN DEFAULT 'true', 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_tafail_id ON tafail (id);

CREATE UNIQUE INDEX ix_tafail_name_ar ON tafail (name_ar);

CREATE INDEX ix_tafail_is_active ON tafail (is_active);

CREATE TYPE analysismode AS ENUM ('fast', 'accurate', 'detailed');

CREATE TABLE analyses (
    id UUID NOT NULL, 
    user_id INTEGER, 
    original_text TEXT NOT NULL, 
    normalized_text TEXT NOT NULL, 
    language VARCHAR(5) DEFAULT 'ar', 
    dialect VARCHAR(20), 
    analysis_mode analysismode DEFAULT 'accurate' NOT NULL, 
    processing_time_ms INTEGER, 
    algorithm_version VARCHAR(20) DEFAULT '1.0' NOT NULL, 
    prosodic_pattern JSONB NOT NULL, 
    syllable_count INTEGER, 
    stress_pattern TEXT, 
    taqti3 TEXT, 
    detected_meter VARCHAR(50), 
    meter_confidence DECIMAL(5, 4), 
    alternative_meters JSONB, 
    quality_score DECIMAL(5, 4), 
    quality_breakdown JSONB, 
    analysis_result JSONB NOT NULL, 
    suggestions JSONB, 
    corrections JSONB, 
    is_public BOOLEAN DEFAULT 'false', 
    view_count INTEGER DEFAULT '0', 
    share_count INTEGER DEFAULT '0', 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE INDEX ix_analyses_id ON analyses (id);

CREATE INDEX ix_analyses_user_id ON analyses (user_id);

CREATE INDEX ix_analyses_detected_meter ON analyses (detected_meter);

CREATE INDEX ix_analyses_quality_score ON analyses (quality_score);

CREATE INDEX ix_analyses_is_public ON analyses (is_public);

CREATE TABLE analysis_cache (
    id SERIAL NOT NULL, 
    text_hash VARCHAR(64) NOT NULL, 
    original_text TEXT NOT NULL, 
    normalized_text TEXT NOT NULL, 
    cached_result JSONB NOT NULL, 
    hit_count INTEGER DEFAULT '0', 
    algorithm_version VARCHAR(20) NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_analysis_cache_id ON analysis_cache (id);

CREATE UNIQUE INDEX ix_analysis_cache_text_hash ON analysis_cache (text_hash);

CREATE INDEX ix_analysis_cache_expires_at ON analysis_cache (expires_at);

INSERT INTO alembic_version (version_num) VALUES ('a8bdbba834b3') RETURNING alembic_version.version_num;

COMMIT;

