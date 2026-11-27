"use client";

import { Loader2, Wifi, WifiOff } from "lucide-react";

export type ConnectionState = "checking" | "connected" | "disconnected";

export function ConnectionStatus({
  state,
  apiBase,
}: {
  state: ConnectionState;
  apiBase: string;
}) {
  if (state === "checking") {
    return (
      <div
        className="flex items-center gap-2 rounded-[var(--radius-md)] border border-[var(--border-default)] bg-[var(--bg-muted)] px-3 py-2 text-sm text-[var(--text-secondary)]"
        role="status"
        aria-live="polite"
      >
        <Loader2 className="h-4 w-4 animate-spin text-[var(--text-muted)]" aria-hidden />
        Checking API connection…
      </div>
    );
  }

  if (state === "connected") {
    return (
      <div
        className="flex items-center gap-2 rounded-[var(--radius-md)] border border-emerald-500/25 bg-[var(--success-muted)] px-3 py-2 text-sm text-emerald-200"
        role="status"
      >
        <Wifi className="h-4 w-4 text-emerald-400" aria-hidden />
        <span>
          Connected · <span className="font-mono text-xs text-emerald-300/90">{apiBase}</span>
        </span>
      </div>
    );
  }

  return (
    <div
      className="rounded-[var(--radius-md)] border border-amber-500/30 bg-[var(--warning-muted)] px-3 py-2 text-sm text-amber-100"
      role="alert"
    >
      <div className="flex items-start gap-2">
        <WifiOff className="mt-0.5 h-4 w-4 shrink-0 text-amber-300" aria-hidden />
        <div>
          <p className="font-medium">API unreachable</p>
          <p className="mt-1 text-amber-200/80">
            Cannot reach <span className="font-mono text-xs">{apiBase}</span>. Start the
            backend with{" "}
            <code className="rounded bg-black/20 px-1 text-amber-100">
              uv run uvicorn main:app --port 8000
            </code>{" "}
            and set{" "}
            <code className="rounded bg-black/20 px-1 text-amber-100">
              NEXT_PUBLIC_API_URL
            </code>{" "}
            if needed.
          </p>
        </div>
      </div>
    </div>
  );
}