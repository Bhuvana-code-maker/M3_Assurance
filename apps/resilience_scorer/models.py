"""Pydantic models for the Resilience Scorer service."""
from pydantic import BaseModel, Field


class ScoreRequest(BaseModel):
    engagement_id: str
    framework_ids: list[str]


class ResilienceScore(BaseModel):
    score_id: str
    engagement_id: str
    composite_score: float = Field(..., ge=0.0, le=100.0)
    coverage_score: float = Field(..., ge=0.0, le=100.0)
    detection_score: float = Field(..., ge=0.0, le=100.0)
    evidence_score: float = Field(..., ge=0.0, le=100.0)
    band: str = Field(..., description="Critical | At Risk | Moderate | Strong | Resilient")
