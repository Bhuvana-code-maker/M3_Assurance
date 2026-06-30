"""Initial schema — all 8 tables from M3 Assurance tech doc §5.2.

Revision ID: 0001
Revises:
Create Date: 2026-07-01
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "frameworks",
        sa.Column("framework_id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("version", sa.String(32), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column(
            "regions", sa.ARRAY(sa.String(64)), nullable=False, server_default="{}"
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    op.create_table(
        "controls",
        sa.Column("control_id", sa.String(64), primary_key=True),
        sa.Column(
            "framework_id",
            sa.String(64),
            sa.ForeignKey("frameworks.framework_id"),
            nullable=False,
        ),
        sa.Column("category", sa.String(255), nullable=False),
        sa.Column("name", sa.String(512), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column(
            "attack_mapping",
            sa.ARRAY(sa.String(32)),
            nullable=False,
            server_default="{}",
        ),
    )
    op.create_index("ix_controls_framework_id", "controls", ["framework_id"])

    op.create_table(
        "control_statuses",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("engagement_id", sa.String(64), nullable=False),
        sa.Column(
            "control_id",
            sa.String(64),
            sa.ForeignKey("controls.control_id"),
            nullable=False,
        ),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("evidence_hash", sa.String(64)),
        sa.Column(
            "last_updated",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )
    op.create_index(
        "ix_control_statuses_engagement", "control_statuses", ["engagement_id"]
    )

    op.create_table(
        "evidence_links",
        sa.Column("link_id", sa.String(64), primary_key=True),
        sa.Column(
            "control_id",
            sa.String(64),
            sa.ForeignKey("controls.control_id"),
            nullable=False,
        ),
        sa.Column("verdict_id", sa.String(64), nullable=False),
        sa.Column("evidence_hash", sa.String(64), nullable=False),
        sa.Column("chain_position", sa.Integer, nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )
    op.create_index("ix_evidence_links_control_id", "evidence_links", ["control_id"])
    op.create_index("ix_evidence_links_verdict_id", "evidence_links", ["verdict_id"])

    op.create_table(
        "resilience_scores",
        sa.Column("score_id", sa.String(64), primary_key=True),
        sa.Column("engagement_id", sa.String(64), nullable=False),
        sa.Column("composite", sa.Numeric(5, 1), nullable=False),
        sa.Column("coverage", sa.Numeric(5, 1), nullable=False),
        sa.Column("detection", sa.Numeric(5, 1), nullable=False),
        sa.Column("evidence", sa.Numeric(5, 1), nullable=False),
        sa.Column("band", sa.String(16), nullable=False),
        sa.Column(
            "calculated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )
    op.create_index(
        "ix_resilience_scores_engagement", "resilience_scores", ["engagement_id"]
    )

    op.create_table(
        "gap_analyses",
        sa.Column("analysis_id", sa.String(64), primary_key=True),
        sa.Column("engagement_id", sa.String(64), nullable=False),
        sa.Column(
            "control_id",
            sa.String(64),
            sa.ForeignKey("controls.control_id"),
            nullable=False,
        ),
        sa.Column("gap_type", sa.String(32), nullable=False),
        sa.Column("priority", sa.SmallInteger, nullable=False),
        sa.Column("remediation", sa.Text, nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )
    op.create_index("ix_gap_analyses_engagement", "gap_analyses", ["engagement_id"])

    op.create_table(
        "reports",
        sa.Column("report_id", sa.String(64), primary_key=True),
        sa.Column("engagement_id", sa.String(64), nullable=False),
        sa.Column("framework_ids", sa.ARRAY(sa.String(64)), nullable=False),
        sa.Column("score", sa.Numeric(5, 1)),
        sa.Column("format", sa.String(8), nullable=False),
        sa.Column("content_hash", sa.String(64)),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )
    op.create_index("ix_reports_engagement", "reports", ["engagement_id"])

    op.create_table(
        "cross_walks",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "source_control_id",
            sa.String(64),
            sa.ForeignKey("controls.control_id"),
            nullable=False,
        ),
        sa.Column(
            "target_control_id",
            sa.String(64),
            sa.ForeignKey("controls.control_id"),
            nullable=False,
        ),
        sa.Column("equivalence_level", sa.String(16), nullable=False),
    )
    op.create_index("ix_cross_walks_source", "cross_walks", ["source_control_id"])


def downgrade() -> None:
    op.drop_table("cross_walks")
    op.drop_table("reports")
    op.drop_table("gap_analyses")
    op.drop_table("resilience_scores")
    op.drop_table("evidence_links")
    op.drop_table("control_statuses")
    op.drop_table("controls")
    op.drop_table("frameworks")
