"""empty message

Revision ID: b1409814eeaf
Revises: f8b4905995ac
Create Date: 2025-03-29 00:09:43.655577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1409814eeaf'
down_revision = 'f8b4905995ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movies', schema=None) as batch_op:
        batch_op.alter_column('deleted',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(),
               existing_nullable=False)

    with op.batch_alter_table('screenings', schema=None) as batch_op:
        batch_op.alter_column('deleted',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(),
               existing_nullable=False)

    with op.batch_alter_table('ticketorders', schema=None) as batch_op:
        batch_op.alter_column('ticket_active',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticketorders', schema=None) as batch_op:
        batch_op.alter_column('ticket_active',
               existing_type=sa.Boolean(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('screenings', schema=None) as batch_op:
        batch_op.alter_column('deleted',
               existing_type=sa.Boolean(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('movies', schema=None) as batch_op:
        batch_op.alter_column('deleted',
               existing_type=sa.Boolean(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
