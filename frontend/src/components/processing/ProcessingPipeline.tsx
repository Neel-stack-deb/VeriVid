"use client";

import { Check, Circle, Loader2 } from "lucide-react";

import { PIPELINE_STAGES } from "@/lib/constants";
import { isStageActive, isStageComplete } from "@/lib/processing-ui";
import type { ProcessingLifecycleStatus, ProcessingStage } from "@/lib/types";

export function ProcessingPipeline({
  lifecycle,
  currentStage,
}: {
  lifecycle: ProcessingLifecycleStatus;
  currentStage: ProcessingStage | null;
}) {
  return (
    <ol className="space-y-3">
      {PIPELINE_STAGES.map((stage) => {
        const done = isStageComplete(stage.id, currentStage, lifecycle);
        const active = isStageActive(stage.id, currentStage, lifecycle);
        return (
          <li
            key={stage.id}
            className={`flex items-start gap-3 rounded-lg border px-4 py-3 ${
              active
                ? "border-violet-500/50 bg-violet-500/10"
                : "border-zinc-800 bg-[#0f1016]"
            }`}
          >
            <span className="mt-0.5 text-zinc-400">
              {done ? (
                <Check className="h-4 w-4 text-emerald-400" aria-label="Completed" />
              ) : active ? (
                <Loader2 className="h-4 w-4 animate-spin text-violet-300" aria-label="In progress" />
              ) : (
                <Circle className="h-4 w-4 text-zinc-600" aria-label="Pending" />
              )}
            </span>
            <div>
              <p className="text-sm font-medium text-zinc-100">{stage.label}</p>
              <p className="text-xs text-zinc-500">{stage.description}</p>
            </div>
          </li>
        );
      })}
    </ol>
  );
}