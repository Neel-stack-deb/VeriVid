"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";

import { AppSidebar } from "@/components/layout/AppSidebar";
import { loadRecentVideos } from "@/lib/recent-videos";
import type { RecentVideoEntry } from "@/lib/types";

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [recent, setRecent] = useState<RecentVideoEntry[]>([]);

  useEffect(() => {
    setRecent(loadRecentVideos());
    const onStorage = () => setRecent(loadRecentVideos());
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  useEffect(() => {
    setRecent(loadRecentVideos());
  }, [pathname]);

  return (
    <div className="flex min-h-screen flex-col bg-[#08090d] lg:flex-row">
      <AppSidebar recent={recent} statuses={{}} />
      <main className="min-h-screen flex-1 overflow-x-hidden">{children}</main>
    </div>
  );
}