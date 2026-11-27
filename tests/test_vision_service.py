from pathlib import Path

from app.schemas.video_artifacts import VideoArtifacts
from app.services.vision_service import VisionService
from tests.conftest import make_workspace_from_video
from tests.mocks import MockVisionClient


def test_vision_service_persists_scenes(sample_mp4, tmp_path):
  workspace = make_workspace_from_video(sample_mp4)
  frame_path = workspace.frames_dir / "frame_0001.jpg"
  frame_path.write_bytes(b"fake-jpeg-bytes")

  artifacts = VideoArtifacts(
    workspace=workspace,
    frame_paths=[frame_path],
  )

  mock_client = MockVisionClient()
  result = VisionService(mock_client).process(artifacts)

  assert result.scene_collection is not None
  assert len(result.scene_collection.scenes) == 1
  assert result.scene_collection.scenes[0].description == "A test scene"
  scenes_file = workspace.scenes_dir / "scenes.json"
  assert scenes_file.exists()
  assert b"test scene" in scenes_file.read_bytes()