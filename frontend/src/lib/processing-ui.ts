import type { ProcessingLifecycleStatus, ProcessingStage } from "@/lib/types";
import { PIPELINE_STAGES } from "@/lib/constants";

export function stageIndex(stage: ProcessingStage | null): number {
  if (!stage) return -1;
  return PIPELINE_STAGES.findIndex((s) => s.id === stage);
}

export function isStageComplete(
  stageId: ProcessingStage,
  current: ProcessingStage | null,
  lifecycle: ProcessingLifecycleStatus,
): boolean {
  if (lifecycle === "completed") return true;
  if (lifecycle === "failed") {
    const failedAt = stageIndex(current);
    const idx = stageIndex(stageId);
    return failedAt >= 0 && idx < failedAt;
  }
  if (!current) return false;
  return stageIndex(stageId) < stageIndex(current);
}

export function isStageActive(
  stageId: ProcessingStage,
  current: ProcessingStage | null,
  lifecycle: ProcessingLifecycleStatus,
): boolean {
  return lifecycle === "processing" && current === stageId;
}