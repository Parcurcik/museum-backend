"""del surname from user model

Revision ID: 9852b3de9981
Revises: ec427d71299a
Create Date: 2024-10-11 23:15:34.387462

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9852b3de9981"
down_revision: Union[str, None] = "ec427d71299a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "surname")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column("surname", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
