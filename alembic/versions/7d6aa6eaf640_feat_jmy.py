"""feat: jmy

Revision ID: 7d6aa6eaf640
Revises: 0bdf3abd5213
Create Date: 2025-03-05 00:15:09.139612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d6aa6eaf640'
down_revision: Union[str, None] = '0bdf3abd5213'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jmy_company',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('size', sa.String(length=255), nullable=False),
    sa.Column('research', sa.String(length=255), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('jmy_time_series',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('b_assigned', sa.Integer(), nullable=False),
    sa.Column('b_new', sa.Integer(), nullable=False),
    sa.Column('b_old', sa.Integer(), nullable=False),
    sa.Column('a_assigned', sa.Integer(), nullable=False),
    sa.Column('a_new', sa.Integer(), nullable=False),
    sa.Column('a_old', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['jmy_company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('jmy_time_series')
    op.drop_table('jmy_company')
    # ### end Alembic commands ###
