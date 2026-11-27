import Link from "next/link";

import { Button } from "@/components/ui/Button";

export function SiteNav() {
  return (
    <header className="sticky top-0 z-50 border-b border-[var(--border-subtle)] bg-[var(--bg-base)]/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3.5 sm:px-6">
        <Link
          href="/"
          className="flex items-center gap-2.5 rounded-[var(--radius-md)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-400"
        >
          <span className="flex h-8 w-8 items-center justify-center rounded-[var(--radius-md)] border border-violet-500/30 bg-[var(--accent-muted)] text-sm font-semibold text-violet-200">
            V
          </span>
          <span className="text-base font-semibold tracking-tight text-[var(--text-primary)]">
            VeriVid
          </span>
        </Link>
        <nav
          className="hidden items-center gap-8 text-sm text-[var(--text-secondary)] md:flex"
          aria-label="Primary"
        >
          <a href="#features" className="transition-colors hover:text-[var(--text-primary)]">
            Features
          </a>
          <a href="#workflow" className="transition-colors hover:text-[var(--text-primary)]">
            How it works
          </a>
          <a href="#council" className="transition-colors hover:text-[var(--text-primary)]">
            Debate Council
          </a>
        </nav>
        <Link href="/app">
          <Button className="px-3.5 py-2 text-sm">Get started</Button>
        </Link>
      </div>
    </header>
  );
}