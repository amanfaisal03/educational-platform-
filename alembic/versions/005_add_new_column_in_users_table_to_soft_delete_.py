"""add new column in users table to soft delete user 

Revision ID: 005
Revises: 004
Create Date: 2026-08-22 17:13:46.264443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '005'
down_revision: Union[str, Sequence[str], None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('users',sa.Column('is_deleted',sa.Boolean(),nullable=False,server_default=sa.false()))


def downgrade():
    op.drop_column('users', 'is_deleted')