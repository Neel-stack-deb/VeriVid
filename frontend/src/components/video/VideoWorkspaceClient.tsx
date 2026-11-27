"use client";

import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { AlertCircle, Play, RefreshCw, BarChart3 } from "lucide-react";

import {
  getVideoDetail,
  startProcessing,
  ApiClientError,
} from "@/lib/api/client";
import { useVideoStatus } from "@/hooks/useVideoStatus";
import { ProcessingPipeline } from "@/components/processing/ProcessingPipeline";
import { StatusBadge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader } from "@/components/ui/Card";
import { Skeleton, SkeletonText } from "@/components/ui/Skeleton";
import type { VideoDetailResponse } from "@/lib/types";

export function VideoWorkspaceClient({ videoId }: { videoId: string }) {
  const { status, error: statusError, loading: statusLoading, refresh } =
    useVideoStatus(videoId);
  const [detail, setDetail] = useState<VideoDetailResponse | null>(null);
  const [detailError, setDetailError] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);
  const [startError, setStartError] = useState<string | null>(null);
  const processingLock = useRef(false);

  const loadDetail = useCallback(async () => {
    try {
      const data = await getVideoDetail(videoId);
      setDetail(data);
      setDetailError(null);
    } catch (err) {
      setDetailError(
        err instanceof ApiClientError ? err.message : "Failed to load video",
      );
    }
  }, [videoId]);

  useEffect(() => {
    void loadDetail();
  }, [loadDetail]);

  const lifecycle = status?.status ?? detail?.status ?? "uploaded";
  const busy =
    lifecycle === "queued" || lifecycle === "processing" || starting;

  const handleStart = async () => {
    if (processingLock.current || busy) return;
    if (lifecycle === "completed") return;
    processingLock.current = true;
    setStarting(true);
    setStartError(null);
    try {
      await startProcessing(videoId);
      await refresh();
      await loadDetail();
    } catch (err) {
      setStartError(
        err instanceof ApiClientError ? err.message : "Could not start processing",
      );
    } finally {
      setStarting(false);
      processingLock.current = false;
    }
  };

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:py-10">
      <header className="mb-8">
        <div className="flex flex-wrap items-center gap-3">
          {!detail && !detailError ? (
            <Skeleton className="h-8 w-48" />
          ) : (
            <h1 className="page-title">
              {detail?.filename ?? `Video ${videoId.slice(0, 8)}…`}
            </h1>
          )}
          <StatusBadge status={lifecycle} />
        </div>
        <p className="mt-2 font-mono text-xs text-[var(--text-muted)]">{videoId}</p>
      </header>

      {(detailError || statusError || startError) && (
        <div
          className="mb-6 flex items-start gap-2 rounded-[var(--radius-lg)] border border-rose-500/30 bg-[var(--error-muted)] px-4 py-3 text-sm text-rose-200"
          role="alert"
        >
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden />
          <span>{startError ?? statusError ?? detailError}</span>
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-[1fr_280px]">
        <Card>
          <CardHeader title="Processing" description="Live pipeline from API status" />
          <div className="space-y-4 px-5 py-5">
            {statusLoading && !status ? (
              <SkeletonText lines={5} />
            ) : (
              <>
                <div className="flex flex-wrap items-center gap-3">
                  <StatusBadge status={lifecycle} />
                  {status?.current_stage ? (
                    <span className="text-xs text-[var(--text-muted)]">
                      Stage{" "}
                      <span className="text-[var(--text-secondary)]">
                        {status.current_stage}
                      </span>
                    </span>
                  ) : null}
                  {status?.progress != null ? (
                    <span className="text-xs text-[var(--text-muted)]">
                      Progress {(status.progress * 100).toFixed(0)}%
                    </span>
                  ) : null}
                </div>
                <ProcessingPipeline
                  lifecycle={lifecycle}
                  currentStage={status?.current_stage ?? null}
                />
                {status?.error ? (
                  <p className="text-sm text-rose-300">{status.error}</p>
                ) : null}
              </>
            )}
          </div>
        </Card>

        <aside className="space-y-4">
          <Card>
            <CardHeader title="Actions" />
            <div className="flex flex-col gap-2 px-5 py-4">
              <Button
                type="button"
                disabled={busy || lifecycle === "completed"}
                onClick={() => void handleStart()}
              >
                <Play className="h-4 w-4" aria-hidden />
                {lifecycle === "failed" ? "Retry analysis" : "Start analysis"}
              </Button>
              <Button
                type="button"
                variant="secondary"
                onClick={() => {
                  void refresh();
                  void loadDetail();
                }}
              >
                <RefreshCw className="h-4 w-4" aria-hidden />
                Refresh
              </Button>
              {lifecycle === "completed" ? (
                <Link href={`/app/videos/${videoId}/analysis`}>
                  <Button type="button" variant="secondary" className="w-full">
                    <BarChart3 className="h-4 w-4" aria-hidden />
                    View results
                  </Button>
                </Link>
              ) : null}
            </div>
          </Card>
          <Card>
            <CardHeader title="Details" />
            <dl className="space-y-2 px-5 py-4 text-sm">
              <DetailRow label="Video ID" value={videoId} mono />
              {detail?.file_size != null ? (
                <DetailRow
                  label="Size"
                  value={`${(detail.file_size / 1e6).toFixed(2)} MB`}
                />
              ) : null}
              {detail?.duration != null ? (
                <DetailRow label="Duration" value={`${detail.duration.toFixed(1)}s`} />
              ) : null}
              {detail?.codec ? <DetailRow label="Codec" value={detail.codec} /> : null}
            </dl>
          </Card>
        </aside>
      </div>
    </div>
  );
}

function DetailRow({
  label,
  value,
  mono,
}: {
  label: string;
  value: string;
  mono?: boolean;
}) {
  return (
    <div className="flex justify-between gap-4">
      <dt className="text-xs text-[var(--text-muted)]">{label}</dt>
      <dd
        className={`text-right text-[var(--text-secondary)] ${mono ? "font-mono text-xs" : ""}`}
      >
        {value}
      </dd>
    </div>
  );
}