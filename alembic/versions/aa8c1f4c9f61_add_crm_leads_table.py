"""add crm leads table

Revision ID: aa8c1f4c9f61
Revises: bb7b3d24225a
Create Date: 2026-04-24 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aa8c1f4c9f61"
down_revision: Union[str, None] = "bb7b3d24225a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


lead_source_enum = sa.Enum(
    "WEBSITE",
    "INSTAGRAM",
    "TELEGRAM",
    "REFERRAL",
    "OTHER",
    name="leadsource",
)

lead_status_enum = sa.Enum(
    "NEW",
    "IN_PROGRESS",
    "WON",
    "LOST",
    name="leadstatus",
)


def upgrade() -> None:
    lead_source_enum.create(op.get_bind(), checkfirst=True)
    lead_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "crm_leads",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column(
            "source",
            lead_source_enum,
            nullable=False,
            server_default="OTHER",
        ),
        sa.Column(
            "status",
            lead_status_enum,
            nullable=False,
            server_default="NEW",
        ),
        sa.Column("assigned_manager_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["assigned_manager_id"], ["user_profiles.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("crm_leads")
    lead_status_enum.drop(op.get_bind(), checkfirst=True)
    lead_source_enum.drop(op.get_bind(), checkfirst=True)
