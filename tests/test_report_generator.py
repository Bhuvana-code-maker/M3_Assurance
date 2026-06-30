"""Tests for report_generator service."""

import pytest

from apps.report_generator.main import app
from apps.report_generator.models import Report, ReportRequest
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
    assert resp.json()["service"] == "report-generator"


def test_report_request_default_format():
    req = ReportRequest(engagement_id="eng-alpha-001", framework_ids=["nist_csf_2.0"])
    assert req.format == "pdf"


def test_report_request_html_format():
    req = ReportRequest(
        engagement_id="eng-alpha-001",
        framework_ids=["nist_csf_2.0"],
        format="html",
    )
    assert req.format == "html"


def test_report_model():
    report = Report(
        report_id="rpt-001",
        engagement_id="eng-alpha-001",
        framework_ids=["nist_csf_2.0", "iso_27001_2022"],
        composite_score=78.5,
        format="pdf",
        content_hash="a" * 64,
    )
    assert len(report.framework_ids) == 2
