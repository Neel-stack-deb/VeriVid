import json
from pathlib import Path

from pydantic import ValidationError

from app.repositories.video_workspace_repository import VideoWorkspaceRepository
from app.schemas.debate.consensus_report import ConsensusReport
from app.schemas.debate.context_report import ContextReport
from app.schemas.debate.risk_report import RiskReport
from app.schemas.debate.verification_report import VerificationReport
from app.schemas.knowledge.knowledge_base import KnowledgeBase
from app.schemas.scene_collection import SceneCollection
from app.schemas.transcript import Transcript
from app.schemas.video_metadata import VideoMetadata


class VideoResultsRepository:

  @staticmethod
  def _read_model(path: Path, model: type):
    if not path.exists():
      return None
    try:
      return model.model_validate(json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, ValidationError):
      return None

  @classmethod
  def load_all(cls, video_id: str) -> dict:
    workspace = VideoWorkspaceRepository.get_workspace(video_id)
    metadata_path = workspace.metadata_dir / "metadata.json"
    transcript_path = workspace.transcript_dir / "transcript.json"
    scenes_path = workspace.scenes_dir / "scenes.json"
    knowledge_path = workspace.knowledge_dir / "knowledge.json"
    debate_dir = workspace.debate_dir

    return {
      "metadata": cls._read_model(metadata_path, VideoMetadata),
      "transcript": cls._read_model(transcript_path, Transcript),
      "scenes": cls._read_model(scenes_path, SceneCollection),
      "knowledge": cls._read_model(knowledge_path, KnowledgeBase),
      "context_report": cls._read_model(
        debate_dir / "context.json",
        ContextReport,
      ),
      "verification_report": cls._read_model(
        debate_dir / "verification.json",
        VerificationReport,
      ),
      "risk_report": cls._read_model(
        debate_dir / "risk.json",
        RiskReport,
      ),
      "consensus_report": cls._read_model(
        debate_dir / "consensus.json",
        ConsensusReport,
      ),
    }