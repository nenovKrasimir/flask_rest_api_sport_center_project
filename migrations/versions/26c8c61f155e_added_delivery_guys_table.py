"""added delivery guys table

Revision ID: 26c8c61f155e
Revises: cd71a2f7f144
Create Date: 2023-04-17 21:33:05.198636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26c8c61f155e'
down_revision = 'cd71a2f7f144'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('delivery_guys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('region', sa.String(), nullable=False),
    sa.Column('contact', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('delivery_guys')
    # ### end Alembic commands ###
