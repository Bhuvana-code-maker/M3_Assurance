"""Tests for apps/shared — settings, db, cache."""
import pytest
from apps.shared.cache import build_redis, check_redis
from apps.shared.db import build_engine, check_db
from apps.shared.settings import Settings
from tests.conftest import _TEST_DB_URL, _REDIS_URL


def test_settings_defaults():
    s = Settings()
    assert s.port_control_mapping == 10001
    assert s.port_report_publisher == 10007


def test_settings_ports_sequential():
    s = Settings()
    ports = [
        s.port_control_mapping,
        s.port_evidence_aggregator,
        s.port_gap_analyzer,
        s.port_resilience_scorer,
        s.port_report_generator,
        s.port_framework_registry,
        s.port_report_publisher,
    ]
    assert len(set(ports)) == 7, "Each service must have a unique port"


@pytest.mark.asyncio
async def test_db_reachable():
    engine = build_engine(_TEST_DB_URL)
    assert await check_db(engine)
    await engine.dispose()


@pytest.mark.asyncio
async def test_redis_reachable():
    client = build_redis(_REDIS_URL)
    assert await check_redis(client)
    await client.aclose()
