"""Tests for gap_analyzer service."""

import pytest

from apps.gap_analyzer.main import app
from apps.gap_analyzer.models import GapAnalysis, GapSummary
from apps.gap_analyzer.prioritization import priority_label, sort_by_priority
from tests.conftest import make_client


def _make_gap(analysis_id: str, priority: int) -> GapAnalysis:
    return GapAnalysis(
        analysis_id=analysis_id,
        engagement_id="eng-alpha-001",
        control_id="DE.AE-02",
        gap_type="uncovered_control",
        priority=priority,
        remediation="Deploy detection rule for T1486.",
    )


@pytest.mark.asyncio
async def test_health_returns_200():
    async with make_client(app) as client:
        resp = await client.get("/health")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_health_service_name():
    async with make_client(app) as client:
        resp = await client.get("/health")
    assert resp.json()["service"] == "gap-analyzer"


def test_priority_label_critical():
    assert priority_label(1) == "Critical"


def test_priority_label_informational():
    assert priority_label(5) == "Informational"


def test_priority_label_unknown():
    assert priority_label(99) == "Unknown"


def test_sort_by_priority_orders_correctly():
    gaps = [_make_gap("g3", 3), _make_gap("g1", 1), _make_gap("g2", 2)]
    result = sort_by_priority(gaps)
    assert [g.analysis_id for g in result] == ["g1", "g2", "g3"]


def test_gap_analysis_model():
    gap = _make_gap("gap-001", 2)
    assert gap.gap_type == "uncovered_control"


def test_gap_summary_model():
    summary = GapSummary(
        engagement_id="eng-alpha-001",
        total_gaps=3,
        critical_gaps=1,
        gaps=[_make_gap("g1", 1)],
    )
    assert summary.critical_gaps == 1
