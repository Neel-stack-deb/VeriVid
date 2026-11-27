"use client";

import Link from "next/link";
import { AlertTriangle } from "lucide-react";

import { DEMO_RESULTS } from "@/demo/sampleResults";
import { VideoResultsView } from "@/components/results/VideoResultsView";
import { Button } from "@/components/ui/Button";

export default function DemoPage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:py-10">
      <div className="mb-8 flex items-start gap-3 rounded-xl border border-violet-500/30 bg-violet-500/10 px-4 py-4">
        <AlertTriangle className="mt-0.5 h-5 w-5 text-violet-300" aria-hidden />
        <div>
          <p className="font-medium text-violet-100">Demo mode — sample data only</p>
          <p className="mt-1 text-sm text-violet-200/80">
            Everything on this page is static portfolio content. It was not produced
            by a live VeriVid pipeline. Real analysis uses the upload and process
            flows in the workspace.
          </p>
        </div>
      </div>
      <VideoResultsView results={DEMO_RESULTS} />
      <p className="mt-8 text-center">
        <Link href="/app">
          <Button type="button" variant="secondary">
            Upload a real video
          </Button>
        </Link>
      </p>
    </div>
  );
}