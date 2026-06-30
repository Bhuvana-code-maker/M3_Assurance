"""Tests for resilience_scorer service."""
import pytest
from apps.resilience_scorer.calculator import composite_score, safe_pct, score_band
from apps.resilience_scorer.main import app
from apps.resilience_scorer.models import ResilienceScore, ScoreRequest
from tests.conftest import make_client


@pytest.mark.asyncio
async def test_health_returns_200():
    async with make_client(app) as client:
        resp = await client.get("/health")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_health_service_name():
    async with make_client(app) as client:
        resp = await client.get("/health")
    assert resp.json()["service"] == "resilience-scorer"


def test_score_band_critical():
    assert score_band(0.0) == "Critical"


def test_score_band_at_risk():
    assert score_band(50.0) == "At Risk"


def test_score_band_moderate():
    assert score_band(70.0) == "Moderate"


def test_score_band_strong():
    assert score_band(85.0) == "Strong"


def test_score_band_resilient():
    assert score_band(100.0) == "Resilient"


def test_composite_score_calculation():
    # 100% coverage, 100% detection, 100% evidence → 100.0
    assert composite_score(100.0, 100.0, 100.0) == 100.0


def test_composite_score_weighted():
    # 40*0.4 + 60*0.35 + 80*0.25 = 16+21+20 = 57
    assert composite_score(40.0, 60.0, 80.0) == 57.0


def test_safe_pct_normal():
    assert safe_pct(7, 10) == 70.0


def test_safe_pct_zero_denominator():
    assert safe_pct(0, 0) == 0.0


def test_score_request_model():
    req = ScoreRequest(engagement_id="eng-alpha-001", framework_ids=["nist_csf_2.0"])
    assert req.engagement_id == "eng-alpha-001"


def test_resilience_score_model():
    score = ResilienceScore(
        score_id="scr-001",
        engagement_id="eng-alpha-001",
        composite_score=72.5,
        coverage_score=80.0,
        detection_score=70.0,
        evidence_score=60.0,
        band="Moderate",
    )
    assert score.band == "Moderate"
