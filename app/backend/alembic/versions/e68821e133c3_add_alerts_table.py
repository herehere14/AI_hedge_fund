"""add alerts table

Revision ID: e68821e133c3
Revises: 2f8c5d9e4b1a
Create Date: 2025-07-01 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e68821e133c3'
down_revision: Union[str, None] = '2f8c5d9e4b1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('ticker', sa.String(length=10), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('emailed', sa.Boolean(), nullable=False, server_default='0'),
    )
    op.create_index(op.f('ix_alerts_id'), 'alerts', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_alerts_id'), table_name='alerts')
    op.drop_table('alerts')
