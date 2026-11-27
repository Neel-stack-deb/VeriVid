import type { RecentVideoEntry } from "@/lib/types";
import { RECENT_VIDEOS_KEY } from "@/lib/constants";

export function loadRecentVideos(): RecentVideoEntry[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(RECENT_VIDEOS_KEY);
    if (!raw) return [];
    return JSON.parse(raw) as RecentVideoEntry[];
  } catch {
    return [];
  }
}

export function saveRecentVideo(entry: RecentVideoEntry): void {
  const existing = loadRecentVideos().filter((v) => v.videoId !== entry.videoId);
  const next = [entry, ...existing].slice(0, 20);
  localStorage.setItem(RECENT_VIDEOS_KEY, JSON.stringify(next));
}

export function removeRecentVideo(videoId: string): void {
  const next = loadRecentVideos().filter((v) => v.videoId !== videoId);
  localStorage.setItem(RECENT_VIDEOS_KEY, JSON.stringify(next));
}