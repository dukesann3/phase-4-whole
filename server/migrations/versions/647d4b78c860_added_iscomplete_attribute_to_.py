"""Added isComplete attribute to assignment and project

Revision ID: 647d4b78c860
Revises: b8f76cfcca28
Create Date: 2024-02-22 22:21:59.455730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '647d4b78c860'
down_revision = 'b8f76cfcca28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assignments', sa.Column('isComplete', sa.Boolean(), nullable=False))
    op.add_column('projects', sa.Column('isComplete', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'isComplete')
    op.drop_column('assignments', 'isComplete')
    # ### end Alembic commands ###
