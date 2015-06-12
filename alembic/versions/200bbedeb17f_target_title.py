"""target_title

Revision ID: 200bbedeb17f
Revises: 36c68d24bd98
Create Date: 2015-06-11 15:38:02.562773

"""

# revision identifiers, used by Alembic.
revision = '200bbedeb17f'
down_revision = '36c68d24bd98'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('campaign_target', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=100), nullable=True))

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('campaign_target', schema=None) as batch_op:
        batch_op.drop_column('title')

    ### end Alembic commands ###