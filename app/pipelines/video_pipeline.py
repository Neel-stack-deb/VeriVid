from app.agents.knowledge_agent import KnowledgeAgent
from app.ai.registry import reasoning_client, vision_client
from app.ai.schemas.knowledge_request import KnowledgeRequest
from app.schemas.video_artifacts import VideoArtifacts
from app.schemas.video_workspace import VideoWorkspace
from app.services.audio_service import AudioService
from app.services.frame_service import FrameService
from app.services.knowledge_persistence_service import (
    KnowledgePersistenceService,
)
from app.services.metadata_service import MetadataService
from app.services.vision_service import VisionService
from app.services.whisper_service import WhisperService

class VideoPipeline:

    @staticmethod
    def process(workspace : VideoWorkspace) -> VideoArtifacts:

        artifacts = VideoArtifacts(
            workspace=workspace
        )

        artifacts = MetadataService.process(artifacts)
        artifacts = FrameService.process(artifacts)
        artifacts = AudioService.process(artifacts)
        artifacts = WhisperService.process(artifacts)
        artifacts = VisionService(
                        vision_client
                    ).process(artifacts)

        knowledge_agent = KnowledgeAgent(reasoning_client)
        knowledge_response = knowledge_agent.extract(
            request=KnowledgeRequest(
                transcript=artifacts.transcript,
                scenes=artifacts.scene_collection,
            )
        )

        artifacts.knowledge = knowledge_response.knowledge

        KnowledgePersistenceService.save(
            artifacts.workspace,
            knowledge_response.knowledge,
        )

        return artifacts