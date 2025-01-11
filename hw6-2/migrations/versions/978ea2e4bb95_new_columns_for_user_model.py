"""new columns for user model

Revision ID: 978ea2e4bb95
Revises: e7d2653e86a7
Create Date: 2025-01-11 16:42:04.133659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '978ea2e4bb95'
down_revision = 'e7d2653e86a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_number', sa.String(length=15), nullable=False))
        batch_op.add_column(sa.Column('birthday', sa.String(length=15), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('birthday')
        batch_op.drop_column('phone_number')

    # ### end Alembic commands ###
