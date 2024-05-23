"""add exhibit

Revision ID: 2a9f8b884bc9
Revises: dd97fe1ac292
Create Date: 2024-05-22 13:03:43.066569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2a9f8b884bc9'
down_revision: Union[str, None] = 'dd97fe1ac292'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exhibit',
                    sa.Column('created_at', sa.DateTime(),
                              server_default=sa.text("TIMEZONE('ASIA/YEKATERINBURG', CURRENT_TIMESTAMP)"),
                              nullable=False),
                    sa.Column('updated_at', sa.DateTime(),
                              server_default=sa.text("TIMEZONE('ASIA/YEKATERINBURG', CURRENT_TIMESTAMP)"),
                              nullable=False),
                    sa.Column('exhibit_id', sa.BigInteger(), nullable=False),
                    sa.Column('floor', sa.Integer(), nullable=True),
                    sa.Column('number', sa.Float(), nullable=True),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('exhibit_id')
                    )
    op.create_table('exhibit_file',
                    sa.Column('created_at', sa.DateTime(),
                              server_default=sa.text("TIMEZONE('ASIA/YEKATERINBURG', CURRENT_TIMESTAMP)"),
                              nullable=False),
                    sa.Column('updated_at', sa.DateTime(),
                              server_default=sa.text("TIMEZONE('ASIA/YEKATERINBURG', CURRENT_TIMESTAMP)"),
                              nullable=False),
                    sa.Column('exhibit_logo_id', sa.BigInteger(), nullable=False),
                    sa.Column('exhibit_id', sa.BigInteger(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('s3_path', sa.String(), nullable=False),
                    sa.Column('upload_date', sa.DateTime(),
                              server_default=sa.text("TIMEZONE('ASIA/YEKATERINBURG', CURRENT_TIMESTAMP)"),
                              nullable=False),
                    sa.ForeignKeyConstraint(['exhibit_id'], ['exhibit.exhibit_id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('exhibit_logo_id'),
                    sa.UniqueConstraint('exhibit_id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('exhibit_file')
    op.drop_table('exhibit')
    # ### end Alembic commands ###