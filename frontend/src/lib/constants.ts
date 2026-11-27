import type { ProcessingStage } from "@/lib/types";

export const ALLOWED_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv", ".webm"];

export const PIPELINE_STAGES: {
  id: ProcessingStage;
  label: string;
  description: string;
}[] = [
  { id: "metadata", label: "Metadata", description: "Extract duration, resolution, codec" },
  { id: "frames", label: "Frames", description: "Sample visual frames from the video" },
  { id: "audio", label: "Audio", description: "Extract speech audio track" },
  { id: "transcription", label: "Transcription", description: "Speech-to-text" },
  { id: "vision", label: "Vision", description: "Scene understanding per frame" },
  { id: "knowledge", label: "Knowledge", description: "Structured knowledge extraction" },
  { id: "debate", label: "Debate Council", description: "Multi-agent verification" },
];

export const POLL_INTERVAL_MS = 2000;

export const RECENT_VIDEOS_KEY = "verivid.recentVideos";