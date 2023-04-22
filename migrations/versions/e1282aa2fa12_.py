"""empty message

Revision ID: e1282aa2fa12
Revises: 16cafb6f7c3b
Create Date: 2023-04-22 20:28:15.412111

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e1282aa2fa12'
down_revision = '16cafb6f7c3b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE TYPE role AS ENUM('admin', 'moderator', 'guest')")
    op.add_column('guest', sa.Column('roles', sa.Enum('admin', 'moderator', 'guest', name='role'), nullable=True,
                                     default='guest'))


def downgrade() -> None:
    op.drop_column('guest', 'roles')
    op.execute('DROP TYPE role')
