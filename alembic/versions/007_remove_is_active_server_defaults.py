"""remove is_active server defaults

Revision ID: f8052bec76df
Revises: 006
Create Date: 2026-08-23 11:24:38.246054

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '007'
down_revision: Union[str, Sequence[str], None] = '006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('courses','is_active',server_default=None,)
    op.alter_column('lessons','is_active',server_default=None,)
    op.alter_column('materials','is_active',server_default=None,)
    op.alter_column('units','is_active',server_default=None,)


def downgrade() -> None:
    op.alter_column('courses','is_active',server_default=True,)
    op.alter_column('lessons','is_active',server_default=True,)
    op.alter_column('materials','is_active',server_default=True,)
    op.alter_column('units','is_active',server_default=True,)