"""add email model

Revision ID: a6f934489210
Revises: 2a9f8b884bc9
Create Date: 2024-05-25 22:29:16.950983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a6f934489210'
down_revision: Union[str, None] = '2a9f8b884bc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email',
                    sa.Column('created_at', sa.DateTime(),
                              server_default=sa.text("TIMEZONE('ASIA/YEKATERINBURG', CURRENT_TIMESTAMP)"),
                              nullable=False),
                    sa.Column('updated_at', sa.DateTime(),
                              server_default=sa.text("TIMEZONE('ASIA/YEKATERINBURG', CURRENT_TIMESTAMP)"),
                              nullable=False),
                    sa.Column('email_id', sa.BigInteger(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('email_id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email')
    # ### end Alembic commands ###
