from pydantic import BaseModel
from app.schemas.transcript import Transcript
from app.schemas.scene_collection import SceneCollection

class KnowledgeRequest(BaseModel):
    transcript: Transcript
    scenes: SceneCollection