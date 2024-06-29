"""add user table

Revision ID: d5cb01eb40d1
Revises: 7fcbdc352527
Create Date: 2024-06-29 14:18:11.926977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5cb01eb40d1'
down_revision: Union[str, None] = '7fcbdc352527'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',    sa.Column('id', sa.Integer(), nullable=False),
                                sa.Column('email', sa.String(), nullable=False),
                                sa.Column('password', sa.String(), nullable=False),
                                sa.Column('timestamp', sa.TIMESTAMP(timezone=True), server_default= sa.text('now()'), nullable=False),
                                sa.PrimaryKeyConstraint('id'),
                                sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')
    pass
