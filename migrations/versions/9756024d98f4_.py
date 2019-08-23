"""empty message

Revision ID: 9756024d98f4
Revises: 26a6b4da8b01
Create Date: 2019-08-16 14:01:42.659328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9756024d98f4'
down_revision = '26a6b4da8b01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###
