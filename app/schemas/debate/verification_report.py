from pydantic import BaseModel

from app.schemas.debate.base_report import BaseReport


class VerifiedClaim(BaseModel):
    claim_id: str

    confidence: float


class UnsupportedClaim(BaseModel):
    claim_id: str

    reason: str


class Contradiction(BaseModel):
    claim_id: str

    conflicting_evidence_ids: list[str]


class VerificationReport(BaseReport):
    verified_claims: list[VerifiedClaim] = []

    unsupported_claims: list[UnsupportedClaim] = []

    contradictions: list[Contradiction] = []