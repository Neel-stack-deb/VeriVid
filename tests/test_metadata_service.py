from app.schemas.video_artifacts import VideoArtifacts
from app.services.metadata_service import MetadataService
from tests.conftest import make_workspace_from_video


def test_metadata_extraction(sample_mp4):
  workspace = make_workspace_from_video(sample_mp4)
  artifacts = VideoArtifacts(workspace=workspace)

  result = MetadataService.extract(artifacts)

  assert result.metadata is not None
  assert result.metadata.duration > 0
  assert result.metadata.width == 320
  assert (workspace.metadata_dir / "metadata.json").exists()