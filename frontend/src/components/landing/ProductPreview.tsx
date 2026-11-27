import { CheckCircle2, Circle, Users } from "lucide-react";

import { Card } from "@/components/ui/Card";

const pipeline = [
  { label: "Metadata", done: true },
  { label: "Vision", done: true },
  { label: "Knowledge", done: true },
  { label: "Debate Council", done: false, active: true },
];

export function ProductPreview() {
  return (
    <Card className="overflow-hidden border-zinc-700/80 bg-[var(--bg-muted)] p-0">
      <div className="flex items-center justify-between border-b border-[var(--border-default)] bg-[var(--bg-inset)] px-4 py-3">
        <WindowChrome />
        <span className="text-xs text-[var(--text-muted)]">analysis_workspace.preview</span>
      </div>
      <div className="space-y-4 p-5">
        <div className="flex items-center gap-2">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-40" />
            <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
          </span>
          <span className="text-sm font-medium text-[var(--text-primary)]">
            demo_interview.mp4
          </span>
          <span className="rounded-full border border-violet-500/30 bg-[var(--accent-muted)] px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-violet-200">
            processing
          </span>
        </div>

        <div className="space-y-2">
          <p className="text-meta">Pipeline</p>
          {pipeline.map((stage) => (
            <div
              key={stage.label}
              className={`flex items-center gap-3 rounded-[var(--radius-md)] border px-3 py-2 ${
                stage.active
                  ? "border-violet-500/40 bg-[var(--accent-muted)]"
                  : "border-[var(--border-subtle)] bg-[var(--bg-inset)]"
              }`}
            >
              {stage.done ? (
                <CheckCircle2 className="h-4 w-4 text-emerald-400" aria-hidden />
              ) : stage.active ? (
                <Circle className="h-4 w-4 text-violet-300" aria-hidden />
              ) : (
                <Circle className="h-4 w-4 text-[var(--text-muted)]" aria-hidden />
              )}
              <span className="text-sm text-[var(--text-secondary)]">{stage.label}</span>
            </div>
          ))}
        </div>

        <div className="rounded-[var(--radius-md)] border border-[var(--border-subtle)] bg-[var(--bg-inset)] p-3">
          <p className="text-meta">Scene · 12.4s</p>
          <p className="mt-1 text-sm text-[var(--text-secondary)]">
            Presenter at desk with slides — objects: laptop, microphone
          </p>
        </div>

        <div className="grid grid-cols-2 gap-2">
          {["Context", "Verification", "Risk", "Consensus"].map((agent, i) => (
            <div
              key={agent}
              className={`rounded-[var(--radius-md)] border px-2 py-2 text-center ${
                i === 3
                  ? "border-violet-500/35 bg-[var(--accent-muted)]"
                  : "border-[var(--border-subtle)] bg-[var(--bg-inset)]"
              }`}
            >
              <Users className="mx-auto h-3 w-3 text-[var(--text-muted)]" aria-hidden />
              <p className="mt-1 text-[10px] font-medium text-[var(--text-secondary)]">
                {agent}
              </p>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}

function WindowChrome() {
  return (
    <div className="flex gap-1.5" aria-hidden>
      <span className="h-2.5 w-2.5 rounded-full bg-zinc-600" />
      <span className="h-2.5 w-2.5 rounded-full bg-zinc-600" />
      <span className="h-2.5 w-2.5 rounded-full bg-zinc-600" />
    </div>
  );
}