import type { ProcessingLifecycleStatus } from "@/lib/types";

const styles: Record<ProcessingLifecycleStatus, string> = {
  uploaded: "bg-zinc-700/50 text-zinc-300 border-zinc-600",
  queued: "bg-amber-500/10 text-amber-200 border-amber-500/30",
  processing: "bg-violet-500/15 text-violet-200 border-violet-500/40",
  completed: "bg-emerald-500/15 text-emerald-200 border-emerald-500/40",
  failed: "bg-rose-500/15 text-rose-200 border-rose-500/40",
};

export function StatusBadge({ status }: { status: ProcessingLifecycleStatus }) {
  return (
    <span
      className={`inline-flex rounded-full border px-2.5 py-0.5 text-xs font-medium capitalize ${styles[status]}`}
    >
      {status}
    </span>
  );
}