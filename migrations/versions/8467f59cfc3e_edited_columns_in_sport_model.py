"""edited columns in sport model

Revision ID: 8467f59cfc3e
Revises: ec78f0062240
Create Date: 2023-04-15 18:50:56.450503

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8467f59cfc3e'
down_revision = 'ec78f0062240'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coaches', schema=None) as batch_op:
        batch_op.add_column(sa.Column('model_type', sa.Enum('boxing', 'swimming', 'fitness', name='coachtype'), nullable=False))
        batch_op.drop_column('type')

    with op.batch_alter_table('sports', schema=None) as batch_op:
        batch_op.add_column(sa.Column('model_type', sa.Enum('boxing', 'swimming', 'fitness', name='sporttype'), nullable=False))
        batch_op.drop_constraint('sports_sport_type_key', type_='unique')
        batch_op.create_unique_constraint(None, ['model_type'])
        batch_op.drop_column('sport_type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sports', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sport_type', postgresql.ENUM('boxing', 'swimming', 'fitness', name='sporttype'), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_unique_constraint('sports_sport_type_key', ['sport_type'])
        batch_op.drop_column('model_type')

    with op.batch_alter_table('coaches', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', postgresql.ENUM('boxing', 'swimming', 'fitness', name='coachtype'), autoincrement=False, nullable=False))
        batch_op.drop_column('model_type')

    # ### end Alembic commands ###
