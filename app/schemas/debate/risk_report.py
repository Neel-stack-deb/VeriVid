from pydantic import BaseModel

from app.schemas.debate.base_report import BaseReport


class Risk(BaseModel):
    title: str

    description: str

    severity: str

    confidence: float


class RiskReport(BaseReport):
    risks: list[Risk] = []

    recommendations: list[str] = []