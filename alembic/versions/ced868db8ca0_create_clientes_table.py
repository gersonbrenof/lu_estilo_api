"""create clientes  table

Revision ID: ced868db8ca0
Revises: e0dbd63eeca5
Create Date: 2025-05-23 17:23:57.144391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ced868db8ca0'
down_revision: Union[str, None] = 'e0dbd63eeca5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
