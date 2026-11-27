"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { Menu } from "lucide-react";

import { AppSidebar } from "@/components/layout/AppSidebar";
import { loadRecentVideos } from "@/lib/recent-videos";
import type { RecentVideoEntry } from "@/lib/types";

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [recent, setRecent] = useState<RecentVideoEntry[]>([]);
  const [mobileNav, setMobileNav] = useState(false);

  useEffect(() => {
    setRecent(loadRecentVideos());
    const onStorage = () => setRecent(loadRecentVideos());
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  useEffect(() => {
    setRecent(loadRecentVideos());
    setMobileNav(false);
  }, [pathname]);

  return (
    <div className="flex min-h-screen bg-[var(--bg-base)]">
      <AppSidebar
        recent={recent}
        statuses={{}}
        mobileOpen={mobileNav}
        onCloseMobile={() => setMobileNav(false)}
      />
      <div className="flex min-h-screen min-w-0 flex-1 flex-col">
        <div className="flex items-center gap-3 border-b border-[var(--border-subtle)] bg-[var(--bg-muted)] px-4 py-3 lg:hidden">
          <button
            type="button"
            className="rounded-[var(--radius-md)] border border-[var(--border-default)] p-2 text-[var(--text-secondary)] hover:bg-white/[0.04]"
            aria-label="Open navigation"
            aria-expanded={mobileNav}
            onClick={() => setMobileNav(true)}
          >
            <Menu className="h-5 w-5" />
          </button>
          <span className="text-sm font-medium text-[var(--text-primary)]">VeriVid</span>
        </div>
        <main className="flex-1 overflow-x-hidden">{children}</main>
      </div>
    </div>
  );
}