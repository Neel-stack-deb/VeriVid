from pydantic import BaseModel

from app.schemas.debate.base_report import BaseReport


class TimelineEvent(BaseModel):
    event_id: str


class ContextReport(BaseReport):
    timeline: list[TimelineEvent] = []

    key_entity_ids: list[str] = []

    key_event_ids: list[str] = []