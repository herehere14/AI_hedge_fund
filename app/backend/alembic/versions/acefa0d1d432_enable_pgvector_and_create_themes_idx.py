"""Enable pgvector and create themes_idx table

Revision ID: acefa0d1d432
Revises: 1b1feba3d897
Create Date: 2025-06-23 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = 'acefa0d1d432'
down_revision: Union[str, None] = '1b1feba3d897'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Enable pgvector and add themes_idx table."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        'themes_idx',
        sa.Column('doc_id', sa.String(), primary_key=True),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('embed_vec', Vector),
    )


def downgrade() -> None:
    """Drop themes_idx table."""
    op.drop_table('themes_idx')

