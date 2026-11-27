from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client(tmp_video_dir):
  return TestClient(app)


def test_upload_endpoint_accepts_mp4(client: TestClient, sample_mp4: Path):
  with sample_mp4.open("rb") as video:
    response = client.post(
      "/upload",
      files={"video": ("sample.mp4", video, "video/mp4")},
    )

  assert response.status_code == 200
  payload = response.json()
  assert payload["filename"] == "sample.mp4"
  assert payload["file_size"] > 0
  assert payload["video_id"]
  assert Path(payload["storage_path"]).exists()