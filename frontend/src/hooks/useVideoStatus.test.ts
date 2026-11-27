import { renderHook } from "@testing-library/react";
import { waitFor } from "@testing-library/dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import { useVideoStatus } from "@/hooks/useVideoStatus";

vi.mock("@/lib/api/client", () => ({
  ApiClientError: class ApiClientError extends Error {},
  getVideoStatus: vi.fn(),
}));

import { getVideoStatus } from "@/lib/api/client";

describe("useVideoStatus", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("stops polling when completed", async () => {
    vi.mocked(getVideoStatus).mockResolvedValue({
      video_id: "v1",
      status: "completed",
      current_stage: null,
      progress: 1,
      error: null,
      created_at: null,
      started_at: null,
      completed_at: null,
    });

    const { result } = renderHook(() => useVideoStatus("v1"));

    await waitFor(() => expect(result.current.status?.status).toBe("completed"));
    expect(result.current.isPolling).toBe(false);
  });
});