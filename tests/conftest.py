"""pytest conftest — session-scoped real Postgres + Redis fixtures. No mocks."""
import json
import os
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from apps.shared.cache import build_redis
from apps.shared.db import build_engine, build_session_factory

_FIXTURES = Path(__file__).parent / "fixtures"

_TEST_DB_URL = os.environ.get(
    "DATABASE_TEST_URL",
    "postgresql+asyncpg://assurance:assurance@localhost:5432/assurance_test",
)
_REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")


@pytest.fixture(scope="session")
def test_db_url() -> str:
    return _TEST_DB_URL


@pytest.fixture(scope="session")
def redis_url() -> str:
    return _REDIS_URL


@pytest_asyncio.fixture(scope="session")
async def db_engine(test_db_url: str):
    engine = build_engine(test_db_url)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def db_session_factory(db_engine):
    return build_session_factory(db_engine)


@pytest_asyncio.fixture(scope="session")
async def redis_client(redis_url: str):
    client = build_redis(redis_url)
    yield client
    await client.aclose()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def seed_db(db_engine):
    """Load fixture JSON files into the test DB once per session."""
    async with db_engine.begin() as conn:
        for framework in _load("frameworks.json"):
            await conn.execute(
                text(
                    "INSERT INTO frameworks (framework_id, name, version, description, regions)"
                    " VALUES (:fid, :name, :ver, :desc, :regions)"
                    " ON CONFLICT (framework_id) DO NOTHING"
                ),
                {
                    "fid": framework["framework_id"],
                    "name": framework["name"],
                    "ver": framework["version"],
                    "desc": framework["description"],
                    "regions": framework["regions"],
                },
            )
        for ctrl in _load("controls.json"):
            await conn.execute(
                text(
                    "INSERT INTO controls (control_id, framework_id, category, name, description, attack_mapping)"
                    " VALUES (:cid, :fid, :cat, :name, :desc, :atk)"
                    " ON CONFLICT (control_id) DO NOTHING"
                ),
                {
                    "cid": ctrl["control_id"],
                    "fid": ctrl["framework_id"],
                    "cat": ctrl["category"],
                    "name": ctrl["name"],
                    "desc": ctrl["description"],
                    "atk": ctrl["attack_mapping"],
                },
            )


def _load(filename: str) -> list[dict]:
    return json.loads((_FIXTURES / filename).read_text())


def make_client(app) -> AsyncClient:
    """Create a test ASGI client for a FastAPI app (no running server needed)."""
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
