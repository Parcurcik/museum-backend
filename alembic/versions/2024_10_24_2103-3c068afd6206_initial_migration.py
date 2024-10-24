"""initial migration

Revision ID: 3c068afd6206
Revises: 
Create Date: 2024-10-24 21:03:32.803948

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3c068afd6206"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "event_genre",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_event_genre")),
    )
    op.create_table(
        "event_tag",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_event_tag")),
    )
    op.create_table(
        "location",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_location")),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("number", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
        sa.UniqueConstraint("email", name=op.f("uq_user_email")),
        sa.UniqueConstraint("number", name=op.f("uq_user_number")),
    )
    op.create_table(
        "visitor_category",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_visitor_category")),
    )
    op.create_table(
        "event",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("disabilities", sa.Boolean(), nullable=True),
        sa.Column("location_id", sa.BigInteger(), nullable=True),
        sa.Column("genre_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["event_genre.id"],
            name=op.f("fk_event_genre_id_event_genre"),
        ),
        sa.ForeignKeyConstraint(
            ["location_id"],
            ["location.id"],
            name=op.f("fk_event_location_id_location"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_event")),
    )
    op.create_table(
        "refresh_token",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("expires", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("fk_refresh_token_user_id_user"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_refresh_token")),
        sa.UniqueConstraint("token", name=op.f("uq_refresh_token_token")),
    )
    op.create_table(
        "user_role",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column(
            "role",
            sa.Enum("admin", "employee", "user", name="userroleenum"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("fk_user_role_user_id_user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_role")),
    )
    op.create_table(
        "event_tag_association",
        sa.Column("event_id", sa.BigInteger(), nullable=False),
        sa.Column("tag_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["event.id"],
            name=op.f("fk_event_tag_association_event_id_event"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["event_tag.id"],
            name=op.f("fk_event_tag_association_tag_id_event_tag"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "event_id", "tag_id", name=op.f("pk_event_tag_association")
        ),
    )
    op.create_table(
        "event_visitor_category_association",
        sa.Column("event_id", sa.BigInteger(), nullable=False),
        sa.Column("visitor_category_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["event.id"],
            name=op.f("fk_event_visitor_category_association_event_id_event"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["visitor_category_id"],
            ["visitor_category.id"],
            name=op.f(
                "fk_event_visitor_category_association_visitor_category_id_visitor_category"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "event_id",
            "visitor_category_id",
            name=op.f("pk_event_visitor_category_association"),
        ),
    )
    op.create_table(
        "ticket",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("event_id", sa.BigInteger(), nullable=False),
        sa.Column("customer_id", sa.BigInteger(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("available", "booked", "sold", name="ticketstatusenum"),
            nullable=True,
        ),
        sa.Column(
            "type",
            sa.Enum("adult", "discount", "child", name="tickettypeenum"),
            nullable=False,
        ),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("booked_at", sa.DateTime(), nullable=True),
        sa.Column("purchased_at", sa.DateTime(), nullable=True),
        sa.Column("event_date", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["user.id"],
            name=op.f("fk_ticket_customer_id_user"),
        ),
        sa.ForeignKeyConstraint(
            ["event_id"], ["event.id"], name=op.f("fk_ticket_event_id_event")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_ticket")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ticket")
    op.drop_table("event_visitor_category_association")
    op.drop_table("event_tag_association")
    op.drop_table("user_role")
    op.drop_table("refresh_token")
    op.drop_table("event")
    op.drop_table("visitor_category")
    op.drop_table("user")
    op.drop_table("location")
    op.drop_table("event_tag")
    op.drop_table("event_genre")
    # ### end Alembic commands ###
