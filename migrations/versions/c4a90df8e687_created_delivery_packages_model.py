"""created delivery packages model

Revision ID: c4a90df8e687
Revises: 26c8c61f155e
Create Date: 2023-04-17 22:14:48.977454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4a90df8e687'
down_revision = '26c8c61f155e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('delivery_packages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipient_name', sa.String(), nullable=False),
    sa.Column('recipient_region', sa.String(), nullable=False),
    sa.Column('recipient_contact', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('expected_delivery_date', sa.Date(), nullable=False),
    sa.Column('delivered_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['delivered_by'], ['delivery_guys.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('delivery_packages')
    # ### end Alembic commands ###
