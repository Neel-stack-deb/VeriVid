"use client";

import Link from "next/link";

import { DEMO_RESULTS } from "@/demo/sampleResults";
import { DemoBanner } from "@/components/demo/DemoBanner";
import { VideoResultsView } from "@/components/results/VideoResultsView";
import { Button } from "@/components/ui/Button";

export default function DemoPage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:py-10">
      <DemoBanner />
      <header className="mb-8">
        <h1 className="page-title">Sample analysis</h1>
        <p className="mt-2 text-sm text-[var(--text-muted)]">
          Precomputed demonstration data mirroring the live results layout.
        </p>
      </header>
      <VideoResultsView results={DEMO_RESULTS} />
      <p className="mt-10 text-center">
        <Link href="/app">
          <Button type="button" variant="secondary">
            Upload a real video
          </Button>
        </Link>
      </p>
    </div>
  );
}