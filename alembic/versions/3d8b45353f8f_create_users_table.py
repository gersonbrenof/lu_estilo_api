"""create users table

Revision ID: 3d8b45353f8f
Revises: 8e13ef05997e
Create Date: 2025-05-23 08:32:17.198471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d8b45353f8f'
down_revision: Union[str, None] = '8e13ef05997e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
