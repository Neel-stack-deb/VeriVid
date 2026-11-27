import Link from "next/link";
import {
  AudioLines,
  Brain,
  CheckCircle2,
  Layers,
  Shield,
  Upload,
  Users,
} from "lucide-react";

import { SiteNav } from "@/components/layout/SiteNav";
import {
  FeaturesMotion,
  HeroMotion,
} from "@/components/landing/HeroMotion";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

const workflow = [
  { step: "Upload", copy: "Ingest video securely via REST API" },
  { step: "Perceive", copy: "Metadata, frames, audio, transcription, vision" },
  { step: "Structure", copy: "Knowledge graph from multimodal signals" },
  { step: "Reason", copy: "Four-agent Debate Council verification" },
  { step: "Present", copy: "Structured reports and insights" },
];

const features = [
  {
    icon: Layers,
    title: "Multimodal understanding",
    body: "Vision, audio, and metadata pipelines behind a single upload — implemented in the FastAPI backend.",
    implemented: true,
  },
  {
    icon: Brain,
    title: "Knowledge extraction",
    body: "Entities and relationships assembled into a structured KnowledgeBase after scene and transcript fusion.",
    implemented: true,
  },
  {
    icon: AudioLines,
    title: "Audio transcription",
    body: "Whisper-backed speech-to-text with segment timestamps when the audio stage succeeds.",
    implemented: true,
  },
  {
    icon: Users,
    title: "Debate Council",
    body: "Context, Verification, Risk, and Consensus agents orchestrated with LangGraph.",
    implemented: true,
  },
  {
    icon: Shield,
    title: "Accessibility insights",
    body: "Richer accessibility-oriented summaries — planned; not yet a dedicated API surface.",
    implemented: false,
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#08090d] text-zinc-200">
      <SiteNav />
      <main>
        <Hero />
        <WorkflowSection />
        <FeaturesSection />
        <CouncilSection />
      </main>
      <SiteFooter />
    </div>
  );
}

function Hero() {
  return (
    <section className="relative overflow-hidden border-b border-zinc-800/80">
      <HeroMotion>
        <div className="mx-auto grid max-w-6xl gap-12 px-4 py-20 sm:px-6 lg:grid-cols-2 lg:py-28">
        <div>
          <p className="text-sm font-medium text-violet-300">VeriVid</p>
          <h1 className="mt-4 text-4xl font-semibold tracking-tight text-zinc-50 sm:text-5xl">
            Every video has a story.{" "}
            <span className="text-violet-300">Verify what&apos;s inside.</span>
          </h1>
          <p className="mt-6 text-lg text-zinc-400">
            Turn videos into structured knowledge, verified insights, and accessible
            intelligence with multimodal AI.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link href="/app">
              <Button>Analyze a video</Button>
            </Link>
            <a href="#workflow">
              <Button variant="secondary">Explore how it works</Button>
            </a>
          </div>
        </div>
        <div className="relative hidden lg:block">
          <ProductPreview />
        </div>
        </div>
      </HeroMotion>
    </section>
  );
}

function ProductPreview() {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-[#0c0d12] p-6 shadow-2xl shadow-violet-950/20">
      <div className="flex items-center gap-2 border-b border-zinc-800 pb-4 text-xs text-zinc-500">
        <span className="h-2 w-2 rounded-full bg-emerald-400" />
        processing · debate
      </div>
      <div className="mt-4 space-y-3">
        {["Metadata", "Vision", "Knowledge", "Council"].map((label, i) => (
          <div
            key={label}
            className="flex items-center gap-3 rounded-lg border border-zinc-800 bg-[#101118] px-3 py-2"
          >
            <CheckCircle2
              className={`h-4 w-4 ${i < 3 ? "text-emerald-400" : "text-violet-400"}`}
            />
            <span className="text-sm text-zinc-300">{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function WorkflowSection() {
  return (
    <section id="workflow" className="mx-auto max-w-6xl px-4 py-20 sm:px-6">
      <h2 className="text-center text-2xl font-semibold text-zinc-50">
        Perceive → Structure → Reason → Present
      </h2>
      <p className="mx-auto mt-3 max-w-2xl text-center text-sm text-zinc-500">
        The same lifecycle your operators see in the workspace — driven by real API
        status, not simulated progress bars.
      </p>
      <ol className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        {workflow.map((item, index) => (
          <li key={item.step}>
            <Card className="h-full p-4">
              <span className="text-xs font-medium text-violet-400">
                {String(index + 1).padStart(2, "0")}
              </span>
              <p className="mt-2 font-medium text-zinc-100">{item.step}</p>
              <p className="mt-1 text-xs text-zinc-500">{item.copy}</p>
            </Card>
          </li>
        ))}
      </ol>
    </section>
  );
}

function FeaturesSection() {
  return (
    <section
      id="features"
      className="border-y border-zinc-800/80 bg-[#0a0b0f] px-4 py-20 sm:px-6"
    >
      <FeaturesMotion>
        <div className="mx-auto max-w-6xl">
        <h2 className="text-2xl font-semibold text-zinc-50">Capabilities</h2>
        <p className="mt-2 max-w-2xl text-sm text-zinc-500">
          Implemented features connect to live endpoints. Planned items are labeled
          explicitly.
        </p>
        <ul className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {features.map(({ icon: Icon, title, body, implemented }) => (
            <li key={title}>
              <Card className="h-full p-5">
                <Icon className="h-5 w-5 text-violet-400" aria-hidden />
                <div className="mt-3 flex items-center gap-2">
                  <p className="font-medium text-zinc-100">{title}</p>
                  <span
                    className={`rounded-full px-2 py-0.5 text-[10px] uppercase tracking-wide ${
                      implemented
                        ? "bg-emerald-500/10 text-emerald-300"
                        : "bg-zinc-700/50 text-zinc-400"
                    }`}
                  >
                    {implemented ? "Live" : "Planned"}
                  </span>
                </div>
                <p className="mt-2 text-sm text-zinc-500">{body}</p>
              </Card>
            </li>
          ))}
        </ul>
        </div>
      </FeaturesMotion>
    </section>
  );
}

function CouncilSection() {
  const agents = [
    "Context",
    "Verification",
    "Risk",
    "Consensus",
  ];
  return (
    <section id="council" className="mx-auto max-w-6xl px-4 py-20 sm:px-6">
      <h2 className="text-2xl font-semibold text-zinc-50">Debate Council</h2>
      <p className="mt-2 max-w-2xl text-sm text-zinc-500">
        Four specialist agents reason in sequence — LangGraph on the backend, a
        retrospective council view on the frontend when reports are ready.
      </p>
      <div className="mt-10 flex flex-col items-stretch gap-3 lg:flex-row lg:items-center">
        {agents.map((name, i) => (
          <div key={name} className="flex flex-1 items-center gap-3">
            <Card className="flex-1 p-4 text-center">
              <p className="text-sm font-medium text-violet-200">{name} Agent</p>
            </Card>
            {i < agents.length - 1 ? (
              <span className="hidden text-zinc-600 lg:inline" aria-hidden>
                →
              </span>
            ) : null}
          </div>
        ))}
      </div>
      <p className="mt-8 text-center">
        <Link href="/app/demo">
          <Button variant="secondary">
            <Upload className="h-4 w-4" />
            View sample council output
          </Button>
        </Link>
      </p>
    </section>
  );
}

function SiteFooter() {
  return (
    <footer className="border-t border-zinc-800/80 bg-[#06070a] px-4 py-12 sm:px-6">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 sm:flex-row sm:justify-between">
        <div>
          <p className="font-semibold text-zinc-200">VeriVid</p>
          <p className="mt-1 text-sm text-zinc-500">
            Multimodal video intelligence · portfolio build
          </p>
        </div>
        <nav className="flex flex-wrap gap-4 text-sm text-zinc-500">
          <Link href="/app" className="hover:text-zinc-300">
            Workspace
          </Link>
          <Link href="/app/demo" className="hover:text-zinc-300">
            Demo
          </Link>
          <a
            href="https://github.com/Neel-stack-deb/VeriVid"
            className="hover:text-zinc-300"
            rel="noopener noreferrer"
          >
            Repository
          </a>
        </nav>
      </div>
    </footer>
  );
}