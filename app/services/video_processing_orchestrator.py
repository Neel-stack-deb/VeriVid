from datetime import datetime

from app.ai.agents.consensus_agent import ConsensusAgent
from app.ai.agents.context_agent import ContextAgent
from app.ai.agents.knowledge_agent import KnowledgeAgent
from app.ai.agents.risk_agent import RiskAgent
from app.ai.agents.verification_agent import VerificationAgent
from app.ai.registry import reasoning_client, vision_client
from app.ai.schemas.knowledge_request import KnowledgeRequest
from app.pipelines.debate_pipeline import DebatePipeline
from app.repositories.processing_status_repository import (
  ProcessingStatusRepository,
)
from app.schemas.processing import (
  ProcessingLifecycleStatus,
  ProcessingStage,
)
from app.schemas.video_artifacts import VideoArtifacts
from app.schemas.video_workspace import VideoWorkspace
from app.services.audio_service import AudioService
from app.services.debate_persistence_service import DebatePersistenceService
from app.services.frame_service import FrameService
from app.services.knowledge_persistence_service import (
  KnowledgePersistenceService,
)
from app.services.metadata_service import MetadataService
from app.services.vision_service import VisionService
from app.services.whisper_service import WhisperService


class VideoProcessingOrchestrator:
  """
  Runs perception + knowledge + debate with status updates between stages.
  Reuses existing services and pipelines (DebatePipeline / LangGraph).
  """

  def __init__(
    self,
    *,
    debate_pipeline: DebatePipeline | None = None,
    knowledge_agent: KnowledgeAgent | None = None,
  ) -> None:
    self._knowledge_agent = knowledge_agent or KnowledgeAgent(reasoning_client)
    self._debate_pipeline = debate_pipeline or DebatePipeline(
      context_agent=ContextAgent(reasoning_client),
      verification_agent=VerificationAgent(reasoning_client),
      risk_agent=RiskAgent(reasoning_client),
      consensus_agent=ConsensusAgent(reasoning_client),
      persistence_service=DebatePersistenceService,
    )

  def run(self, workspace: VideoWorkspace) -> None:
    record = ProcessingStatusRepository.load(workspace.video_id)
    record.status = ProcessingLifecycleStatus.PROCESSING
    record.started_at = record.started_at or datetime.utcnow()
    record.error = None
    ProcessingStatusRepository.save(record)

    try:
      artifacts = VideoArtifacts(workspace=workspace)

      self._set_stage(workspace.video_id, ProcessingStage.METADATA)
      artifacts = MetadataService.extract(artifacts)

      self._set_stage(workspace.video_id, ProcessingStage.FRAMES)
      artifacts = FrameService.extract_frames(artifacts)

      self._set_stage(workspace.video_id, ProcessingStage.AUDIO)
      artifacts = AudioService.process(artifacts)

      self._set_stage(workspace.video_id, ProcessingStage.TRANSCRIPTION)
      artifacts = WhisperService.process(artifacts)

      self._set_stage(workspace.video_id, ProcessingStage.VISION)
      artifacts = VisionService(vision_client).process(artifacts)

      self._set_stage(workspace.video_id, ProcessingStage.KNOWLEDGE)
      knowledge_response = self._knowledge_agent.extract(
        KnowledgeRequest(
          transcript=artifacts.transcript,
          scenes=artifacts.scene_collection,
        )
      )
      artifacts.knowledge = knowledge_response.knowledge
      KnowledgePersistenceService.save(
        workspace,
        knowledge_response.knowledge,
      )

      self._set_stage(workspace.video_id, ProcessingStage.DEBATE)
      self._debate_pipeline.process(workspace, artifacts.knowledge)

      record = ProcessingStatusRepository.load(workspace.video_id)
      record.status = ProcessingLifecycleStatus.COMPLETED
      record.current_stage = None
      record.completed_at = datetime.utcnow()
      ProcessingStatusRepository.save(record)

    except Exception as exc:
      record = ProcessingStatusRepository.load(workspace.video_id)
      record.status = ProcessingLifecycleStatus.FAILED
      record.error = str(exc)
      record.completed_at = datetime.utcnow()
      ProcessingStatusRepository.save(record)
      raise

  @staticmethod
  def _set_stage(video_id: str, stage: ProcessingStage) -> None:
    record = ProcessingStatusRepository.load(video_id)
    record.current_stage = stage
    ProcessingStatusRepository.save(record)