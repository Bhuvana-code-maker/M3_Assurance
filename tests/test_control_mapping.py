"""Tests for control_mapping service."""
import pytest
from apps.control_mapping.main import app
from apps.control_mapping.mappers import coverage_pct, outcome_to_status
from apps.control_mapping.models import ControlMappingRequest, ControlMappingResponse, ControlStatus
from tests.conftest import make_client


@pytest.mark.asyncio
async def test_health_returns_200():
    async with make_client(app) as client:
        resp = await client.get("/health")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_health_db_and_redis_ok():
    async with make_client(app) as client:
        resp = await client.get("/health")
    body = resp.json()
    assert body["service"] == "control-mapping"
    assert body["db"] is True
    assert body["redis"] is True


def test_outcome_to_status_detected():
    assert outcome_to_status("Detected") == "Met"


def test_outcome_to_status_missed():
    assert outcome_to_status("Missed") == "Not Met"


def test_outcome_to_status_no_data():
    assert outcome_to_status("No Data") == "Not Met"


def test_outcome_to_status_partial():
    assert outcome_to_status("Partial") == "Partial"


def test_outcome_to_status_unknown_defaults_partial():
    assert outcome_to_status("SomethingElse") == "Partial"


def test_coverage_pct_all_met():
    statuses = {"c1": "Met", "c2": "Met", "c3": "Met"}
    assert coverage_pct(statuses) == 100.0


def test_coverage_pct_half_met():
    statuses = {"c1": "Met", "c2": "Not Met"}
    assert coverage_pct(statuses) == 50.0


def test_coverage_pct_empty():
    assert coverage_pct({}) == 0.0


def test_control_mapping_request_model():
    req = ControlMappingRequest(
        verdict_id="vrd-001",
        framework_ids=["nist_csf_2.0"],
        engagement_id="eng-alpha-001",
    )
    assert req.verdict_id == "vrd-001"


def test_control_status_model():
    cs = ControlStatus(control_id="DE.AE-02", status="Met", evidence_hash=None)
    assert cs.status == "Met"


def test_control_mapping_response_model():
    resp = ControlMappingResponse(
        engagement_id="eng-alpha-001",
        control_statuses={"DE.AE-02": "Met"},
        coverage_pct=100.0,
        framework_ids=["nist_csf_2.0"],
    )
    assert resp.coverage_pct == 100.0
