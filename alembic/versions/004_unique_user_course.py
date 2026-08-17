"""Add a unique constraint for student-course enrollments.

Revision ID: 004
Revises: 003
"""

from typing import Sequence, Union

from alembic import op


revision: str = "004"
down_revision: Union[str, Sequence[str], None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_user_courses_user_course",
        "user_courses",
        ["user_id", "course_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_user_courses_user_course",
        "user_courses",
        type_="unique",
    )
