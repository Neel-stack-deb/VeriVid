# VeriVid REST API

Base URL: `http://localhost:8000` (development)

OpenAPI: `/docs`

## Video identity

Each upload creates a workspace under `data/videos/{video_id}/` where `video_id` is a UUID. All endpoints use this id.

## Endpoints

### `POST /api/videos/upload`

Upload a video file (multipart field `video`).

**201 response**

```json
{
  "video_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "example.mp4",
  "status": "uploaded"
}
```

### `POST /api/videos/{video_id}/process`

Queue in-process background analysis. Returns immediately.

**200 response**

```json
{
  "video_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Processing started"
}
```

If processing is already `queued` or `processing`, the message indicates work is in progress. Completed videos are not re-run automatically.

### `GET /api/videos/{video_id}/status`

**200 response**

```json
{
  "video_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "current_stage": "vision",
  "progress": null,
  "error": null,
  "created_at": "2026-11-27T12:00:00",
  "started_at": "2026-11-27T12:00:05",
  "completed_at": null
}
```

### `GET /api/videos/{video_id}`

Video metadata and lifecycle fields (duration, dimensions when metadata artifact exists).

### `GET /api/videos/{video_id}/results`

Structured artifacts. Sections may be `null` until generated.

Includes: `metadata`, `transcript`, `scenes`, `knowledge`, `context_report`, `verification_report`, `risk_report`, `consensus_report`.

### `DELETE /api/videos/{video_id}`

Removes the workspace directory. Returns **409** if processing is active.

## Legacy upload

`POST /upload` remains available. Response includes `video_id` plus legacy fields (`storage_path`, etc.).

## Lifecycle

| Status | Meaning |
| --- | --- |
| `uploaded` | Stored, not processed |
| `queued` | Job accepted by in-process executor |
| `processing` | Pipeline running |
| `completed` | Success |
| `failed` | Error recorded in `error` |

### Stages (during `processing`)

`metadata` → `frames` → `audio` → `transcription` → `vision` → `knowledge` → `debate`

`progress` is optional and usually omitted.

## Errors

| Code | HTTP | When |
| --- | --- | --- |
| `internal_error` | 500 | Unhandled server error (no stack trace in body) |
| — | 404 | Unknown `video_id` |
| — | 400 | Invalid upload |
| — | 409 | Delete while processing |

## Background execution

Implementation: `InProcessJobExecutor` (`app/jobs/executor.py`) using a `ThreadPoolExecutor`.

**Limitations**

- Jobs are lost on process restart.
- Not suitable for multi-instance deployment without a durable queue.
- One active job per `video_id`; duplicates while running are rejected or reported as in progress.

Replace `JobExecutor` to add Redis/Celery later without changing route handlers.

## Configuration

| Variable | Purpose |
| --- | --- |
| `CORS_ORIGINS` | Comma-separated browser origins |
| `FIREWORKS_*`, `AMD_*`, `AI_*` | Inference providers (required only when processing runs for real) |

## Frontend consumption

1. `POST /api/videos/upload` → store `video_id`.
2. `POST /api/videos/{video_id}/process`.
3. Poll `GET /api/videos/{video_id}/status` until `completed` or `failed`.
4. `GET /api/videos/{video_id}/results` for the full structured payload.
5. Use `GET /api/videos/{video_id}` for summary cards.