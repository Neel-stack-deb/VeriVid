import type {
  ApiErrorBody,
  ProcessVideoResponse,
  VideoDetailResponse,
  VideoResultsResponse,
  VideoStatusResponse,
  VideoUploadResponse,
} from "@/lib/types";

const DEFAULT_BASE =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ?? "http://localhost:8000";

export class ApiClientError extends Error {
  status: number;
  body: ApiErrorBody | null;

  constructor(message: string, status: number, body: ApiErrorBody | null = null) {
    super(message);
    this.name = "ApiClientError";
    this.status = status;
    this.body = body;
  }
}

function baseUrl(): string {
  return DEFAULT_BASE;
}

async function parseError(response: Response): Promise<ApiClientError> {
  let body: ApiErrorBody | null = null;
  try {
    body = (await response.json()) as ApiErrorBody;
  } catch {
    body = null;
  }
  const detail = body?.detail ?? `Request failed with status ${response.status}`;
  return new ApiClientError(detail, response.status, body);
}

export async function uploadVideo(
  file: File,
  onProgress?: (ratio: number) => void,
  signal?: AbortSignal,
): Promise<VideoUploadResponse> {
  const form = new FormData();
  form.append("video", file);

  // Fetch does not expose upload progress natively; simulate coarse steps.
  onProgress?.(0.2);

  const response = await fetch(`${baseUrl()}/api/videos/upload`, {
    method: "POST",
    body: form,
    signal,
  });

  onProgress?.(0.9);

  if (!response.ok) {
    throw await parseError(response);
  }

  onProgress?.(1);
  return (await response.json()) as VideoUploadResponse;
}

export async function startProcessing(
  videoId: string,
  signal?: AbortSignal,
): Promise<ProcessVideoResponse> {
  const response = await fetch(`${baseUrl()}/api/videos/${videoId}/process`, {
    method: "POST",
    signal,
  });
  if (!response.ok) throw await parseError(response);
  return (await response.json()) as ProcessVideoResponse;
}

export async function getVideoStatus(
  videoId: string,
  signal?: AbortSignal,
): Promise<VideoStatusResponse> {
  const response = await fetch(`${baseUrl()}/api/videos/${videoId}/status`, {
    signal,
    cache: "no-store",
  });
  if (!response.ok) throw await parseError(response);
  return (await response.json()) as VideoStatusResponse;
}

export async function getVideoDetail(
  videoId: string,
  signal?: AbortSignal,
): Promise<VideoDetailResponse> {
  const response = await fetch(`${baseUrl()}/api/videos/${videoId}`, {
    signal,
    cache: "no-store",
  });
  if (!response.ok) throw await parseError(response);
  return (await response.json()) as VideoDetailResponse;
}

export async function getVideoResults(
  videoId: string,
  signal?: AbortSignal,
): Promise<VideoResultsResponse> {
  const response = await fetch(`${baseUrl()}/api/videos/${videoId}/results`, {
    signal,
    cache: "no-store",
  });
  if (!response.ok) throw await parseError(response);
  return (await response.json()) as VideoResultsResponse;
}

export async function deleteVideo(
  videoId: string,
  signal?: AbortSignal,
): Promise<void> {
  const response = await fetch(`${baseUrl()}/api/videos/${videoId}`, {
    method: "DELETE",
    signal,
  });
  if (!response.ok) throw await parseError(response);
}

export function getApiBaseUrl(): string {
  return baseUrl();
}