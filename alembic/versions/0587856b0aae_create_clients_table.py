"""create clients  table

Revision ID: 0587856b0aae
Revises: ced868db8ca0
Create Date: 2025-05-23 17:28:27.131126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0587856b0aae'
down_revision: Union[str, None] = 'ced868db8ca0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
