"""add token reset timestamps

Revision ID: add_token_reset_timestamps
Revises: add_participants
Create Date: 2026-03-12

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_token_reset_timestamps'
down_revision = 'add_participants'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add tokens_reset_at_daily and tokens_reset_at_monthly columns to agents table."""
    op.add_column('agents', sa.Column('tokens_reset_at_daily', sa.DateTime(timezone=True), nullable=True))
    op.add_column('agents', sa.Column('tokens_reset_at_monthly', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Remove tokens_reset_at_daily and tokens_reset_at_monthly columns from agents table."""
    op.drop_column('agents', 'tokens_reset_at_monthly')
    op.drop_column('agents', 'tokens_reset_at_daily')
