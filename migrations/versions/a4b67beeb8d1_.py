"""empty message

Revision ID: a4b67beeb8d1
Revises: c5ab278334e4
Create Date: 2020-09-13 19:19:05.766016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4b67beeb8d1'
down_revision = 'c5ab278334e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('services', sa.Column('service_icon', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('services', 'service_icon')
    # ### end Alembic commands ###
