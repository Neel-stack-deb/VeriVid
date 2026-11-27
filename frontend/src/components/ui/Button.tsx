import type { ButtonHTMLAttributes } from "react";

const variants = {
  primary:
    "bg-[var(--accent)] text-white hover:bg-[var(--accent-hover)] border border-violet-500/40 active:scale-[0.98]",
  secondary:
    "bg-[var(--bg-hover)] text-[var(--text-primary)] border border-[var(--border-default)] hover:border-zinc-600 hover:bg-[var(--bg-elevated)] active:scale-[0.98]",
  ghost:
    "text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-white/[0.04] active:scale-[0.98]",
};

type Variant = keyof typeof variants;

export function Button({
  variant = "primary",
  className = "",
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant }) {
  return (
    <button
      className={`inline-flex items-center justify-center gap-2 rounded-[var(--radius-md)] px-4 py-2.5 text-sm font-medium transition-[color,background-color,border-color,transform] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-400 disabled:opacity-50 disabled:pointer-events-none ${variants[variant]} ${className}`}
      {...props}
    />
  );
}