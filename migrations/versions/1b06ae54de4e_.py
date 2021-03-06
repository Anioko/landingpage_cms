"""empty message

Revision ID: 1b06ae54de4e
Revises: c9c2bcfee4a7
Create Date: 2020-09-14 21:47:42.391294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b06ae54de4e'
down_revision = 'c9c2bcfee4a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('services', 'service_description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('services', sa.Column('service_description', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
