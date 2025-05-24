"""create clientes  table

Revision ID: e0dbd63eeca5
Revises: 3d8b45353f8f
Create Date: 2025-05-23 17:19:22.758637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0dbd63eeca5'
down_revision: Union[str, None] = '3d8b45353f8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
