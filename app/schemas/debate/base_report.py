from datetime import datetime

from pydantic import BaseModel, Field


class BaseReport(BaseModel):
    summary: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    model_name: str

    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
    )