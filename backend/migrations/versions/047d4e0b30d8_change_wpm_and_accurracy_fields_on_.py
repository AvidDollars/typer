"""change WPM and accurracy fields on 'typing_sessions' table to be less precise

Revision ID: 047d4e0b30d8
Revises: 9d1b887fdf6e
Create Date: 2025-04-23 14:07:54.942148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '047d4e0b30d8'
down_revision = '9d1b887fdf6e'
branch_labels = None
depends_on = None


# NOTE: created manually
def upgrade() -> None:
    op.execute('ALTER Table typing_sessions ALTER COLUMN gross_wpm TYPE DECIMAL(6,2)')
    op.execute('ALTER Table typing_sessions ALTER COLUMN net_wpm TYPE DECIMAL(6,2)')
    op.execute('ALTER Table typing_sessions ALTER COLUMN accuracy TYPE DECIMAL(5,2)')


def downgrade() -> None:
    raise ValueError("Missing downgrade logic.")