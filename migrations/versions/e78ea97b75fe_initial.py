"""initial

Revision ID: e78ea97b75fe
Revises: 
Create Date: 2024-07-16 19:40:12.525351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e78ea97b75fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('transaction_history')
    with op.batch_alter_table('user__details', schema=None) as batch_op:
        batch_op.add_column(sa.Column('confirm_password', sa.String(length=512), nullable=False))
        batch_op.drop_column('confing_passwird')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user__details', schema=None) as batch_op:
        batch_op.add_column(sa.Column('confing_passwird', sa.VARCHAR(length=512), nullable=False))
        batch_op.drop_column('confirm_password')

    op.create_table('transaction_history',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('from_username', sa.VARCHAR(length=100), nullable=False),
    sa.Column('to_username', sa.VARCHAR(length=100), nullable=False),
    sa.Column('amount', sa.FLOAT(), nullable=False),
    sa.Column('timestamp', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=128), nullable=False),
    sa.Column('email', sa.VARCHAR(length=128), nullable=False),
    sa.Column('phone', sa.VARCHAR(length=512), nullable=False),
    sa.Column('password', sa.VARCHAR(length=512), nullable=False),
    sa.Column('confirm_password', sa.VARCHAR(length=512), nullable=False),
    sa.Column('create_at', sa.DATE(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###
