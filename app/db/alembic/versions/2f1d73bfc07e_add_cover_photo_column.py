"""add cover photo column

Revision ID: 2f1d73bfc07e
Revises: 8fdba1519f85
Create Date: 2025-08-10 08:18:58.650320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f1d73bfc07e'
down_revision: Union[str, Sequence[str], None] = '8fdba1519f85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('cover_photo_id', sa.Integer()))



def downgrade() -> None:
    op.drop_column('posts', 'cover_photo_id')
