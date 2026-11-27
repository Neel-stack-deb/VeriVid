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
    <ol className="space-y-2">
      {PIPELINE_STAGES.map((stage) => {
        const done = isStageComplete(stage.id, currentStage, lifecycle);
        const active = isStageActive(stage.id, currentStage, lifecycle);
        const failed = lifecycle === "failed" && active;
        return (
          <li
            key={stage.id}
            className={`flex items-start gap-3 rounded-[var(--radius-md)] border px-4 py-3 transition-colors ${
              failed
                ? "border-rose-500/35 bg-[var(--error-muted)]"
                : active
                  ? "border-violet-500/40 bg-[var(--accent-muted)]"
                  : done
                    ? "border-[var(--border-subtle)] bg-[var(--bg-inset)]"
                    : "border-[var(--border-subtle)] bg-[var(--bg-muted)] opacity-80"
            }`}
          >
            <span className="mt-0.5">
              {done ? (
                <Check className="h-4 w-4 text-emerald-400" aria-label="Completed" />
              ) : active ? (
                <Loader2
                  className="h-4 w-4 animate-spin text-violet-300"
                  aria-label="In progress"
                />
              ) : (
                <Circle className="h-4 w-4 text-[var(--text-muted)]" aria-label="Pending" />
              )}
            </span>
            <div>
              <p className="text-sm font-medium text-[var(--text-primary)]">{stage.label}</p>
              <p className="text-xs text-[var(--text-muted)]">{stage.description}</p>
            </div>
          </li>
        );
      })}
    </ol>
  );
}