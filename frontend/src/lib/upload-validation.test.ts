import { describe, expect, it } from "vitest";

import { validateVideoFile } from "@/lib/upload-validation";

describe("validateVideoFile", () => {
  it("rejects unsupported extensions", () => {
    const file = new File(["x"], "clip.txt", { type: "text/plain" });
    expect(validateVideoFile(file)).toMatch(/Unsupported/);
  });

  it("accepts mp4", () => {
    const file = new File(["x"], "clip.mp4", { type: "video/mp4" });
    expect(validateVideoFile(file)).toBeNull();
  });

  it("rejects empty files", () => {
    const file = new File([], "clip.mp4", { type: "video/mp4" });
    expect(validateVideoFile(file)).toMatch(/empty/i);
  });
});