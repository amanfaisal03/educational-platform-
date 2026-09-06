"""rename lesson foreign-key column to unit_id

Revision ID: 008
Revises: 007
"""

from typing import Sequence, Union

from alembic import op


revision: str = "008"
down_revision: Union[str, Sequence[str], None] = "007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("lessons", "unite_id", new_column_name="unit_id")


def downgrade() -> None:
    op.alter_column("lessons", "unit_id", new_column_name="unite_id")
