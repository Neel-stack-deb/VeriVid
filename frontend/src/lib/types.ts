export type ProcessingLifecycleStatus =
  | "uploaded"
  | "queued"
  | "processing"
  | "completed"
  | "failed";

export type ProcessingStage =
  | "metadata"
  | "frames"
  | "audio"
  | "transcription"
  | "vision"
  | "knowledge"
  | "debate";

export interface VideoUploadResponse {
  video_id: string;
  filename: string;
  status: ProcessingLifecycleStatus;
}

export interface ProcessVideoResponse {
  video_id: string;
  status: ProcessingLifecycleStatus;
  message: string;
}

export interface VideoStatusResponse {
  video_id: string;
  status: ProcessingLifecycleStatus;
  current_stage: ProcessingStage | null;
  progress: number | null;
  error: string | null;
  created_at: string | null;
  started_at: string | null;
  completed_at: string | null;
}

export interface VideoDetailResponse {
  video_id: string;
  filename: string | null;
  content_type: string | null;
  file_size: number | null;
  status: ProcessingLifecycleStatus;
  current_stage: ProcessingStage | null;
  duration: number | null;
  width: number | null;
  height: number | null;
  fps: number | null;
  codec: string | null;
  created_at: string | null;
  started_at: string | null;
  completed_at: string | null;
  error: string | null;
}

export interface VideoMetadata {
  filename: string;
  duration: number;
  size: number;
  width: number;
  height: number;
  fps: number;
  codec: string;
}

export interface TranscriptSegment {
  start: number;
  end: number;
  text: string;
}

export interface Transcript {
  language: string;
  full_text: string;
  segments: TranscriptSegment[];
}

export interface DetectedObject {
  name: string;
  confidence?: number | null;
}

export interface VisibleText {
  text: string;
}

export interface Scene {
  timestamp: number;
  frame_path: string;
  description: string;
  objects: DetectedObject[];
  visible_text: VisibleText[];
}

export interface SceneCollection {
  scenes: Scene[];
}

export interface Entity {
  id: string;
  name: string;
  type: string;
  description: string | null;
  confidence: number;
}

export interface KnowledgeBase {
  entities: Entity[];
  events: unknown[];
  claims: unknown[];
  evidence: unknown[];
  relationships: unknown[];
}

export interface BaseReport {
  summary: string;
  confidence: number;
  model_name: string;
  generated_at: string;
}

export interface ContextReport extends BaseReport {
  timeline?: unknown[];
  key_entity_ids?: string[];
  key_event_ids?: string[];
}

export interface VerificationReport extends BaseReport {
  verified_claims?: unknown[];
  unsupported_claims?: unknown[];
  contradictions?: unknown[];
}

export interface RiskReport extends BaseReport {
  risks?: unknown[];
  recommendations?: string[];
}

export interface ConsensusReport extends BaseReport {
  findings?: unknown[];
  unresolved_conflicts?: string[];
}

export interface VideoResultsResponse {
  video_id: string;
  status: ProcessingLifecycleStatus;
  metadata: VideoMetadata | null;
  transcript: Transcript | null;
  scenes: SceneCollection | null;
  knowledge: KnowledgeBase | null;
  context_report: ContextReport | null;
  verification_report: VerificationReport | null;
  risk_report: RiskReport | null;
  consensus_report: ConsensusReport | null;
}

export interface ApiErrorBody {
  detail: string;
  code?: string | null;
}

export interface RecentVideoEntry {
  videoId: string;
  filename: string;
  addedAt: string;
}