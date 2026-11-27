"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { getApiBaseUrl } from "@/lib/api/client";
import { UploadZone } from "@/components/upload/UploadZone";
import { Card, CardHeader } from "@/components/ui/Card";

export default function WorkspacePage() {
  const router = useRouter();
  const [apiReachable, setApiReachable] = useState<boolean | null>(null);

  useEffect(() => {
    const base = getApiBaseUrl();
    fetch(`${base}/health`, { method: "GET" })
      .then((r) => setApiReachable(r.ok))
      .catch(() => setApiReachable(false));
  }, []);

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6 lg:py-12">
      <header className="mb-8">
        <h1 className="text-2xl font-semibold tracking-tight text-zinc-50">
          New analysis
        </h1>
        <p className="mt-2 text-sm text-zinc-500">
          Upload a video to start the VeriVid pipeline. Results stay on your API
          server; recent uploads are remembered in this browser only.
        </p>
        {apiReachable === false ? (
          <p className="mt-3 rounded-lg border border-amber-500/30 bg-amber-500/10 px-3 py-2 text-sm text-amber-200">
            Cannot reach the API at {getApiBaseUrl()}. Start the backend with{" "}
            <code className="text-amber-100">uv run uvicorn main:app --port 8000</code>{" "}
            and set <code className="text-amber-100">NEXT_PUBLIC_API_URL</code> if
            needed.
          </p>
        ) : null}
      </header>

      <UploadZone
        onUploaded={(videoId) => {
          router.push(`/app/videos/${videoId}`);
        }}
      />

      <div className="mt-10">
        <Card>
          <CardHeader
            title="Empty workspace"
            description="Your processing queue lives on the server"
          />
          <p className="px-5 py-4 text-sm text-zinc-500">
            There is no multi-tenant account system in this build. Use the
            sidebar to reopen recent <code className="text-zinc-400">video_id</code>{" "}
            values, or try{" "}
            <a href="/app/demo" className="text-violet-300 hover:text-violet-200">
              Demo mode
            </a>{" "}
            for labeled sample output without calling AI.
          </p>
        </Card>
      </div>
    </div>
  );
}