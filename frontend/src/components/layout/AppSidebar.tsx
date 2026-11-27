"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Film, LayoutDashboard, Sparkles, X } from "lucide-react";

import type { RecentVideoEntry } from "@/lib/types";
import { StatusBadge } from "@/components/ui/Badge";

function navLinkClass(active: boolean) {
  return active
    ? "bg-[var(--accent-muted)] text-violet-200 border border-violet-500/20"
    : "text-[var(--text-secondary)] border border-transparent hover:bg-white/[0.04] hover:text-[var(--text-primary)]";
}

export function AppSidebar({
  recent,
  statuses,
  mobileOpen,
  onCloseMobile,
}: {
  recent: RecentVideoEntry[];
  statuses: Record<string, string | undefined>;
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
}) {
  const pathname = usePathname();

  const asideClass = [
    "flex w-72 shrink-0 flex-col border-r border-[var(--border-default)] bg-[var(--bg-muted)]",
    "fixed inset-y-0 left-0 z-40 transform transition-transform duration-200 lg:static lg:translate-x-0",
    mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0",
  ].join(" ");

  return (
    <>
      {mobileOpen ? (
        <button
          type="button"
          className="fixed inset-0 z-30 bg-black/60 lg:hidden"
          aria-label="Close navigation"
          onClick={onCloseMobile}
        />
      ) : null}
      <aside className={asideClass} aria-label="Workspace">
        <div className="flex items-center justify-between border-b border-[var(--border-subtle)] px-4 py-4">
          <Link href="/" className="flex items-center gap-2" onClick={onCloseMobile}>
            <span className="flex h-8 w-8 items-center justify-center rounded-[var(--radius-md)] border border-violet-500/30 bg-[var(--accent-muted)] text-sm font-semibold text-violet-200">
              V
            </span>
            <span className="font-semibold text-[var(--text-primary)]">VeriVid</span>
          </Link>
          <button
            type="button"
            className="rounded-[var(--radius-md)] p-2 text-[var(--text-muted)] hover:bg-white/5 lg:hidden"
            onClick={onCloseMobile}
            aria-label="Close sidebar"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
        <nav className="flex flex-col gap-1 p-3">
          <Link
            href="/app"
            onClick={onCloseMobile}
            className={`flex items-center gap-2 rounded-[var(--radius-md)] px-3 py-2 text-sm transition-colors ${navLinkClass(pathname === "/app")}`}
          >
            <LayoutDashboard className="h-4 w-4" aria-hidden />
            Workspace
          </Link>
          <Link
            href="/app/demo"
            onClick={onCloseMobile}
            className={`flex items-center gap-2 rounded-[var(--radius-md)] px-3 py-2 text-sm transition-colors ${navLinkClass(pathname === "/app/demo")}`}
          >
            <Sparkles className="h-4 w-4" aria-hidden />
            Demo (sample data)
          </Link>
        </nav>
        <RecentVideosLabel />
        <ul className="flex-1 space-y-0.5 overflow-y-auto px-2 pb-4">
          {recent.length === 0 ? (
            <li className="px-2 py-4 text-xs leading-relaxed text-[var(--text-muted)]">
              Upload a video to see it here. IDs are stored locally in your browser only.
            </li>
          ) : (
            recent.map((item) => (
              <li key={item.videoId}>
                <Link
                  href={`/app/videos/${item.videoId}`}
                  onClick={onCloseMobile}
                  className={`flex items-center gap-2 rounded-[var(--radius-md)] px-2 py-2 text-sm transition-colors ${
                    pathname.includes(item.videoId)
                      ? "bg-white/[0.04] text-[var(--text-primary)]"
                      : "text-[var(--text-secondary)] hover:bg-white/[0.04]"
                  }`}
                >
                  <Film className="h-4 w-4 shrink-0 text-[var(--text-muted)]" aria-hidden />
                  <span className="min-w-0 flex-1 truncate">{item.filename}</span>
                  {statuses[item.videoId] ? (
                    <StatusBadge
                      status={
                        statuses[item.videoId] as import("@/lib/types").ProcessingLifecycleStatus
                      }
                    />
                  ) : null}
                </Link>
              </li>
            ))
          )}
        </ul>
      </aside>
    </>
  );
}

function RecentVideosLabel() {
  return <div className="mt-2 px-4 pb-2 text-meta">Recent videos</div>;
}