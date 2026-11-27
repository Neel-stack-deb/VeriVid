import { render } from "@testing-library/react";
import { screen } from "@testing-library/dom";
import { describe, expect, it } from "vitest";

import { DebateCouncil } from "@/components/debate/DebateCouncil";

describe("DebateCouncil", () => {
  it("renders agent cards and summaries", () => {
    render(
      <DebateCouncil
        reports={{
          context_report: {
            summary: "Context output",
            confidence: 0.9,
            model_name: "test",
            generated_at: "2026-01-01T00:00:00Z",
          },
          verification_report: null,
          risk_report: null,
          consensus_report: {
            summary: "Final consensus",
            confidence: 0.95,
            model_name: "test",
            generated_at: "2026-01-01T00:00:00Z",
          },
        }}
      />,
    );

    expect(screen.getByText("Context Agent")).toBeInTheDocument();
    expect(screen.getByText("Consensus Agent")).toBeInTheDocument();
    expect(screen.getAllByText("Report available").length).toBeGreaterThan(0);
  });
});