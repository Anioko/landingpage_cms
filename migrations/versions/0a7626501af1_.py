"""empty message

Revision ID: 0a7626501af1
Revises: c60b807c925f
Create Date: 2020-09-11 18:09:06.489717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a7626501af1'
down_revision = 'c60b807c925f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('organisation_name', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'organisation_name')
    # ### end Alembic commands ###
