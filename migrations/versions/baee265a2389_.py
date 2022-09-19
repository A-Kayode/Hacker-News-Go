"""empty message

Revision ID: baee265a2389
Revises: 5ab639fca601
Create Date: 2022-09-17 19:29:00.572470

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'baee265a2389'
down_revision = '5ab639fca601'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('show_stories')
    op.drop_table('top_news')
    op.drop_table('ask_stories')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ask_stories',
    sa.Column('nid', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('itemid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('ntype', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('written_by', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('comment_no', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('created', mysql.DATETIME(), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('text', mysql.TEXT(), nullable=False),
    sa.Column('url', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('nid'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('top_news',
    sa.Column('nid', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('itemid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('ntype', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('written_by', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('comment_no', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('created', mysql.DATETIME(), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('text', mysql.TEXT(), nullable=False),
    sa.Column('url', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('nid'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('show_stories',
    sa.Column('nid', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('itemid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('ntype', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('written_by', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('comment_no', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('created', mysql.DATETIME(), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('text', mysql.TEXT(), nullable=False),
    sa.Column('url', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('nid'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
