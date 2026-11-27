# VeriVid — Phase 2 Backend Validation Report

**Date:** 2026-11-27 (Asia/Calcutta)  
**Branch:** `cursor/backend-validation-62f3`  
**Base:** `cursor/project-audit-phase1-62f3`

## Issues discovered (from Phase 1 + validation)

| Issue | Resolution |
| --- | --- |
| `settings.fireworks` / `settings.amd` undefined | Added `ProviderCredentials` properties on `Settings` with `FIREWORKS_*` / `AMD_*` env vars |
| `AISettings` required credentials at import | Default empty `base_url` / `api_key`; errors on provider invocation |
| Eager registry imports (Whisper, clients) | Lazy `_LazyProxy` wrappers in `app/ai/registry.py` |
| `VideoPipeline` wrong service methods | Call `MetadataService.extract` / `FrameService.extract_frames` |
| `VisionPromptBuilder` double-read | Return loaded template string directly |
| `QwenVisionClient` wrong fields | Use `frame_path` and `ai_settings.models["vision"]` |
| `ScenePersistenceService` wrong attribute | Use `scenes_dir` |
| `KnowledgeAgent` stub / wrong client | Implemented `extract()` with `Prompt` + `self._client` |
| `DebatePipeline` passed reports into request DTOs | Pass `ContextResponse` / `VerificationResponse` / `RiskResponse` per schemas |
| `DebatePersistenceService` datetime JSON | `model_dump(mode="json")` |

## Changes made (by area)

### Configuration & startup
- `app/core/config.py` — provider credential fields and properties
- `app/core/ai_settings.py` — optional credential defaults
- `app/ai/providers/openai_compatible_client.py` — lazy OpenAI client + credential guard
- `app/ai/clients/base/vllm_client.py` — credential guard for vision
- `app/ai/registry.py` — lazy client construction

### Perception
- `app/pipelines/video_pipeline.py`
- `app/ai/prompts/builders/vision_prompt_builder.py`
- `app/ai/clients/qwen_vision_client.py`
- `app/services/scene_persistence_service.py`

### Knowledge
- `app/ai/agents/knowledge_agent.py`
- `app/ai/prompts/builders/knowledge_prompt_builder.py`

### Debate
- `app/pipelines/debate_pipeline.py`
- `app/services/debate_persistence_service.py`

### Tooling
- `pyproject.toml` — `[dependency-groups] dev` with pytest, pytest-asyncio, httpx
- `pytest.ini`
- `tests/` — 13 modules + `tests/mocks.py`

## Tests created

| Test module | Coverage |
| --- | --- |
| `test_config.py` | Settings import, `main` app bootstrap |
| `test_inference_credentials.py` | Fireworks client rejects missing credentials |
| `test_workspace.py` | Async workspace directories |
| `test_metadata_service.py` | ffprobe metadata + JSON artifact |
| `test_frame_service.py` | ffmpeg frame JPEG outputs |
| `test_vision_service.py` | Mocked vision client + scene persistence |
| `test_knowledge_agent.py` | Mocked knowledge extraction |
| `test_debate_agents.py` | Four agents with mock inference |
| `test_debate_pipeline.py` | Orchestration + four JSON files |
| `test_persistence.py` | Knowledge + partial debate persistence |
| `test_video_pipeline.py` | Full perception chain with mocks |
| `test_e2e_mocked_pipeline.py` | Upload fixture → perception → debate → artifacts |
| `test_upload_api.py` | FastAPI `POST /upload` |

## Commands executed

```bash
uv sync --group dev
uv run pytest tests/ -q --tb=short
```

## Results

```
16 passed, 1 warning in ~2s
```

(Warning: Starlette deprecation for `httpx` vs `httpx2` in TestClient — cosmetic only.)

## Mock vs live verification

| Component | Mocked in CI tests | Live external service |
| --- | --- | --- |
| Fireworks / AMD reasoning | Yes (`MockInferenceClient`) | **Not verified** (no API keys in CI) |
| Qwen / vLLM vision | Yes (`MockVisionClient`) | **Not verified** |
| Whisper transcription | Yes (`MockTranscriptionClient`) | **Not verified** (local Whisper exists but not loaded in tests) |
| FFmpeg / ffprobe | **Real** (system binaries) | Used in metadata, frame, audio, E2E tests |
| FastAPI upload | **Real** (TestClient) | In-process |

## Phase 3 — LangGraph orchestration (branch `cursor/langgraph-orchestration-62f3`)

### Changes

- Added `langgraph` dependency (`langgraph==1.2.24`).
- New package `app/ai/graph/` — `DebateState`, four nodes, `build_debate_graph`, artifact conversion.
- `DebatePipeline` now invokes the compiled graph (no duplicated orchestration).
- Documentation: `LANGGRAPH_ARCHITECTURE.md`.

### New tests (`tests/test_debate_graph.py`)

| Test | Coverage |
| --- | --- |
| Graph compilation | Builds without credentials |
| Node unit tests | Context, verification prerequisites, full node chain |
| Execution order | Four inference calls in agent order |
| Failure propagation | `error` state + `DebateGraphError` |
| Pipeline integration | Persistence via graph-backed pipeline |

### Commands & results (Phase 3)

```bash
uv run pytest tests/ -q --tb=short
# 23 passed in ~2.5s
```

All 16 Phase 2 tests remain green.

## Remaining blockers (before API / frontend)

1. **Upload response still lacks `video_id`** — needed for product APIs.
2. **No `POST /api/videos/{id}/process` or status/results endpoints.**
3. **No frontend.**
4. **Live inference** requires `FIREWORKS_*`, `AMD_*`, and/or `AI_*` credentials — not validated here.
5. **Frame timestamps** still derived from frame index, not wall-clock seconds.
6. **`KnowledgeAgent` does not use `BaseAgent.process`** — uses dedicated `extract()` (by design).
7. **Whisper model load** remains heavy when transcription client is first accessed (lazy, but still costly).
8. **LangGraph**: sequential only; no checkpointing or conditional edges yet.

## Completion criteria checklist

| Criterion | Status |
| --- | --- |
| App starts without unnecessary credentials | **Pass** |
| Perception pipeline executes (with mocks for AI steps) | **Pass** |
| Knowledge extraction with mocked inference | **Pass** |
| Four debate agents + pipeline with mocks | **Pass** |
| Persistence produces valid JSON | **Pass** |
| E2E mocked pipeline test | **Pass** |
| This report | **Pass** |