"""unique email

Revision ID: 003
Revises: 002
Create Date: 2026-08-11 14:03:36.973204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, Sequence[str], None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_unique_constraint(
        "uq_users_email",
        "users",
        ["email"]
    )

def downgrade() -> None:
    op.drop_constraint(
        "uq_users_email",
        "users",
        type_="unique"
    )