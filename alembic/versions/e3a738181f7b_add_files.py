"""add files

Revision ID: e3a738181f7b
Revises: dee77a46900d
Create Date: 2024-04-21 13:04:06.541714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3a738181f7b'
down_revision: Union[str, None] = 'dee77a46900d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_file',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('ASIA/YEKATERINBURG', CURRENT_TIMESTAMP)"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('ASIA/YEKATERINBURG', CURRENT_TIMESTAMP)"), nullable=False),
    sa.Column('event_logo_id', sa.BigInteger(), nullable=False),
    sa.Column('event_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('s3_path', sa.String(), nullable=False),
    sa.Column('upload_date', sa.DateTime(), server_default=sa.text("TIMEZONE('ASIA/YEKATERINBURG', CURRENT_TIMESTAMP)"), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.event_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('event_logo_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_file')
    # ### end Alembic commands ###
