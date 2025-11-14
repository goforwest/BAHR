"""add analytics_events table

Revision ID: b9f2c3d4e5f6
Revises: a8bdbba834b3
Create Date: 2025-01-11 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b9f2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'a8bdbba834b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add analytics_events table for usage tracking."""
    
    op.create_table(
        'analytics_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('event_name', sa.String(length=100), nullable=False),
        sa.Column('session_id', sa.String(length=100), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('timestamp', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('properties', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('referrer', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for efficient querying
    op.create_index('ix_analytics_events_event_name', 'analytics_events', ['event_name'])
    op.create_index('ix_analytics_events_session_id', 'analytics_events', ['session_id'])
    op.create_index('ix_analytics_events_user_id', 'analytics_events', ['user_id'])
    op.create_index('ix_analytics_events_timestamp', 'analytics_events', ['timestamp'])


def downgrade() -> None:
    """Remove analytics_events table."""
    
    op.drop_index('ix_analytics_events_timestamp', table_name='analytics_events')
    op.drop_index('ix_analytics_events_user_id', table_name='analytics_events')
    op.drop_index('ix_analytics_events_session_id', table_name='analytics_events')
    op.drop_index('ix_analytics_events_event_name', table_name='analytics_events')
    op.drop_table('analytics_events')
