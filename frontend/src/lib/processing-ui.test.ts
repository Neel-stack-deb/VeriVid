import { describe, expect, it } from "vitest";

import { isStageActive, isStageComplete } from "@/lib/processing-ui";

describe("processing-ui", () => {
  it("marks stages before current as complete while processing", () => {
    expect(isStageComplete("metadata", "vision", "processing")).toBe(true);
    expect(isStageComplete("debate", "vision", "processing")).toBe(false);
  });

  it("marks all stages complete when lifecycle completed", () => {
    expect(isStageComplete("metadata", null, "completed")).toBe(true);
  });

  it("activates only matching stage", () => {
    expect(isStageActive("vision", "vision", "processing")).toBe(true);
    expect(isStageActive("metadata", "vision", "processing")).toBe(false);
  });
});