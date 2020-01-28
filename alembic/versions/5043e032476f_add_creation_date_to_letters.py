"""Add creation_date to letters

Revision ID: 5043e032476f
Revises: 
Create Date: 2020-01-27 23:02:36.436786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5043e032476f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('letters', sa.Column('creation_date', sa.DateTime))


def downgrade():
    pass
