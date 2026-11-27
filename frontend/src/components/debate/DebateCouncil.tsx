"use client";

import { motion, useReducedMotion } from "framer-motion";
import { ArrowDown, ArrowRight } from "lucide-react";

import type {
  ConsensusReport,
  ContextReport,
  RiskReport,
  VerificationReport,
} from "@/lib/types";
import { Card, CardHeader } from "@/components/ui/Card";

const agents = [
  {
    key: "context",
    title: "Context Agent",
    role: "Situates knowledge in narrative and timeline context",
    accent: "border-t-sky-500/40",
    badge: "text-sky-300",
    dot: "bg-sky-400",
  },
  {
    key: "verification",
    title: "Verification Agent",
    role: "Cross-checks claims against available evidence",
    accent: "border-t-emerald-500/40",
    badge: "text-emerald-300",
    dot: "bg-emerald-400",
  },
  {
    key: "risk",
    title: "Risk Agent",
    role: "Surfaces uncertainty, bias, and harm vectors",
    accent: "border-t-amber-500/40",
    badge: "text-amber-300",
    dot: "bg-amber-400",
  },
  {
    key: "consensus",
    title: "Consensus Agent",
    role: "Synthesizes council findings into verified output",
    accent: "border-t-violet-500/50",
    badge: "text-violet-200",
    dot: "bg-violet-400",
  },
] as const;

type Reports = {
  context_report: ContextReport | null;
  verification_report: VerificationReport | null;
  risk_report: RiskReport | null;
  consensus_report: ConsensusReport | null;
};

export function DebateCouncil({ reports }: { reports: Reports }) {
  const reduceMotion = useReducedMotion();

  const reportMap: Record<
    (typeof agents)[number]["key"],
    ContextReport | RiskReport | VerificationReport | ConsensusReport | null
  > = {
    context: reports.context_report,
    verification: reports.verification_report,
    risk: reports.risk_report,
    consensus: reports.consensus_report,
  };

  return (
    <div>
      <p className="mb-6 text-sm text-[var(--text-muted)]">
        Retrospective council workflow — final reports from the backend, not live agent
        streaming.
      </p>
      <ol className="flex flex-col gap-3 lg:flex-row lg:items-stretch lg:gap-2">
        {agents.map((agent, index) => {
          const report = reportMap[agent.key];
          const ready = Boolean(report);
          const isConsensus = agent.key === "consensus";
          return (
            <li key={agent.key} className="flex flex-1 flex-col items-center gap-3 lg:flex-row">
              <motion.div
                className="w-full flex-1"
                initial={reduceMotion ? false : { opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.06 }}
              >
                <Card
                  className={`h-full border-t-2 ${agent.accent} ${
                    isConsensus && ready ? "ring-1 ring-violet-500/35" : ""
                  }`}
                >
                  <CardHeader title={agent.title} description={agent.role} />
                  <div className="px-5 py-4">
                    <div className="flex items-center gap-2">
                      <span className={`h-1.5 w-1.5 rounded-full ${agent.dot}`} aria-hidden />
                      <p
                        className={`text-xs font-medium uppercase tracking-wide ${
                          ready ? agent.badge : "text-[var(--text-muted)]"
                        }`}
                      >
                        {ready ? "Report available" : "Awaiting execution"}
                      </p>
                    </div>
                    {report ? (
                      <details className="details-chevron mt-4 group">
                        <summary className="flex cursor-pointer items-center gap-2 text-sm text-violet-300 transition-colors hover:text-violet-200 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-400">
                          <span className="text-[var(--text-muted)] transition-transform group-open:rotate-90">
                            ▶
                          </span>
                          Full report
                        </summary>
                        <p className="mt-3 text-sm leading-relaxed text-[var(--text-secondary)]">
                          {report.summary}
                        </p>
                        <p className="mt-3 text-xs text-[var(--text-muted)]">
                          Confidence {(report.confidence * 100).toFixed(0)}% · {report.model_name}
                        </p>
                      </details>
                    ) : null}
                  </div>
                </Card>
              </motion.div>
              {index < agents.length - 1 ? (
                <>
                  <ArrowRight
                    className="hidden h-4 w-4 shrink-0 text-[var(--text-muted)] lg:block"
                    aria-hidden
                  />
                  <ArrowDown
                    className="h-4 w-4 shrink-0 text-[var(--text-muted)] lg:hidden"
                    aria-hidden
                  />
                </>
              ) : null}
            </li>
          );
        })}
      </ol>
    </div>
  );
}