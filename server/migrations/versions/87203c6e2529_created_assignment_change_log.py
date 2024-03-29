"""created assignment change log

Revision ID: 87203c6e2529
Revises: a3828e1b5d00
Create Date: 2024-02-17 16:54:50.681067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87203c6e2529'
down_revision = 'a3828e1b5d00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assignment_change_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('assignment_id', sa.Integer(), nullable=True),
    sa.Column('detail', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['assignment_id'], ['assignments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assignment_change_logs')
    # ### end Alembic commands ###
