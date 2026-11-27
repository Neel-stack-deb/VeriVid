"use client";

import { motion, useReducedMotion } from "framer-motion";

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
  },
  {
    key: "verification",
    title: "Verification Agent",
    role: "Cross-checks claims against available evidence",
  },
  {
    key: "risk",
    title: "Risk Agent",
    role: "Surfaces uncertainty, bias, and harm vectors",
  },
  {
    key: "consensus",
    title: "Consensus Agent",
    role: "Synthesizes council findings into verified output",
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

  const reportMap: Record<(typeof agents)[number]["key"], ContextReport | RiskReport | VerificationReport | ConsensusReport | null> = {
    context: reports.context_report,
    verification: reports.verification_report,
    risk: reports.risk_report,
    consensus: reports.consensus_report,
  };

  return (
    <div>
      <p className="mb-4 text-xs text-zinc-500">
        Retrospective view of the completed council workflow — reports from the
        backend, not live agent streaming.
      </p>
      <div className="grid gap-4 lg:grid-cols-4">
        {agents.map((agent, index) => {
          const report = reportMap[agent.key];
          const ready = Boolean(report);
          return (
            <div key={agent.key} className="relative">
              {index > 0 ? (
                <div
                  className="absolute -left-2 top-10 hidden h-px w-4 bg-zinc-700 lg:block"
                  aria-hidden
                />
              ) : null}
              <motion.div
                initial={reduceMotion ? false : { opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.08 }}
              >
                <Card
                  className={`h-full ${
                    agent.key === "consensus" && ready
                      ? "ring-1 ring-violet-500/40"
                      : ""
                  }`}
                >
                  <CardHeader title={agent.title} description={agent.role} />
                  <div className="px-5 py-4">
                    <p
                      className={`text-xs font-medium uppercase tracking-wide ${
                        ready ? "text-emerald-400" : "text-zinc-500"
                      }`}
                    >
                      {ready ? "Report available" : "Awaiting execution"}
                    </p>
                    {report ? (
                      <details className="mt-3">
                        <summary className="cursor-pointer text-sm text-violet-300 hover:text-violet-200">
                          View report
                        </summary>
                        <p className="mt-2 text-sm text-zinc-300">
                          {report.summary}
                        </p>
                        <p className="mt-2 text-xs text-zinc-500">
                          Confidence {(report.confidence * 100).toFixed(0)}% ·{" "}
                          {report.model_name}
                        </p>
                      </details>
                    ) : null}
                  </div>
                </Card>
              </motion.div>
            </div>
          );
        })}
      </div>
    </div>
  );
}