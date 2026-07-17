from pydantic import BaseModel

from app.schemas.debate.context_report import ContextReport


class ContextResponse(BaseModel):
    report: ContextReport