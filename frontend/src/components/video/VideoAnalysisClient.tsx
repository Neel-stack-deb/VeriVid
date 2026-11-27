"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { ArrowLeft } from "lucide-react";

import { getVideoResults, ApiClientError } from "@/lib/api/client";
import { VideoResultsView } from "@/components/results/VideoResultsView";
import { Button } from "@/components/ui/Button";
import type { VideoResultsResponse } from "@/lib/types";

export function VideoAnalysisClient({ videoId }: { videoId: string }) {
  const [results, setResults] = useState<VideoResultsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getVideoResults(videoId);
      setResults(data);
      setError(null);
    } catch (err) {
      setError(
        err instanceof ApiClientError ? err.message : "Failed to load results",
      );
      setResults(null);
    } finally {
      setLoading(false);
    }
  }, [videoId]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:py-10">
      <div className="mb-8 flex flex-wrap items-center gap-4">
        <Link href={`/app/videos/${videoId}`}>
          <Button type="button" variant="ghost">
            <ArrowLeft className="h-4 w-4" />
            Workspace
          </Button>
        </Link>
        <h1 className="text-2xl font-semibold text-zinc-50">Analysis results</h1>
      </div>

      {loading ? (
        <p className="text-sm text-zinc-500">Loading results from API…</p>
      ) : error ? (
        <div className="rounded-lg border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
          {error}
          <div className="mt-3">
            <Button type="button" variant="secondary" onClick={() => void load()}>
              Retry
            </Button>
          </div>
        </div>
      ) : results ? (
        <VideoResultsView results={results} />
      ) : null}
    </div>
  );
}