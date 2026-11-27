import { FlaskConical } from "lucide-react";

export function DemoBanner() {
  return (
    <div
      className="sticky top-0 z-20 mb-8 flex items-start gap-3 rounded-[var(--radius-lg)] border border-violet-500/35 bg-[var(--accent-muted)] px-4 py-3 backdrop-blur-sm"
      role="note"
      aria-label="Demo mode"
    >
      <FlaskConical className="mt-0.5 h-5 w-5 shrink-0 text-violet-300" aria-hidden />
      <div>
        <p className="text-sm font-medium text-violet-100">Demo mode — sample data only</p>
        <p className="mt-0.5 text-sm text-violet-200/75">
          Static portfolio content. Not produced by a live VeriVid pipeline. Use the workspace
          to upload and analyze real videos.
        </p>
      </div>
    </div>
  );
}