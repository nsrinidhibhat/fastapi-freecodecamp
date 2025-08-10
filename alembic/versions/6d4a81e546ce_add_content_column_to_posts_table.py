"""add content column to posts table

Revision ID: 6d4a81e546ce
Revises: 0c0aec726d98
Create Date: 2025-08-09 18:42:33.342355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d4a81e546ce'
down_revision: Union[str, Sequence[str], None] = '0c0aec726d98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
