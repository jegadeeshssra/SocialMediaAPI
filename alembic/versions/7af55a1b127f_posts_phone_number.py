"""posts-phone_number

Revision ID: 7af55a1b127f
Revises: 7d8b971e660b
Create Date: 2025-11-27 17:48:29.670060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7af55a1b127f'
down_revision: Union[str, Sequence[str], None] = '7d8b971e660b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'owner_id')
    pass
