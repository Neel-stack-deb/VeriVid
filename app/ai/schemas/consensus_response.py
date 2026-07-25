from pydantic import BaseModel

from app.schemas.debate.consensus_report import ConsensusReport


class ConsensusResponse(BaseModel):
    report: ConsensusReport