import json

import pytest

from app.ai.agents.consensus_agent import ConsensusAgent
from app.ai.agents.context_agent import ContextAgent
from app.ai.agents.risk_agent import RiskAgent
from app.ai.agents.verification_agent import VerificationAgent
from app.ai.graph.debate_graph import (
  DebateGraphError,
  build_debate_graph,
  debate_state_to_artifacts,
)
from app.ai.graph.nodes.consensus_node import consensus_node
from app.ai.graph.nodes.context_node import context_node
from app.ai.graph.nodes.risk_node import risk_node
from app.ai.graph.nodes.verification_node import verification_node
from app.ai.schemas.consensus_response import ConsensusResponse
from app.ai.schemas.context_response import ContextResponse
from app.ai.schemas.inference_request import InferenceRequest
from app.ai.schemas.risk_response import RiskResponse
from app.ai.schemas.verification_response import VerificationResponse
from app.pipelines.debate_pipeline import DebatePipeline
from app.services.debate_persistence_service import DebatePersistenceService
from tests.conftest import make_workspace_from_video
from tests.mocks import MockInferenceClient


def _debate_client(
  mock_context_report,
  mock_verification_report,
  mock_risk_report,
  mock_consensus_report,
) -> MockInferenceClient:
  client = MockInferenceClient()
  client.register(ContextResponse, ContextResponse(report=mock_context_report))
  client.register(
    VerificationResponse,
    VerificationResponse(report=mock_verification_report),
  )
  client.register(RiskResponse, RiskResponse(report=mock_risk_report))
  client.register(
    ConsensusResponse,
    ConsensusResponse(report=mock_consensus_report),
  )
  return client


def test_build_debate_graph_compiles_without_credentials(
  mock_knowledge_base,
  mock_context_report,
  mock_verification_report,
  mock_risk_report,
  mock_consensus_report,
):
  client = _debate_client(
    mock_context_report,
    mock_verification_report,
    mock_risk_report,
    mock_consensus_report,
  )
  graph = build_debate_graph(
    context_agent=ContextAgent(client),
    verification_agent=VerificationAgent(client),
    risk_agent=RiskAgent(client),
    consensus_agent=ConsensusAgent(client),
  )
  assert graph is not None
  assert hasattr(graph, "invoke")


def test_context_node_updates_state(
  mock_knowledge_base,
  mock_context_report,
):
  client = MockInferenceClient()
  client.register(
    ContextResponse,
    ContextResponse(report=mock_context_report),
  )
  update = context_node(
    {"knowledge": mock_knowledge_base},
    agent=ContextAgent(client),
  )
  assert update["context_report"].summary == "Test context summary"


def test_verification_node_requires_context_report(mock_knowledge_base):
  client = MockInferenceClient()
  with pytest.raises(ValueError, match="context_report"):
    verification_node(
      {"knowledge": mock_knowledge_base},
      agent=VerificationAgent(client),
    )


def test_graph_execution_order_and_artifacts(
  mock_knowledge_base,
  mock_context_report,
  mock_verification_report,
  mock_risk_report,
  mock_consensus_report,
):
  client = _debate_client(
    mock_context_report,
    mock_verification_report,
    mock_risk_report,
    mock_consensus_report,
  )
  graph = build_debate_graph(
    context_agent=ContextAgent(client),
    verification_agent=VerificationAgent(client),
    risk_agent=RiskAgent(client),
    consensus_agent=ConsensusAgent(client),
  )

  final_state = graph.invoke({"knowledge": mock_knowledge_base})
  artifacts = debate_state_to_artifacts(mock_knowledge_base, final_state)

  assert artifacts.consensus_report.summary == "Consensus reached"
  assert len(client.calls) == 4
  assert client.calls[0].response_model is ContextResponse
  assert client.calls[1].response_model is VerificationResponse
  assert client.calls[2].response_model is RiskResponse
  assert client.calls[3].response_model is ConsensusResponse


def test_agent_failure_sets_error_state(mock_knowledge_base):
  class FailingClient(MockInferenceClient):
    def generate(self, request: InferenceRequest):
      raise RuntimeError("inference failed")

  graph = build_debate_graph(
    context_agent=ContextAgent(FailingClient()),
    verification_agent=VerificationAgent(FailingClient()),
    risk_agent=RiskAgent(FailingClient()),
    consensus_agent=ConsensusAgent(FailingClient()),
  )

  final_state = graph.invoke({"knowledge": mock_knowledge_base})
  assert "error" in final_state
  with pytest.raises(DebateGraphError):
    debate_state_to_artifacts(mock_knowledge_base, final_state)


def test_debate_pipeline_uses_graph_persistence(
  sample_mp4,
  mock_knowledge_base,
  mock_context_report,
  mock_verification_report,
  mock_risk_report,
  mock_consensus_report,
):
  client = _debate_client(
    mock_context_report,
    mock_verification_report,
    mock_risk_report,
    mock_consensus_report,
  )
  workspace = make_workspace_from_video(sample_mp4)
  pipeline = DebatePipeline(
    context_agent=ContextAgent(client),
    verification_agent=VerificationAgent(client),
    risk_agent=RiskAgent(client),
    consensus_agent=ConsensusAgent(client),
    persistence_service=DebatePersistenceService,
  )

  artifacts = pipeline.process(workspace, mock_knowledge_base)

  assert artifacts.consensus_report is not None
  path = workspace.debate_dir / "consensus.json"
  payload = json.loads(path.read_text(encoding="utf-8"))
  assert payload["summary"] == "Consensus reached"


def test_risk_and_consensus_nodes_chain_reports(
  mock_knowledge_base,
  mock_context_report,
  mock_verification_report,
  mock_risk_report,
  mock_consensus_report,
):
  client = _debate_client(
    mock_context_report,
    mock_verification_report,
    mock_risk_report,
    mock_consensus_report,
  )

  context_update = context_node(
    {"knowledge": mock_knowledge_base},
    agent=ContextAgent(client),
  )
  state = {"knowledge": mock_knowledge_base, **context_update}

  verification_update = verification_node(
    state,
    agent=VerificationAgent(client),
  )
  state = {**state, **verification_update}

  risk_update = risk_node(state, agent=RiskAgent(client))
  state = {**state, **risk_update}

  consensus_update = consensus_node(
    state,
    agent=ConsensusAgent(client),
  )

  assert consensus_update["consensus_report"].summary == "Consensus reached"