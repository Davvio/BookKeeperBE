"""phase1: items, structure_settings, item_values

Revision ID: c509ef01678f
Revises: 6ddc8bef9bbc
Create Date: 2025-08-09 01:48:34.202096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c509ef01678f'
down_revision: Union[str, Sequence[str], None] = '6ddc8bef9bbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "item_categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.UniqueConstraint("code", name="uq_item_categories_code"),
    )

    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("code", sa.String(length=60), nullable=False, unique=True),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("stack_size", sa.Integer(), nullable=False, server_default="64"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_by_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    # unique case-insensitive su name
    op.execute('CREATE UNIQUE INDEX uq_items_name_ci ON items ((lower(name)));')

    op.create_table(
        "structure_settings",
        sa.Column("structure_id", sa.String(length=50), primary_key=True),
        sa.Column("currency_item_id", sa.Integer(), sa.ForeignKey("items.id")),
        sa.Column("updated_by_user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "item_values",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("structure_id", sa.String(length=50), nullable=False),
        sa.Column("item_id", sa.Integer(), sa.ForeignKey("items.id"), nullable=False),
        sa.Column("value_in_currency", sa.Numeric(20, 6), nullable=False),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("structure_id", "item_id", "effective_from", name="uq_item_values_hist"),
    )
    op.create_index("ix_item_values_lookup", "item_values", ["structure_id", "item_id", "effective_from"])
    op.execute(
        "ALTER TABLE item_values ADD CONSTRAINT chk_item_values_range "
        "CHECK (value_in_currency >= 0.001 AND value_in_currency <= 1000000)"
    )

def downgrade():
    op.drop_constraint("chk_item_values_range", "item_values", type_="check")
    op.drop_index("ix_item_values_lookup", table_name="item_values")
    op.drop_table("item_values")
    op.drop_table("structure_settings")
    op.execute("DROP INDEX IF EXISTS uq_items_name_ci;")
    op.drop_table("items")
    op.drop_table("item_categories")