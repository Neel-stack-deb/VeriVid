import { afterEach, describe, expect, it, vi } from "vitest";

import { ApiClientError, getVideoStatus, uploadVideo } from "@/lib/api/client";

describe("api client", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("parses API errors", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 404,
        json: async () => ({ detail: "Video not found" }),
      }),
    );

    await expect(getVideoStatus("missing")).rejects.toBeInstanceOf(
      ApiClientError,
    );
    await expect(getVideoStatus("missing")).rejects.toMatchObject({
      message: "Video not found",
      status: 404,
    });
  });

  it("uploads video and returns payload", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          video_id: "abc",
          filename: "a.mp4",
          status: "uploaded",
        }),
      }),
    );

    const file = new File(["data"], "a.mp4", { type: "video/mp4" });
    const result = await uploadVideo(file);
    expect(result.video_id).toBe("abc");
  });
});