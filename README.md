# VeriVid

Multimodal video intelligence backend: upload a video, extract perception artifacts, structure knowledge, and run a four-agent debate council for verified insights.

**Pipeline:** Upload → Workspace → VideoPipeline → Knowledge → DebatePipeline → JSON persistence

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended)
- `ffmpeg` and `ffprobe` on `PATH`

## Setup

```bash
uv sync --group dev
```

## Run API

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

- Health: `GET /health`
- Upload (legacy): `POST /upload`
- Upload (API): `POST /api/videos/upload`
- Process: `POST /api/videos/{video_id}/process`
- Status: `GET /api/videos/{video_id}/status`
- Results: `GET /api/videos/{video_id}/results`

See `API_DOCUMENTATION.md`.

## Environment variables

| Variable | Purpose |
| --- | --- |
| `FIREWORKS_BASE_URL`, `FIREWORKS_API_KEY` | Fireworks reasoning client (used at inference time) |
| `AMD_BASE_URL`, `AMD_API_KEY` | AMD OpenAI-compatible endpoint |
| `AI_BASE_URL`, `AI_API_KEY` | Vision (vLLM / Qwen) endpoint |
| `AI_PROVIDER` | `fireworks` or `amd` (informational today) |
| `WHISPER_MODEL` | Hugging Face model id for local transcription (default `openai/whisper-base`) |
| `CORS_ORIGINS` | Comma-separated allowed browser origins |

Credentials are **not** required for application import or unit tests. Missing credentials raise `AuthenticationError` when a provider is invoked.

## Tests

```bash
uv run pytest tests/ -q
```

Tests use mocks for external AI; FFmpeg is used for real media fixtures. See `TESTING_REPORT.md`.

## Project docs

- `PROJECT_AUDIT.md` — Phase 1 architecture audit
- `TESTING_REPORT.md` — Validation results (Phases 2–3)
- `LANGGRAPH_ARCHITECTURE.md` — Debate council LangGraph design
- `API_DOCUMENTATION.md` — REST API reference