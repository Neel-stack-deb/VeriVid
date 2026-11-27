# VeriVid — Phase 1 Project Audit

**Audit date:** 2026-11-27 (Asia/Calcutta)  
**Repository:** `Neel-stack-deb/VeriVid`  
**Auditor scope:** Static inspection of the full backend tree; no application code was modified for this report.  
**Note:** Day 1–4 “memory” documentation referenced in the project brief was **not found** in the repository (no matching files under the repo root). This audit is based on source files, `pyproject.toml`, `README.md`, and `.cursor/environment.json` only.

---

## 1. Current architecture

VeriVid is organized as a **layered FastAPI backend** with a clear intended pipeline:

```
Upload (API)
  → WorkspaceService (disk layout under data/videos/{video_id}/)
  → VideoPipeline (perception: metadata, frames, audio, transcript, vision, knowledge)
  → DebatePipeline (reasoning: context → verification → risk → consensus)
  → Persistence (JSON artifacts per workspace)
```

### High-level module map

| Layer | Location | Role |
| --- | --- | --- |
| API | `app/api/` | HTTP routes (`health`, `upload` only) |
| Services | `app/services/` | Workspace, media extraction, vision orchestration, persistence |
| Pipelines | `app/pipelines/` | `VideoPipeline`, `DebatePipeline` orchestration |
| AI clients | `app/ai/clients/` | Fireworks/AMD inference, Qwen vision, Whisper transcription |
| AI agents | `app/ai/agents/` | Debate council + incomplete `KnowledgeAgent` |
| Prompts | `app/ai/prompts/` | Markdown templates + typed `PromptBuilder`s |
| Schemas | `app/schemas/`, `app/ai/schemas/` | Pydantic DTOs for API, artifacts, inference |
| Core | `app/core/` | `Settings`, `AISettings`, constants |
| Exceptions | `app/exceptions/` | Domain-specific errors |

### Design patterns (preserved intentionally)

- **Request DTO → Agent → Response DTO** for debate agents via `BaseAgent`.
- **DebatePipeline** owns sequencing and `DebateArtifacts` mutation; agents do not persist.
- **OpenAI-compatible structured output** via `OpenAICompatibleClient.generate()` and `beta.chat.completions.parse`.
- **Workspace-centric storage**: all artifacts live under `data/videos/{video_id}/` with named subdirectories.

### Runtime wiring

- `app/ai/registry.py` constructs singleton clients at import time (`WhisperTranscriptionClient`, `QwenVisionClient`, `FireworksClient`, `AMDClient`).
- `main.py` mounts only `health` and `upload` routers; no processing, status, or results APIs.

### What is absent (vs. stated product vision)

- **No frontend** (no `frontend/`, `web/`, or Next.js tree).
- **No LangGraph** (`langgraph` not in dependencies; no `app/ai/graph/`).
- **No OpenCV** usage (video work is **FFmpeg/ffprobe** subprocesses only).
- **No automated tests** (`tests/`, `pytest`, or test files).
- **No job queue / background workers** for long-running analysis.
- **No processing status model** or API.

---

## 2. Completed modules

“Completed” means the module has a coherent implementation that matches its apparent design **and** is plausibly callable without obvious internal contradictions. Several modules are **structurally complete** but **not safely invocable end-to-end** today (see §4).

| Module | Evidence | Assessment |
| --- | --- | --- |
| Workspace creation | `WorkspaceService.create` creates full directory tree, stores original video, enforces size limits | **Complete** (upload path validated in prior env setup) |
| Video validation | `VideoValidator` extension + MIME checks | **Complete** |
| Upload API | `POST /upload` + `UploadService` | **Complete** for storage only |
| Health API | `GET /health` | **Complete** |
| Metadata extraction | `MetadataService.extract` (ffprobe → `VideoMetadata` + JSON) | **Complete** as a function; not wired correctly from pipeline |
| Frame extraction | `FrameService.extract_frames` (ffmpeg, interval from constants) | **Complete** as a function; not wired correctly from pipeline |
| Audio extraction | `AudioService.process` | **Complete** |
| Local Whisper transcription | `WhisperTranscriptionClient` (transformers pipeline) | **Implemented**; heavy import at registry load |
| Vision orchestration | `VisionService.process` loop over frames | **Structurally complete** |
| Scene model + collection | `Scene`, `SceneCollection` | **Complete** |
| Debate agents (4) | `ContextAgent`, `VerificationAgent`, `RiskAgent`, `ConsensusAgent` extend `BaseAgent` | **Complete** pattern |
| Debate orchestration | `DebatePipeline.process` order + `.report` unwrapping | **Complete** pattern |
| Debate persistence | `DebatePersistenceService` → four JSON files | **Complete** |
| Knowledge persistence | `KnowledgePersistenceService` → `knowledge.json` | **Complete** |
| Prompt templates | Six debate/vision/knowledge `.md` files under `templates/` | **Present** |
| Prompt builders (debate) | Context, verification, risk, consensus builders return `Prompt` | **Complete** |
| Inference abstraction | `InferenceClient`, `InferenceRequest`, `OpenAICompatibleClient` | **Complete** |
| Exception taxonomy | Metadata, frame, audio, storage, inference, media | **Present** |

---

## 3. Incomplete modules

| Module | Gap |
| --- | --- |
| **VideoPipeline** | Calls non-existent `MetadataService.process` / `FrameService.process` instead of `extract` / `extract_frames`. |
| **KnowledgeAgent** | `NotImplementedError`; wrong attribute `_reasoning_client`; empty `system_prompt` would fail `OpenAICompatibleClient` validation; does not follow `BaseAgent.process` pattern. |
| **Knowledge extraction flow** | Prompt builder returns a single string, not `Prompt`; pipeline expects working agent. |
| **Provider configuration** | `FireworksClient` / `AMDClient` read `settings.fireworks` / `settings.amd`, but `Settings` in `config.py` defines neither. |
| **AISettings bootstrap** | `AISettings` requires `AI_BASE_URL` and `AI_API_KEY` with no defaults; module-level `ai_settings = AISettings()` fails without env. |
| **QwenVisionClient** | Uses `request.image_path` but `VisionRequest` defines `frame_path`; uses `ai_settings.vision_model` which is not a field (models live under `ai_settings.models["vision"]`). |
| **VisionPromptBuilder** | Loads prompt as string then calls `.read_text()` on it (treats string as path). |
| **ScenePersistenceService** | Uses `workspace.scenes_directory`; workspace schema field is `scenes_dir`. |
| **REST API (product)** | No `/api/videos/{id}/process`, `status`, `results`, `reports`, or chat. |
| **LangGraph** | Not started. |
| **Job / status tracking** | No models or services. |
| **Frontend** | Not started. |
| **Documentation** | `README.md` is empty. |
| **Demo mode** | Not started. |
| **Chat layer** | No routes, agents, or schemas. |
| **Style / accessibility outputs** | `PromptName.STYLE` references missing `style_prompt.md`; no style agent. |

---

## 4. Broken or potentially broken functionality

Issues below are backed by **direct code references** (not hypothetical).

| # | Symptom | Root cause (file evidence) | Severity |
| --- | --- | --- | --- |
| 1 | Importing `app.ai.registry` likely crashes | `FireworksClient` → `settings.fireworks.*` (`app/ai/clients/fireworks_client.py`) but `Settings` has no `fireworks` (`app/core/config.py`) | **Critical** |
| 2 | Same for AMD path | `AMDClient` → `settings.amd.*` (`app/ai/clients/amd_client.py`) | **Critical** |
| 3 | `ai_settings` import without env | `base_url: str`, `api_key: str` required (`app/core/ai_settings.py` L20–22, L34) | **Critical** |
| 4 | `VideoPipeline.process` cannot run | Calls `MetadataService.process`, `FrameService.process` (`app/pipelines/video_pipeline.py` L24–25); only `extract` / `extract_frames` exist | **Critical** |
| 5 | Knowledge step always fails | `raise NotImplementedError` (`app/ai/agents/knowledge_agent.py` L39) | **Critical** |
| 6 | Knowledge inference call wrong | `self._reasoning_client` undefined; should be `self._client` (`knowledge_agent.py` L37) | **Critical** |
| 7 | Vision frame analysis attribute error | `ImageEncoder.encode(request.image_path)` vs `frame_path` (`qwen_vision_client.py` L35, `vision_request.py` L7) | **Critical** |
| 8 | Vision prompt builder runtime error | `VisionPromptBuilder.build()` calls `.read_text()` on loaded string (`vision_prompt_builder.py` L6–12) | **Critical** |
| 9 | Scene save fails when vision runs | `workspace.scenes_directory` (`scene_persistence_service.py` L16) vs `scenes_dir` (`video_workspace.py` L17) | **High** |
| 10 | Upload response insufficient for API design | No `video_id` in `UploadResponse` (`app/schemas/upload.py`) though workspace UUID is created internally | **High** |
| 11 | Whisper on silent / no-audio video | `WhisperService` assumes `artifacts.audio_path` exists; audio extraction may fail or produce empty input without graceful skip | **Medium** |
| 12 | Vision timestamp from frame names | `ffmpeg` pattern `frame_%04d.jpg` → stem `frame_0001`; regex `(\d+)` yields index not seconds (`vision_service.py` L68–76) | **Medium** |
| 13 | Eager heavy ML at import | `registry.py` instantiates Whisper + clients on import | **Medium** (perf / dev UX) |
| 14 | `main.py` duplicate import | `from fastapi import FastAPI` twice (`main.py` L2, L5) | **Low** |
| 15 | Knowledge empty system prompt | Would violate `_validate_request` if call reached client (`openai_compatible_client.py` L121–122) | **High** (when implemented) |

---

## 5. Missing integrations

| Integration | Expected | Actual |
| --- | --- | --- |
| Fireworks AI | OpenAI-compatible reasoning | Client class exists; **settings not defined** |
| AMD MI300X / vLLM | Provider switch | `AMDClient` exists; **settings not defined**; not used in `registry` for debate |
| LangGraph | Debate orchestration | **Missing**; sequential `DebatePipeline` only |
| OpenCV | Video loading (per brief) | **Not used**; FFmpeg only |
| Processing API | Trigger full workflow | **Missing** |
| Background execution | Non-blocking process endpoint | **Missing** |
| CORS / frontend origin | Browser app | **Missing** |
| Authentication / authorization | Production API | **Missing** |
| Observability | Metrics, token/cost tracking | **Missing** (only basic inference logging) |
| CI / pytest | Automated validation | **Missing** |

---

## 6. Architectural inconsistencies

1. **Dual settings models**: `Settings` (`app/core/config.py`) vs `AISettings` (`app/core/ai_settings.py`) vs provider-specific `settings.fireworks` / `settings.amd` that are not declared anywhere.
2. **Knowledge vs debate agents**: Debate agents use `Prompt` + `BaseAgent.process`; knowledge uses static string builder and a bespoke `extract()` — intentional per brief, but knowledge must still satisfy inference validation.
3. **Service method naming**: Mix of `process`, `extract`, `extract_frames` without a shared `VideoArtifacts` processor protocol; pipeline assumes uniform `.process`.
4. **Persistence path naming**: `scenes_dir` vs `scenes_directory` breaks scene persistence.
5. **Vision stack split**: `QwenVisionClient` extends `VLLMClient` + raw chat completions, while debate uses structured parse API — two different client patterns (acceptable if documented).
6. **Registry singletons**: Tight coupling makes testing and provider swapping harder; no factory/DI layer yet (required later for LangGraph nodes).
7. **Product API prefix**: Brief expects `/api/videos/...`; current upload is `/upload` without versioned API namespace.

---

## 7. Dependency issues

From `pyproject.toml` (pinned via `uv.lock`):

| Declared | Used in code? | Notes |
| --- | --- | --- |
| `fastapi[standard]` | Yes | App runs |
| `openai` | Yes | Inference + vision |
| `pydantic-settings` | Yes | Config |
| `torch`, `transformers`, `accelerate` | Yes | Whisper pipeline |
| `librosa` | **Not referenced** in `app/` | Possibly planned audio analysis |
| **LangGraph** | No | Required by roadmap, not installed |
| **OpenCV** | No | Not installed |
| **pytest / httpx** | No | No test tooling |

**Operational dependencies (system):** `ffmpeg`, `ffprobe` (used via subprocess; present in Cloud Agent Dockerfile).

**Weight / install cost:** Full CUDA-linked `torch` stack in lockfile makes install large (~500MB+ wheels); appropriate for Whisper-local but heavy for API-only dev unless transcription is mocked or optional.

---

## 8. Security concerns

| Area | Risk | Mitigation status |
| --- | --- | --- |
| API keys | Must use env / secrets | `.env` pattern supported; **never commit keys** |
| Upload | User-controlled files written under `data/videos/` | Extension/MIME validation only; no virus scan; path is UUID-based (good) |
| No auth on upload | Anyone with network access can upload up to 500MB | **Open endpoint** |
| Path disclosure | `UploadResponse.storage_path` exposes server path | Consider returning `video_id` only |
| Inference logging | Logs model name, not prompts | Good; ensure prompts never logged at INFO in production |
| SSRF | Vision client reads local frame paths only | OK if frames stay in workspace |
| Rate limiting | None | Missing |

---

## 9. Testing gaps

- **Zero test files** under the repository.
- **No `pytest` configuration** or dev dependency group in `pyproject.toml`.
- **No CI workflow** in `.github/` (not present in tree).
- **No mock clients** for Fireworks/AMD/vision in repo.
- **No contract tests** for Pydantic schemas or prompt builders.
- End-to-end path (`VideoPipeline` + `DebatePipeline`) is **not runnable** without fixes (§4).

---

## 10. Recommended implementation order

Phases align with the project brief; order is adjusted for **dependency and unblockers** found in this audit.

| Order | Phase | Rationale |
| --- | --- | --- |
| 1 | **Configuration unification** | Fix `Settings` / `AISettings` / Fireworks & AMD env vars so imports and registry load reliably. |
| 2 | **Video pipeline wiring** | Align `VideoPipeline` with `MetadataService.extract` / `FrameService.extract_frames` (or add thin `process` wrappers). |
| 3 | **Vision + scene fixes** | `VisionPromptBuilder`, `QwenVisionClient` field names, `ScenePersistenceService.scenes_dir`, timestamp strategy. |
| 4 | **KnowledgeAgent completion** | Implement generation with valid `Prompt` (non-empty system), use `_client`, return `KnowledgeExtractionResponse` without breaking debate agent patterns. |
| 5 | **pytest + mocks** | Add unit tests for services/schemas; mock `InferenceClient` / `VisionClient` / transcription. |
| 6 | **Processing API + status model** | `video_id` in upload response; background task or worker; status/results/report routes. |
| 7 | **LangGraph** | Wrap existing agents in nodes; keep `DebatePipeline` as facade. |
| 8 | **Integration + mock E2E** | Single small sample video path with mocks; optional live tests behind flags. |
| 9 | **Frontend** | Next.js app against real APIs; demo mode with labeled fixtures. |
| 10 | **Documentation** | README, env vars, architecture, `TESTING_REPORT.md`, `FINAL_VALIDATION_REPORT.md`. |

**Do not** rewrite working debate agent / `DebatePipeline` structure unless LangGraph integration requires a thin adapter layer.

---

## Functionality matrix

Status legend: **Complete** = callable and consistent; **Partial** = substantial code but blocked defects; **Stub** = placeholder; **Missing** = not in repo.

| Module | Status | Tests | Issues |
| --- | --- | --- | --- |
| Workspace | Complete | None | Upload response omits `video_id` |
| Video Processing | Partial | None | `VideoPipeline` wrong method names; pipeline never wired to API |
| Metadata Extraction | Partial | None | Works via `extract()`; not called correctly from pipeline |
| Frame Extraction | Partial | None | Works via `extract_frames()`; not called correctly from pipeline |
| Audio Extraction | Complete | None | No silent-video policy |
| Transcription | Partial | None | Heavy import; depends on audio file |
| Vision | Partial | None | Prompt builder bug; wrong request field; scene persistence path bug |
| Knowledge Extraction | Stub | None | `NotImplementedError`; broken client attr; empty system prompt |
| Inference Layer | Partial | None | Good abstraction; provider settings missing; env required |
| Prompt System | Partial | None | Debate builders OK; vision builder broken; style template missing |
| Debate Agents | Complete | None | Need live/mock inference to verify |
| Debate Pipeline | Complete | None | Depends on knowledge + working clients |
| LangGraph | Missing | None | Not implemented |
| Persistence | Partial | None | Debate/knowledge OK; scenes broken field name |
| API | Partial | None | Only health + upload |
| Frontend | Missing | None | No UI |

---

## Phase 1 exit criteria (this document)

- [x] Repository inspected (structure, services, pipelines, AI layer, API, config, dependencies).
- [x] No application logic modified for audit purposes.
- [x] Architecture, gaps, risks, and ordered roadmap documented.
- [ ] Day 1–4 memory files — **not in repo**; user may supply separately for cross-check.

---

## Next phase (Phase 2 — Backend validation)

1. Fix **import blockers** (`Settings`, registry, `ai_settings`) with minimal diffs.
2. Run **isolated validation** per layer (workspace → metadata → frames → audio → transcript → vision → knowledge → debate → persistence) with mocks.
3. Record results in a running validation log (to become `TESTING_REPORT.md` in Phase 5).

**Blockers requiring credentials for live verification (not required for mock validation):**

- `AI_BASE_URL`, `AI_API_KEY` (and/or Fireworks/AMD-specific variables once settings are unified).
- Remote vision endpoint hosting Qwen2.5-VL (if not local).

---

## Appendix A — Key file index

| Concern | Primary files |
| --- | --- |
| App entry | `main.py` |
| Upload | `app/api/upload.py`, `app/services/upload_service.py`, `app/services/workspace_service.py` |
| Perception pipeline | `app/pipelines/video_pipeline.py`, `app/services/*_service.py` |
| Debate pipeline | `app/pipelines/debate_pipeline.py`, `app/ai/agents/*_agent.py` |
| Inference | `app/ai/providers/openai_compatible_client.py`, `app/ai/clients/*.py` |
| Config | `app/core/config.py`, `app/core/ai_settings.py` |
| Cloud dev env | `.cursor/environment.json`, `scripts/cloud-agent-install.sh` |

## Appendix B — Evidence snapshots

**VideoPipeline calls missing methods:**

```24:27:app/pipelines/video_pipeline.py
        artifacts = MetadataService.process(artifacts)
        artifacts = FrameService.process(artifacts)
        artifacts = AudioService.process(artifacts)
        artifacts = WhisperService.process(artifacts)
```

**KnowledgeAgent stub:**

```37:39:app/ai/agents/knowledge_agent.py
        self._reasoning_client.generate(inference_request)

        raise NotImplementedError
```

**Provider settings mismatch:**

```9:14:app/ai/clients/fireworks_client.py
        super().__init__(
            base_url=settings.fireworks.base_url,
            api_key=settings.fireworks.api_key,
        )
```

```3:9:app/core/config.py
class Settings(BaseSettings):
    ...
    whisper_model: str = "openai/whisper-base"
    app_name: str = "VeriVid"
```