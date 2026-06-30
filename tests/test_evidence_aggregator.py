"""Tests for evidence_aggregator service."""
import pytest
from apps.evidence_aggregator.chain_validator import completeness_pct, is_valid_sha256
from apps.evidence_aggregator.main import app
from apps.evidence_aggregator.models import EvidenceLink, EvidenceSummary
from tests.conftest import make_client

_VALID_HASH = "a3f5c2d1e8b4a7f0c9d2e5b8a1f4c7d0e3b6a9f2c5d8e1b4a7f0c3d6e9b2a5f8"


@pytest.mark.asyncio
async def test_health_returns_200():
    async with make_client(app) as client:
        resp = await client.get("/health")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_health_service_name():
    async with make_client(app) as client:
        resp = await client.get("/health")
    assert resp.json()["service"] == "evidence-aggregator"


def test_is_valid_sha256_valid():
    assert is_valid_sha256(_VALID_HASH) is True


def test_is_valid_sha256_wrong_length():
    assert is_valid_sha256("abc123") is False


def test_is_valid_sha256_invalid_chars():
    assert is_valid_sha256("z" * 64) is False


def test_completeness_pct_full():
    assert completeness_pct(10, 10) == 100.0


def test_completeness_pct_partial():
    assert completeness_pct(7, 10) == 70.0


def test_completeness_pct_zero_expected():
    assert completeness_pct(0, 0) == 0.0


def test_evidence_link_model():
    link = EvidenceLink(
        link_id="lnk-001",
        control_id="DE.AE-02",
        verdict_id="vrd-001",
        evidence_hash=_VALID_HASH,
        chain_position=0,
    )
    assert link.chain_position == 0


def test_evidence_summary_model():
    summary = EvidenceSummary(
        engagement_id="eng-alpha-001",
        total_links=5,
        unique_hashes=4,
        completeness_pct=80.0,
    )
    assert summary.total_links == 5
