"""init: replaced old broken migrations

Revision ID: a8139aab8261
Revises: 
Create Date: 2024-09-02 13:45:12.531710

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = 'a8139aab8261'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('email_subscription', sa.Boolean(), nullable=True),
    sa.Column('is_activated', sa.Boolean(), nullable=True),
    sa.Column('activation_link', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('texts',
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('added_by', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('is_public', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['added_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_texts_id'), 'texts', ['id'], unique=False)
    op.create_table('text_ratings',
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('rated_text', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('rated_by', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['rated_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['rated_text'], ['texts.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('rated_by', 'rated_text', name='uix_1')
    )
    op.create_index(op.f('ix_text_ratings_id'), 'text_ratings', ['id'], unique=False)
    op.create_table('typing_sessions',
    sa.Column('stats', sa.JSON(), nullable=True),
    sa.Column('duration_in_seconds', sa.Integer(), nullable=False),
    sa.Column('text_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['text_id'], ['texts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_typing_sessions_id'), 'typing_sessions', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_typing_sessions_id'), table_name='typing_sessions')
    op.drop_table('typing_sessions')
    op.drop_index(op.f('ix_text_ratings_id'), table_name='text_ratings')
    op.drop_table('text_ratings')
    op.drop_index(op.f('ix_texts_id'), table_name='texts')
    op.drop_table('texts')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
