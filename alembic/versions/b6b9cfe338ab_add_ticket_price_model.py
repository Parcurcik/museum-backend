"""add ticket price model

Revision ID: b6b9cfe338ab
Revises: 470959564138
Create Date: 2024-05-17 19:51:40.262506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b6b9cfe338ab'
down_revision: Union[str, None] = '470959564138'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_price',
                    sa.Column('price_id', sa.BigInteger(), nullable=False),
                    sa.Column('event_id', sa.BigInteger(), nullable=False),
                    sa.Column('price_type', sa.Enum('adult', 'discount', 'child', name='tickettypeenum'),
                              nullable=False),
                    sa.Column('price', sa.Float(), nullable=False),
                    sa.ForeignKeyConstraint(['event_id'], ['event.event_id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('price_id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum(name='tickettypeenum').drop(op.get_bind(), checkfirst=False)
    op.drop_table('event_price')
    # ### end Alembic commands ###
