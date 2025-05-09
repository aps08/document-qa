"""drop usage column

Revision ID: 51a460cd2273
Revises: ff3f727e564e
Create Date: 2025-04-12 09:03:49.401871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51a460cd2273'
down_revision: Union[str, None] = 'ff3f727e564e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chats', 'usage')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('usage', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
