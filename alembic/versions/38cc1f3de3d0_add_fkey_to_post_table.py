"""add fkey to post table

Revision ID: 38cc1f3de3d0
Revises: d5cb01eb40d1
Create Date: 2024-06-29 14:29:44.545862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38cc1f3de3d0'
down_revision: Union[str, None] = 'd5cb01eb40d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_owner_id', 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('fk_owner_id', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
