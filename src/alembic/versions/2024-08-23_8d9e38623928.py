"""create table

Revision ID: 8d9e38623928
Revises: 71a328ad83eb
Create Date: 2024-08-23 09:43:11.402342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8d9e38623928'
down_revision: Union[str, None] = '71a328ad83eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('data_electricity_price')
    op.drop_table('data_electricity_price_query')
    op.drop_table('data_electricity_price_test')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data_electricity_price_test',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('metadata_', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('node_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('embedding', sa.NullType(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='data_electricity_price_test_pkey')
    )
    op.create_table('data_electricity_price_query',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('metadata_', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('node_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('embedding', sa.NullType(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='data_electricity_price_query_pkey')
    )
    op.create_table('data_electricity_price',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('metadata_', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('node_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('embedding', sa.NullType(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='data_electricity_price_pkey')
    )
    # ### end Alembic commands ###
