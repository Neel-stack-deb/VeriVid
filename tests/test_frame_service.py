from app.schemas.video_artifacts import VideoArtifacts
from app.services.frame_service import FrameService
from app.services.metadata_service import MetadataService
from tests.conftest import make_workspace_from_video


def test_frame_extraction_creates_jpeg_frames(sample_mp4):
  workspace = make_workspace_from_video(sample_mp4)
  artifacts = VideoArtifacts(workspace=workspace)
  artifacts = MetadataService.extract(artifacts)

  result = FrameService.extract_frames(artifacts)

  assert len(result.frame_paths) >= 1
  assert all(path.suffix == ".jpg" for path in result.frame_paths)