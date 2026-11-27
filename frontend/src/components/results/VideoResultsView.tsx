"use client";

import { useState } from "react";

import type { VideoResultsResponse } from "@/lib/types";
import { DebateCouncil } from "@/components/debate/DebateCouncil";
import { Card, CardHeader } from "@/components/ui/Card";

const SECTIONS = [
  { id: "overview", label: "Overview" },
  { id: "transcript", label: "Transcript" },
  { id: "scenes", label: "Scenes" },
  { id: "knowledge", label: "Knowledge" },
  { id: "council", label: "Council" },
] as const;

type SectionId = (typeof SECTIONS)[number]["id"];

export function VideoResultsView({ results }: { results: VideoResultsResponse }) {
  const [section, setSection] = useState<SectionId>("overview");

  return (
    <div className="space-y-6">
      <nav
        className="flex flex-wrap gap-2 border-b border-[var(--border-subtle)] pb-4"
        aria-label="Results sections"
      >
        {SECTIONS.map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={() => setSection(tab.id)}
            className={`rounded-[var(--radius-md)] px-3 py-1.5 text-sm font-medium transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-400 ${
              section === tab.id
                ? "bg-[var(--accent-muted)] text-violet-200"
                : "text-[var(--text-muted)] hover:bg-white/[0.04] hover:text-[var(--text-secondary)]"
            }`}
            aria-current={section === tab.id ? "true" : undefined}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {section === "overview" ? <OverviewSection results={results} /> : null}
      {section === "transcript" ? <TranscriptSection results={results} /> : null}
      {section === "scenes" ? <ScenesSection results={results} /> : null}
      {section === "knowledge" ? <KnowledgeSection results={results} /> : null}
      {section === "council" ? <CouncilSection results={results} /> : null}
    </div>
  );
}

function OverviewSection({ results }: { results: VideoResultsResponse }) {
  return (
    <Card>
      <CardHeader title="Overview" description="Metadata and processing status" />
      <div className="grid gap-4 px-5 py-5 sm:grid-cols-2 lg:grid-cols-4">
        <MetaCell label="Status" value={results.status} capitalize />
        {results.metadata ? (
          <>
            <MetaCell label="Duration" value={`${results.metadata.duration.toFixed(1)}s`} />
            <MetaCell
              label="Resolution"
              value={`${results.metadata.width}×${results.metadata.height}`}
            />
            <MetaCell label="Codec" value={results.metadata.codec} />
            <MetaCell label="FPS" value={String(results.metadata.fps)} />
            <MetaCell label="Filename" value={results.metadata.filename} />
          </>
        ) : (
          <p className="text-sm text-[var(--text-muted)] sm:col-span-3">
            Metadata not available yet.
          </p>
        )}
      </div>
    </Card>
  );
}

function MetaCell({
  label,
  value,
  capitalize,
}: {
  label: string;
  value: string;
  capitalize?: boolean;
}) {
  return (
    <div className="rounded-[var(--radius-md)] border border-[var(--border-subtle)] bg-[var(--bg-inset)] px-3 py-2.5">
      <p className="text-meta">{label}</p>
      <p className={`mt-1 text-sm text-[var(--text-primary)] ${capitalize ? "capitalize" : ""}`}>
        {value}
      </p>
    </div>
  );
}

function TranscriptSection({ results }: { results: VideoResultsResponse }) {
  return (
    <Card>
      <CardHeader title="Transcript" description="Speech-to-text with segment timestamps" />
      <div className="px-5 py-5">
        {results.transcript ? (
          <>
            <p className="text-sm leading-relaxed text-[var(--text-secondary)]">
              {results.transcript.full_text}
            </p>
            <ul className="mt-6 max-h-96 space-y-2 overflow-y-auto pr-1">
              {results.transcript.segments.map((seg, i) => (
                <li
                  key={i}
                  className="rounded-[var(--radius-md)] border border-[var(--border-subtle)] bg-[var(--bg-inset)] px-3 py-2.5"
                >
                  <span className="font-mono text-xs text-violet-300/90">
                    {formatTimestamp(seg.start)} → {formatTimestamp(seg.end)}
                  </span>
                  <p className="mt-1 text-sm leading-relaxed text-[var(--text-secondary)]">
                    {seg.text}
                  </p>
                </li>
              ))}
            </ul>
          </>
        ) : (
          <p className="text-sm text-[var(--text-muted)]">No transcript available.</p>
        )}
      </div>
    </Card>
  );
}

function ScenesSection({ results }: { results: VideoResultsResponse }) {
  const scenes = results.scenes?.scenes ?? [];
  const maxTs = scenes.reduce((m, s) => Math.max(m, s.timestamp), 0) || 1;

  return (
    <Card>
      <CardHeader title="Scene intelligence" description="Vision-derived scene understanding" />
      <div className="space-y-4 px-5 py-5">
        {scenes.length > 0 ? (
          <>
            <SceneTimeline scenes={scenes} maxTs={maxTs} />
            {scenes.map((scene, i) => (
              <article
                key={i}
                className="rounded-[var(--radius-md)] border border-[var(--border-subtle)] bg-[var(--bg-inset)] p-4"
              >
                <p className="font-mono text-xs text-violet-300">
                  t = {scene.timestamp.toFixed(1)}s
                </p>
                <p className="mt-2 text-sm leading-relaxed text-[var(--text-secondary)]">
                  {scene.description}
                </p>
                {scene.objects.length > 0 ? (
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {scene.objects.map((o) => (
                      <span
                        key={o.name}
                        className="rounded-full border border-[var(--border-default)] px-2 py-0.5 text-xs text-[var(--text-muted)]"
                      >
                        {o.name}
                      </span>
                    ))}
                  </div>
                ) : null}
                {scene.visible_text.length > 0 ? (
                  <p className="mt-2 text-xs text-[var(--text-muted)]">
                    Visible text:{" "}
                    {scene.visible_text.map((t) => t.text).join(", ")}
                  </p>
                ) : null}
              </article>
            ))}
          </>
        ) : (
          <p className="text-sm text-[var(--text-muted)]">No scenes extracted.</p>
        )}
      </div>
    </Card>
  );
}

function SceneTimeline({
  scenes,
  maxTs,
}: {
  scenes: NonNullable<VideoResultsResponse["scenes"]>["scenes"];
  maxTs: number;
}) {
  return (
    <div className="relative mb-2 h-2 rounded-full bg-[var(--bg-hover)]" aria-hidden>
      {scenes.map((scene, i) => (
        <span
          key={i}
          className="absolute top-0 h-2 w-1.5 -translate-x-1/2 rounded-full bg-violet-400"
          style={{ left: `${(scene.timestamp / maxTs) * 100}%` }}
        />
      ))}
    </div>
  );
}

function KnowledgeSection({ results }: { results: VideoResultsResponse }) {
  const kb = results.knowledge;
  return (
    <Card>
      <CardHeader title="Knowledge" description="Structured entities from multimodal fusion" />
      <div className="space-y-4 px-5 py-5">
        {kb?.entities.length ? (
          <ul className="grid gap-3 sm:grid-cols-2">
            {kb.entities.map((entity) => (
              <li
                key={entity.id}
                className="rounded-[var(--radius-md)] border border-[var(--border-subtle)] bg-[var(--bg-inset)] px-4 py-3"
              >
                <EntityHeader name={entity.name} type={entity.type} />
                {entity.description ? (
                  <p className="mt-2 text-xs leading-relaxed text-[var(--text-muted)]">
                    {entity.description}
                  </p>
                ) : null}
                <p className="mt-2 text-xs text-[var(--text-muted)]">
                  Confidence {(entity.confidence * 100).toFixed(0)}%
                </p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-[var(--text-muted)]">No knowledge graph yet.</p>
        )}
        {kb && (kb.relationships.length > 0 || kb.claims.length > 0) ? (
          <p className="text-xs text-[var(--text-muted)]">
            Additional relationships and claims are available in the API payload when the
            knowledge stage completes.
          </p>
        ) : null}
      </div>
    </Card>
  );
}

function EntityHeader({ name, type }: { name: string; type: string }) {
  return (
    <div className="flex flex-wrap items-baseline gap-2">
      <span className="font-medium text-[var(--text-primary)]">{name}</span>
      <span className="text-xs text-[var(--text-muted)]">{type}</span>
    </div>
  );
}

function CouncilSection({ results }: { results: VideoResultsResponse }) {
  return (
    <Card>
      <CardHeader
        title="Debate Council"
        description="Context → Verification → Risk → Consensus"
      />
      <div className="px-5 py-5">
        <DebateCouncil
          reports={{
            context_report: results.context_report,
            verification_report: results.verification_report,
            risk_report: results.risk_report,
            consensus_report: results.consensus_report,
          }}
        />
      </div>
    </Card>
  );
}

function formatTimestamp(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s.toFixed(1).padStart(4, "0")}`;
}