"""add last few columns to posts

Revision ID: a480dc61aef1
Revises: 38cc1f3de3d0
Create Date: 2024-06-29 14:57:36.974767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a480dc61aef1'
down_revision: Union[str, None] = '38cc1f3de3d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('timestamp', sa.TIMESTAMP(timezone=True), server_default= sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'timestamp')
    op.drop_column('posts', 'published')
    pass
