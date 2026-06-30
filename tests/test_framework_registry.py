"""Tests for framework_registry service."""

import pytest

from apps.framework_registry.main import app
from apps.framework_registry.models import Control, CrossWalk, Framework
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
    assert resp.json()["service"] == "framework-registry"


def test_framework_model():
    fw = Framework(
        framework_id="nist_csf_2.0",
        name="NIST CSF",
        version="2.0",
        description="Six core functions.",
        regions=["global", "us"],
    )
    assert fw.framework_id == "nist_csf_2.0"


def test_control_model():
    ctrl = Control(
        control_id="DE.AE-02",
        framework_id="nist_csf_2.0",
        category="Detect",
        name="Anomalies and Events",
        description="Detect anomalous events.",
        attack_mapping=["T1486", "T1059"],
    )
    assert len(ctrl.attack_mapping) == 2


def test_cross_walk_model():
    cw = CrossWalk(
        source_control_id="DE.AE-02",
        target_control_id="ISO-8.16",
        equivalence_level="Partial",
    )
    assert cw.equivalence_level == "Partial"
