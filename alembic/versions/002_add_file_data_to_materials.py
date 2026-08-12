"""add file_data to materials

Revision ID: 002
Revises: 9b0a194347e0
Create Date: 2026-05-02 12:33:27.395963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, Sequence[str], None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'materials',
        sa.Column('file_data', sa.LargeBinary(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('materials', 'file_data')
