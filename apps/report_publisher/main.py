"""Report Publisher Service — FastAPI application entry point."""

from fastapi import FastAPI

from apps.shared.cache import build_redis, check_redis
from apps.shared.db import build_engine, check_db
from apps.shared.settings import Settings

_settings = Settings()
_engine = build_engine(_settings.database_url)
_redis = build_redis(_settings.redis_url)

app = FastAPI(
    title="Report Publisher Service",
    description="Publishes reports and handles delivery.",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict[str, object]:
    """Liveness + dependency check for report-publisher."""
    db_ok = await check_db(_engine)
    redis_ok = await check_redis(_redis)
    return {
        "service": "report-publisher",
        "port": _settings.port_report_publisher,
        "db": db_ok,
        "redis": redis_ok,
    }
