"""new delivery model added

Revision ID: d0ad1fe20a76
Revises: c4a90df8e687
Create Date: 2023-04-18 21:32:56.420947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0ad1fe20a76'
down_revision = 'c4a90df8e687'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('delivered_packages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('delivered_by', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('delivered_packages')
    # ### end Alembic commands ###
