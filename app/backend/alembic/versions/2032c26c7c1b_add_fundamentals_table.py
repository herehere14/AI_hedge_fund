"""add fundamentals table

Revision ID: 2032c26c7c1b
Revises: e68821e133c3
Create Date: 2025-07-11 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "2032c26c7c1b"
down_revision: Union[str, None] = "e68821e133c3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "fundamentals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ticker", sa.String(length=20), nullable=False, index=True),
        sa.Column("fiscal_date", sa.Date(), nullable=False),
        sa.Column("roe", sa.Float(), nullable=True),
        sa.Column("pe", sa.Float(), nullable=True),
        sa.Column("peg", sa.Float(), nullable=True),
        sa.Column("moat_pct", sa.Float(), nullable=True),
        sa.UniqueConstraint("ticker", "fiscal_date", name="uix_ticker_fiscal_date"),
    )
    op.create_index(op.f("ix_fundamentals_ticker"), "fundamentals", ["ticker"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_fundamentals_ticker"), table_name="fundamentals")
    op.drop_table("fundamentals")
