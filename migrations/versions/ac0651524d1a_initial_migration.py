"""initial migration

Revision ID: ac0651524d1a
Revises: 
Create Date: 2022-12-05 13:35:10.942029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac0651524d1a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('slug', sa.String(length=128), nullable=True),
    sa.Column('views', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_posts_slug'), ['slug'], unique=True)

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.String(length=36), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('stuff', sa.Boolean(), nullable=True),
    sa.Column('superuser', sa.Boolean(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_uid'), ['uid'], unique=True)

    op.create_table('tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.String(length=36), nullable=True),
    sa.Column('value', sa.String(length=40), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['users.uid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user')
    )
    with op.batch_alter_table('tokens', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_tokens_value'), ['value'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tokens', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tokens_value'))

    op.drop_table('tokens')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_uid'))

    op.drop_table('users')
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_posts_slug'))

    op.drop_table('posts')
    # ### end Alembic commands ###
