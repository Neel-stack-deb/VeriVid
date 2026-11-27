"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Film, LayoutDashboard, Sparkles } from "lucide-react";

import type { RecentVideoEntry } from "@/lib/types";
import { StatusBadge } from "@/components/ui/Badge";

export function AppSidebar({
  recent,
  statuses,
}: {
  recent: RecentVideoEntry[];
  statuses: Record<string, string | undefined>;
}) {
  const pathname = usePathname();

  return (
    <aside className="flex w-full flex-col border-r border-zinc-800 bg-[#0b0c10] lg:w-72 lg:min-h-screen">
      <div className="border-b border-zinc-800 px-4 py-5">
        <Link href="/" className="flex items-center gap-2">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-violet-600 text-sm font-bold">
            V
          </span>
          <span className="font-semibold text-zinc-100">VeriVid</span>
        </Link>
      </div>
      <nav className="flex flex-col gap-1 p-3">
        <Link
          href="/app"
          className={`flex items-center gap-2 rounded-lg px-3 py-2 text-sm ${
            pathname === "/app"
              ? "bg-violet-500/10 text-violet-200"
              : "text-zinc-400 hover:bg-white/5"
          }`}
        >
          <LayoutDashboard className="h-4 w-4" />
          Workspace
        </Link>
        <Link
          href="/app/demo"
          className={`flex items-center gap-2 rounded-lg px-3 py-2 text-sm ${
            pathname === "/app/demo"
              ? "bg-violet-500/10 text-violet-200"
              : "text-zinc-400 hover:bg-white/5"
          }`}
        >
          <Sparkles className="h-4 w-4" />
          Demo (sample data)
        </Link>
      </nav>
      <div className="mt-2 px-4 pb-2 text-xs font-medium uppercase tracking-wide text-zinc-500">
        Recent videos
      </div>
      <ul className="flex-1 space-y-1 overflow-y-auto px-2 pb-4">
        {recent.length === 0 ? (
          <li className="px-2 py-4 text-xs text-zinc-600">
            Upload a video to see it here. IDs are stored locally in your
            browser only.
          </li>
        ) : (
          recent.map((item) => (
            <li key={item.videoId}>
              <Link
                href={`/app/videos/${item.videoId}`}
                className="flex items-center gap-2 rounded-lg px-2 py-2 text-sm text-zinc-300 hover:bg-white/5"
              >
                <Film className="h-4 w-4 shrink-0 text-zinc-500" />
                <span className="min-w-0 flex-1 truncate">{item.filename}</span>
                {statuses[item.videoId] ? (
                  <StatusBadge
                    status={statuses[item.videoId] as import("@/lib/types").ProcessingLifecycleStatus}
                  />
                ) : null}
              </Link>
            </li>
          ))
        )}
      </ul>
    </aside>
  );
}