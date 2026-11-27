"use client";

import { useEffect, useState } from "react";

import { getApiBaseUrl } from "@/lib/api/client";
import type { ConnectionState } from "@/components/ui/ConnectionStatus";

export function useApiHealth(): ConnectionState {
  const [state, setState] = useState<ConnectionState>("checking");

  useEffect(() => {
    const base = getApiBaseUrl();
    let cancelled = false;
    setState("checking");
    fetch(`${base}/health`, { method: "GET" })
      .then((r) => {
        if (!cancelled) setState(r.ok ? "connected" : "disconnected");
      })
      .catch(() => {
        if (!cancelled) setState("disconnected");
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return state;
}