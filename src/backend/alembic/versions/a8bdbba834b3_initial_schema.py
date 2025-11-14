"""initial schema

Revision ID: a8bdbba834b3
Revises: 
Create Date: 2025-11-09 22:17:08.925492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a8bdbba834b3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Create all MVP tables."""
    
    # Create custom enum types
    op.execute("CREATE TYPE userrole AS ENUM ('student', 'poet', 'teacher', 'moderator', 'admin')")
    op.execute("CREATE TYPE privacylevel AS ENUM ('public', 'friends', 'private')")
    op.execute("CREATE TYPE metertype AS ENUM ('classical', 'modern', 'folk', 'experimental')")
    op.execute("CREATE TYPE analysismode AS ENUM ('fast', 'accurate', 'detailed')")
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.String(length=500), nullable=True),
        sa.Column('birth_date', sa.Date(), nullable=True),
        sa.Column('location', sa.String(length=100), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('role', postgresql.ENUM('student', 'poet', 'teacher', 'moderator', 'admin', name='userrole'), nullable=False, server_default='student'),
        sa.Column('level', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('xp', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('coins', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('email_verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('preferred_language', sa.String(length=5), nullable=True, server_default='ar'),
        sa.Column('theme', sa.String(length=10), nullable=True, server_default='light'),
        sa.Column('notifications', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('profile_visibility', postgresql.ENUM('public', 'friends', 'private', name='privacylevel'), nullable=True, server_default='public'),
        sa.Column('analysis_privacy', postgresql.ENUM('public', 'friends', 'private', name='privacylevel'), nullable=True, server_default='private'),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)
    op.create_index(op.f('ix_users_level'), 'users', ['level'], unique=False)
    op.create_index(op.f('ix_users_is_active'), 'users', ['is_active'], unique=False)
    
    # Create meters table
    op.create_table(
        'meters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('english_name', sa.String(length=100), nullable=True),
        sa.Column('base_pattern', sa.Text(), nullable=False),
        sa.Column('pattern_type', postgresql.ENUM('classical', 'modern', 'folk', 'experimental', name='metertype'), nullable=False, server_default='classical'),
        sa.Column('complexity_level', sa.Integer(), nullable=True),
        sa.Column('syllable_count', sa.Integer(), nullable=True),
        sa.Column('foot_pattern', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('common_variations', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('frequency_rank', sa.Integer(), nullable=True),
        sa.Column('usage_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('difficulty_score', sa.DECIMAL(precision=3, scale=2), nullable=True),
        sa.Column('origin_period', sa.String(length=50), nullable=True),
        sa.Column('famous_poets', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('description_ar', sa.Text(), nullable=True),
        sa.Column('description_en', sa.Text(), nullable=True),
        sa.Column('example_verses', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('audio_samples', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('is_classical', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meters_id'), 'meters', ['id'], unique=False)
    op.create_index(op.f('ix_meters_name'), 'meters', ['name'], unique=True)
    op.create_index(op.f('ix_meters_pattern_type'), 'meters', ['pattern_type'], unique=False)
    op.create_index(op.f('ix_meters_frequency_rank'), 'meters', ['frequency_rank'], unique=False)
    op.create_index(op.f('ix_meters_is_active'), 'meters', ['is_active'], unique=False)
    
    # Create tafail table (prosodic feet)
    op.create_table(
        'tafail',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name_ar', sa.String(length=50), nullable=False),
        sa.Column('name_en', sa.String(length=50), nullable=True),
        sa.Column('pattern', sa.String(length=50), nullable=False),
        sa.Column('arabic_notation', sa.String(length=50), nullable=True),
        sa.Column('syllable_structure', sa.String(length=50), nullable=True),
        sa.Column('syllable_count', sa.Integer(), nullable=False),
        sa.Column('long_syllables', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('short_syllables', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('common_variations', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('alternative_forms', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('used_in_meters', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('usage_frequency', sa.DECIMAL(precision=5, scale=4), nullable=True),
        sa.Column('example_words', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tafail_id'), 'tafail', ['id'], unique=False)
    op.create_index(op.f('ix_tafail_name_ar'), 'tafail', ['name_ar'], unique=True)
    op.create_index(op.f('ix_tafail_is_active'), 'tafail', ['is_active'], unique=False)
    
    # Create analyses table
    op.create_table(
        'analyses',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('original_text', sa.Text(), nullable=False),
        sa.Column('normalized_text', sa.Text(), nullable=False),
        sa.Column('language', sa.String(length=5), nullable=True, server_default='ar'),
        sa.Column('dialect', sa.String(length=20), nullable=True),
        sa.Column('analysis_mode', postgresql.ENUM('fast', 'accurate', 'detailed', name='analysismode'), nullable=False, server_default='accurate'),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('algorithm_version', sa.String(length=20), nullable=False, server_default='1.0'),
        sa.Column('prosodic_pattern', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('syllable_count', sa.Integer(), nullable=True),
        sa.Column('stress_pattern', sa.Text(), nullable=True),
        sa.Column('taqti3', sa.Text(), nullable=True),
        sa.Column('detected_meter', sa.String(length=50), nullable=True),
        sa.Column('meter_confidence', sa.DECIMAL(precision=5, scale=4), nullable=True),
        sa.Column('alternative_meters', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('quality_score', sa.DECIMAL(precision=5, scale=4), nullable=True),
        sa.Column('quality_breakdown', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('analysis_result', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('suggestions', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('corrections', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('view_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('share_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analyses_id'), 'analyses', ['id'], unique=False)
    op.create_index(op.f('ix_analyses_user_id'), 'analyses', ['user_id'], unique=False)
    op.create_index(op.f('ix_analyses_detected_meter'), 'analyses', ['detected_meter'], unique=False)
    op.create_index(op.f('ix_analyses_quality_score'), 'analyses', ['quality_score'], unique=False)
    op.create_index(op.f('ix_analyses_is_public'), 'analyses', ['is_public'], unique=False)
    
    # Create analysis_cache table
    op.create_table(
        'analysis_cache',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('text_hash', sa.String(length=64), nullable=False),
        sa.Column('original_text', sa.Text(), nullable=False),
        sa.Column('normalized_text', sa.Text(), nullable=False),
        sa.Column('cached_result', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('hit_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('algorithm_version', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('last_accessed', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analysis_cache_id'), 'analysis_cache', ['id'], unique=False)
    op.create_index(op.f('ix_analysis_cache_text_hash'), 'analysis_cache', ['text_hash'], unique=True)
    op.create_index(op.f('ix_analysis_cache_expires_at'), 'analysis_cache', ['expires_at'], unique=False)


def downgrade() -> None:
    """Downgrade schema - Drop all MVP tables."""
    
    # Drop tables in reverse order (respecting foreign keys)
    op.drop_index(op.f('ix_analysis_cache_expires_at'), table_name='analysis_cache')
    op.drop_index(op.f('ix_analysis_cache_text_hash'), table_name='analysis_cache')
    op.drop_index(op.f('ix_analysis_cache_id'), table_name='analysis_cache')
    op.drop_table('analysis_cache')
    
    op.drop_index(op.f('ix_analyses_is_public'), table_name='analyses')
    op.drop_index(op.f('ix_analyses_quality_score'), table_name='analyses')
    op.drop_index(op.f('ix_analyses_detected_meter'), table_name='analyses')
    op.drop_index(op.f('ix_analyses_user_id'), table_name='analyses')
    op.drop_index(op.f('ix_analyses_id'), table_name='analyses')
    op.drop_table('analyses')
    
    op.drop_index(op.f('ix_tafail_is_active'), table_name='tafail')
    op.drop_index(op.f('ix_tafail_name_ar'), table_name='tafail')
    op.drop_index(op.f('ix_tafail_id'), table_name='tafail')
    op.drop_table('tafail')
    
    op.drop_index(op.f('ix_meters_is_active'), table_name='meters')
    op.drop_index(op.f('ix_meters_frequency_rank'), table_name='meters')
    op.drop_index(op.f('ix_meters_pattern_type'), table_name='meters')
    op.drop_index(op.f('ix_meters_name'), table_name='meters')
    op.drop_index(op.f('ix_meters_id'), table_name='meters')
    op.drop_table('meters')
    
    op.drop_index(op.f('ix_users_is_active'), table_name='users')
    op.drop_index(op.f('ix_users_level'), table_name='users')
    op.drop_index(op.f('ix_users_role'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    
    # Drop custom enum types
    op.execute("DROP TYPE IF EXISTS analysismode")
    op.execute("DROP TYPE IF EXISTS metertype")
    op.execute("DROP TYPE IF EXISTS privacylevel")
    op.execute("DROP TYPE IF EXISTS userrole")

