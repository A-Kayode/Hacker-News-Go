"""empty message

Revision ID: 2302a4911e3e
Revises: 
Create Date: 2022-09-14 13:08:42.691556

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2302a4911e3e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('parent_id', sa.Integer(), nullable=False))
    op.drop_constraint('comments_ibfk_1', 'comments', type_='foreignkey')
    op.drop_constraint('comments_ibfk_4', 'comments', type_='foreignkey')
    op.drop_constraint('comments_ibfk_2', 'comments', type_='foreignkey')
    op.drop_constraint('comments_ibfk_3', 'comments', type_='foreignkey')
    op.drop_column('comments', 'tn_fk')
    op.drop_column('comments', 'as_fk')
    op.drop_column('comments', 'ss_fk')
    op.drop_column('comments', 'nn_fk')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('nn_fk', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('comments', sa.Column('ss_fk', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('comments', sa.Column('as_fk', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('comments', sa.Column('tn_fk', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('comments_ibfk_3', 'comments', 'ask_stories', ['as_fk'], ['nid'])
    op.create_foreign_key('comments_ibfk_2', 'comments', 'top_news', ['tn_fk'], ['nid'])
    op.create_foreign_key('comments_ibfk_4', 'comments', 'show_stories', ['ss_fk'], ['nid'])
    op.create_foreign_key('comments_ibfk_1', 'comments', 'new_news', ['nn_fk'], ['nid'])
    op.drop_column('comments', 'parent_id')
    # ### end Alembic commands ###
