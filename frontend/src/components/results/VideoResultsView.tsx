"use client";

import type { VideoResultsResponse } from "@/lib/types";
import { DebateCouncil } from "@/components/debate/DebateCouncil";
import { Card, CardHeader } from "@/components/ui/Card";

export function VideoResultsView({ results }: { results: VideoResultsResponse }) {
  return (
    <div className="space-y-6">
      <section>
        <Card>
          <CardHeader title="Overview" description="Metadata and status" />
          <div className="grid gap-4 px-5 py-4 text-sm text-zinc-300 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              <p className="text-xs text-zinc-500">Status</p>
              <p className="capitalize">{results.status}</p>
            </div>
            {results.metadata ? (
              <>
                <div>
                  <p className="text-xs text-zinc-500">Duration</p>
                  <p>{results.metadata.duration.toFixed(1)}s</p>
                </div>
                <div>
                  <p className="text-xs text-zinc-500">Resolution</p>
                  <p>
                    {results.metadata.width}×{results.metadata.height}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-zinc-500">Codec</p>
                  <p>{results.metadata.codec}</p>
                </div>
              </>
            ) : (
              <p className="text-zinc-500">Metadata not available yet.</p>
            )}
          </div>
        </Card>
      </section>

      <section>
        <Card>
          <CardHeader title="Transcript" />
          <div className="px-5 py-4">
            {results.transcript ? (
              <>
                <p className="text-sm text-zinc-200">{results.transcript.full_text}</p>
                <ul className="mt-4 space-y-2">
                  {results.transcript.segments.map((seg, i) => (
                    <li key={i} className="text-xs text-zinc-500">
                      <span className="text-violet-300/80">
                        [{seg.start.toFixed(1)}s]
                      </span>{" "}
                      {seg.text}
                    </li>
                  ))}
                </ul>
              </>
            ) : (
              <p className="text-sm text-zinc-500">No transcript available.</p>
            )}
          </div>
        </Card>
      </section>

      <section>
        <Card>
          <CardHeader title="Scene intelligence" />
          <div className="space-y-4 px-5 py-4">
            {results.scenes?.scenes.length ? (
              results.scenes.scenes.map((scene, i) => (
                <div
                  key={i}
                  className="rounded-lg border border-zinc-800 bg-[#0d0e13] p-4"
                >
                  <p className="text-xs text-violet-300">
                    t={scene.timestamp}s
                  </p>
                  <p className="mt-1 text-sm text-zinc-200">{scene.description}</p>
                  {scene.objects.length > 0 ? (
                    <p className="mt-2 text-xs text-zinc-500">
                      Objects: {scene.objects.map((o) => o.name).join(", ")}
                    </p>
                  ) : null}
                </div>
              ))
            ) : (
              <p className="text-sm text-zinc-500">No scenes extracted.</p>
            )}
          </div>
        </Card>
      </section>

      <section>
        <Card>
          <CardHeader title="Knowledge" />
          <div className="px-5 py-4">
            {results.knowledge?.entities.length ? (
              <ul className="space-y-2">
                {results.knowledge.entities.map((entity) => (
                  <li
                    key={entity.id}
                    className="rounded-lg border border-zinc-800 px-3 py-2 text-sm"
                  >
                    <span className="font-medium text-zinc-100">{entity.name}</span>
                    <span className="ml-2 text-xs text-zinc-500">{entity.type}</span>
                    {entity.description ? (
                      <p className="mt-1 text-xs text-zinc-400">{entity.description}</p>
                    ) : null}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-zinc-500">No knowledge graph yet.</p>
            )}
          </div>
        </Card>
      </section>

      <section>
        <Card>
          <CardHeader
            title="Debate Council"
            description="Context → Verification → Risk → Consensus"
          />
          <div className="px-5 py-4">
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
      </section>
    </div>
  );
}