from pydantic import BaseModel

from app.schemas.debate.verification_report import VerificationReport


class VerificationResponse(BaseModel):
    report: VerificationReport