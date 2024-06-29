"""add content column to posts

Revision ID: 7fcbdc352527
Revises: 87b4c4ec6371
Create Date: 2024-06-29 14:12:20.560597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fcbdc352527'
down_revision: Union[str, None] = '87b4c4ec6371'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
