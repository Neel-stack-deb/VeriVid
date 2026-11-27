from app.ai.agents.knowledge_agent import KnowledgeAgent
from app.ai.schemas.knowledge_extraction_response import KnowledgeExtractionResponse
from app.ai.schemas.knowledge_request import KnowledgeRequest
from app.schemas.knowledge.knowledge_base import KnowledgeBase
from app.schemas.scene_collection import SceneCollection
from tests.mocks import MockInferenceClient


def test_knowledge_agent_returns_structured_knowledge(mock_transcript, mock_knowledge_base):
  mock_client = MockInferenceClient()
  mock_client.register(
    KnowledgeExtractionResponse,
    KnowledgeExtractionResponse(knowledge=mock_knowledge_base),
  )

  agent = KnowledgeAgent(mock_client)
  response = agent.extract(
    KnowledgeRequest(
      transcript=mock_transcript,
      scenes=SceneCollection(scenes=[]),
    )
  )

  assert response.knowledge.entities[0].name == "Speaker"
  assert mock_client.calls[0].system_prompt.strip()
  assert mock_client.calls[0].user_prompt.strip()