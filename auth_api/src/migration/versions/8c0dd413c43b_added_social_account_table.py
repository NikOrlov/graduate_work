"""Added social account table

Revision ID: 8c0dd413c43b
Revises: f88885364854
Create Date: 2024-02-08 15:03:36.692722

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8c0dd413c43b"
down_revision = "f88885364854"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "social_account",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("social_id", sa.String(length=255), nullable=True),
        sa.Column("social_name", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_unique_constraint(None, "role", ["id"])
    op.create_unique_constraint(None, "token_pair", ["id"])
    op.create_unique_constraint(None, "user", ["id"])
    op.create_unique_constraint(None, "userrole", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "userrole", type_="unique")
    op.drop_constraint(None, "user", type_="unique")
    op.drop_constraint(None, "token_pair", type_="unique")
    op.drop_constraint(None, "role", type_="unique")
    op.drop_table("social_account")
    # ### end Alembic commands ###
