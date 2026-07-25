from pydantic import BaseModel

from app.schemas.debate.risk_report import RiskReport


class RiskResponse(BaseModel):
    report: RiskReport