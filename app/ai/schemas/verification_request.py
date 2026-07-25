from pydantic import BaseModel

from app.ai.schemas.context_response import ContextResponse
from app.schemas.knowledge.knowledge_base import KnowledgeBase


class VerificationRequest(BaseModel):
    knowledge: KnowledgeBase
    context: ContextResponse