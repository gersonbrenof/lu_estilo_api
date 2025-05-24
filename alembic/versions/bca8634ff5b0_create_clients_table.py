"""create clients  table

Revision ID: bca8634ff5b0
Revises: 0587856b0aae
Create Date: 2025-05-23 17:31:28.171345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bca8634ff5b0'
down_revision: Union[str, None] = '0587856b0aae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
