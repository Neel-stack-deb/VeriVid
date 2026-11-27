"use client";

import { useRouter } from "next/navigation";
import Link from "next/link";
import { Film } from "lucide-react";

import { getApiBaseUrl } from "@/lib/api/client";
import { useApiHealth } from "@/hooks/useApiHealth";
import { UploadZone } from "@/components/upload/UploadZone";
import { ConnectionStatus } from "@/components/ui/ConnectionStatus";
import { Card, CardHeader } from "@/components/ui/Card";

export default function WorkspacePage() {
  const router = useRouter();
  const connection = useApiHealth();
  const apiBase = getApiBaseUrl();

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6 lg:py-12">
      <header className="mb-8 space-y-4">
        <div>
          <h1 className="page-title">New analysis</h1>
          <p className="mt-2 text-sm text-[var(--text-muted)]">
            Upload a video to start the VeriVid pipeline. Results stay on your API server.
          </p>
        </div>
        <ConnectionStatus state={connection} apiBase={apiBase} />
      </header>

      <UploadZone
        onUploaded={(videoId) => {
          router.push(`/app/videos/${videoId}`);
        }}
      />

      <div className="mt-10">
        <Card>
          <CardHeader
            title="Getting started"
            description="No account system in this build — server-side queue, local recent list"
          />
          <ul className="space-y-3 px-5 py-5 text-sm leading-relaxed text-[var(--text-muted)]">
            <li className="flex gap-2">
              <Film className="mt-0.5 h-4 w-4 shrink-0 text-[var(--text-muted)]" aria-hidden />
              <span>
                After upload, open the video workspace to start processing and poll live status.
              </span>
            </li>
            <li>
              Reopen recent uploads from the sidebar —{" "}
              <code className="rounded bg-[var(--bg-hover)] px-1 text-[var(--text-secondary)]">
                video_id
              </code>{" "}
              values are stored in this browser only.
            </li>
            <li>
              Explore{" "}
              <Link href="/app/demo" className="text-violet-300 hover:text-violet-200">
                Demo mode
              </Link>{" "}
              for labeled sample intelligence without calling AI.
            </li>
          </ul>
        </Card>
      </div>
    </div>
  );
}