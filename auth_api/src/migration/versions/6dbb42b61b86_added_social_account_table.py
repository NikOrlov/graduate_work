"""Added social account table

Revision ID: 6dbb42b61b86
Revises: 8c0dd413c43b
Create Date: 2024-02-08 15:22:43.793406

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "6dbb42b61b86"
down_revision = "8c0dd413c43b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "social_account", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "social_account", type_="unique")
    # ### end Alembic commands ###
