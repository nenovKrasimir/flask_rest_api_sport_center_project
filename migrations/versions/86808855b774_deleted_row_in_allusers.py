"""deleted row in allusers

Revision ID: 86808855b774
Revises: 29d28810b02b
Create Date: 2023-04-13 22:54:24.527110

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '86808855b774'
down_revision = '29d28810b02b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('registered_users', schema=None) as batch_op:
        batch_op.drop_column('active_subscriptions')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('registered_users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active_subscriptions', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
