"""empty message

Revision ID: 8b8a75ba1182
Revises: 6d38f1481dc1
Create Date: 2022-01-15 00:39:29.055622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b8a75ba1182'
down_revision = '6d38f1481dc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('created_at', sa.DATETIME(), nullable=True))
    op.add_column('user', sa.Column('created_at', sa.DATETIME(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'created_at')
    op.drop_column('post', 'created_at')
    # ### end Alembic commands ###
