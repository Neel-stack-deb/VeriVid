import type { VideoResultsResponse } from "@/lib/types";

/** Static sample data — labeled demo only; not from live AI inference. */
export const DEMO_RESULTS: VideoResultsResponse = {
  video_id: "demo-sample",
  status: "completed",
  metadata: {
    filename: "demo_interview.mp4",
    duration: 42.5,
    size: 1200000,
    width: 1920,
    height: 1080,
    fps: 30,
    codec: "h264",
  },
  transcript: {
    language: "en",
    full_text: "Sample transcript for portfolio demonstration only.",
    segments: [
      { start: 0, end: 3.2, text: "Welcome to the demonstration." },
      { start: 3.2, end: 8.1, text: "This is precomputed demo content." },
    ],
  },
  scenes: {
    scenes: [
      {
        timestamp: 1,
        frame_path: "demo/frame.jpg",
        description: "Presenter at desk with slides",
        objects: [{ name: "laptop" }],
        visible_text: [{ text: "DEMO" }],
      },
    ],
  },
  knowledge: {
    entities: [
      {
        id: "demo-ent",
        name: "Presenter",
        type: "Person",
        description: "Sample entity",
        confidence: 0.9,
      },
    ],
    events: [],
    claims: [],
    evidence: [],
    relationships: [],
  },
  context_report: {
    summary: "Demo context summary — not live AI output.",
    confidence: 0.85,
    model_name: "demo",
    generated_at: "2026-01-01T00:00:00Z",
  },
  verification_report: {
    summary: "Demo verification summary.",
    confidence: 0.8,
    model_name: "demo",
    generated_at: "2026-01-01T00:00:00Z",
  },
  risk_report: {
    summary: "Demo risk summary.",
    confidence: 0.75,
    model_name: "demo",
    generated_at: "2026-01-01T00:00:00Z",
  },
  consensus_report: {
    summary: "Demo consensus — sample data only.",
    confidence: 0.9,
    model_name: "demo",
    generated_at: "2026-01-01T00:00:00Z",
    findings: [],
    unresolved_conflicts: [],
  },
};