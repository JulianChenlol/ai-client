"""create table

Revision ID: 2794b6553afb
Revises: 1aa4c06fe2cf
Create Date: 2024-08-14 11:34:04.521014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2794b6553afb'
down_revision: Union[str, None] = '1aa4c06fe2cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('llm_model', sa.Column('server_port', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('llm_model', 'server_port')
    # ### end Alembic commands ###
