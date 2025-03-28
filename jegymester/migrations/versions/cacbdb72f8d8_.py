"""empty message

Revision ID: cacbdb72f8d8
Revises: b1409814eeaf
Create Date: 2025-03-29 00:39:23.527287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cacbdb72f8d8'
down_revision = 'b1409814eeaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('payment_status',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.Enum('Pending', 'Succesful', 'Canceled', name='statusenum'),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('payment_status',
               existing_type=sa.Enum('Pending', 'Succesful', 'Canceled', name='statusenum'),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###
