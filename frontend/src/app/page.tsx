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

import { ProductPreview } from "@/components/landing/ProductPreview";
import { SiteNav } from "@/components/layout/SiteNav";
import {
  FeaturesMotion,
  HeroMotion,
} from "@/components/landing/HeroMotion";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

const workflow = [
  { step: "Perceive", copy: "Metadata, frames, audio, transcription, and vision" },
  { step: "Structure", copy: "Knowledge graph from multimodal signals" },
  { step: "Reason", copy: "Four-agent Debate Council verification" },
  { step: "Present", copy: "Structured reports and intelligence dashboard" },
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
    <div className="min-h-screen bg-[var(--bg-base)] text-[var(--text-secondary)]">
      <SiteNav />
      <main>
        <Hero />
        <WorkflowSection />
        <FeaturesSection />
        <CouncilSection />
        <FinalCta />
      </main>
      <SiteFooter />
    </div>
  );
}

function Hero() {
  return (
    <section className="landing-grid-bg relative overflow-hidden border-b border-[var(--border-subtle)]">
      <HeroMotion>
        <div className="mx-auto grid max-w-6xl gap-12 px-4 py-16 sm:px-6 md:grid-cols-2 md:py-24 lg:gap-16 lg:py-28">
          <div>
            <p className="text-meta text-violet-300/90">VeriVid</p>
            <h1 className="mt-4 text-4xl font-semibold tracking-tight text-[var(--text-primary)] sm:text-5xl lg:leading-[1.1]">
              Every video has a story.{" "}
              <span className="text-violet-300">Verify what&apos;s inside.</span>
            </h1>
            <p className="mt-6 max-w-xl text-lg leading-relaxed text-[var(--text-secondary)]">
              Transform video into structured knowledge, verified insights, and accessible
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
          <div className="md:block">
            <ProductPreview />
          </div>
        </div>
      </HeroMotion>
    </section>
  );
}

function WorkflowSection() {
  return (
    <section id="workflow" className="mx-auto max-w-6xl px-4 py-20 sm:px-6">
      <h2 className="text-center text-2xl font-semibold tracking-tight text-[var(--text-primary)]">
        Perceive → Structure → Reason → Present
      </h2>
      <p className="mx-auto mt-3 max-w-2xl text-center text-sm leading-relaxed text-[var(--text-muted)]">
        The same lifecycle your operators see in the workspace — driven by real API status, not
        simulated progress bars.
      </p>
      <ol className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {workflow.map((item, index) => (
          <li key={item.step}>
            <Card hover className="h-full p-5">
              <span className="text-meta text-violet-400/90">
                {String(index + 1).padStart(2, "0")}
              </span>
              <p className="mt-3 font-medium text-[var(--text-primary)]">{item.step}</p>
              <p className="mt-2 text-sm leading-relaxed text-[var(--text-muted)]">
                {item.copy}
              </p>
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
      className="border-y border-[var(--border-subtle)] bg-[var(--bg-muted)] px-4 py-20 sm:px-6"
    >
      <FeaturesMotion>
        <div className="mx-auto max-w-6xl">
          <h2 className="text-2xl font-semibold tracking-tight text-[var(--text-primary)]">
            Capabilities
          </h2>
          <p className="mt-2 max-w-2xl text-sm text-[var(--text-muted)]">
            Implemented features connect to live endpoints. Planned items are labeled explicitly.
          </p>
          <ul className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {features.map(({ icon: Icon, title, body, implemented }) => (
              <li key={title}>
                <Card hover className="h-full p-5">
                  <Icon className="h-5 w-5 text-violet-400" aria-hidden />
                  <div className="mt-3 flex flex-wrap items-center gap-2">
                    <p className="font-medium text-[var(--text-primary)]">{title}</p>
                    <span
                      className={`rounded-full px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide ${
                        implemented
                          ? "border border-emerald-500/25 bg-[var(--success-muted)] text-emerald-300"
                          : "border border-[var(--border-default)] text-[var(--text-muted)]"
                      }`}
                    >
                      {implemented ? "Live" : "Planned"}
                    </span>
                  </div>
                  <p className="mt-2 text-sm leading-relaxed text-[var(--text-muted)]">{body}</p>
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
  const agents = ["Context", "Verification", "Risk", "Consensus"];
  return (
    <section id="council" className="mx-auto max-w-6xl px-4 py-20 sm:px-6">
      <h2 className="text-2xl font-semibold tracking-tight text-[var(--text-primary)]">
        Debate Council
      </h2>
      <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[var(--text-muted)]">
        Four specialist agents reason in sequence — LangGraph on the backend, a retrospective
        council view on the frontend when reports are ready.
      </p>
      <div className="mt-10 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {agents.map((name, i) => (
          <Card
            key={name}
            className={`p-4 text-center ${
              i === 3 ? "border-violet-500/30 bg-[var(--accent-muted)]" : ""
            }`}
          >
            <p className="text-sm font-medium text-violet-200">{name} Agent</p>
          </Card>
        ))}
      </div>
      <p className="mt-8 text-center">
        <Link href="/app/demo">
          <Button variant="secondary">
            <CheckCircle2 className="h-4 w-4" aria-hidden />
            View sample council output
          </Button>
        </Link>
      </p>
    </section>
  );
}

function FinalCta() {
  return (
    <section className="border-t border-[var(--border-subtle)] bg-[var(--bg-muted)] px-4 py-16 sm:px-6">
      <div className="mx-auto flex max-w-6xl flex-col items-center gap-6 text-center">
        <h2 className="text-2xl font-semibold tracking-tight text-[var(--text-primary)]">
          Ready to verify your next video?
        </h2>
        <p className="max-w-lg text-sm text-[var(--text-muted)]">
          Upload through the workspace, poll real processing status, and explore structured
          intelligence when the pipeline completes.
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          <Link href="/app">
            <Button>
              <Upload className="h-4 w-4" aria-hidden />
              Open workspace
            </Button>
          </Link>
          <Link href="/app/demo">
            <Button variant="secondary">Try demo</Button>
          </Link>
        </div>
      </div>
    </section>
  );
}

function SiteFooter() {
  return (
    <footer className="border-t border-[var(--border-subtle)] bg-[var(--bg-inset)] px-4 py-12 sm:px-6">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 sm:flex-row sm:justify-between">
        <div>
          <p className="font-semibold text-[var(--text-primary)]">VeriVid</p>
          <p className="mt-1 text-sm text-[var(--text-muted)]">
            Multimodal video intelligence · portfolio build
          </p>
        </div>
        <nav className="flex flex-wrap gap-4 text-sm text-[var(--text-muted)]" aria-label="Footer">
          <Link href="/app" className="hover:text-[var(--text-secondary)]">
            Workspace
          </Link>
          <Link href="/app/demo" className="hover:text-[var(--text-secondary)]">
            Demo
          </Link>
          <a
            href="https://github.com/Neel-stack-deb/VeriVid"
            className="hover:text-[var(--text-secondary)]"
            rel="noopener noreferrer"
          >
            Repository
          </a>
        </nav>
      </div>
    </footer>
  );
}