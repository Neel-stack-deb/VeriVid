"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { ArrowLeft } from "lucide-react";

import { getVideoResults, ApiClientError } from "@/lib/api/client";
import { VideoResultsView } from "@/components/results/VideoResultsView";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader } from "@/components/ui/Card";
import { SkeletonText } from "@/components/ui/Skeleton";
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
            <ArrowLeft className="h-4 w-4" aria-hidden />
            Workspace
          </Button>
        </Link>
        <div>
          <h1 className="page-title">Analysis results</h1>
          <p className="mt-1 font-mono text-xs text-[var(--text-muted)]">{videoId}</p>
        </div>
      </div>

      {loading ? (
        <Card>
          <CardHeader title="Loading results" />
          <div className="px-5 py-6">
            <SkeletonText lines={4} />
          </div>
        </Card>
      ) : error ? (
        <div
          className="rounded-[var(--radius-lg)] border border-rose-500/30 bg-[var(--error-muted)] px-4 py-4 text-sm text-rose-200"
          role="alert"
        >
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