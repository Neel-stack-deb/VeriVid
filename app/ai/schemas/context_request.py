from pydantic import BaseModel

from app.schemas.knowledge.knowledge_base import KnowledgeBase


class ContextRequest(BaseModel):
    knowledge: KnowledgeBase