"""created assignment and project tables

Revision ID: a3828e1b5d00
Revises: 4dbfe7c4d616
Create Date: 2024-02-12 21:55:26.560960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3828e1b5d00'
down_revision = '4dbfe7c4d616'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sales_order', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('expected_end_date', sa.Date(), nullable=False),
    sa.Column('customer_name', sa.String(), nullable=True),
    sa.Column('sale_price', sa.Float(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assignments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('comments', sa.String(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('expected_end_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assignments')
    op.drop_table('projects')
    # ### end Alembic commands ###
