"""create clients  table

Revision ID: b969b2be045f
Revises: bca8634ff5b0
Create Date: 2025-05-23 17:33:55.319380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b969b2be045f'
down_revision: Union[str, None] = 'bca8634ff5b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
