"""Tests for report_publisher service."""
import pytest
from apps.report_publisher.main import app
from apps.report_publisher.models import DeliveryRequest, DeliveryStatus
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
    assert resp.json()["service"] == "report-publisher"


def test_delivery_request_email():
    req = DeliveryRequest(
        report_id="rpt-001",
        channel="email",
        recipient="audit@example.com",
    )
    assert req.channel == "email"


def test_delivery_request_webhook():
    req = DeliveryRequest(
        report_id="rpt-001",
        channel="webhook",
        recipient="https://hooks.example.com/notify",
    )
    assert req.channel == "webhook"


def test_delivery_status_model():
    status = DeliveryStatus(
        delivery_id="dlv-001",
        report_id="rpt-001",
        channel="email",
        recipient="audit@example.com",
        status="delivered",
    )
    assert status.status == "delivered"
