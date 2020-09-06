"""empty message

Revision ID: 2da0c70186db
Revises: beeb7b850ddc
Create Date: 2020-09-06 15:23:19.861375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2da0c70186db'
down_revision = 'beeb7b850ddc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('htmls',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('block_content_one', sa.Text(), nullable=True),
    sa.Column('html_code_one', sa.Text(), nullable=True),
    sa.Column('html_code_two', sa.Text(), nullable=True),
    sa.Column('html_code_three', sa.Text(), nullable=True),
    sa.Column('html_code_four', sa.Text(), nullable=True),
    sa.Column('organisation_id', sa.Integer(), nullable=False),
    sa.Column('owner_organisation', sa.String(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['organisation_id'], ['organisations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('socials',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('twitter_name', sa.String(length=25), nullable=True),
    sa.Column('facebook_name', sa.String(length=25), nullable=True),
    sa.Column('instagram_name', sa.String(length=25), nullable=True),
    sa.Column('linkedin_name', sa.String(length=25), nullable=True),
    sa.Column('tiktok_name', sa.String(length=25), nullable=True),
    sa.Column('snap_chat_name', sa.String(length=25), nullable=True),
    sa.Column('youtube', sa.String(length=25), nullable=True),
    sa.Column('organisation_id', sa.Integer(), nullable=False),
    sa.Column('owner_organisation', sa.String(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['organisation_id'], ['organisations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('facebook_name'),
    sa.UniqueConstraint('instagram_name'),
    sa.UniqueConstraint('linkedin_name'),
    sa.UniqueConstraint('snap_chat_name'),
    sa.UniqueConstraint('tiktok_name'),
    sa.UniqueConstraint('twitter_name'),
    sa.UniqueConstraint('youtube')
    )
    op.create_table('testimonials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_name', sa.String(), nullable=True),
    sa.Column('testimonial_title', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('organisation_id', sa.Integer(), nullable=False),
    sa.Column('owner_organisation', sa.String(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['organisation_id'], ['organisations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trackings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('google_analytics_id', sa.String(length=25), nullable=True),
    sa.Column('other_tracking_analytics_one', sa.Text(), nullable=True),
    sa.Column('other_tracking_analytics_two', sa.Text(), nullable=True),
    sa.Column('other_tracking_analytics_three', sa.Text(), nullable=True),
    sa.Column('other_tracking_analytics_four', sa.Text(), nullable=True),
    sa.Column('other_tracking_analytics_five', sa.Text(), nullable=True),
    sa.Column('other_tracking_analytics_six', sa.Text(), nullable=True),
    sa.Column('organisation_id', sa.Integer(), nullable=False),
    sa.Column('owner_organisation', sa.String(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['organisation_id'], ['organisations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('google_analytics_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trackings')
    op.drop_table('testimonials')
    op.drop_table('socials')
    op.drop_table('htmls')
    # ### end Alembic commands ###
