"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { getVideoStatus, ApiClientError } from "@/lib/api/client";
import { POLL_INTERVAL_MS } from "@/lib/constants";
import type { VideoStatusResponse } from "@/lib/types";

export function useVideoStatus(videoId: string | null) {
  const [status, setStatus] = useState<VideoStatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(Boolean(videoId));
  const controllerRef = useRef<AbortController | null>(null);

  const refresh = useCallback(async () => {
    if (!videoId) return;
    controllerRef.current?.abort();
    const controller = new AbortController();
    controllerRef.current = controller;
    try {
      const data = await getVideoStatus(videoId, controller.signal);
      setStatus(data);
      setError(null);
    } catch (err) {
      if (controller.signal.aborted) return;
      const message =
        err instanceof ApiClientError
          ? err.message
          : "Unable to reach the VeriVid API.";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [videoId]);

  useEffect(() => {
    if (!videoId) return;
    setLoading(true);
    void refresh();
  }, [videoId, refresh]);

  useEffect(() => {
    if (!videoId || !status) return;
    const terminal = status.status === "completed" || status.status === "failed";
    if (terminal) return;

    const timer = window.setInterval(() => {
      void refresh();
    }, POLL_INTERVAL_MS);

    return () => window.clearInterval(timer);
  }, [videoId, status, refresh]);

  useEffect(
    () => () => {
      controllerRef.current?.abort();
    },
    [],
  );

  const isPolling =
    Boolean(videoId && status) &&
    status!.status !== "completed" &&
    status!.status !== "failed";

  return { status, error, loading, refresh, isPolling };
}