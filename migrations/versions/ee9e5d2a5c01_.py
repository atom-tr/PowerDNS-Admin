"""empty message

Revision ID: ee9e5d2a5c01
Revises: 6ea7dc05f496
Create Date: 2022-08-26 02:24:25.883851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee9e5d2a5c01'
down_revision = '6ea7dc05f496'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('domain_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain_id', sa.Integer(), nullable=True),
    sa.Column('cus_name', sa.String(length=64), nullable=True),
    sa.Column('cus_email', sa.String(length=64), nullable=True),
    sa.Column('cus_phone', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['domain_id'], ['domain.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('url_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('content', sa.String(length=255), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('domain_id', sa.Integer(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['domain_id'], ['domain.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_url_record_comment'), 'url_record', ['comment'], unique=False)
    op.create_index(op.f('ix_url_record_content'), 'url_record', ['content'], unique=False)
    op.create_index(op.f('ix_url_record_name'), 'url_record', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_url_record_name'), table_name='url_record')
    op.drop_index(op.f('ix_url_record_content'), table_name='url_record')
    op.drop_index(op.f('ix_url_record_comment'), table_name='url_record')
    op.drop_table('url_record')
    op.drop_table('domain_info')
    # ### end Alembic commands ###