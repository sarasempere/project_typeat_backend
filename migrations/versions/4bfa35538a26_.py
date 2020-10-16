"""empty message

Revision ID: 4bfa35538a26
Revises: 5e85166e9a6e
Create Date: 2020-10-15 17:33:37.523202

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4bfa35538a26'
down_revision = '5e85166e9a6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('phone', table_name='user')
    op.drop_column('user', 'role')
    op.drop_column('user', 'phone')
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'gender')
    op.drop_column('user', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('name', mysql.VARCHAR(length=120), nullable=False))
    op.add_column('user', sa.Column('gender', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('last_name', mysql.VARCHAR(length=120), nullable=False))
    op.add_column('user', sa.Column('phone', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('role', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.create_index('phone', 'user', ['phone'], unique=True)
    # ### end Alembic commands ###