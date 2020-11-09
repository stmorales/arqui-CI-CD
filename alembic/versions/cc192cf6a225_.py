"""empty message

Revision ID: cc192cf6a225
Revises: d409c171c396
Create Date: 2020-11-02 01:40:28.308603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc192cf6a225'
down_revision = 'd409c171c396'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('admin', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('email', sa.String(), nullable=True))
    op.add_column('user', sa.Column('password', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password')
    op.drop_column('user', 'email')
    op.drop_column('user', 'admin')
    # ### end Alembic commands ###