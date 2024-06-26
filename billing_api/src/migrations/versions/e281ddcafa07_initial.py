"""initial

Revision ID: e281ddcafa07
Revises: 937ea9781c57
Create Date: 2024-04-24 14:50:59.611645

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e281ddcafa07"
down_revision: Union[str, None] = "937ea9781c57"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user_subscriptions",
        "auto_prolongate",
        existing_type=sa.BOOLEAN(),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user_subscriptions",
        "auto_prolongate",
        existing_type=sa.BOOLEAN(),
        nullable=True,
    )
    # ### end Alembic commands ###
