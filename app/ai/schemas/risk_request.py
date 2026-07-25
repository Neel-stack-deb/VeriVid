from pydantic import BaseModel

from app.ai.schemas.context_response import ContextResponse
from app.ai.schemas.verification_response import VerificationResponse
from app.schemas.knowledge.knowledge_base import KnowledgeBase


class RiskRequest(BaseModel):
    knowledge: KnowledgeBase
    context: ContextResponse
    verification: VerificationResponse