"""Pydantic models for the Evidence Aggregator service."""

from pydantic import BaseModel, Field


class EvidenceLink(BaseModel):
    link_id: str
    control_id: str
    verdict_id: str
    evidence_hash: str
    chain_position: int = Field(..., ge=0)


class EvidenceSummary(BaseModel):
    engagement_id: str
    total_links: int
    unique_hashes: int
    completeness_pct: float
