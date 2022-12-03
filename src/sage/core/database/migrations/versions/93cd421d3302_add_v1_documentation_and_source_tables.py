"""add v1 documentation and source tables

Revision ID: 93cd421d3302
Revises:
Create Date: 2022-12-02 20:17:19.223346

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "93cd421d3302"
down_revision = None
branch_labels = None
depends_on = None

programming_language_enum = sa.Enum(
    "python",
    "text",
    "other",
    name="programminglanguage",
)
language_code_enum = sa.Enum(
    "bg",
    "cs",
    "da",
    "de",
    "el",
    "en_GB",
    "en_US",
    "es_ES",
    "fi",
    "fr",
    "hi",
    "hr",
    "it",
    "ja",
    "ko",
    "lt",
    "hu",
    "nl",
    "no",
    "pl",
    "pt_BR",
    "ro",
    "ru",
    "sv_SE",
    "th",
    "tr",
    "uk",
    "vi",
    "zh_CN",
    "zh_TW",
    name="languagecode",
)


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "doc_packages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("homepage", sa.String(length=512), nullable=False),
        sa.Column(
            "programming_language",
            programming_language_enum,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "doc_sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("package_id", sa.Integer(), nullable=True),
        sa.Column("preview", sa.Boolean(), nullable=False),
        sa.Column("inventory_url", sa.String(length=250), nullable=True),
        sa.Column("human_friendly_url", sa.String(length=250), nullable=False),
        sa.Column("version", sa.String(length=30), nullable=True),
        sa.Column(
            "language_code",
            language_code_enum,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["package_id"],
            ["doc_packages.id"],
            name="doc_sources_package_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("doc_sources")
    op.drop_table("doc_packages")
    # ### end Alembic commands ###

    language_code_enum.drop(op.get_bind())
    programming_language_enum.drop(op.get_bind())
