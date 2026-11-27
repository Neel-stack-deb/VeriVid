# VeriVid Frontend (Phase 5)

Next.js 15 App Router application under `frontend/`. It talks to the FastAPI backend via `NEXT_PUBLIC_API_URL`.

## Architecture

```
frontend/src/
  app/                 # Routes (App Router)
  components/          # UI, layout, feature components
  demo/                # Labeled static demo data (not from live AI)
  hooks/               # Client hooks (status polling)
  lib/
    api/client.ts      # Typed REST client
    types.ts           # Mirrors API schemas
```

Server Components are used for static shells; interactive flows are Client Components.

## Routes

| Route | Purpose |
| --- | --- |
| `/` | Product landing page |
| `/app` | Workspace — upload entry |
| `/app/videos/[videoId]` | Video workspace, process, live status |
| `/app/videos/[videoId]/analysis` | Full results dashboard |
| `/app/demo` | Sample results only (clearly labeled) |

## API integration

Base URL: `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`).

| Client function | Endpoint |
| --- | --- |
| `uploadVideo` | `POST /api/videos/upload` |
| `startProcessing` | `POST /api/videos/{id}/process` |
| `getVideoStatus` | `GET /api/videos/{id}/status` |
| `getVideoDetail` | `GET /api/videos/{id}` |
| `getVideoResults` | `GET /api/videos/{id}/results` |
| `deleteVideo` | `DELETE /api/videos/{id}` |

Errors surface as `ApiClientError` with HTTP status and `detail` body.

For local development, set backend `CORS_ORIGINS` to include `http://localhost:3000`.

## State

- Processing status is always refreshed from the API (`useVideoStatus`, 2s poll until `completed` or `failed`).
- Recent uploads are stored in `localStorage` (`verivid.recentVideos`) for navigation only — not authoritative.

## Environment

Copy `frontend/.env.example` to `frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

No secrets belong in frontend env vars.

## Local development

Terminal 1 — API:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

Terminal 2 — frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Testing

```bash
cd frontend
npm run test
npm run typecheck
npm run lint
npm run build
```

Vitest covers upload validation, processing stage helpers, API client error handling, status polling termination, and Debate Council rendering.

## Demo mode

`/app/demo` renders `demo/sampleResults.ts`. Banners state that outputs are static portfolio samples, separate from live API execution.

## Known limitations

- No authentication or server-side user accounts.
- Upload progress is coarse (Fetch has no native upload progress).
- No in-browser video preview stream from API (metadata and pipeline UI only).
- Sidebar does not batch-fetch live status for every recent video.
- Accessibility-oriented insights called out on landing as planned backend work.