"""create table

Revision ID: f659954b8eb1
Revises: b9d39d99899a
Create Date: 2024-09-11 15:33:29.306687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f659954b8eb1'
down_revision: Union[str, None] = 'b9d39d99899a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('api_key', 'endpoint')
    op.drop_column('api_key', 'model')
    op.drop_column('api_key', 'official_key')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_key', sa.Column('official_key', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('api_key', sa.Column('model', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('api_key', sa.Column('endpoint', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
