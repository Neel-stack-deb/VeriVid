from pydantic import BaseModel
from app.schemas.knowledge.entity import Entity
from app.schemas.knowledge.event import Event
from app.schemas.knowledge.claim import Claim
from app.schemas.knowledge.evidence import Evidence
from app.schemas.knowledge.relationship import Relationship
class KnowledgeBase(BaseModel):
    entities: list[Entity] = []
    events: list[Event] = []
    claims: list[Claim] = []
    evidence: list[Evidence] = []
    relationships: list[Relationship] = []