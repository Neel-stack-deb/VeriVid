from pydantic import BaseModel

from app.schemas.debate.base_report import BaseReport


class ConsensusFinding(BaseModel):
    title: str

    description: str

    supporting_reports: list[str]


class ConsensusReport(BaseReport):
    findings: list[ConsensusFinding] = []

    unresolved_conflicts: list[str] = []