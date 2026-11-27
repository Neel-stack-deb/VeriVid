import Link from "next/link";

import { Button } from "@/components/ui/Button";

export function SiteNav() {
  return (
    <header className="sticky top-0 z-50 border-b border-zinc-800/80 bg-[#08090d]/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
        <Link href="/" className="flex items-center gap-2">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-violet-600 text-sm font-bold text-white">
            V
          </span>
          <span className="text-lg font-semibold tracking-tight text-zinc-100">
            VeriVid
          </span>
        </Link>
        <nav className="hidden items-center gap-6 text-sm text-zinc-400 md:flex">
          <a href="#features" className="hover:text-zinc-200">
            Features
          </a>
          <a href="#workflow" className="hover:text-zinc-200">
            How it works
          </a>
          <a href="#council" className="hover:text-zinc-200">
            Debate Council
          </a>
        </nav>
        <Link href="/app">
          <Button>Get started</Button>
        </Link>
      </div>
    </header>
  );
}