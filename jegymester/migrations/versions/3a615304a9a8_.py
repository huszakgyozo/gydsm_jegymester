"""empty message

Revision ID: 3a615304a9a8
Revises: 13b311f91c51
Create Date: 2025-03-28 19:13:23.490175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a615304a9a8'
down_revision = '13b311f91c51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('theaters', schema=None) as batch_op:
        batch_op.alter_column('theatname',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('theaters', schema=None) as batch_op:
        batch_op.alter_column('theatname',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###
