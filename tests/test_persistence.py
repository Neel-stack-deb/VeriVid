import json

from app.schemas.debate.debate_artifacts import DebateArtifacts
from app.services.debate_persistence_service import DebatePersistenceService
from app.services.knowledge_persistence_service import KnowledgePersistenceService
from tests.conftest import make_workspace_from_video


def test_knowledge_persistence_writes_utf8_json(
  sample_mp4,
  mock_knowledge_base,
):
  workspace = make_workspace_from_video(sample_mp4)
  KnowledgePersistenceService.save(workspace, mock_knowledge_base)

  path = workspace.knowledge_dir / "knowledge.json"
  data = json.loads(path.read_text(encoding="utf-8"))
  assert data["entities"][0]["name"] == "Speaker"


def test_debate_persistence_skips_none_reports(
  sample_mp4,
  mock_knowledge_base,
  mock_context_report,
):
  workspace = make_workspace_from_video(sample_mp4)
  artifacts = DebateArtifacts(
    knowledge=mock_knowledge_base,
    context_report=mock_context_report,
  )

  DebatePersistenceService.save(workspace, artifacts)

  assert (workspace.debate_dir / "context.json").exists()
  assert not (workspace.debate_dir / "consensus.json").exists()